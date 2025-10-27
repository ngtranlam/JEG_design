import json
import hashlib
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import requests
import threading
import time

class UserManager:
    """
    Manages user authentication, usage tracking, and cost calculation for JEG Design Extract
    """
    
    # Pricing configuration
    IMAGE_PROCESSING_COST = 0.0203  # $0.0203 per image processing
    VIDEO_GENERATION_COST = 6.4     # $6.4 per video generation
    
    # Default password for all users
    DEFAULT_PASSWORD = "jeg@12345"
    
    # Predefined usernames
    PREDEFINED_USERS = [
        "lamdev", "huynhtan", "nguyen", "toniwintheiser15754", "minhductran1996",
        "hoangbao2411", "quangduc.24696@gmail.com", "ducmy10081987@gmail.com",
        "linkkany21", "thucuyen97", "hoanguyen14", "chautuan154", "tongthaomy",
        "ngockim96", "chaulien1807", "nguyentuyenktdt@gmail.com", "Vantich2021",
        "thao1607", "HongNhung", "phamthuyvan9x", "sumydn", "XuanThuy",
        "trucquynh1099@gmail.com", "congnguyen0312@gmail.com", "hoang0806",
        "chienpv96", "nthaqtkd", "thanhtd", "thuthaokt982023", "thaoptt235@gmail.com",
        "ngocanh25101996", "nguyenngocvnhcm", "anhthu27901", "tuyetsuong2k1",
        "nhnguyen12a1@gmail", "tranhien", "anhthu309", "tranhainam",
        "ngocsanghuynh", "baongocle", "minhtiendao", "hoang1492001",
        "nguyentung", "Nguyendo", "phuongtrinhjeg", "anbinhjeg", "lethangjeg",
        "khanhhung", "ngochuyenjeg", "ngocthanhjeg"
    ]
    
    def __init__(self, api_endpoint: str = None):
        self.api_endpoint = api_endpoint or "https://jegdn.com/api/tools/update"
        self.current_user = None
        self.session_data = {}
        
        # Setup local data directory
        self.data_dir = self._get_data_directory()
        self.users_file = self.data_dir / "users.json"
        self.session_file = self.data_dir / "session.json"
        self.device_id_file = self.data_dir / "device_id.txt"
        
        # Initialize data files
        self._initialize_data_files()
        
        # Generate or load device ID
        self.device_id = self._get_or_create_device_id()
    
    def _get_data_directory(self) -> Path:
        """Get the data directory for storing user data"""
        try:
            home_dir = Path.home()
            data_dir = home_dir / "JEGDesignExtract" / "user_data"
        except:
            import tempfile
            data_dir = Path(tempfile.gettempdir()) / "JEGDesignExtract" / "user_data"
        
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    def _get_or_create_device_id(self) -> str:
        """Generate or load unique device ID"""
        if self.device_id_file.exists():
            try:
                return self.device_id_file.read_text().strip()
            except:
                pass
        
        # Generate new device ID
        import uuid
        device_id = str(uuid.uuid4())
        try:
            self.device_id_file.write_text(device_id)
        except:
            pass
        return device_id
    
    def _initialize_data_files(self):
        """Initialize user data files with predefined users"""
        if not self.users_file.exists():
            # Create initial user database
            users_data = {}
            for username in self.PREDEFINED_USERS:
                users_data[username] = {
                    "password_hash": self._hash_password(self.DEFAULT_PASSWORD),
                    "first_login_completed": False,
                    "image_usage_count": 0,
                    "video_usage_count": 0,
                    "total_image_cost": 0.0,
                    "total_video_cost": 0.0,
                    "created_at": datetime.now().isoformat(),
                    "last_login": None,
                    "device_ids": []  # Track which devices this user has logged in from
                }
            
            self._save_users_data(users_data)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users_data(self) -> Dict:
        """Load users data from file"""
        try:
            if self.users_file.exists():
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading users data: {e}")
        return {}
    
    def _save_users_data(self, data: Dict):
        """Save users data to file"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving users data: {e}")
    
    def _load_session_data(self) -> Dict:
        """Load session data from file"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading session data: {e}")
        return {}
    
    def _save_session_data(self, data: Dict):
        """Save session data to file"""
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving session data: {e}")
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user with username and password
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        users_data = self._load_users_data()
        
        if username not in users_data:
            return False, "Username not found"
        
        user_data = users_data[username]
        password_hash = self._hash_password(password)
        
        if user_data["password_hash"] != password_hash:
            return False, "Invalid password"
        
        # Update last login
        user_data["last_login"] = datetime.now().isoformat()
        
        # Add device ID if not already present
        if self.device_id not in user_data["device_ids"]:
            user_data["device_ids"].append(self.device_id)
        
        self._save_users_data(users_data)
        
        # Set current user (no session saving)
        self.current_user = username
        self.session_data = {
            "username": username,
            "login_time": datetime.now().isoformat(),
            "device_id": self.device_id
        }
        # Don't save session to force login every time
        
        return True, "Login successful"
    
    def is_first_login_on_device(self, username: str) -> bool:
        """Check if this is the first login for this user on this device"""
        users_data = self._load_users_data()
        if username not in users_data:
            return False
        
        user_data = users_data[username]
        return (not user_data["first_login_completed"] and 
                self.device_id not in user_data["device_ids"])
    
    def complete_first_login(self, username: str):
        """Mark first login as completed for this user on this device"""
        users_data = self._load_users_data()
        if username in users_data:
            users_data[username]["first_login_completed"] = True
            self._save_users_data(users_data)
    
    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user password
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        users_data = self._load_users_data()
        
        if username not in users_data:
            return False, "Username not found"
        
        user_data = users_data[username]
        old_password_hash = self._hash_password(old_password)
        
        if user_data["password_hash"] != old_password_hash:
            return False, "Current password is incorrect"
        
        # Update password
        user_data["password_hash"] = self._hash_password(new_password)
        self._save_users_data(users_data)
        
        return True, "Password changed successfully"
    
    def get_user_stats(self, username: str = None) -> Optional[Dict]:
        """Get user usage statistics and costs"""
        if not username:
            username = self.current_user
        
        if not username:
            return None
        
        users_data = self._load_users_data()
        if username not in users_data:
            return None
        
        user_data = users_data[username]
        
        return {
            "username": username,
            "image_usage_count": user_data["image_usage_count"],
            "video_usage_count": user_data["video_usage_count"],
            "total_image_cost": user_data["total_image_cost"],
            "total_video_cost": user_data["total_video_cost"],
            "total_cost": user_data["total_image_cost"] + user_data["total_video_cost"],
            "last_login": user_data["last_login"],
            "created_at": user_data["created_at"]
        }
    
    def record_image_usage(self, username: str = None, count: int = 1):
        """Record image processing usage"""
        if not username:
            username = self.current_user
        
        if not username:
            return False
        
        users_data = self._load_users_data()
        if username not in users_data:
            return False
        
        user_data = users_data[username]
        user_data["image_usage_count"] += count
        user_data["total_image_cost"] += count * self.IMAGE_PROCESSING_COST
        
        # Add to usage history
        if "usage_history" not in user_data:
            user_data["usage_history"] = []
        
        timestamp = datetime.now().isoformat()
        user_data["usage_history"].append({
            "type": "image",
            "count": count,
            "cost": count * self.IMAGE_PROCESSING_COST,
            "timestamp": timestamp
        })
        
        self._save_users_data(users_data)
        
        # Sync to API in background
        threading.Thread(target=self._sync_usage_to_api, 
                        args=(username, "image", count), daemon=True).start()
        
        return True
    
    def record_video_usage(self, username: str = None, count: int = 1):
        """Record video generation usage"""
        if not username:
            username = self.current_user
        
        if not username:
            return False
        
        users_data = self._load_users_data()
        if username not in users_data:
            return False
        
        user_data = users_data[username]
        user_data["video_usage_count"] += count
        user_data["total_video_cost"] += count * self.VIDEO_GENERATION_COST
        
        # Add to usage history
        if "usage_history" not in user_data:
            user_data["usage_history"] = []
        
        timestamp = datetime.now().isoformat()
        user_data["usage_history"].append({
            "type": "video",
            "count": count,
            "cost": count * self.VIDEO_GENERATION_COST,
            "timestamp": timestamp
        })
        
        self._save_users_data(users_data)
        
        # Sync to API in background
        threading.Thread(target=self._sync_usage_to_api, 
                        args=(username, "video", count), daemon=True).start()
        
        return True
    
    def get_user_stats_by_date_range(self, username: str = None, start_date: datetime = None, end_date: datetime = None):
        """Get user statistics filtered by date range"""
        if not username:
            username = self.current_user
        
        if not username:
            return None
        
        users_data = self._load_users_data()
        if username not in users_data:
            return None
        
        user_data = users_data[username]
        usage_history = user_data.get("usage_history", [])
        
        # Filter by date range if provided
        filtered_history = []
        if start_date or end_date:
            for record in usage_history:
                record_date = datetime.fromisoformat(record["timestamp"])
                
                # Check if within date range
                if start_date and record_date < start_date:
                    continue
                if end_date and record_date > end_date:
                    continue
                    
                filtered_history.append(record)
        else:
            filtered_history = usage_history
        
        # Calculate stats from filtered history
        image_count = sum(r["count"] for r in filtered_history if r["type"] == "image")
        video_count = sum(r["count"] for r in filtered_history if r["type"] == "video")
        image_cost = sum(r["cost"] for r in filtered_history if r["type"] == "image")
        video_cost = sum(r["cost"] for r in filtered_history if r["type"] == "video")
        
        return {
            "username": username,
            "image_usage_count": image_count,
            "video_usage_count": video_count,
            "total_image_cost": image_cost,
            "total_video_cost": video_cost,
            "total_cost": image_cost + video_cost,
            "last_login": user_data["last_login"],
            "created_at": user_data["created_at"],
            "date_range": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            }
        }
    
    def get_stats_today(self, username: str = None):
        """Get today's statistics"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        return self.get_user_stats_by_date_range(username, today, tomorrow)
    
    def get_stats_yesterday(self, username: str = None):
        """Get yesterday's statistics"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        yesterday_end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
        return self.get_user_stats_by_date_range(username, yesterday, yesterday_end)
    
    def get_stats_last_7_days(self, username: str = None):
        """Get last 7 days statistics"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        return self.get_user_stats_by_date_range(username, start_date, end_date)
    
    def get_stats_last_30_days(self, username: str = None):
        """Get last 30 days statistics"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        return self.get_user_stats_by_date_range(username, start_date, end_date)
    
    def get_stats_this_month(self, username: str = None):
        """Get this month's statistics"""
        now = datetime.now()
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.get_user_stats_by_date_range(username, start_date, now)
    
    def get_stats_last_month(self, username: str = None):
        """Get last month's statistics"""
        now = datetime.now()
        if now.month == 1:
            last_month_start = now.replace(year=now.year-1, month=12, day=1, hour=0, minute=0, second=0, microsecond=0)
            last_month_end = now.replace(year=now.year-1, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        else:
            last_month_start = now.replace(month=now.month-1, day=1, hour=0, minute=0, second=0, microsecond=0)
            # Get last day of previous month
            if now.month-1 in [1, 3, 5, 7, 8, 10, 12]:
                last_day = 31
            elif now.month-1 in [4, 6, 9, 11]:
                last_day = 30
            else:  # February
                last_day = 29 if now.year % 4 == 0 else 28
            last_month_end = now.replace(month=now.month-1, day=last_day, hour=23, minute=59, second=59, microsecond=999999)
        
        return self.get_user_stats_by_date_range(username, last_month_start, last_month_end)
    
    def _sync_usage_to_api(self, username: str, usage_type: str, count: int):
        """Sync usage data to API endpoint"""
        try:
            # Calculate cost based on usage type
            cost = count * (self.IMAGE_PROCESSING_COST if usage_type == "image" else self.VIDEO_GENERATION_COST)
            
            # Prepare payload according to API documentation
            payload = {
                "userName": username,  # Note: API expects 'userName' not 'username'
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Add usage-specific fields with full precision
            if usage_type == "image":
                payload["image_count"] = count
                payload["image_cost"] = f"{cost:.4f}"  # Ensure 4 decimal places
            elif usage_type == "video":
                payload["video_count"] = count
                payload["video_cost"] = f"{cost:.2f}"  # Ensure 2 decimal places
            
            # Send as form data (application/x-www-form-urlencoded)
            response = requests.post(
                self.api_endpoint,
                data=payload,  # Use 'data' instead of 'json' for form encoding
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    print(f"✅ Usage synced to API: {username} - {usage_type} x{count} (${cost:.4f})")
                    if 'data' in result and 'record_id' in result['data']:
                        print(f"   Record ID: {result['data']['record_id']}")
                else:
                    print(f"❌ API Error: {result.get('message', 'Unknown error')}")
            else:
                print(f"❌ Failed to sync usage to API: HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('message', 'Unknown error')}")
                except:
                    print(f"   Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Error syncing usage to API: {e}")
    
    def sync_total_usage_to_api(self, username: str = None):
        """Sync total usage statistics to API when tool opens"""
        if not username:
            username = self.current_user
        
        if not username:
            print("❌ No user logged in for API sync")
            return False
        
        try:
            # Get current total stats
            stats = self.get_user_stats(username)
            if not stats:
                print(f"❌ No stats found for user: {username}")
                return False
            
            # Prepare payload with total usage data (full precision)
            payload = {
                "userName": username,
                "image_count": stats['image_usage_count'],
                "image_cost": f"{stats['total_image_cost']:.4f}",  # 4 decimal places
                "video_count": stats['video_usage_count'],
                "video_cost": f"{stats['total_video_cost']:.2f}",  # 2 decimal places
                "total_cost": f"{stats['total_cost']:.4f}",        # 4 decimal places
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"🔄 Syncing total usage to API for {username}...")
            print(f"   Images: {stats['image_usage_count']} (${stats['total_image_cost']:.4f})")
            print(f"   Videos: {stats['video_usage_count']} (${stats['total_video_cost']:.2f})")
            print(f"   Total: ${stats['total_cost']:.4f}")
            
            # Send to API
            response = requests.post(
                self.api_endpoint,
                data=payload,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    print(f"✅ Total usage synced successfully!")
                    if 'data' in result and 'record_id' in result['data']:
                        print(f"   Record ID: {result['data']['record_id']}")
                    return True
                else:
                    print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Failed to sync total usage: HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('message', 'Unknown error')}")
                except:
                    print(f"   Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Error syncing total usage to API: {e}")
            return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.session_data = {}
        
        # Clear session file (ensure no session is saved)
        try:
            if self.session_file.exists():
                self.session_file.unlink()
        except:
            pass
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[str]:
        """Get current logged in username"""
        return self.current_user
    
    def restore_session(self) -> bool:
        """Restore session from saved data"""
        session_data = self._load_session_data()
        if session_data and "username" in session_data:
            self.current_user = session_data["username"]
            self.session_data = session_data
            return True
        return False
