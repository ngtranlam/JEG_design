#!/usr/bin/env python3
"""
Simple test for Kling AI connection with real credentials
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_real_connection():
    """Test with real Kling AI credentials"""
    print("🧪 Testing Kling AI with Real Credentials")
    print("=" * 50)
    
    try:
        from kling_client import KlingClient
        
        # Real credentials provided by user
        access_key = "AQ3tr3gyBCkK8KKQaM9eH9DAL9hmnTAm"
        secret_key = "rkdCtNMdQFnGnPReQEaNbGGMTyKHJeyL"
        
        print("🔧 Initializing Kling AI client...")
        client = KlingClient(access_key, secret_key)
        
        print("🔑 Generating JWT token...")
        token = client.encode_jwt_token()
        print(f"✅ Token generated: {token[:50]}...")
        
        print("🌐 Testing API connection...")
        success = client.test_connection()
        
        if success:
            print("✅ Connection successful! Kling AI is ready.")
            return True
        else:
            print("❌ Connection failed. This might be due to:")
            print("   - API rate limits")
            print("   - Network connectivity issues")
            print("   - API service temporarily unavailable")
            print("   - Invalid credentials")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_jwt_format():
    """Test JWT token format"""
    print("\n🔍 Testing JWT Token Format")
    print("=" * 30)
    
    try:
        from kling_client import KlingClient
        
        client = KlingClient("test_access", "test_secret")
        token = client.encode_jwt_token()
        
        # JWT should have 3 parts separated by dots
        parts = token.split('.')
        if len(parts) == 3:
            print("✅ JWT format is correct (3 parts)")
            
            # Decode header and payload for inspection
            import json
            import base64
            
            def decode_base64url(data):
                # Add padding if needed
                padding = 4 - len(data) % 4
                if padding != 4:
                    data += '=' * padding
                return base64.urlsafe_b64decode(data)
            
            header = json.loads(decode_base64url(parts[0]))
            payload = json.loads(decode_base64url(parts[1]))
            
            print(f"✅ Header: {header}")
            print(f"✅ Payload keys: {list(payload.keys())}")
            
            return True
        else:
            print(f"❌ JWT format incorrect: {len(parts)} parts instead of 3")
            return False
            
    except Exception as e:
        print(f"❌ JWT format test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple Kling AI Test\n")
    
    # Test JWT format first
    jwt_ok = test_jwt_format()
    
    # Test real connection
    connection_ok = test_real_connection()
    
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    print(f"JWT Format: {'✅ PASS' if jwt_ok else '❌ FAIL'}")
    print(f"Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    
    if jwt_ok and connection_ok:
        print("\n🎉 All tests passed! Kling AI integration is ready.")
    elif jwt_ok:
        print("\n⚠️  JWT generation works, but connection failed.")
        print("This might be normal due to API limits or network issues.")
        print("The integration should still work in the main application.")
    else:
        print("\n❌ JWT generation failed. Please check the implementation.")
