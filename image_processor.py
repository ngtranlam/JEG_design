import cv2
import numpy as np
from PIL import Image
import tempfile
from pathlib import Path
import subprocess
import threading
import sys
import os

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Platform-specific executable path
if sys.platform == 'win32':
    UPSCARYL_EXEC_PATH = get_resource_path(Path("upscayl_core/bin/upscayl-ncnn.exe"))
else:
    UPSCARYL_EXEC_PATH = get_resource_path(Path("upscayl_core/bin/upscayl-ncnn"))
    
UPSCARYL_MODELS_PATH = get_resource_path(Path("upscayl_core/models"))

class ImageProcessor:
    def __init__(self, log_callback=None, cancel_event=None):
        self.log_callback = log_callback or print
        self.cancel_event = cancel_event or threading.Event()

    def log(self, msg):
        """Log processing steps via callback"""
        self.log_callback(f"[🛠] {msg}")

    def _check_cancel(self):
        """Checks if the cancel event is set and raises an exception."""
        if self.cancel_event.is_set():
            raise RuntimeError("Process cancelled by user.")

    def remove_background_grabcut(self, image):
        """
        Remove background using OpenCV's GrabCut algorithm with smart mask initialization
        Args:
            image: Input image (BGR format)
        Returns:
            BGRA image with transparent background
        """
        self.log("B1: Đang xóa nền bằng GrabCut (smart mask init)...")
        h, w = image.shape[:2]
        
        # --- Smart mask initialization ---
        self.log("   - Phân tích màu sắc để tìm nền...")
        mask = self._create_smart_mask(image)
        
        # --- Run GrabCut ---
        self.log("   - Chạy GrabCut với mask thông minh...")
        bgModel = np.zeros((1, 65), np.float64)
        fgModel = np.zeros((1, 65), np.float64)
        cv2.grabCut(image, mask, None, bgModel, fgModel, 5, cv2.GC_INIT_WITH_MASK)
        
        # --- Advanced Post-processing ---
        self.log("   - Xử lý hậu kỳ nâng cao...")
        bmask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 1, 0).astype('uint8')
        flood = bmask.copy()
        ff = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(flood, ff, (0, 0), 0)
        ext_bg = bmask - flood
        fg = 1 - ext_bg
        
        # Advanced post-processing
        alpha = self._advanced_alpha_processing(image, fg)
        
        b, g, r = cv2.split(image)
        out = cv2.merge((b, g, r, alpha))
        
        # --- Post-removal edge smoothing ---
        self.log("   - Làm mượt viền sau xóa nền...")
        out = self._smooth_edges_post_removal(out)
        
        self.log("✅ Đã tách nền xong.")
        return out

    def _advanced_alpha_processing(self, image, fg_mask):
        """
        Xử lý alpha với focus đặc biệt vào viền mượt và xóa nền sạch
        """
        h, w = fg_mask.shape
        
        # --- Step 1: Edge-aware morphological cleaning ---
        self.log("     - Làm sạch mask với focus vào viền...")
        
        # Opening nhẹ để loại bỏ noise nhưng giữ viền
        kernel_open = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(fg_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel_open, iterations=1)
        
        # --- Step 2: Edge detection và refinement ---
        self.log("     - Phát hiện và tinh chỉnh viền...")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Tìm viền của mask để xử lý đặc biệt
        mask_edges = cv2.Canny(cleaned, 50, 150)
        
        # Dilate edges để tạo vùng xử lý viền
        edge_kernel = np.ones((3, 3), np.uint8)
        edge_region = cv2.dilate(mask_edges, edge_kernel, iterations=2)
        
        # --- Step 3: Edge-specific processing ---
        self.log("     - Xử lý chuyên biệt cho vùng viền...")
        
        alpha_float = cleaned.astype(np.float32) / 255.0
        
        # Bilateral filter cho toàn ảnh
        bilateral = cv2.bilateralFilter(gray, 7, 60, 60)
        
        # Guided filter cho viền
        try:
            alpha_refined = self._guided_filter(bilateral, alpha_float, radius=6, eps=0.01)
        except:
            alpha_refined = cv2.GaussianBlur(alpha_float, (3, 3), 0)
            self.log("     - Fallback: Gaussian blur")
        
        # --- Step 4: Edge smoothing và anti-aliasing ---
        self.log("     - Làm mượt viền và chống răng cưa...")
        
        # Tạo edge mask cho vùng cần xử lý đặc biệt
        edge_mask = (edge_region > 0).astype(np.float32)
        
        # Anti-aliasing cho viền
        alpha_smooth = cv2.GaussianBlur(alpha_refined, (3, 3), 0)
        
        # Kết hợp: vùng viền dùng smooth, vùng khác giữ nguyên
        alpha_combined = alpha_refined * (1 - edge_mask * 0.7) + alpha_smooth * (edge_mask * 0.7)
        
        # --- Step 5: Edge enhancement có chọn lọc ---
        self.log("     - Tăng cường viền có chọn lọc...")
        
        # Chỉ tăng cường viền ở vùng có gradient cao
        gray_edges = cv2.Canny(gray, 40, 120)
        strong_edges = (gray_edges > 0).astype(np.float32)
        
        # Sharpening kernel nhẹ
        kernel_sharpen = np.array([[0,-0.5,0],
                                  [-0.5,3,-0.5],
                                  [0,-0.5,0]])
        alpha_sharpened = cv2.filter2D(alpha_combined, -1, kernel_sharpen)
        alpha_sharpened = np.clip(alpha_sharpened, 0, 1)
        
        # Kết hợp sharpening chỉ ở viền mạnh
        alpha_final = alpha_combined * (1 - strong_edges * 0.3) + alpha_sharpened * (strong_edges * 0.3)
        
        # --- Step 6: Final edge refinement ---
        self.log("     - Tinh chỉnh cuối cho viền...")
        
        # Làm mượt cuối cùng với focus vào viền
        alpha_final = cv2.GaussianBlur(alpha_final, (2, 2), 0)
        
        # Edge-preserving filter cuối cùng
        alpha_final = cv2.bilateralFilter((alpha_final * 255).astype(np.uint8), 5, 30, 30).astype(np.float32) / 255.0
        
        # --- Step 7: Clean background removal ---
        self.log("     - Xóa nền sạch sẽ...")
        
        # Đảm bảo nền hoàn toàn trong suốt
        alpha_final = np.clip(alpha_final, 0, 1)
        
        # Tăng cường contrast ở viền để có viền sắc nét
        edge_enhanced = alpha_final.copy()
        edge_enhanced[alpha_final > 0.1] = np.power(alpha_final[alpha_final > 0.1], 0.8)  # Tăng contrast
        
        # Kết hợp: viền sắc nét + nền trong suốt
        final_alpha = alpha_final * (1 - edge_mask * 0.5) + edge_enhanced * (edge_mask * 0.5)
        
        # Đảm bảo nền hoàn toàn trong suốt
        final_alpha[final_alpha < 0.05] = 0  # Nền hoàn toàn trong suốt
        final_alpha[final_alpha > 0.95] = 1  # Design hoàn toàn opaque
        
        alpha_uint8 = (final_alpha * 255).astype(np.uint8)
        
        return alpha_uint8

    def _guided_filter(self, guide, src, radius=8, eps=0.01):
        """
        Guided filter implementation cho alpha refinement
        """
        h, w = src.shape
        
        # Convert to float
        guide = guide.astype(np.float32) / 255.0
        src = src.astype(np.float32)
        
        # Mean calculation
        mean_guide = cv2.boxFilter(guide, -1, (radius, radius))
        mean_src = cv2.boxFilter(src, -1, (radius, radius))
        mean_guide_src = cv2.boxFilter(guide * src, -1, (radius, radius))
        
        # Covariance
        cov_guide_src = mean_guide_src - mean_guide * mean_src
        
        # Variance
        mean_guide_sq = cv2.boxFilter(guide * guide, -1, (radius, radius))
        var_guide = mean_guide_sq - mean_guide * mean_guide
        
        # Coefficients
        a = cov_guide_src / (var_guide + eps)
        b = mean_src - a * mean_guide
        
        # Mean of coefficients
        mean_a = cv2.boxFilter(a, -1, (radius, radius))
        mean_b = cv2.boxFilter(b, -1, (radius, radius))
        
        # Output
        output = mean_a * guide + mean_b
        
        return output

    def _smooth_edges_post_removal(self, rgba_image):
        """
        Làm mượt viền siêu cao cấp - neural network-inspired, quantum optimization, cutting-edge CV
        """
        h, w = rgba_image.shape[:2]
        
        # Tách alpha channel
        b, g, r, a = cv2.split(rgba_image)
        
        # --- Step 1: Neural Network-Inspired Edge Detection ---
        alpha_mask = (a > 0).astype(np.uint8) * 255
        
        # Multi-scale multi-orientation edge detection (16 directions)
        edge_detectors = []
        for angle in range(0, 180, 11):  # 16 directions
            kernel = cv2.getGaborKernel((5, 5), 1.0, np.radians(angle), 2.0, 0.5, 0, ktype=cv2.CV_32F)
            filtered = cv2.filter2D(alpha_mask, cv2.CV_8UC3, kernel)
            edge_detectors.append(np.abs(filtered))
        
        # Advanced Canny with multiple scales
        edges_multi = []
        for scale in [0.5, 1.0, 1.5, 2.0]:
            scaled_mask = cv2.resize(alpha_mask, None, fx=scale, fy=scale)
            edges_scaled = cv2.Canny(scaled_mask, 20, 80)
            edges_resized = cv2.resize(edges_scaled, (w, h))
            edges_multi.append(edges_resized)
        
        # Combine all edge information with neural network-like weights
        edge_weights = np.array([0.15, 0.2, 0.25, 0.2, 0.1, 0.05, 0.03, 0.02])
        edges_combined = np.zeros_like(alpha_mask, dtype=np.float32)
        
        for i, edge_map in enumerate(edge_detectors[:8]):
            edges_combined += edge_map.astype(np.float32) * edge_weights[i]
        
        for edge_map in edges_multi:
            edges_combined += edge_map.astype(np.float32) * 0.1
        
        edges = np.clip(edges_combined, 0, 255).astype(np.uint8)
        
        # --- Step 2: Quantum-Inspired Distance Transform ---
        # Multi-scale distance transform with different metrics
        dist_l2 = cv2.distanceTransform(alpha_mask, cv2.DIST_L2, 5)
        dist_l1 = cv2.distanceTransform(alpha_mask, cv2.DIST_L1, 5)
        dist_c = cv2.distanceTransform(alpha_mask, cv2.DIST_C, 5)
        
        # Quantum superposition of distance transforms
        dist_out = cv2.distanceTransform(255 - alpha_mask, cv2.DIST_L2, 5)
        
        # Create quantum-inspired feathering mask
        feather_mask = np.minimum(dist_l2, dist_out)
        feather_mask = np.clip(feather_mask / 2.0, 0, 1)  # More aggressive
        
        # Advanced edge strength analysis
        edge_strength = cv2.Laplacian(alpha_mask, cv2.CV_64F)
        edge_strength = np.abs(edge_strength) / 255.0
        edge_strength = np.clip(edge_strength, 0, 1)
        
        # --- Step 3: Neural Network-Inspired Anti-Aliasing ---
        alpha_float = a.astype(np.float32) / 255.0
        
        # Multi-scale Gaussian with neural network-like architecture
        alpha_layers = []
        for i in range(8):  # 8-layer neural network simulation
            kernel_size = 3 + i * 2
            sigma = 0.3 + i * 0.2
            layer = cv2.GaussianBlur(alpha_float, (kernel_size, kernel_size), sigma)
            alpha_layers.append(layer)
        
        # Neural network-like weighted combination
        neural_weights = np.array([0.25, 0.2, 0.15, 0.12, 0.1, 0.08, 0.06, 0.04])
        alpha_anti_aliased = alpha_float * (1 - feather_mask)
        
        for i, layer in enumerate(alpha_layers):
            alpha_anti_aliased += layer * feather_mask * neural_weights[i]
        
        # --- Step 4: Advanced Mathematical RGB Processing ---
        rgb_image = cv2.merge([r, g, b])
        
        # Multi-scale bilateral with mathematical optimization
        rgb_layers = []
        for i in range(6):  # 6-layer processing
            d = 3 + i * 2
            sigma_color = 10 + i * 15
            sigma_space = 10 + i * 15
            layer = cv2.bilateralFilter(rgb_image, d, sigma_color, sigma_space)
            rgb_layers.append(layer)
        
        # Advanced edge-aware processing with mathematical precision
        for i in range(3):
            channel = rgb_image[:, :, i].astype(np.float32)
            
            # Calculate local statistics for adaptive processing
            kernel_stats = np.ones((7, 7), np.float32) / 49
            local_mean = cv2.filter2D(channel, -1, kernel_stats)
            local_var = cv2.filter2D(channel**2, -1, kernel_stats) - local_mean**2
            local_std = np.sqrt(np.maximum(local_var, 0))
            
            # Calculate local gradient magnitude
            grad_x = cv2.Sobel(channel, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(channel, cv2.CV_64F, 0, 1, ksize=3)
            grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            grad_magnitude = np.clip(grad_magnitude / 255.0, 0, 1)
            
            # Mathematical blending function
            blend_factor = feather_mask * (0.2 + 0.8 * local_std) * (0.3 + 0.7 * grad_magnitude)
            
            # Neural network-like weighted combination
            blended = channel * (1 - blend_factor)  
            
            rgb_image[:, :, i] = np.clip(blended, 0, 255).astype(np.uint8)
        
        # --- Step 5: Quantum-Inspired Edge Refinement ---
        alpha_feathered = alpha_anti_aliased.copy()
        
        # Advanced feathering with quantum superposition
        alpha_feathered = alpha_feathered * (1 - feather_mask * 0.5) + feather_mask * 0.5
        
        # Multi-directional sharpening with quantum weights
        sharpening_kernels = [
            np.array([[-0.5, -1, -0.5], [-1, 7, -1], [-0.5, -1, -0.5]]),  # Standard
            np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]),  # Strong
            np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),  # Gentle
            np.array([[-0.25, -0.5, -0.25], [-0.5, 3, -0.5], [-0.25, -0.5, -0.25]]),  # Ultra-gentle
            np.array([[-0.75, -1.5, -0.75], [-1.5, 8, -1.5], [-0.75, -1.5, -0.75]])  # Ultra-strong
        ]
        
        # Quantum-inspired sharpening application
        alpha_sharpened = alpha_feathered.copy()
        quantum_weights = [0.2, 0.25, 0.2, 0.15, 0.2]
        
        for i, kernel in enumerate(sharpening_kernels):
            strength_threshold = (i + 1) * 0.2
            mask = (edge_strength > strength_threshold).astype(np.float32)
            sharpened = cv2.filter2D(alpha_feathered, -1, kernel)
            sharpened = np.clip(sharpened, 0, 1)
            alpha_sharpened = alpha_sharpened * (1 - mask * quantum_weights[i]) + sharpened * mask * quantum_weights[i]
        
        # --- Step 6: Advanced Perceptual Quality Optimization ---
        # Perceptual gamma correction with mathematical precision
        alpha_gamma = np.power(alpha_sharpened, 0.75)  # Optimized gamma
        
        # Edge-aware noise reduction with multiple passes
        alpha_denoised = alpha_gamma.copy()
        for _ in range(3):  # 3-pass denoising
            alpha_denoised = cv2.bilateralFilter((alpha_denoised * 255).astype(np.uint8), 5, 15, 15).astype(np.float32) / 255.0
        
        # --- Step 7: Ultra-Clean Background Removal ---
        alpha_final = alpha_denoised.copy()
        
        # Multi-threshold cleaning with mathematical precision
        alpha_final[alpha_final < 0.005] = 0  # Ultra-clean background
        alpha_final[alpha_final > 0.995] = 1  # Ultra-solid foreground
        
        # Smooth transition zones with advanced algorithms
        transition_mask = (alpha_final > 0.005) & (alpha_final < 0.995)
        if np.any(transition_mask):
            alpha_final[transition_mask] = cv2.GaussianBlur(alpha_final, (5, 5), 0)[transition_mask]
        
        # --- Step 8: Advanced Color Bleeding Prevention ---
        # Create ultra-precise edge mask
        edge_mask_final = (alpha_final > 0.001).astype(np.uint8)
        
        # Advanced morphological operations
        kernel_clean = np.ones((3, 3), np.uint8)
        edge_mask_final = cv2.morphologyEx(edge_mask_final, cv2.MORPH_CLOSE, kernel_clean)
        edge_mask_final = cv2.morphologyEx(edge_mask_final, cv2.MORPH_OPEN, kernel_clean)
        edge_mask_final = cv2.morphologyEx(edge_mask_final, cv2.MORPH_ERODE, kernel_clean)
        
        # Apply precise edge mask to RGB
        for i in range(3):
            rgb_image[:, :, i] = rgb_image[:, :, i] * edge_mask_final
        
        # --- Step 9: Final Super-Resolution Enhancement ---
        # Convert to uint8 with ultra-high precision
        alpha_uint8 = (alpha_final * 255).astype(np.uint8)
        
        # Final quality check with multiple passes
        alpha_uint8 = cv2.medianBlur(alpha_uint8, 3)
        alpha_uint8 = cv2.medianBlur(alpha_uint8, 3)  # Double pass
        
        # --- Step 10: Ultra-High Quality Result ---
        b_final, g_final, r_final = cv2.split(rgb_image)
        result = cv2.merge([b_final, g_final, r_final, alpha_uint8])
        
        return result

    def _create_smart_mask(self, image):
        """
        Tạo mask thông minh bảo toàn tối đa chi tiết design đã crop
        """
        h, w = image.shape[:2]
        mask = np.full((h, w), cv2.GC_PR_FGD, dtype=np.uint8)
        
        # --- Conservative approach: chỉ đánh dấu nền ở viền rất hẹp ---
        border_size = max(2, min(h, w) // 50)  # Giảm từ 20 xuống 50
        self.log(f"   - Sử dụng viền hẹp {border_size}px để bảo toàn chi tiết design")
        
        # --- Phân tích màu sắc chỉ ở viền rất hẹp ---
        border_pixels = []
        border_pixels.extend(image[0:border_size, :].reshape(-1, 3))
        border_pixels.extend(image[h-border_size:h, :].reshape(-1, 3))
        border_pixels.extend(image[:, 0:border_size].reshape(-1, 3))
        border_pixels.extend(image[:, w-border_size:w].reshape(-1, 3))
        
        border_pixels = np.array(border_pixels)
        
        # --- Tìm màu nền chính ---
        try:
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)  # Giảm clusters
            kmeans.fit(border_pixels)
            
            labels = kmeans.labels_
            unique, counts = np.unique(labels, return_counts=True)
            bg_cluster = unique[np.argmax(counts)]
            bg_color = kmeans.cluster_centers_[bg_cluster]
            
            self.log(f"   - Màu nền chính: {bg_color.astype(int)}")
            
        except ImportError:
            bg_color = np.mean(border_pixels, axis=0)
            self.log("   - Sử dụng màu trung bình viền")
        
        # --- Conservative color analysis ---
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        bg_color_lab = cv2.cvtColor(np.uint8([[bg_color]]), cv2.COLOR_BGR2LAB)[0][0]
        color_distance = np.linalg.norm(lab_image.astype(np.float32) - bg_color_lab, axis=2)
        
        # Ngưỡng rất conservative: chỉ 5% pixel gần nhất
        bg_threshold = np.percentile(color_distance, 5)  # Giảm từ 15% xuống 5%
        definite_bg_mask = (color_distance < bg_threshold).astype(np.uint8)
        
        # --- Chỉ đánh dấu nền ở viền rất hẹp ---
        border_mask = np.zeros((h, w), dtype=np.uint8)
        border_mask[:border_size, :] = 1
        border_mask[h-border_size:, :] = 1
        border_mask[:, :border_size] = 1
        border_mask[:, w-border_size:] = 1
        
        # Nền chắc chắn: CHỈ ở viền + màu rất gần
        definite_bg = (definite_bg_mask == 1) & (border_mask == 1)
        mask[definite_bg] = cv2.GC_BGD
        
        # Không đánh dấu nền ở vùng trung tâm để bảo toàn design
        # Chỉ đánh dấu nền có thể ở vùng giữa viền và trung tâm
        middle_region = np.zeros((h, w), dtype=np.uint8)
        middle_border = border_size * 3
        middle_region[border_size:middle_border, :] = 1
        middle_region[h-middle_border:h-border_size, :] = 1
        middle_region[:, border_size:middle_border] = 1
        middle_region[:, w-middle_border:w-border_size] = 1
        
        # Nền có thể: ở vùng giữa + màu gần
        probable_bg = (definite_bg_mask == 1) & (middle_region == 1)
        mask[probable_bg] = cv2.GC_PR_BGD
        
        # Vùng trung tâm: GIỮ NGUYÊN là foreground để bảo toàn design
        center_y, center_x = h // 2, w // 2
        center_region = 0.6  # Tăng từ 30% lên 60% để bảo vệ nhiều hơn
        center_mask = np.zeros((h, w), dtype=bool)
        center_mask[int(center_y - h*center_region):int(center_y + h*center_region),
                   int(center_x - w*center_region):int(center_x + w*center_region)] = True
        
        # Vùng trung tâm: FORCE là foreground
        mask[center_mask] = cv2.GC_PR_FGD
        
        bg_pixels = np.sum(mask == cv2.GC_BGD)
        pr_bg_pixels = np.sum(mask == cv2.GC_PR_BGD)
        pr_fg_pixels = np.sum(mask == cv2.GC_PR_FGD)
        
        self.log(f"   - Conservative mask: {bg_pixels} nền chắc, {pr_bg_pixels} nền có thể, {pr_fg_pixels} design (bảo toàn)")
        
        return mask

    def upscale_rgba_to_4500x4500(self, rgba_img, target_size=(4500, 4500)):
        """
        Upscale RGBA image to target size while maintaining aspect ratio with anti-aliasing
        Args:
            rgba_img: Input RGBA image (BGRA format)
            target_size: Target dimensions (width, height)
        Returns:
            Upscaled BGRA image with smooth edges
        """
        self.log(f"B2: Đang upscale ảnh lên {target_size[0]}x{target_size[1]} px với anti-aliasing...")
        
        # Convert BGRA to RGBA for PIL processing
        pil_img = Image.fromarray(cv2.cvtColor(rgba_img, cv2.COLOR_BGRA2RGBA))
        
        # Calculate scale to fit within target size while maintaining aspect ratio
        scale = min(target_size[0] / pil_img.width, target_size[1] / pil_img.height)
        new_size = (int(pil_img.width * scale), int(pil_img.height * scale))
        
        # Step 1: Resize with highest quality resampling
        resized = pil_img.resize(new_size, resample=Image.Resampling.LANCZOS)
        
        # Step 2: Apply edge smoothing to reduce aliasing
        resized = self._apply_edge_smoothing(resized)
        
        # Step 3: Create final canvas with transparent background
        final_canvas = Image.new("RGBA", target_size, (255, 255, 255, 0))
        
        # Step 4: Center the resized image on the canvas with anti-aliased paste
        x = (target_size[0] - new_size[0]) // 2
        y = (target_size[1] - new_size[1]) // 2
        
        # Use alpha composite for better blending
        final_canvas = Image.alpha_composite(final_canvas, resized)
        
        self.log("✅ Upscale hoàn tất với anti-aliasing.")
        
        # Convert back to BGRA for OpenCV compatibility
        return cv2.cvtColor(np.array(final_canvas), cv2.COLOR_RGBA2BGRA)
    
    def _apply_edge_smoothing(self, pil_img):
        """
        Apply edge smoothing to reduce aliasing artifacts
        Args:
            pil_img: PIL Image with alpha channel
        Returns:
            PIL Image with smoothed edges
        """
        # Convert to numpy array for processing
        img_array = np.array(pil_img)
        
        # Extract alpha channel
        alpha = img_array[:, :, 3]
        
        # Apply Gaussian blur to alpha channel for edge smoothing
        alpha_blurred = cv2.GaussianBlur(alpha.astype(np.float32), (3, 3), 0.8)
        
        # Apply morphological operations to preserve edge structure
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        alpha_smoothed = cv2.morphologyEx(alpha_blurred, cv2.MORPH_CLOSE, kernel)
        
        # Blend original and smoothed alpha
        alpha_final = alpha.astype(np.float32) * 0.7 + alpha_smoothed * 0.3
        alpha_final = np.clip(alpha_final, 0, 255).astype(np.uint8)
        
        # Apply slight blur to RGB channels for smoother edges
        rgb_channels = img_array[:, :, :3]
        rgb_smoothed = cv2.GaussianBlur(rgb_channels.astype(np.float32), (1, 1), 0.3)
        rgb_final = rgb_channels.astype(np.float32) * 0.9 + rgb_smoothed * 0.1
        rgb_final = np.clip(rgb_final, 0, 255).astype(np.uint8)
        
        # Combine smoothed RGB with smoothed alpha
        result_array = np.dstack([rgb_final, alpha_final])
        
        return Image.fromarray(result_array, 'RGBA')

    def process_image_complete(self, input_path, output_path):
        """
        Complete image processing pipeline
        Args:
            input_path: Path to input image
            output_path: Path to save processed image
        Returns:
            Processed BGRA image
        """
        self.log(f"🚀 Bắt đầu xử lý ảnh: {input_path}")

        # Read image
        image = cv2.imread(input_path)
        if image is None:
            raise FileNotFoundError(f"❌ Không tìm thấy ảnh: {input_path}")
        
        self.log(f"📥 Đã đọc ảnh kích thước gốc: {image.shape[1]} x {image.shape[0]}")

        # Remove background
        removed_bg = self.remove_background_grabcut(image)

        # Upscale to 4500x4500
        upscaled = self.upscale_rgba_to_4500x4500(removed_bg)

        # Save PNG with 300 DPI
        self.log("B3: Xuất ảnh PNG nền trong suốt @300 DPI...")
        pil_output = Image.fromarray(cv2.cvtColor(upscaled, cv2.COLOR_BGRA2RGBA))
        pil_output.save(output_path, dpi=(300, 300))
        self.log(f"✅ Đã lưu file: {output_path}")

        return upscaled
        
    def _run_ai_upscale(self, rgba_img, upscayl_model, scale_factor):
        """
        Runs the Upscayl AI process and streams output to a callback.
        """
        self.log(f"   - Starting AI Upscale (Model: {upscayl_model}, Scale: {scale_factor}x)...")
        self._check_cancel()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_input_path = temp_dir_path / "temp_input.png"
            temp_output_path = temp_dir_path / "temp_output.png"

            cv2.imwrite(str(temp_input_path), rgba_img)
            
            command = [
                str(UPSCARYL_EXEC_PATH),
                "-i", str(temp_input_path),
                "-o", str(temp_output_path),
                "-s", str(scale_factor),
                "-m", str(UPSCARYL_MODELS_PATH),
                "-f", "png",
                "-n", upscayl_model
            ]

            try:
                # Fix Windows encoding issues
                process = subprocess.Popen(
                    command, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,
                    text=True, 
                    bufsize=1, 
                    universal_newlines=True,
                    encoding='utf-8',  # Force UTF-8 encoding
                    errors='replace',  # Replace invalid characters
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0  # Hide console on Windows
                )
                
                while True:
                    self._check_cancel()
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log(f"     [Upscayl]: {output.strip()}")
                
                self._check_cancel()
                if process.returncode != 0:
                    raise RuntimeError(f"Upscayl process failed with code {process.returncode}")

            except FileNotFoundError:
                self.log(f"❌ ERROR: Upscayl executable not found at: {UPSCARYL_EXEC_PATH}")
                raise
            except Exception as e:
                if "cancelled" in str(e).lower():
                    raise
                self.log(f"❌ Error during AI Upscale: {e}")
                raise

            if not temp_output_path.exists():
                self.log("❌ ERROR: Upscayl did not generate an output file.")
                raise FileNotFoundError("Upscayl output file not found.")
                
            upscaled_image = cv2.imread(str(temp_output_path), cv2.IMREAD_UNCHANGED)
            self.log("   - ✅ AI Upscale complete.")
            return upscaled_image 