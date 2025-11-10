#!/usr/bin/env python3
"""
Test script for Kling AI integration
"""

import os
import sys
from PIL import Image

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_kling_client():
    """Test Kling AI client functionality"""
    print("=== Testing Kling AI Client ===")
    
    try:
        from kling_client import KlingClient
        
        # Test credentials (provided by user)
        access_key = "AQ3tr3gyBCkK8KKQaM9eH9DAL9hmnTAm"
        secret_key = "rkdCtNMdQFnGnPReQEaNbGGMTyKHJeyL"
        
        print(f"✓ Kling client imported successfully")
        
        # Initialize client
        client = KlingClient(access_key, secret_key)
        print(f"✓ Kling client initialized")
        
        # Test JWT token generation
        token = client.encode_jwt_token()
        print(f"✓ JWT token generated: {token[:50]}...")
        
        # Test connection
        print("Testing API connection...")
        success = client.test_connection()
        
        if success:
            print("✅ Connection test successful!")
        else:
            print("❌ Connection test failed")
            
        return success
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_image_conversion():
    """Test image to base64 conversion"""
    print("\n=== Testing Image Conversion ===")
    
    try:
        from kling_client import KlingClient
        
        # Create a simple test image
        test_image = Image.new('RGB', (512, 512), color='red')
        
        client = KlingClient("test", "test")  # Dummy keys for testing conversion
        
        # Test PIL image to base64
        base64_data = client.pil_image_to_base64(test_image)
        
        if base64_data and len(base64_data) > 100:
            print(f"✅ Image conversion successful! Base64 length: {len(base64_data)}")
            return True
        else:
            print("❌ Image conversion failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_user_manager_integration():
    """Test user manager API key storage"""
    print("\n=== Testing User Manager Integration ===")
    
    try:
        from user_manager import UserManager
        
        # Initialize user manager (this might fail if no user is logged in)
        user_manager = UserManager()
        
        # Test saving Kling API keys
        test_access_key = "test_access_key_123"
        test_secret_key = "test_secret_key_456"
        
        success1 = user_manager.save_api_key("kling_access_key", test_access_key)
        success2 = user_manager.save_api_key("kling_secret_key", test_secret_key)
        
        if success1 and success2:
            print("✅ API keys saved successfully")
            
            # Test retrieving keys
            retrieved_access = user_manager.get_api_key("kling_access_key")
            retrieved_secret = user_manager.get_api_key("kling_secret_key")
            
            if retrieved_access == test_access_key and retrieved_secret == test_secret_key:
                print("✅ API keys retrieved successfully")
                
                # Clean up test keys
                user_manager.delete_api_key("kling_access_key")
                user_manager.delete_api_key("kling_secret_key")
                print("✅ Test keys cleaned up")
                
                return True
            else:
                print("❌ API key retrieval failed")
                return False
        else:
            print("❌ API key saving failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting Kling AI Integration Tests\n")
    
    tests = [
        ("Kling Client", test_kling_client),
        ("Image Conversion", test_image_conversion),
        ("User Manager Integration", test_user_manager_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Kling AI integration is ready.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()
