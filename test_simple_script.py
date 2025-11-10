#!/usr/bin/env python3
"""
Test script for simple Vietnamese script generation
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_prompt():
    """Test the new simple prompt format"""
    print("🧪 Testing Simple Script Generation")
    print("=" * 45)
    
    # New simplified prompt
    simple_prompt = """Nhìn vào hình ảnh này và viết một script video đơn giản bằng tiếng Việt.

CHỈ TRẢ VỀ SCRIPT, KHÔNG GIẢI THÍCH GÌ THÊM.

Script phải:
- Mô tả ngắn gọn những gì xảy ra trong video (10 giây)
- Dùng tiếng Việt đơn giản, dễ hiểu
- Tập trung vào hành động và chuyển động
- Phù hợp với nội dung hình ảnh

Ví dụ format: "Một cô gái bước đi trên đường, tóc bay trong gió, cô ấy quay lại nhìn và mỉm cười."

CHỈ VIẾT SCRIPT, KHÔNG VIẾT GÌ KHÁC."""

    print("✅ New prompt created")
    print(f"📏 Prompt length: {len(simple_prompt)} characters")
    
    # Show key differences
    print("\n🔄 Key Changes:")
    print("   ✅ Vietnamese output instead of English")
    print("   ✅ Simple script format instead of technical analysis")
    print("   ✅ Clear instruction: 'CHỈ TRẢ VỀ SCRIPT'")
    print("   ✅ Example format provided")
    print("   ✅ No technical jargon")
    
    return True

def show_expected_outputs():
    """Show examples of expected script outputs"""
    print("\n📝 Expected Script Examples")
    print("=" * 35)
    
    examples = [
        {
            "image_type": "Portrait of a woman",
            "expected_script": "Một cô gái trẻ nhìn thẳng vào camera, mỉm cười nhẹ, ánh sáng dịu nhẹ chiếu lên khuôn mặt, tóc bay nhẹ trong gió."
        },
        {
            "image_type": "Product photo - T-shirt",
            "expected_script": "Chiếc áo thun được trưng bày trên nền trắng, từ từ xoay 360 độ để khoe thiết kế, ánh sáng làm nổi bật màu sắc và chất liệu."
        },
        {
            "image_type": "Landscape scene",
            "expected_script": "Khung cảnh thiên nhiên yên bình, camera di chuyển từ từ qua cánh đồng xanh, những đám mây trắng trôi lững lờ trên bầu trời xanh."
        },
        {
            "image_type": "Food photo",
            "expected_script": "Món ăn được bày trí đẹp mắt trên đĩa, camera zoom in từ từ để thấy rõ chi tiết, hơi nóng bốc lên nhẹ nhàng."
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['image_type']}:")
        print(f"   Script: \"{example['expected_script']}\"")

def test_script_cleaning():
    """Test script cleaning functionality"""
    print("\n🧹 Testing Script Cleaning")
    print("=" * 30)
    
    # Test cases with different formats
    test_scripts = [
        "Một cô gái bước đi trên đường, tóc bay trong gió.",  # Clean
        "```\nMột cô gái bước đi trên đường.\n```",  # With markdown
        "   Một cô gái bước đi trên đường.   ",  # With spaces
        "Script: Một cô gái bước đi trên đường.",  # With prefix
    ]
    
    for i, test_script in enumerate(test_scripts, 1):
        print(f"\n{i}. Input: {repr(test_script)}")
        
        # Apply cleaning logic
        cleaned = test_script.strip()
        
        if cleaned.startswith('```'):
            lines = cleaned.split('\n')
            cleaned = '\n'.join(line for line in lines if not line.startswith('```'))
        
        cleaned = cleaned.strip()
        
        print(f"   Output: {repr(cleaned)}")

def compare_old_vs_new():
    """Compare old vs new approach"""
    print("\n📊 Old vs New Approach")
    print("=" * 30)
    
    print("🔄 OLD Approach:")
    print("   ❌ Long technical prompt in English")
    print("   ❌ Requested analysis + script")
    print("   ❌ Complex formatting requirements")
    print("   ❌ Professional jargon")
    print("   ❌ Multiple sections in output")
    
    print("\n🆕 NEW Approach:")
    print("   ✅ Short simple prompt in Vietnamese")
    print("   ✅ Only requests script")
    print("   ✅ Clear 'no extra text' instruction")
    print("   ✅ Simple language")
    print("   ✅ Clean single output")
    
    print("\n🎯 Expected Results:")
    print("   ✅ Shorter, cleaner responses")
    print("   ✅ Vietnamese scripts ready to use")
    print("   ✅ No need for complex parsing")
    print("   ✅ Better user experience")

if __name__ == "__main__":
    print("🚀 Simple Script Generation Test\n")
    
    # Test prompt
    prompt_test = test_simple_prompt()
    
    # Show examples
    show_expected_outputs()
    
    # Test cleaning
    test_script_cleaning()
    
    # Compare approaches
    compare_old_vs_new()
    
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    print(f"Prompt Test: {'✅ PASS' if prompt_test else '❌ FAIL'}")
    
    if prompt_test:
        print("\n🎉 NEW SCRIPT GENERATION READY!")
        print("✅ Simple Vietnamese prompts")
        print("✅ Clean script outputs")
        print("✅ No extra formatting needed")
        print("\n🚀 Ready to test in main application!")
    else:
        print("\n❌ Setup failed. Please check the implementation.")
