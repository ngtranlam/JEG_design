import requests
import base64
import io
from PIL import Image
import json
import hashlib
import os
import time
from typing import Optional, Tuple
from pathlib import Path

# Import Google GenAI library
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google.genai library not available. Install with: pip install google-genai")

class GeminiClient:
    """
    Client for Google Gemini API to handle background removal and image processing
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }
        # Setup cache directory - use user's home directory for PyInstaller compatibility
        import os
        import tempfile
        
        # Try to use user's home directory first, fallback to temp directory
        try:
            home_dir = Path.home()
            self.cache_dir = home_dir / "JEGDesignExtract" / "extract_cache"
        except:
            self.cache_dir = Path(tempfile.gettempdir()) / "JEGDesignExtract" / "extract_cache"
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    # def remove_background_with_gemini(self, image_data: bytes, model: str = "gemini-2.5-flash") -> Optional[Image.Image]:
    #     """
    #     Remove background from image using Gemini API
        
    #     Args:
    #         image_data: Image bytes
    #         model: Gemini model to use
            
    #     Returns:
    #         PIL Image with transparent background or None if failed
    #     """
    #     try:
    #         # Convert image to base64
    #         image_base64 = base64.b64encode(image_data).decode('utf-8')
            
    #         # Determine MIME type
    #         mime_type = "image/jpeg"
    #         if image_data.startswith(b'\x89PNG'):
    #             mime_type = "image/png"
    #         elif image_data.startswith(b'GIF'):
    #             mime_type = "image/gif"
            
    #         # Create the prompt for background removal
    #         # prompt = """
    #         # Please remove the background from this image and return only the main subject/design with a transparent background. 
            
    #         # Requirements:
    #         # - Keep all details, colors, and text exactly as they appear
    #         # - Remove any background, shadows, or unwanted elements
    #         # - Output should be a clean PNG with transparent background
    #         # - Maintain the original quality and sharpness
    #         # - If this is a design on clothing, extract only the design part
    #         # """
            
    #         prompt ="""
    #                 Như một designer chuyên nghiệp, hãy vẽ lại thiết kế này trên nền chrome key với các yêu cầu sau:
    #                 - Chọn màu chrome key có độ tương phản cao nhất với các màu có trong thiết kế (có 3 màu nền chính là Green screen, Blue screen, Red screen)
    #                 - Các chi tiết của hình ảnh được vẽ lại hoàn toàn, giữ nguyên màu sắc, văn bản, hình ảnh và chi tiết như trong hình gốc.
    #                 - Căn chỉnh đặt thiết kế mới vào giữa khung ảnh mới và căn thẳng.
    #                 """
    #         # Prepare the request payload
    #         payload = {
    #             "contents": [
    #                 {
    #                     "parts": [
    #                         {
    #                             "inline_data": {
    #                                 "mime_type": mime_type,
    #                                 "data": image_base64
    #                             }
    #                         },
    #                         {
    #                             "text": prompt
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "generationConfig": {
    #                 "temperature": 0.1,
    #                 "topK": 1,
    #                 "topP": 0.8,
    #                 "maxOutputTokens": 1024
    #             }
    #         }
            
    #         # Make API request
    #         model_url = f"{self.base_url}/{model}:generateContent"
    #         response = requests.post(model_url, headers=self.headers, json=payload, timeout=60)
            
    #         if response.status_code == 200:
    #             result = response.json()
                
    #             # Extract the generated image from response
    #             if "candidates" in result and len(result["candidates"]) > 0:
    #                 candidate = result["candidates"][0]
    #                 if "content" in candidate and "parts" in candidate["content"]:
    #                     parts = candidate["content"]["parts"]
                        
    #                     # Look for image data in the response
    #                     for part in parts:
    #                         if "inline_data" in part:
    #                             # Decode the base64 image
    #                             image_data = base64.b64decode(part["inline_data"]["data"])
    #                             return Image.open(io.BytesIO(image_data))
    #                         elif "text" in part:
    #                             # If text response, try to extract image from text description
    #                             # This is a fallback - Gemini might not return image directly
    #                             print(f"Text response: {part['text']}")
    #                             continue
                
    #             print("No image data found in Gemini response")
    #             return None
    #         else:
    #             print(f"Gemini API error: {response.status_code} - {response.text}")
    #             return None
                
    #     except Exception as e:
    #         print(f"Error calling Gemini API: {str(e)}")
    #         return None
    
    def _get_cache_key(self, image_data: bytes, model: str, processing_type: str = "print", prompt: str = None) -> str:
        """Generate cache key for image data, model, processing type and prompt"""
        hasher = hashlib.md5()
        hasher.update(image_data)
        hasher.update(model.encode())
        hasher.update(processing_type.encode())
        if prompt:
            hasher.update(prompt.encode())
        return hasher.hexdigest()
    
    def _get_cached_result(self, cache_key: str) -> Optional[Image.Image]:
        """Get cached result if exists"""
        cache_file = self.cache_dir / f"gemini_extracted_{cache_key}.png"
        if cache_file.exists():
            try:
                return Image.open(cache_file)
            except Exception as e:
                print(f"Error loading cached result: {e}")
                cache_file.unlink(missing_ok=True)  # Remove corrupted cache
        return None
    
    def _save_to_cache(self, cache_key: str, image: Image.Image):
        """Save result to cache"""
        try:
            cache_file = self.cache_dir / f"gemini_extracted_{cache_key}.png"
            image.save(cache_file, "PNG")
            print(f"Saved result to cache: {cache_file}")
        except Exception as e:
            print(f"Error saving to cache: {e}")
    
    def clear_cache(self):
        """Clear all cached results"""
        try:
            for cache_file in self.cache_dir.glob("gemini_extracted_*.png"):
                cache_file.unlink()
            print("✅ Cache cleared successfully")
        except Exception as e:
            print(f"Error clearing cache: {e}")
    
    
    def extract_design_with_gemini(self, image_data: bytes, model: str = "gemini-2.5-flash-image-preview", processing_type: str = "print", prompt: str = None) -> Optional[Image.Image]:
        """
        Extract design from image using Gemini Image Generation API with caching
        
        Args:
            image_data: Image bytes
            model: Gemini model to use (should be gemini-2.5-flash-image-preview)
            processing_type: "print", "embroidery", or "mockup" - determines the prompt style
            prompt: Custom prompt to use (overrides processing_type prompt)
            
        Returns:
            PIL Image with extracted design or None if failed
        """
        try:
            # Check cache first
            cache_key = self._get_cache_key(image_data, model, processing_type, prompt)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                print("✅ Using cached Gemini result")
                return cached_result
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Determine MIME type
            mime_type = "image/jpeg"
            if image_data.startswith(b'\x89PNG'):
                mime_type = "image/png"
            elif image_data.startswith(b'GIF'):
                mime_type = "image/gif"
            
            # Choose prompt based on processing type or use custom prompt
            if prompt:
                # Use custom prompt (for mockup mode)
                print(f"📝 Using custom prompt:")
                print(f"   {prompt}")
                print("=" * 80)
            elif processing_type.lower() == "embroidery":
                # prompt = "Vẽ lại thiết kế này theo phong cách thêu thực tế với chỉ len. Sau đó tạo mockup trên áo thun gấp gọn để bán trên Etsy, có trang trí một vài điểm trang trí để làm cho nó trông thực tế."
                prompt = "Như một Designer chuyên nghiệp, hãy thực hiện vẽ lại thiết kế này theo phong cách thêu thực tế trên nền xanh lá tươi có độ tương phản cao phù hợp cho việc tách nền. Thiết kế được khâu bằng chỉ, các đường chỉ thêu ngang và căng bóng, với kết cấu rõ ràng và thể hiện tốt độ sâu 3D. Chỉ thực hiện thêu phần thiết kế, phần nền là màu xanh Chromakey hoàn toàn."
            else:
                # Default print prompt
                prompt = """
                        Như một designer chuyên nghiệp, hãy vẽ lại thiết kế này trên nền xanh lá tươi có độ tương phản cao phù hợp cho việc tách nền. Với các chi tiết của hình ảnh được vẽ lại hoàn toàn, giữ nguyên màu sắc, văn bản, hình ảnh và chi tiết như trong hình gốc. Hãy loại bỏ watermark và logo nếu có trên hình. Điều chỉnh căn giữa và thẳng, đặt thiết kế lớn lên vừa bằng khung ảnh.
                        """
                print(f"📝 Using PRINT prompt:")
                print(f"   {prompt}")
                print("=" * 80)
            
            # Prepare the request payload for image generation
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            },
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "topK": 16,
                    "topP": 0.7,
                    "maxOutputTokens": 8192
                }
            }
            
            # Make API request to image generation model
            model_url = f"{self.base_url}/{model}:generateContent"
            response = requests.post(model_url, headers=self.headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                print(f"API Response structure: {list(result.keys())}")
                
                # Process response according to Gemini Image Generation API format
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]
                    print(f"Candidate structure: {list(candidate.keys())}")
                    
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        print(f"Found {len(parts)} parts in response")
                        
                        # Look for image data in the response parts
                        for i, part in enumerate(parts):
                            print(f"Part {i}: {list(part.keys())}")
                            
                            # Check for inline_data (base64 image)
                            if "inline_data" in part or "inlineData" in part:
                                inline_data = part.get("inline_data") or part.get("inlineData")
                                if inline_data and "data" in inline_data:
                                    print("Found image data in response!")
                                    # Decode the base64 image
                                    image_data_b64 = inline_data["data"]
                                    image_bytes = base64.b64decode(image_data_b64)
                                    raw_image = Image.open(io.BytesIO(image_bytes))
                                    
                                    # Use image directly from API (no background removal)
                                    result_image = raw_image.convert('RGBA') if raw_image.mode != 'RGBA' else raw_image
                                    
                                    # Save processed result to cache
                                    self._save_to_cache(cache_key, result_image)
                                    
                                    return result_image
                            
                            # Log text responses for debugging
                            elif "text" in part:
                                print(f"Text response: {part['text'][:200]}...")
                
                print("No image data found in Gemini response - trying alternative prompt")
                
                # Try with alternative prompt
                if processing_type.lower() == "embroidery":
                    # alternative_prompt = "Vẽ lại thiết kế này theo phong cách thêu thực tế với chỉ len. Sau đó tạo mockup trên áo thun gấp gọn để bán trên Etsy, có trang trí một vài điểm trang trí để làm cho nó trông thực tế."
                    alternative_prompt =  "Như một Designer chuyên nghiệp, hãy thực hiện vẽ lại thiết kế này theo phong cách thêu thực tế trên nền xanh lá tươi có độ tương phản cao phù hợp cho việc tách nền. Thiết kế được khâu bằng chỉ, các đường chỉ thêu ngang và căng bóng, với kết cấu rõ ràng và thể hiện tốt độ sâu 3D. Chỉ thực hiện thêu phần thiết kế, phần nền là màu xanh Chromakey hoàn toàn."
                else:
                    alternative_prompt = """
                                        Như một designer chuyên nghiệp, hãy vẽ lại thiết kế này trên nền xanh lá tươi có độ tương phản cao phù hợp cho việc tách nền. Với các chi tiết của hình ảnh được vẽ lại hoàn toàn, giữ nguyên màu sắc, văn bản, hình ảnh và chi tiết như trong hình gốc. Hãy loại bỏ watermark và logo nếu có trên hình. Điều chỉnh căn giữa và thẳng, đặt thiết kế lớn lên vừa bằng khung ảnh.
                                        """
                # Try alternative request
                alt_payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": alternative_prompt},
                                {
                                    "inline_data": {
                                        "mime_type": mime_type,
                                        "data": image_base64
                                    }
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.05,
                        "topK": 8,
                        "topP": 0.6,
                        "maxOutputTokens": 4096
                    }
                }
                
                print("🔄 Trying alternative prompt...")
                alt_response = requests.post(model_url, headers=self.headers, json=alt_payload, timeout=120)
                
                if alt_response.status_code == 200:
                    alt_result = alt_response.json()
                    if "candidates" in alt_result and len(alt_result["candidates"]) > 0:
                        candidate = alt_result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            parts = candidate["content"]["parts"]
                            for part in parts:
                                if "inline_data" in part or "inlineData" in part:
                                    inline_data = part.get("inline_data") or part.get("inlineData")
                                    if inline_data and "data" in inline_data:
                                        print("✅ Found image data in alternative response!")
                                        image_data_b64 = inline_data["data"]
                                        image_bytes = base64.b64decode(image_data_b64)
                                        raw_image = Image.open(io.BytesIO(image_bytes))
                                        
                                        # Use image directly from API (no background removal)
                                        result_image = raw_image.convert('RGBA') if raw_image.mode != 'RGBA' else raw_image
                                        
                                        # Save processed result to cache
                                        self._save_to_cache(cache_key, result_image)
                                        
                                        return result_image
                
                print("❌ Both attempts failed to generate image")
                print(f"Original response: {result}")
                return None
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_connection(self) -> bool:
        """
        Test the connection to Gemini API
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Test with image generation model
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": "Hello, this is a connection test."
                            }
                        ]
                    }
                ]
            }
            
            # Test with the image generation model
            model_url = f"{self.base_url}/gemini-2.5-flash-image-preview:generateContent"
            response = requests.post(model_url, headers=self.headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ Gemini API connection test successful")
                return True
            else:
                print(f"❌ Gemini API connection test failed: {response.status_code} - {response.text}")
                return False
            
        except Exception as e:
            print(f"Gemini API connection test failed: {str(e)}")
            return False

    def generate_dual_videos_from_image(self, image_path: str, combined_script: str) -> Optional[str]:
        """
        Generate 2 videos with different camera angles and merge them into one 16s video
        
        Args:
            image_path: Path to the input image
            combined_script: Combined script containing both video scripts
            
        Returns:
            Path to merged 16s video file or None if failed
        """
        try:
            if not self.api_key:
                print("❌ API key not provided")
                return None
            
            if not GENAI_AVAILABLE:
                print("❌ Google GenAI library not available. Please install with: pip install google-genai")
                return None
            
            print("🎬 Starting dual video generation with Gemini Veo3...")
            
            # Extract individual scripts from combined script
            try:
                # Split the combined script to get individual scripts
                parts = combined_script.split("🎬 VIDEO 2 (8s) - FULL BODY MOVEMENT:")
                if len(parts) >= 2:
                    script1_part = parts[0].replace("🎬 VIDEO 1 (8s) - CLOSE-UP FOCUS:", "").strip()
                    script2_part = parts[1].split("📝 FINAL:")[0].strip()
                else:
                    # Fallback to original method if script format is different
                    script1_part = combined_script
                    script2_part = combined_script
                    
            except Exception as e:
                print(f"⚠️ Could not parse combined script, using fallback: {e}")
                script1_part = combined_script
                script2_part = combined_script
            
            # Create 2 different prompts using the individual scripts
            prompt1 = f"{script1_part}\n\n**Technical Requirements:**\n- Tỉ lệ khung hình: 9:16 (vertical) - FULL FRAME\n- Thời lượng: 8 giây\n- Focus: Close-up details của thiết kế áo\n- NO TEXT, NO SUBTITLES, NO OVERLAY - chỉ video thuần\n- Fill toàn bộ khung hình 9:16, không có viền đen"
            
            prompt2 = f"{script2_part}\n\n**Technical Requirements:**\n- Tỉ lệ khung hình: 9:16 (vertical) - FULL FRAME\n- Thời lượng: 8 giây\n- Focus: Full body movement và dynamic shots\n- NO TEXT, NO SUBTITLES, NO OVERLAY - chỉ video thuần\n- Fill toàn bộ khung hình 9:16, không có viền đen"
            
            print(f"📝 Prompt 1 (Close-up): {prompt1[:100]}...")
            print(f"📝 Prompt 2 (Medium): {prompt2[:100]}...")
            
            # Generate both videos
            video1_path = self.generate_video_from_image(image_path, prompt1)
            if not video1_path or not os.path.exists(video1_path):
                print("❌ Failed to generate first video")
                return None
                
            print(f"✅ First video generated successfully: {video1_path}")
            
            video2_path = self.generate_video_from_image(image_path, prompt2)
            if not video2_path or not os.path.exists(video2_path):
                print("❌ Failed to generate second video")
                
            print(f"✅ Second video generated successfully: {video2_path}")
            
            # Merge videos using ffmpeg
            merged_video_path = self._merge_videos(video1_path, video2_path)
            
            if merged_video_path:
                print(f"✅ Videos merged successfully: {merged_video_path}")
                return merged_video_path
            else:
                print("⚠️ Failed to merge videos, returning first video as fallback")
                print(f"💡 Install ffmpeg to enable 16s merged videos: brew install ffmpeg")
                return video1_path
                
        except Exception as e:
            print(f"❌ Error in dual video generation: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def generate_video_from_image(self, image_path: str, prompt: str) -> Optional[str]:
        """
        Generate video from image using Gemini Veo3 API with Google GenAI library
        
        Args:
            image_path: Path to the input image
            prompt: Text prompt for video generation
            
        Returns:
            Path to generated video file or None if failed
        """
        try:
            if not self.api_key:
                print("❌ API key not provided")
                return None
            
            if not GENAI_AVAILABLE:
                print("❌ Google GenAI library not available. Please install with: pip install google-genai")
                return None
            
            print("🎬 Starting video generation with Gemini Veo3...")
            print(f"📝 Prompt: {prompt[:100]}...")
            
            # Initialize Google GenAI client
            client = genai.Client(api_key=self.api_key)
            
            # Read image file
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Determine MIME type
            mime_type = "image/jpeg"
            if image_data.startswith(b'\x89PNG'):
                mime_type = "image/png"
            elif image_data.startswith(b'GIF'):
                mime_type = "image/gif"
            
            print("📤 Generating video with Veo3...")
            
            # Generate video using Veo3 with config
            operation = client.models.generate_videos(\
                model="veo-3.0-generate-001",
                prompt=prompt,
                image=types.Image(
                    image_bytes=image_data,
                    mime_type=mime_type
                ),
                config=types.GenerateVideosConfig(
                    aspect_ratio="9:16",
                    person_generation="allow_adult"
                )
            )
            
            print("⏳ Polling for completion...")
            
            # Poll the operation status until the video is ready
            while not operation.done:
                print("Waiting for video generation to complete...")
                time.sleep(10)
                operation = client.operations.get(operation)
            
            print("✅ Video generation completed!")
            
            # Debug: Check operation structure
            print(f"Operation response: {operation.response}")
            print(f"Operation result: {operation.result}")
            
            # Get the generated video - try different possible structures
            video = None
            if operation.response and hasattr(operation.response, 'generated_videos'):
                video = operation.response.generated_videos[0]
            elif operation.result and hasattr(operation.result, 'generated_videos'):
                video = operation.result.generated_videos[0]
            elif hasattr(operation, 'generated_videos'):
                video = operation.generated_videos[0]
            else:
                print("❌ Could not find generated_videos in operation")
                print(f"Available attributes: {dir(operation)}")
                if operation.response:
                    print(f"Response attributes: {dir(operation.response)}")
                if operation.result:
                    print(f"Result attributes: {dir(operation.result)}")
                return None
            
            if not video:
                print("❌ No video found in operation")
                return None
            
            # Setup video cache directory
            video_cache_dir = self.cache_dir.parent / "video_cache"
            video_cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Save video to cache
            video_filename = f"generated_video_{int(time.time())}.mp4"
            video_path = video_cache_dir / video_filename
            
            # Download and save the video
            client.files.download(file=video.video)
            video.video.save(str(video_path))
            
            print(f"✅ Video saved to: {video_path}")
            return str(video_path)
                
        except Exception as e:
            print(f"❌ Error calling Veo3 API: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def generate_text(self, prompt: str) -> Optional[str]:
        """Generate text using Gemini API."""
        try:
            if not GENAI_AVAILABLE:
                print("❌ Google GenAI library not available. Please install with: pip install google-genai")
                return None
            
            print(f"📝 Generating text with gemini-2.5-pro...")
            print(f"📝 Prompt: {prompt[:100]}...")
            
            # Initialize client with API key
            client = genai.Client(api_key=self.api_key)
            
            # Generate text using gemini-2.5-pro
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt
            )
            
            if response and response.text:
                print("✅ Text generated successfully!")
                return response.text
            else:
                print("❌ No text generated")
                return None
                
        except Exception as e:
            print(f"❌ Error generating text: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def generate_text_with_image(self, prompt: str, pil_image: Image.Image = None, image_path: str = None) -> Optional[str]:
        """Generate text with image analysis using Gemini API."""
        try:
            if not GENAI_AVAILABLE:
                print("❌ Google GenAI library not available. Please install with: pip install google-genai")
                return None
            
            print(f"📝 Generating text with image analysis using gemini-2.5-pro...")
            print(f"📝 Prompt: {prompt[:100]}...")
            
            # Initialize client with API key
            client = genai.Client(api_key=self.api_key)
            
            # Prepare image data
            if pil_image is not None:
                # Convert PIL image to bytes
                img_byte_arr = io.BytesIO()
                
                # Convert RGBA to RGB if necessary (JPEG doesn't support transparency)
                if pil_image.mode == 'RGBA':
                    # Create white background
                    background = Image.new('RGB', pil_image.size, (255, 255, 255))
                    background.paste(pil_image, mask=pil_image.split()[-1])  # Use alpha channel as mask
                    pil_image = background
                elif pil_image.mode not in ('RGB', 'L'):
                    # Convert other modes to RGB
                    pil_image = pil_image.convert('RGB')
                
                pil_image.save(img_byte_arr, format='JPEG', quality=95)
                image_data = img_byte_arr.getvalue()
            elif image_path is not None:
                # Read image from file
                with open(image_path, 'rb') as f:
                    image_data = f.read()
            else:
                print("❌ No image provided")
                return None
            
            print("📸 Processing image with Gemini...")
            
            # Use the simplest approach - PIL Image directly
            if pil_image is not None:
                print("📸 Using PIL Image directly...")
                contents = [prompt, pil_image]
            else:
                print("📸 Loading image from path...")
                # Load image from path and use directly
                pil_image_from_path = Image.open(image_path)
                
                # Apply same RGBA conversion if needed
                if pil_image_from_path.mode == 'RGBA':
                    background = Image.new('RGB', pil_image_from_path.size, (255, 255, 255))
                    background.paste(pil_image_from_path, mask=pil_image_from_path.split()[-1])
                    pil_image_from_path = background
                elif pil_image_from_path.mode not in ('RGB', 'L'):
                    pil_image_from_path = pil_image_from_path.convert('RGB')
                
                contents = [prompt, pil_image_from_path]
            
            # Generate text with image using gemini-2.5-pro
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=contents
            )
            
            if response and response.text:
                print("✅ Text with image analysis generated successfully!")
                return response.text
            else:
                print("❌ No text generated from image analysis")
                return None
                
        except Exception as e:
            print(f"❌ Error generating text with image: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _merge_videos(self, video1_path: str, video2_path: str) -> Optional[str]:
        """
        Merge two 8s videos into one 16s video using ffmpeg
        
        Args:
            video1_path: Path to first video
            video2_path: Path to second video
            
        Returns:
            Path to merged video or None if failed
        """
        try:
            import subprocess
            import os
            
            print("🔄 Merging videos with ffmpeg...")
            
            # Setup merged video path
            video_cache_dir = self.cache_dir.parent / "video_cache"
            video_cache_dir.mkdir(parents=True, exist_ok=True)
            
            merged_filename = f"merged_video_{int(time.time())}.mp4"
            merged_path = video_cache_dir / merged_filename
            
            # Create a temporary file list for ffmpeg concat
            filelist_path = video_cache_dir / f"filelist_{int(time.time())}.txt"
            
            with open(filelist_path, 'w') as f:
                f.write(f"file '{video1_path}'\n")
                f.write(f"file '{video2_path}'\n")
            
            # Use ffmpeg to concatenate videos
            ffmpeg_cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(filelist_path),
                '-c', 'copy',
                '-y',  # Overwrite output file
                str(merged_path)
            ]
            
            print(f"🔧 Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
            
            # Run ffmpeg
            result = subprocess.run(ffmpeg_cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=120)
            
            # Clean up temporary file list
            try:
                os.remove(filelist_path)
            except:
                pass
            
            if result.returncode == 0:
                print(f"✅ Videos merged successfully: {merged_path}")
                return str(merged_path)
            else:
                print(f"❌ ffmpeg error (return code: {result.returncode})")
                print(f"❌ stderr: {result.stderr}")
                print(f"❌ stdout: {result.stdout}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ ffmpeg timeout - merging took too long")
            return None
        except FileNotFoundError:
            print("❌ ffmpeg not found. Please install ffmpeg to merge videos")
            return None
        except Exception as e:
            print(f"❌ Error merging videos: {str(e)}")
            return None

