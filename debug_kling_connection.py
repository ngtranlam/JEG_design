#!/usr/bin/env python3
"""
Debug script for Kling AI connection issues
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_connection():
    """Debug Kling AI connection with detailed output"""
    print("🔧 Kling AI Connection Debug")
    print("=" * 50)
    
    try:
        from kling_client import KlingClient
        import requests
        
        # API credentials
        access_key = "AQ3tr3gyBCkK8KKQaM9eH9DAL9hmnTAm"
        secret_key = "rkdCtNMdQFnGnPReQEaNbGGMTyKHJeyL"
        
        print(f"🔑 Access Key: {access_key[:10]}...{access_key[-10:]}")
        print(f"🔑 Secret Key: {secret_key[:10]}...{secret_key[-10:]}")
        
        # Initialize client
        client = KlingClient(access_key, secret_key)
        print(f"✅ Client initialized")
        
        # Test JWT generation
        print("\n🔍 Testing JWT Generation...")
        token = client.encode_jwt_token()
        print(f"Token length: {len(token)}")
        print(f"Token preview: {token[:50]}...")
        
        # Test headers
        print("\n🔍 Testing Headers...")
        headers = client.get_auth_headers()
        print(f"Headers: {headers}")
        
        # Test basic connectivity
        print("\n🔍 Testing Basic Connectivity...")
        try:
            response = requests.get("https://api-singapore.klingai.com", timeout=10)
            print(f"Basic connectivity: {response.status_code}")
        except Exception as e:
            print(f"Basic connectivity failed: {e}")
        
        # Test API endpoint
        print("\n🔍 Testing API Endpoint...")
        url = "https://api-singapore.klingai.com/v1/videos/image2video"
        params = {"pageNum": 1, "pageSize": 1}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            print(f"API Response Status: {response.status_code}")
            print(f"API Response Headers: {dict(response.headers)}")
            
            if response.text:
                print(f"API Response Body: {response.text[:500]}...")
            
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    print(f"JSON Response: {json_data}")
                except:
                    print("Response is not valid JSON")
            
        except Exception as e:
            print(f"API endpoint test failed: {e}")
        
        # Test full connection method
        print("\n🔍 Testing Full Connection Method...")
        success = client.test_connection()
        print(f"Connection test result: {success}")
        
        return success
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_jwt_manually():
    """Test JWT generation manually"""
    print("\n🔍 Manual JWT Test")
    print("=" * 30)
    
    try:
        import time
        import json
        import base64
        import hmac
        import hashlib
        
        access_key = "AQ3tr3gyBCkK8KKQaM9eH9DAL9hmnTAm"
        secret_key = "rkdCtNMdQFnGnPReQEaNbGGMTyKHJeyL"
        
        # Create header and payload
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "iss": access_key,
            "exp": int(time.time()) + 1800,
            "nbf": int(time.time()) - 5
        }
        
        print(f"Header: {header}")
        print(f"Payload: {payload}")
        
        # Encode
        def base64url_encode(data):
            return base64.urlsafe_b64encode(json.dumps(data, separators=(',', ':')).encode()).decode().rstrip('=')
        
        encoded_header = base64url_encode(header)
        encoded_payload = base64url_encode(payload)
        
        print(f"Encoded Header: {encoded_header}")
        print(f"Encoded Payload: {encoded_payload}")
        
        # Create signature
        message = f"{encoded_header}.{encoded_payload}"
        signature = hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        
        encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        # Final token
        token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
        
        print(f"Final Token: {token}")
        print(f"Token Length: {len(token)}")
        
        return token
        
    except Exception as e:
        print(f"Manual JWT test failed: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Kling AI Connection Debugger\n")
    
    # Test JWT manually
    jwt_token = test_jwt_manually()
    
    # Debug connection
    connection_ok = debug_connection()
    
    print("\n" + "="*50)
    print("📊 DEBUG SUMMARY")
    print("="*50)
    print(f"JWT Generation: {'✅ OK' if jwt_token else '❌ FAIL'}")
    print(f"Connection Test: {'✅ OK' if connection_ok else '❌ FAIL'}")
    
    if jwt_token and not connection_ok:
        print("\n💡 RECOMMENDATIONS:")
        print("1. Check your internet connection")
        print("2. Try using a VPN if behind corporate firewall")
        print("3. Verify API keys are still valid")
        print("4. Check if Kling AI service is operational")
    elif jwt_token and connection_ok:
        print("\n🎉 Everything looks good! The integration should work.")
    else:
        print("\n❌ There are issues with the JWT generation.")
