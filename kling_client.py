import time
import requests
import json
import base64
import hmac
import hashlib
from typing import Optional, Dict, Any
import os
from PIL import Image
import io

class KlingClient:
    """
    Kling AI client for video generation from images
    """
    
    def __init__(self, access_key: str, secret_key: str):
        """
        Initialize Kling AI client
        
        Args:
            access_key: Kling AI access key
            secret_key: Kling AI secret key
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_domain = "https://api-singapore.klingai.com"
        
    def encode_jwt_token(self) -> str:
        """
        Generate JWT token for API authentication (manual implementation)
        
        Returns:
            JWT token string
        """
        # JWT Header
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        
        # JWT Payload
        payload = {
            "iss": self.access_key,
            "exp": int(time.time()) + 1800,  # Valid for 30 minutes
            "nbf": int(time.time()) - 5      # Start 5 seconds ago
        }
        
        # Encode header and payload
        def base64url_encode(data):
            return base64.urlsafe_b64encode(json.dumps(data, separators=(',', ':')).encode()).decode().rstrip('=')
        
        encoded_header = base64url_encode(headers)
        encoded_payload = base64url_encode(payload)
        
        # Create signature
        message = f"{encoded_header}.{encoded_payload}"
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        
        encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        # Combine all parts
        token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
        return token
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests
        
        Returns:
            Dictionary with authorization headers
        """
        token = self.encode_jwt_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def image_to_base64(self, image_path: str, crop_to_9_16: bool = True) -> Optional[str]:
        """
        Convert image file to base64 string
        
        Args:
            image_path: Path to image file
            crop_to_9_16: Whether to crop image to 9:16 ratio before encoding
            
        Returns:
            Base64 encoded string or None if error
        """
        try:
            # Load image as PIL Image for processing
            pil_image = Image.open(image_path)
            return self.pil_image_to_base64(pil_image, crop_to_9_16)
        except Exception as e:
            print(f"Error converting image to base64: {str(e)}")
            return None
    
    def crop_to_9_16_ratio(self, pil_image: Image.Image) -> Image.Image:
        """
        Crop image to 9:16 aspect ratio (vertical format for mobile/social media)
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            Cropped PIL Image with 9:16 aspect ratio
        """
        try:
            width, height = pil_image.size
            target_ratio = 9 / 16  # 0.5625
            current_ratio = width / height
            
            if abs(current_ratio - target_ratio) < 0.01:
                # Already close to 9:16 ratio
                return pil_image
            
            if current_ratio > target_ratio:
                # Image is too wide, crop width
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                right = left + new_width
                cropped = pil_image.crop((left, 0, right, height))
            else:
                # Image is too tall, crop height
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                bottom = top + new_height
                cropped = pil_image.crop((0, top, width, bottom))
            
            print(f"🔄 Image cropped from {width}x{height} to {cropped.size[0]}x{cropped.size[1]} (9:16 ratio)")
            return cropped
            
        except Exception as e:
            print(f"Error cropping image to 9:16 ratio: {str(e)}")
            return pil_image  # Return original if cropping fails
    
    def pil_image_to_base64(self, pil_image: Image.Image, crop_to_9_16: bool = True) -> Optional[str]:
        """
        Convert PIL Image to base64 string
        
        Args:
            pil_image: PIL Image object
            crop_to_9_16: Whether to crop image to 9:16 ratio before encoding
            
        Returns:
            Base64 encoded string or None if error
        """
        try:
            # Crop to 9:16 ratio if requested
            if crop_to_9_16:
                pil_image = self.crop_to_9_16_ratio(pil_image)
            
            # Convert to RGB if not already (handle RGBA properly)
            if pil_image.mode == 'RGBA':
                # Create white background for RGBA images
                background = Image.new('RGB', pil_image.size, (255, 255, 255))
                background.paste(pil_image, mask=pil_image.split()[-1])  # Use alpha channel as mask
                pil_image = background
            elif pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Save to bytes buffer
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=95)
            image_data = buffer.getvalue()
            
            # Encode to base64
            base64_string = base64.b64encode(image_data).decode('utf-8')
            return base64_string
        except Exception as e:
            print(f"Error converting PIL image to base64: {str(e)}")
            return None
    
    def create_video_task(self, image_path: str = None, pil_image: Image.Image = None, 
                         prompt: str = "", model_name: str = "kling-v2-5-turbo", 
                         mode: str = "pro", duration: str = "10", 
                         cfg_scale: float = 0.5) -> Optional[Dict[str, Any]]:
        """
        Create a video generation task
        
        Args:
            image_path: Path to input image file
            pil_image: PIL Image object (alternative to image_path)
            prompt: Text prompt for video generation
            model_name: Model to use (kling-v1, kling-v1-5, etc.)
            mode: Generation mode (std, pro)
            duration: Video duration in seconds (5, 10)
            cfg_scale: Configuration scale (0-1)
            
        Returns:
            Task creation response or None if failed
        """
        try:
            # Get image as base64
            if pil_image is not None:
                image_base64 = self.pil_image_to_base64(pil_image)
            elif image_path and os.path.exists(image_path):
                image_base64 = self.image_to_base64(image_path)
            else:
                print("Error: No valid image provided")
                return None
            
            if not image_base64:
                print("Error: Failed to convert image to base64")
                return None
            
            # Prepare request data
            data = {
                "model_name": model_name,
                "mode": mode,
                "duration": duration,
                "image": image_base64,
                "prompt": prompt,
                "cfg_scale": cfg_scale
            }
            
            # Make API request
            url = f"{self.api_domain}/v1/videos/image2video"
            headers = self.get_auth_headers()
            
            print(f"Creating video task with Kling AI...")
            print(f"Model: {model_name}, Mode: {mode}, Duration: {duration}s")
            print(f"Prompt: {prompt[:100]}..." if len(prompt) > 100 else f"Prompt: {prompt}")
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    print("✅ Video task created successfully!")
                    return result
                else:
                    print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating video task: {str(e)}")
            return None
    
    def query_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Query the status of a video generation task
        
        Args:
            task_id: Task ID returned from create_video_task
            
        Returns:
            Task status response or None if failed
        """
        try:
            url = f"{self.api_domain}/v1/videos/image2video/{task_id}"
            headers = self.get_auth_headers()
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    return result
                else:
                    print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error querying task status: {str(e)}")
            return None
    
    def wait_for_completion(self, task_id: str, max_wait_time: int = 300, 
                           check_interval: int = 10) -> Optional[Dict[str, Any]]:
        """
        Wait for a video generation task to complete
        
        Args:
            task_id: Task ID to wait for
            max_wait_time: Maximum time to wait in seconds
            check_interval: How often to check status in seconds
            
        Returns:
            Final task result or None if failed/timeout
        """
        start_time = time.time()
        
        print(f"⏳ Waiting for video generation to complete...")
        print(f"Task ID: {task_id}")
        
        while time.time() - start_time < max_wait_time:
            result = self.query_task_status(task_id)
            
            if not result:
                print("❌ Failed to query task status")
                return None
            
            task_status = result.get("data", {}).get("task_status", "")
            
            if task_status == "succeed":
                print("✅ Video generation completed successfully!")
                return result
            elif task_status == "failed":
                error_msg = result.get("data", {}).get("task_status_msg", "Unknown error")
                print(f"❌ Video generation failed: {error_msg}")
                return None
            elif task_status in ["submitted", "processing"]:
                elapsed = int(time.time() - start_time)
                print(f"⏳ Status: {task_status} (elapsed: {elapsed}s)")
                time.sleep(check_interval)
            else:
                print(f"⚠️ Unknown status: {task_status}")
                time.sleep(check_interval)
        
        print(f"⏰ Timeout: Video generation took longer than {max_wait_time} seconds")
        return None
    
    def generate_video_from_image(self, image_path: str = None, pil_image: Image.Image = None,
                                 prompt: str = "", model_name: str = "kling-v2-5-turbo",
                                 mode: str = "pro", duration: str = "10") -> Optional[str]:
        """
        Generate video from image (complete workflow)
        
        Args:
            image_path: Path to input image file
            pil_image: PIL Image object (alternative to image_path)
            prompt: Text prompt for video generation
            model_name: Model to use
            mode: Generation mode (std, pro)
            duration: Video duration in seconds
            
        Returns:
            URL of generated video or None if failed
        """
        try:
            # Create task
            task_result = self.create_video_task(
                image_path=image_path,
                pil_image=pil_image,
                prompt=prompt,
                model_name=model_name,
                mode=mode,
                duration=duration
            )
            
            if not task_result:
                return None
            
            task_id = task_result.get("data", {}).get("task_id")
            if not task_id:
                print("❌ No task ID received")
                return None
            
            # Wait for completion
            final_result = self.wait_for_completion(task_id)
            
            if not final_result:
                return None
            
            # Extract video URL
            videos = final_result.get("data", {}).get("task_result", {}).get("videos", [])
            if videos and len(videos) > 0:
                video_url = videos[0].get("url")
                if video_url:
                    print(f"🎬 Video generated successfully: {video_url}")
                    return video_url
                else:
                    print("❌ No video URL in response")
                    return None
            else:
                print("❌ No videos in response")
                return None
                
        except Exception as e:
            print(f"❌ Error in video generation workflow: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test the API connection and credentials
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            print("🔍 Testing Kling AI connection...")
            
            # Try to get a JWT token
            token = self.encode_jwt_token()
            if not token:
                print("❌ Failed to generate JWT token")
                return False
            
            print(f"✅ JWT token generated successfully")
            
            # Test with a simple API call (query tasks list)
            url = f"{self.api_domain}/v1/videos/image2video"
            headers = self.get_auth_headers()
            
            print(f"🌐 Testing API endpoint: {url}")
            
            # Add query parameters for list endpoint
            params = {"pageNum": 1, "pageSize": 1}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📄 Response data: {result}")
                
                if result.get("code") == 0:
                    print("✅ API connection successful!")
                    return True
                else:
                    print(f"⚠️ API returned error code: {result.get('code')} - {result.get('message', 'Unknown error')}")
                    # Still consider it a successful connection if we got a proper response
                    return True
            elif response.status_code == 401:
                print("❌ Authentication failed - please check your API keys")
                return False
            elif response.status_code == 403:
                print("❌ Access forbidden - API keys may be invalid or expired")
                return False
            else:
                print(f"⚠️ Unexpected status code: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                # For other status codes, we'll consider it a connection issue but keys might be valid
                return True
                
        except requests.exceptions.Timeout:
            print("⏰ Connection timeout - API may be slow or unavailable")
            return False
        except requests.exceptions.ConnectionError:
            print("🌐 Connection error - please check your internet connection")
            return False
        except Exception as e:
            print(f"❌ Connection test failed: {str(e)}")
            return False
