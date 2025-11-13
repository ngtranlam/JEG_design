import requests
import cv2
import numpy as np
from PIL import Image
import io
import tempfile
import os
from typing import Optional

class PhotoRoomClient:
    """
    Client for PhotoRoom API background removal service
    """
    
    def __init__(self, api_key: str = None):
        if not api_key:
            raise ValueError("PhotoRoom API key is required. Please configure your API key in the Account tab.")
        self.api_key = api_key
        self.base_url = "https://sdk.photoroom.com/v1/segment"
        
    def remove_background(self, image_data: np.ndarray) -> Optional[np.ndarray]:
        """
        Remove background from image using PhotoRoom API
        
        Args:
            image_data: Input image as numpy array (BGR format)
            
        Returns:
            Processed image with background removed (BGRA format) or None if failed
        """
        try:
            print("🎨 Calling PhotoRoom API for background removal...")
            
            # Convert numpy array to PIL Image
            if len(image_data.shape) == 3 and image_data.shape[2] == 4:
                # BGRA to RGBA
                rgba_image = cv2.cvtColor(image_data, cv2.COLOR_BGRA2RGBA)
                pil_image = Image.fromarray(rgba_image)
            elif len(image_data.shape) == 3 and image_data.shape[2] == 3:
                # BGR to RGB
                rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_image)
            else:
                pil_image = Image.fromarray(image_data)
            
            # Save to temporary file with high quality to preserve colors
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                # Save with maximum quality and no compression to preserve colors
                pil_image.save(temp_file.name, 'PNG', optimize=False, compress_level=0)
                temp_path = temp_file.name
            
            try:
                # Prepare headers - Note: Don't set Content-Type when using files parameter
                headers = {
                    'Accept': 'image/png, application/json',
                    'x-api-key': self.api_key
                }
                
                # Prepare files - Use original filename and let requests set Content-Type
                with open(temp_path, 'rb') as image_file:
                    files = {
                        'image_file': ('image.png', image_file, 'image/png')
                    }
                    
                    # Add parameters to ensure transparent background
                    data = {
                        'format': 'png',
                        'quality': '100',
                        'bg.color': 'transparent'  # Explicitly request transparent background
                    }
                    
                    # Make API request
                    response = requests.post(
                        self.base_url,
                        headers=headers,
                        files=files,
                        data=data,
                        timeout=30
                    )
                
                if response.status_code == 200:
                    # Process response image
                    result_image = Image.open(io.BytesIO(response.content))
                    result_array = np.array(result_image)
                    
                    # Convert to BGRA format
                    if len(result_array.shape) == 3:
                        if result_array.shape[2] == 4:
                            # RGBA to BGRA
                            result_bgra = cv2.cvtColor(result_array, cv2.COLOR_RGBA2BGRA)
                            print(f"🔍 PhotoRoom returned RGBA image: {result_array.shape}")
                        else:
                            # RGB to BGRA - PhotoRoom might return RGB with white background
                            print(f"🔍 PhotoRoom returned RGB image: {result_array.shape}")
                            print("⚠️ Warning: PhotoRoom returned RGB instead of RGBA - no transparency data")
                            result_bgra = cv2.cvtColor(result_array, cv2.COLOR_RGB2BGRA)
                    else:
                        # Grayscale to BGRA
                        print(f"🔍 PhotoRoom returned Grayscale image: {result_array.shape}")
                        result_bgra = cv2.cvtColor(result_array, cv2.COLOR_GRAY2BGRA)
                    
                    print("✅ PhotoRoom API background removal completed successfully")
                    return result_bgra
                    
                else:
                    print(f"❌ PhotoRoom API error: {response.status_code} - {response.text}")
                    return None
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            print(f"❌ PhotoRoom API error: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to PhotoRoom API
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create a simple test image
            test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255  # White image
            
            result = self.remove_background(test_image)
            return result is not None
            
        except Exception as e:
            print(f"❌ PhotoRoom API connection test failed: {str(e)}")
            return False
