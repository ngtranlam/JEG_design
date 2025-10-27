import subprocess
import tempfile
from pathlib import Path
import threading
import cv2
from PIL import Image
import numpy as np
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

class UpscaylProcessor:
    def __init__(self, log_callback=None, cancel_event=None):
        self.log_callback = log_callback or print
        self.cancel_event = cancel_event or threading.Event()

    def log(self, msg):
        """Log processing steps via callback"""
        self.log_callback(f"[Upscayl] {msg}")

    def _check_cancel(self):
        """Checks if the cancel event is set and raises an exception."""
        if self.cancel_event.is_set():
            raise RuntimeError("Upscale process cancelled by user.")

    def run_upscayl(self, image: Image.Image, model: str, scale: int = 4):
        """
        Runs the Upscayl AI process on a PIL Image and streams output to a callback.
        """
        self.log(f"Starting AI Upscale (Model: {model}, Scale: {scale}x)...")
        self.log(f"Input image size: {image.size}")
        self._check_cancel()
        
        # Convert PIL Image to a format cv2 can use (BGR)
        # If it's RGBA, we need to handle the alpha channel separately
        is_rgba = image.mode == 'RGBA'
        if is_rgba:
            alpha_channel = np.array(image.split()[-1])
            cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
        else:
            cv2_image = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_input_path = temp_dir_path / "temp_input.png"
            temp_output_path = temp_dir_path / "temp_output.png"

            # Save the image using cv2
            cv2.imwrite(str(temp_input_path), cv2_image)
            
            command = [
                str(UPSCARYL_EXEC_PATH),
                "-i", str(temp_input_path),
                "-o", str(temp_output_path),
                "-s", str(scale),
                "-m", str(UPSCARYL_MODELS_PATH),
                "-f", "png",
                "-n", model
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
                
                # Stream the output
                for line in iter(process.stdout.readline, ''):
                    self._check_cancel()
                    if line:
                        self.log(line.strip())
                
                process.stdout.close()
                return_code = process.wait()
                self._check_cancel()

                if return_code != 0:
                    raise RuntimeError(f"Upscayl process failed with code {return_code}")

            except FileNotFoundError:
                self.log(f"ERROR: Upscayl executable not found at: {UPSCARYL_EXEC_PATH}")
                raise
            except Exception as e:
                self.log(f"Error during AI Upscale: {e}")
                raise

            if not temp_output_path.exists():
                self.log("ERROR: Upscayl did not generate an output file.")
                raise FileNotFoundError("Upscayl output file not found.")
                
            # Read the upscaled image using cv2
            upscaled_bgr = cv2.imread(str(temp_output_path), cv2.IMREAD_COLOR)
            
            # Convert back to PIL Image (RGB)
            upscaled_rgb = cv2.cvtColor(upscaled_bgr, cv2.COLOR_BGR2RGB)
            final_image = Image.fromarray(upscaled_rgb)

            # If the original image had an alpha channel, resize it and re-apply it
            if is_rgba:
                self.log("Re-applying alpha channel...")
                original_width, original_height = image.size
                new_width, new_height = final_image.size
                
                # Use PIL for resizing the alpha channel to ensure quality
                alpha_pil = Image.fromarray(alpha_channel)
                resized_alpha_pil = alpha_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                final_image.putalpha(resized_alpha_pil)

            self.log(f"Output image size: {final_image.size}")
            self.log("AI Upscale complete.")
            return final_image

            
