#!/usr/bin/env python3
"""
Setup script to configure Kling AI API keys
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_kling_keys():
    """Setup Kling AI API keys"""
    print("🔑 Kling AI API Keys Setup")
    print("=" * 40)
    
    try:
        from user_manager import UserManager
        
        # Initialize user manager
        user_manager = UserManager()
        
        # Check if user is logged in
        if not user_manager.is_logged_in():
            print("❌ No user is currently logged in.")
            print("Please run the main application and login first.")
            return False
        
        current_user = user_manager.get_current_user()
        print(f"👤 Current user: {current_user}")
        
        # Provided API keys
        access_key = "AQ3tr3gyBCkK8KKQaM9eH9DAL9hmnTAm"
        secret_key = "rkdCtNMdQFnGnPReQEaNbGGMTyKHJeyL"
        
        print(f"\n🔧 Setting up Kling AI API keys...")
        
        # Save the keys
        success1 = user_manager.save_api_key("kling_access_key", access_key)
        success2 = user_manager.save_api_key("kling_secret_key", secret_key)
        
        if success1 and success2:
            print("✅ Kling AI API keys saved successfully!")
            
            # Verify the keys
            print("🔍 Verifying saved keys...")
            saved_access = user_manager.get_api_key("kling_access_key")
            saved_secret = user_manager.get_api_key("kling_secret_key")
            
            if saved_access and saved_secret:
                print("✅ Keys verified successfully!")
                print(f"Access Key: {saved_access[:10]}...{saved_access[-10:]}")
                print(f"Secret Key: {saved_secret[:10]}...{saved_secret[-10:]}")
                
                # Test connection
                print("\n🌐 Testing connection to Kling AI...")
                try:
                    from kling_client import KlingClient
                    client = KlingClient(saved_access, saved_secret)
                    
                    if client.test_connection():
                        print("✅ Connection test successful!")
                        print("🎉 Kling AI is ready for video generation!")
                        return True
                    else:
                        print("❌ Connection test failed")
                        return False
                        
                except Exception as e:
                    print(f"❌ Connection test error: {e}")
                    return False
            else:
                print("❌ Key verification failed")
                return False
        else:
            print("❌ Failed to save API keys")
            return False
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def check_existing_keys():
    """Check if Kling AI keys are already configured"""
    print("🔍 Checking existing Kling AI configuration...")
    
    try:
        from user_manager import UserManager
        user_manager = UserManager()
        
        if not user_manager.is_logged_in():
            print("❌ No user logged in")
            return False
        
        access_key = user_manager.get_api_key("kling_access_key")
        secret_key = user_manager.get_api_key("kling_secret_key")
        
        if access_key and secret_key:
            print("✅ Kling AI keys are already configured")
            print(f"Access Key: {access_key[:10]}...{access_key[-10:]}")
            print(f"Secret Key: {secret_key[:10]}...{secret_key[-10:]}")
            return True
        else:
            print("❌ Kling AI keys not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking keys: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Kling AI Setup Utility")
    print("=" * 50)
    
    # Check existing configuration
    if check_existing_keys():
        response = input("\nKeys already exist. Do you want to overwrite them? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Setup new keys
    if setup_kling_keys():
        print("\n✅ Setup completed successfully!")
        print("You can now use video generation in the JEG Design Studio.")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
