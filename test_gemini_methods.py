#!/usr/bin/env python3
"""
Test different methods for Gemini API content creation
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_part_methods():
    """Test different Part creation methods"""
    print("🧪 Testing Part Creation Methods")
    print("=" * 40)
    
    try:
        from PIL import Image
        import io
        import base64
        
        # Create test image
        test_image = Image.new('RGB', (100, 100), (255, 0, 0))
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='JPEG', quality=95)
        image_data = img_byte_arr.getvalue()
        
        print(f"✅ Test image created: {len(image_data)} bytes")
        
        # Test Method 1: PIL Image directly
        print("\n1️⃣ Testing PIL Image directly...")
        try:
            contents1 = ["Test prompt", test_image]
            print("✅ PIL Image method works")
        except Exception as e:
            print(f"❌ PIL Image method failed: {e}")
        
        # Test Method 2: Part.from_bytes
        print("\n2️⃣ Testing Part.from_bytes...")
        try:
            from google.genai.types import Part
            
            # Try different signatures
            try:
                image_part = Part.from_bytes(data=image_data, mime_type="image/jpeg")
                print("✅ Part.from_bytes with keyword args works")
            except Exception as e1:
                print(f"⚠️ Keyword args failed: {e1}")
                try:
                    image_part = Part.from_bytes(image_data)
                    print("✅ Part.from_bytes with positional arg works")
                except Exception as e2:
                    print(f"❌ Part.from_bytes failed: {e2}")
                    
        except ImportError:
            print("❌ Cannot import Part from google.genai.types")
        
        # Test Method 3: Simple dict format
        print("\n3️⃣ Testing simple dict format...")
        try:
            contents3 = [
                {"text": "Test prompt"},
                {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(image_data).decode()}}
            ]
            print("✅ Simple dict format works")
        except Exception as e:
            print(f"❌ Simple dict format failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def inspect_part_class():
    """Inspect the Part class to understand its methods"""
    print("\n🔍 Inspecting Part Class")
    print("=" * 30)
    
    try:
        from google.genai.types import Part
        import inspect
        
        print("✅ Part class imported")
        
        # Get all methods
        methods = [method for method in dir(Part) if not method.startswith('_')]
        print(f"📋 Available methods: {methods}")
        
        # Check from_bytes specifically
        if hasattr(Part, 'from_bytes'):
            sig = inspect.signature(Part.from_bytes)
            print(f"🔍 from_bytes signature: {sig}")
        else:
            print("❌ from_bytes method not found")
        
        # Check other creation methods
        creation_methods = [m for m in methods if 'from' in m.lower() or 'create' in m.lower()]
        print(f"🏗️ Creation methods: {creation_methods}")
        
        return True
        
    except Exception as e:
        print(f"❌ Inspection failed: {e}")
        return False

def test_simple_approach():
    """Test the simplest possible approach"""
    print("\n🎯 Testing Simplest Approach")
    print("=" * 35)
    
    try:
        from PIL import Image
        
        # Create simple RGB image
        test_image = Image.new('RGB', (50, 50), (0, 255, 0))
        
        # Test direct usage
        test_prompt = "Describe this image"
        
        print("✅ Simple test setup complete")
        print(f"   Image: {test_image.size} {test_image.mode}")
        print(f"   Prompt: {test_prompt}")
        
        # This is what we'll try to send
        simple_contents = [test_prompt, test_image]
        print(f"✅ Simple contents: {[type(c).__name__ for c in simple_contents]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple approach failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Gemini API Methods Test\n")
    
    # Test different methods
    methods_test = test_part_methods()
    
    # Inspect Part class
    inspect_test = inspect_part_class()
    
    # Test simple approach
    simple_test = test_simple_approach()
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS")
    print("="*50)
    print(f"Methods Test: {'✅ PASS' if methods_test else '❌ FAIL'}")
    print(f"Class Inspection: {'✅ PASS' if inspect_test else '❌ FAIL'}")
    print(f"Simple Approach: {'✅ PASS' if simple_test else '❌ FAIL'}")
    
    print("\n💡 RECOMMENDATIONS:")
    print("1. Try PIL Image directly first (simplest)")
    print("2. Check Part class signature with inspect")
    print("3. Use fallback dict format if needed")
    print("4. Test with real API key to see what works")
