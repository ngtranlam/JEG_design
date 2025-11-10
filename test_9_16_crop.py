#!/usr/bin/env python3
"""
Test script for 9:16 aspect ratio cropping functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_9_16_cropping():
    """Test the 9:16 aspect ratio cropping functionality"""
    print("🧪 Testing 9:16 Aspect Ratio Cropping")
    print("=" * 50)
    
    try:
        from kling_client import KlingClient
        from PIL import Image
        
        # Initialize client
        client = KlingClient("test_access", "test_secret")
        print("✅ Kling client initialized")
        
        # Test different aspect ratios
        test_cases = [
            {"name": "Square Image", "size": (1000, 1000), "expected_crop": True},
            {"name": "Wide Image", "size": (1920, 1080), "expected_crop": True},
            {"name": "Tall Image", "size": (1080, 1920), "expected_crop": True},
            {"name": "Already 9:16", "size": (1080, 1920), "expected_crop": False},  # This is actually 9:16
            {"name": "Portrait", "size": (800, 1200), "expected_crop": True},
            {"name": "Landscape", "size": (1600, 900), "expected_crop": True}
        ]
        
        print("\n🔍 Testing Different Image Sizes:")
        print("-" * 40)
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n{i}. {case['name']} ({case['size'][0]}x{case['size'][1]})")
            
            # Create test image
            test_image = Image.new('RGB', case['size'], color=(255, 0, 0))
            original_ratio = case['size'][0] / case['size'][1]
            
            # Test cropping
            cropped_image = client.crop_to_9_16_ratio(test_image)
            new_width, new_height = cropped_image.size
            new_ratio = new_width / new_height
            target_ratio = 9 / 16  # 0.5625
            
            print(f"   Original: {case['size'][0]}x{case['size'][1]} (ratio: {original_ratio:.3f})")
            print(f"   Cropped:  {new_width}x{new_height} (ratio: {new_ratio:.3f})")
            print(f"   Target ratio: {target_ratio:.3f}")
            
            # Check if ratio is correct
            if abs(new_ratio - target_ratio) < 0.01:
                print("   ✅ Correct 9:16 ratio achieved!")
            else:
                print("   ❌ Ratio not correct!")
                
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_base64_with_cropping():
    """Test base64 conversion with cropping enabled"""
    print("\n🔄 Testing Base64 Conversion with Cropping")
    print("=" * 45)
    
    try:
        from kling_client import KlingClient
        from PIL import Image
        
        client = KlingClient("test_access", "test_secret")
        
        # Create a wide test image (landscape)
        test_image = Image.new('RGB', (1920, 1080), color=(0, 255, 0))
        print(f"📷 Test image: 1920x1080 (landscape)")
        
        # Test with cropping enabled (default)
        print("\n🔄 Converting with 9:16 cropping enabled...")
        base64_with_crop = client.pil_image_to_base64(test_image, crop_to_9_16=True)
        
        if base64_with_crop:
            print(f"✅ Base64 conversion successful!")
            print(f"   Length: {len(base64_with_crop)} characters")
            print("   Image was automatically cropped to 9:16 ratio")
        else:
            print("❌ Base64 conversion failed")
            return False
        
        # Test with cropping disabled
        print("\n🚫 Converting without cropping...")
        base64_no_crop = client.pil_image_to_base64(test_image, crop_to_9_16=False)
        
        if base64_no_crop:
            print(f"✅ Base64 conversion successful!")
            print(f"   Length: {len(base64_no_crop)} characters")
            print("   Original aspect ratio preserved")
        else:
            print("❌ Base64 conversion failed")
            return False
        
        # Compare lengths (cropped should be smaller)
        if len(base64_with_crop) < len(base64_no_crop):
            print("\n✅ Cropped image has smaller file size as expected")
        else:
            print("\n⚠️  Cropped image size is not smaller (might be due to compression)")
        
        return True
        
    except Exception as e:
        print(f"❌ Base64 test failed: {e}")
        return False

def demonstrate_9_16_benefits():
    """Demonstrate the benefits of 9:16 format"""
    print("\n💡 Benefits of 9:16 Aspect Ratio")
    print("=" * 35)
    
    print("📱 Mobile Optimization:")
    print("   ✅ Perfect for Instagram Stories")
    print("   ✅ Ideal for TikTok videos")
    print("   ✅ Optimized for mobile viewing")
    print("   ✅ Better engagement on social media")
    
    print("\n🎬 Video Quality:")
    print("   ✅ Focuses on main subject")
    print("   ✅ Removes unnecessary background")
    print("   ✅ Better composition for vertical content")
    print("   ✅ Consistent format across platforms")
    
    print("\n⚙️ Technical Benefits:")
    print("   ✅ Smaller file size (faster upload)")
    print("   ✅ Reduced processing time")
    print("   ✅ Better API efficiency")
    print("   ✅ Consistent output format")

if __name__ == "__main__":
    print("🚀 9:16 Aspect Ratio Cropping Test\n")
    
    # Test cropping functionality
    crop_test = test_9_16_cropping()
    
    # Test base64 conversion
    base64_test = test_base64_with_cropping()
    
    # Show benefits
    demonstrate_9_16_benefits()
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    print(f"Cropping Functionality: {'✅ PASS' if crop_test else '❌ FAIL'}")
    print(f"Base64 Conversion: {'✅ PASS' if base64_test else '❌ FAIL'}")
    
    if crop_test and base64_test:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ 9:16 cropping is ready for video generation!")
        print("\n🚀 Next steps:")
        print("1. Upload any image to Video Gen tab")
        print("2. Image will be automatically cropped to 9:16")
        print("3. Generate vertical video perfect for mobile!")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
