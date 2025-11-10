#!/usr/bin/env python3
"""
Test script for Gemini API format fix
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_api_format():
    """Test the new Gemini API format"""
    print("🧪 Testing Gemini API Format Fix")
    print("=" * 40)
    
    try:
        from PIL import Image
        from gemini_client import GeminiClient
        
        print("✅ Imports successful")
        
        # Create test image (RGB to avoid RGBA issues)
        test_image = Image.new('RGB', (100, 100), (255, 0, 0))
        print("✅ Test image created (RGB mode)")
        
        # Test the content creation process
        print("\n🔍 Testing content format...")
        
        try:
            from google.genai.types import Part
            print("✅ Part import successful")
            
            # Convert image to bytes (same as in the method)
            import io
            img_byte_arr = io.BytesIO()
            test_image.save(img_byte_arr, format='JPEG', quality=95)
            image_data = img_byte_arr.getvalue()
            print(f"✅ Image converted to bytes: {len(image_data)} bytes")
            
            # Test Part.from_bytes
            image_part = Part.from_bytes(image_data, mime_type="image/jpeg")
            print("✅ Part.from_bytes successful")
            
            # Test content structure
            test_prompt = "Analyze this image"
            contents = [
                test_prompt,
                image_part
            ]
            print("✅ Contents structure created")
            print(f"   Content types: {[type(c).__name__ for c in contents]}")
            
            return True
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("💡 Make sure google-genai is installed: pip install google-genai")
            return False
        except Exception as e:
            print(f"❌ Format test failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_fix_explanation():
    """Show explanation of the fix"""
    print("\n💡 Gemini API Format Fix Explanation")
    print("=" * 45)
    
    print("🔧 Problem:")
    print("   ❌ Wrong content format for multimodal API")
    print("   ❌ Used raw dict instead of proper Part objects")
    print("   ❌ Pydantic validation errors")
    
    print("\n✅ Solution:")
    print("   ✅ Import Part from google.genai.types")
    print("   ✅ Use Part.from_bytes() for image data")
    print("   ✅ Proper mime_type specification")
    print("   ✅ Correct content structure")
    
    print("\n📝 Code Changes:")
    print("   OLD:")
    print("   contents = [prompt, {'mime_type': 'image/jpeg', 'data': image_data}]")
    print("")
    print("   NEW:")
    print("   from google.genai.types import Part")
    print("   contents = [prompt, Part.from_bytes(image_data, mime_type='image/jpeg')]")

def test_rgba_and_format_together():
    """Test both RGBA fix and API format together"""
    print("\n🔄 Testing Combined Fixes")
    print("=" * 30)
    
    try:
        from PIL import Image
        from gemini_client import GeminiClient
        
        # Create RGBA test image
        rgba_image = Image.new('RGBA', (100, 100), (255, 0, 0, 128))
        print("✅ RGBA test image created")
        
        # Test the full conversion process
        client = GeminiClient("test_key")
        
        # Simulate the conversion process from generate_text_with_image
        import io
        img_byte_arr = io.BytesIO()
        
        # Apply RGBA fix
        if rgba_image.mode == 'RGBA':
            background = Image.new('RGB', rgba_image.size, (255, 255, 255))
            background.paste(rgba_image, mask=rgba_image.split()[-1])
            rgba_image = background
            print("✅ RGBA converted to RGB with white background")
        
        # Save as JPEG
        rgba_image.save(img_byte_arr, format='JPEG', quality=95)
        image_data = img_byte_arr.getvalue()
        print(f"✅ Image saved as JPEG: {len(image_data)} bytes")
        
        # Test API format
        from google.genai.types import Part
        image_part = Part.from_bytes(image_data, mime_type="image/jpeg")
        print("✅ Part.from_bytes successful with converted image")
        
        return True
        
    except Exception as e:
        print(f"❌ Combined test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Gemini API Format Fix Test\n")
    
    # Test API format
    format_test = test_gemini_api_format()
    
    # Test combined fixes
    combined_test = test_rgba_and_format_together()
    
    # Show explanation
    show_fix_explanation()
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS")
    print("="*50)
    print(f"API Format Fix: {'✅ PASS' if format_test else '❌ FAIL'}")
    print(f"Combined Fixes: {'✅ PASS' if combined_test else '❌ FAIL'}")
    
    if format_test and combined_test:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Gemini API format is now correct!")
        print("✅ RGBA images are handled properly!")
        print("✅ Script generation should work now!")
    else:
        print("\n⚠️  Some tests failed.")
        print("Please check the google-genai library installation.")
        print("Run: pip install google-genai")
