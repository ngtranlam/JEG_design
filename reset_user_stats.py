#!/usr/bin/env python3
"""
Reset user statistics script
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from user_manager import UserManager

def reset_user_stats(username):
    """Reset statistics for a specific user"""
    print(f"🔄 Resetting stats for user: {username}")
    
    # Initialize user manager
    user_manager = UserManager()
    
    # Load users data
    users_data = user_manager._load_users_data()
    
    if username not in users_data:
        print(f"❌ User {username} not found!")
        return False
    
    # Get current stats
    user_data = users_data[username]
    usage_history = user_data.get('usage_history', [])
    print(f"\n📊 Current Stats for {username}:")
    print(f"  Image usage: {user_data['image_usage_count']}")
    print(f"  Video usage: {user_data['video_usage_count']}")
    print(f"  Image cost: ${user_data['total_image_cost']:.4f}")
    print(f"  Video cost: ${user_data['total_video_cost']:.2f}")
    print(f"  Total cost: ${user_data['total_image_cost'] + user_data['total_video_cost']:.4f}")
    print(f"  Usage history records: {len(usage_history)}")
    
    # Reset ALL stats including usage history
    user_data['image_usage_count'] = 0
    user_data['video_usage_count'] = 0
    user_data['total_image_cost'] = 0.0
    user_data['total_video_cost'] = 0.0
    user_data['usage_history'] = []  # Clear all historical data
    
    # Save updated data
    user_manager._save_users_data(users_data)
    
    print(f"\n✅ Stats reset successfully for {username}!")
    print(f"📊 New Stats:")
    print(f"  Image usage: 0")
    print(f"  Video usage: 0")
    print(f"  Image cost: $0.0000")
    print(f"  Video cost: $0.00")
    print(f"  Total cost: $0.0000")
    print(f"  Usage history records: 0")
    
    return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Reset user statistics')
    parser.add_argument('username', nargs='?', default='lamdev', 
                       help='Username to reset (default: lamdev)')
    
    args = parser.parse_args()
    
    # Confirm reset
    print(f"⚠️  WARNING: This will completely reset ALL data for '{args.username}':")
    print("   - All usage counts (image/video)")
    print("   - All cost calculations")
    print("   - Complete usage history (all dates)")
    print("   - This action cannot be undone!")
    
    response = input(f"\nAre you sure you want to COMPLETELY RESET all data for '{args.username}'? (y/N): ")
    if response.lower() != 'y':
        print("❌ Reset cancelled")
        return
    
    # Reset stats
    success = reset_user_stats(args.username)
    
    if success:
        print(f"\n🎉 User '{args.username}' stats have been reset!")
    else:
        print(f"\n❌ Failed to reset stats for '{args.username}'")

if __name__ == "__main__":
    main()
