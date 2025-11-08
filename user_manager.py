import json
import hashlib
import os
import uuid
import queue
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
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
    
    # Session configuration
    SESSION_DURATION_HOURS = 5  # Login session lasts for 5 hours
    
    # Default password for all users
    DEFAULT_PASSWORD = "jeg@12345"
    
    # Predefined usernames
    PREDEFINED_USERS = [
        "admin.tu",
        "thusuong01",
        "huynhtan",
        "nguyen",
        "toniwintheiser15754",
        "minhductran1996",
        "hoangbao2411",
        "quangduc.24696@gmail.com",
        "ducmy10081987@gmail.com",
        "tranthanhtu",
        "linkkany21",
        "tm591595@gmail.com",
        "thucuyen97",
        "hoanguyen14",
        "chautuan154",
        "tongthaomy",
        "ngockim96",
        "chaulien1807",
        "adminq",
        "nguyentuyenktdt@gmail.com",
        "Vantich2021",
        "phamthikimlien42",
        "thao1607",
        "trinh268",
        "HongNhung",
        "phamthuyvan9x",
        "sumydn",
        "XuanThuy",
        "trucquynh1099@gmail.com",
        "congnguyen0312@gmail.com",
        "hoang0806",
        "chienpv96",
        "nthaqtkd",
        "thanhtd",
        "giwehsp",
        "phammyhao104",
        "thaoptt235@gmail.com",
        "ngocanh25101996",
        "nguyenngocvnhcm",
        "letramyk8",
        "kimngan69",
        "hongnhile",
        "anhthu27901",
        "hlinh8821",
        "tuyetsuong2k1",
        "nhnguyen12a1@gmail",
        "tranhien",
        "thaonguyen",
        "tanlam",
        "hoailinh",
        "tranhainam",
        "hongnhungdo098",
        "nytran2582002",
        "phuongthuy2710",
        "thuylinh",
        "ketoan",
        "lamdev",
        "ngocsanghuynh",
        "baongocle",
        "minhtiendao",
        "hoang1492001",
        "nguyentung",
        "Nguyendo",
        "phuongtrinhjeg",
        "anbinhjeg",
        "lethangjeg",
        "khanhhung",
        "ngochuyenjeg",
        "ngocthanhjeg",
        "sptest",
        "AIAgentDesign",
        "lamdev",
        "seller"
    ]

    
    def __init__(self, api_endpoint: str = None):
        self.api_endpoint = api_endpoint or "https://jegdn.com/api/tools/update"
        self.api_stats_endpoint = "https://jegdn.com/api/tools/stats"
        self.current_user = None
        self.session_data = {}
        
        # Setup local data directory
        self.data_dir = self._get_data_directory()
        self.users_file = self.data_dir / "users.json"
        self.session_file = self.data_dir / "session.json"
        self.api_keys_file = self.data_dir / "api_keys.json"
        self.device_id_file = self.data_dir / "device_id.txt"
        self.sync_queue_file = self.data_dir / "sync_queue.json"
        
        # Initialize data files
        self._initialize_data_files()
        
        # Generate or load device ID
        self.device_id = self._get_or_create_device_id()
        
        # Initialize sync queue system
        self.sync_queue = queue.Queue()
        self.sync_thread = None
        self.sync_running = False
        self._load_pending_sync_items()
        self._start_sync_worker()
    
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
        
        # Set current user and save session with 5-hour expiration
        self.current_user = username
        login_time = datetime.now()
        expiry_time = login_time + timedelta(hours=self.SESSION_DURATION_HOURS)
        
        self.session_data = {
            "username": username,
            "login_time": login_time.isoformat(),
            "expiry_time": expiry_time.isoformat(),
            "device_id": self.device_id
        }
        
        # Save session to file for 5-hour persistence
        self._save_session_data(self.session_data)
        
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
        """Get user usage statistics and costs (API baseline + local session)"""
        # Use the new display stats method that combines API + local data
        return self.get_display_stats(username)
    
    def record_image_usage(self, username: str = None, count: int = 1):
        """Record image processing usage with sync queue"""
        if not username:
            username = self.current_user
        
        if not username:
            return False
        
        users_data = self._load_users_data()
        if username not in users_data:
            return False
        
        # Create usage record with unique ID
        usage_record = self._create_usage_record(username, "image", count)
        
        user_data = users_data[username]
        user_data["image_usage_count"] += count
        user_data["total_image_cost"] += count * self.IMAGE_PROCESSING_COST
        
        # Add to usage history with unique ID and sync status
        if "usage_history" not in user_data:
            user_data["usage_history"] = []
        
        user_data["usage_history"].append({
            "id": usage_record["id"],
            "type": "image",
            "count": count,
            "cost": count * self.IMAGE_PROCESSING_COST,
            "timestamp": usage_record["created_at"],
            "synced": False,
            "created_at": usage_record["created_at"]
        })
        
        self._save_users_data(users_data)
        
        # Add to sync queue for background processing
        self.sync_queue.put(usage_record)
        print(f"📤 Queued image usage: {usage_record['id']} - {count} images (${usage_record['cost']:.4f})")
        
        return True
    
    def record_video_usage(self, username: str = None, count: int = 1):
        """Record video generation usage with sync queue"""
        if not username:
            username = self.current_user
        
        if not username:
            return False
        
        users_data = self._load_users_data()
        if username not in users_data:
            return False
        
        # Create usage record with unique ID
        usage_record = self._create_usage_record(username, "video", count)
        
        user_data = users_data[username]
        user_data["video_usage_count"] += count
        user_data["total_video_cost"] += count * self.VIDEO_GENERATION_COST
        
        # Add to usage history with unique ID and sync status
        if "usage_history" not in user_data:
            user_data["usage_history"] = []
        
        user_data["usage_history"].append({
            "id": usage_record["id"],
            "type": "video",
            "count": count,
            "cost": count * self.VIDEO_GENERATION_COST,
            "timestamp": usage_record["created_at"],
            "synced": False,
            "created_at": usage_record["created_at"]
        })
        
        self._save_users_data(users_data)
        
        # Add to sync queue for background processing
        self.sync_queue.put(usage_record)
        print(f"📤 Queued video usage: {usage_record['id']} - {count} videos (${usage_record['cost']:.2f})")
        
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
    
    def sync_unsynced_records_to_api(self, username: str = None):
        """Sync only unsynced usage records to API"""
        if not username:
            username = self.current_user
        
        if not username:
            print("❌ No user logged in for API sync")
            return False
        
        try:
            users_data = self._load_users_data()
            if username not in users_data:
                print(f"❌ User {username} not found")
                return False
            
            user_data = users_data[username]
            usage_history = user_data.get("usage_history", [])
            
            # Find unsynced records
            unsynced_records = [record for record in usage_history if not record.get("synced", False)]
            
            if not unsynced_records:
                print(f"✅ All records already synced for {username}")
                return True
            
            print(f"🔄 Found {len(unsynced_records)} unsynced records for {username}")
            
            # Add unsynced records to sync queue
            for record in unsynced_records:
                # Convert to sync queue format
                queue_item = {
                    "id": record.get("id", str(uuid.uuid4())),
                    "username": username,
                    "type": record["type"],
                    "count": record["count"],
                    "cost": record["cost"],
                    "timestamp": record.get("timestamp", record.get("created_at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))),
                    "created_at": record.get("created_at", datetime.now().isoformat()),
                    "status": "pending",
                    "synced": False,
                    "retry_count": 0
                }
                
                self.sync_queue.put(queue_item)
                print(f"📤 Queued unsynced {record['type']}: {queue_item['id']} - {record['count']} (${record['cost']:.4f})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error syncing unsynced records: {e}")
            return False
    
    def sync_total_usage_to_api(self, username: str = None):
        """Sync only unsynced usage records to API (no more total sync to avoid duplicates)"""
        if not username:
            username = self.current_user
        
        if not username:
            print("❌ No user logged in for API sync")
            return False
        
        print(f"🔄 Syncing unsynced records for {username}...")
        return self.sync_unsynced_records_to_api(username)
    
    def logout(self):
        """Logout current user"""
        # Stop sync worker gracefully
        self.stop_sync_worker()
        
        self.current_user = None
        self.session_data = {}
        
        # Clear session file
        self._clear_session_file()
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in"""
        return self.current_user is not None
    
    def _clear_session_file(self):
        """Clear the session file"""
        try:
            if self.session_file.exists():
                self.session_file.unlink()
        except Exception as e:
            print(f"Error clearing session file: {e}")
    
    def get_session_info(self) -> Optional[Dict]:
        """Get current session information including expiry time"""
        if not self.session_data:
            return None
        
        session_info = self.session_data.copy()
        
        # Add time remaining if session has expiry
        if "expiry_time" in session_info:
            try:
                expiry_time = datetime.fromisoformat(session_info["expiry_time"])
                current_time = datetime.now()
                time_remaining = expiry_time - current_time
                
                if time_remaining.total_seconds() > 0:
                    hours, remainder = divmod(int(time_remaining.total_seconds()), 3600)
                    minutes, _ = divmod(remainder, 60)
                    session_info["time_remaining"] = f"{hours}h {minutes}m"
                else:
                    session_info["time_remaining"] = "Expired"
            except ValueError:
                session_info["time_remaining"] = "Unknown"
        
        return session_info
    
    def get_current_user(self) -> Optional[str]:
        """Get current logged in username"""
        return self.current_user
    
    def restore_session(self) -> bool:
        """Restore session from saved data if not expired"""
        session_data = self._load_session_data()
        
        if not session_data or "username" not in session_data:
            return False
        
        # Check if session has expiry_time (for backward compatibility)
        if "expiry_time" not in session_data:
            # Old session format, require re-login
            self._clear_session_file()
            return False
        
        try:
            # Check if session has expired
            expiry_time = datetime.fromisoformat(session_data["expiry_time"])
            current_time = datetime.now()
            
            if current_time > expiry_time:
                # Session expired, clear it
                self._clear_session_file()
                return False
            
            # Session is still valid
            self.current_user = session_data["username"]
            self.session_data = session_data
            return True
            
        except (ValueError, KeyError) as e:
            # Invalid session data, clear it
            print(f"Invalid session data: {e}")
            self._clear_session_file()
            return False
    
    # API Key Management Methods
    def save_api_key(self, service: str, api_key: str) -> bool:
        """Save API key for a specific service"""
        try:
            api_keys = self._load_api_keys()
            api_keys[service] = api_key
            
            with open(self.api_keys_file, 'w') as f:
                json.dump(api_keys, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving API key: {e}")
            return False
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service"""
        try:
            api_keys = self._load_api_keys()
            return api_keys.get(service)
        except Exception as e:
            print(f"Error loading API key: {e}")
            return None
    
    def has_api_key(self, service: str) -> bool:
        """Check if API key exists for a service"""
        return self.get_api_key(service) is not None
    
    def delete_api_key(self, service: str) -> bool:
        """Delete API key for a specific service"""
        try:
            api_keys = self._load_api_keys()
            if service in api_keys:
                del api_keys[service]
                with open(self.api_keys_file, 'w') as f:
                    json.dump(api_keys, f, indent=2)
            return True
        except Exception as e:
            print(f"Error deleting API key: {e}")
            return False
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from file"""
        try:
            if self.api_keys_file.exists():
                with open(self.api_keys_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading API keys: {e}")
            return {}
    
    # ==================== SYNC QUEUE SYSTEM ====================
    
    def _load_pending_sync_items(self):
        """Load pending sync items from file to queue"""
        try:
            if self.sync_queue_file.exists():
                with open(self.sync_queue_file, 'r') as f:
                    pending_items = json.load(f)
                
                for item in pending_items:
                    if item.get('status') == 'pending':
                        self.sync_queue.put(item)
                
                print(f"📥 Loaded {len(pending_items)} pending sync items")
        except Exception as e:
            print(f"❌ Error loading pending sync items: {e}")
    
    def _save_sync_queue_to_file(self):
        """Save current sync queue to file"""
        try:
            # Get all items from queue without removing them
            items = []
            temp_queue = queue.Queue()
            
            while not self.sync_queue.empty():
                try:
                    item = self.sync_queue.get_nowait()
                    items.append(item)
                    temp_queue.put(item)
                except queue.Empty:
                    break
            
            # Put items back to queue
            while not temp_queue.empty():
                try:
                    self.sync_queue.put(temp_queue.get_nowait())
                except queue.Empty:
                    break
            
            # Save to file
            with open(self.sync_queue_file, 'w') as f:
                json.dump(items, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving sync queue: {e}")
    
    def _start_sync_worker(self):
        """Start background sync worker thread"""
        if not self.sync_running:
            self.sync_running = True
            self.sync_thread = threading.Thread(target=self._sync_worker, daemon=True)
            self.sync_thread.start()
            print("🔄 Sync worker started")
    
    def _sync_worker(self):
        """Background worker to process sync queue"""
        retry_delays = [1, 2, 4, 8, 16]  # Exponential backoff
        
        while self.sync_running:
            try:
                # Get item from queue with timeout
                item = self.sync_queue.get(timeout=5)
                
                success = False
                for attempt in range(len(retry_delays)):
                    try:
                        success = self._send_usage_to_api(item)
                        if success:
                            print(f"✅ Synced: {item['id']} - {item['type']} x{item['count']}")
                            break
                        else:
                            if attempt < len(retry_delays) - 1:
                                delay = retry_delays[attempt]
                                print(f"⏳ Retry {attempt + 1} in {delay}s for {item['id']}")
                                time.sleep(delay)
                    except Exception as e:
                        print(f"❌ Sync attempt {attempt + 1} failed: {e}")
                        if attempt < len(retry_delays) - 1:
                            time.sleep(retry_delays[attempt])
                
                if not success:
                    print(f"❌ Failed to sync after all retries: {item['id']}")
                    # Put back to queue for later retry
                    item['retry_count'] = item.get('retry_count', 0) + 1
                    if item['retry_count'] < 10:  # Max 10 retries
                        self.sync_queue.put(item)
                
                self.sync_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Sync worker error: {e}")
                time.sleep(1)
    
    def _send_usage_to_api(self, item: Dict) -> bool:
        """Send individual usage item to API"""
        try:
            # Handle both old format (from queue) and new format (from force sync)
            username = item.get('userName') or item.get('username')
            if not username:
                print(f"❌ No username found in item: {item.keys()}")
                return False
            
            payload = {
                "userName": username,
                "timestamp": item.get('timestamp', item.get('created_at', datetime.now().isoformat()))
            }
            
            # Add usage-specific fields based on item format
            if 'image_count' in item and item['image_count'] > 0:
                payload["image_count"] = item['image_count']
                payload["image_cost"] = f"{item['image_cost']:.4f}"
            elif 'video_count' in item and item['video_count'] > 0:
                payload["video_count"] = item['video_count']
                payload["video_cost"] = f"{item['video_cost']:.2f}"
            elif 'type' in item:
                # Old format compatibility
                if item['type'] == "image":
                    payload["image_count"] = item['count']
                    payload["image_cost"] = f"{item['cost']:.4f}"
                elif item['type'] == "video":
                    payload["video_count"] = item['count']
                    payload["video_cost"] = f"{item['cost']:.2f}"
            
            print(f"🔄 Sending to API: {payload}")
            
            response = requests.post(
                self.api_endpoint,
                data=payload,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    # Mark as synced in local storage
                    if 'id' in item:
                        self._mark_usage_as_synced(item['id'])
                    return True
                else:
                    print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Send API error: {e}")
            return False
    
    def _mark_usage_as_synced(self, usage_id: str):
        """Mark usage record as synced in user data"""
        try:
            users_data = self._load_users_data()
            if self.current_user and self.current_user in users_data:
                user_data = users_data[self.current_user]
                
                # Mark in usage_history
                if "usage_history" in user_data:
                    for usage in user_data["usage_history"]:
                        if usage.get("id") == usage_id:
                            usage["synced"] = True
                            usage["synced_at"] = datetime.now().isoformat()
                            break
                
                self._save_users_data(users_data)
        except Exception as e:
            print(f"❌ Error marking as synced: {e}")
    
    def _create_usage_record(self, username: str, usage_type: str, count: int) -> Dict:
        """Create a usage record with unique ID"""
        usage_id = str(uuid.uuid4())
        cost = count * (self.IMAGE_PROCESSING_COST if usage_type == "image" else self.VIDEO_GENERATION_COST)
        
        return {
            "id": usage_id,
            "username": username,
            "type": usage_type,
            "count": count,
            "cost": cost,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "synced": False,
            "retry_count": 0
        }
    
    def stop_sync_worker(self):
        """Stop sync worker gracefully"""
        self.sync_running = False
        if self.sync_thread and self.sync_thread.is_alive():
            self.sync_thread.join(timeout=5)
        self._save_sync_queue_to_file()
        print("🛑 Sync worker stopped")
    
    # ==================== API STATS FETCHING ====================
    
    def fetch_stats_from_api(self, username: str = None, period: str = "all_time") -> Optional[Dict]:
        """Fetch user stats from API server"""
        if not username:
            username = self.current_user
        
        if not username:
            print("❌ No user logged in for API fetch")
            return None
        
        try:
            # Build API URL
            url = f"{self.api_stats_endpoint}/{username}"
            params = {}
            if period != "all_time":
                params["period"] = period
            
            print(f"🔄 Fetching stats from API for {username} (period: {period})...")
            
            # Make API request
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    api_stats = result['data']['stats']
                    print(f"✅ Stats fetched from API successfully!")
                    print(f"   Images: {api_stats['total_image_count']} (${api_stats['total_image_cost']:.4f})")
                    print(f"   Videos: {api_stats['total_video_count']} (${api_stats['total_video_cost']:.2f})")
                    print(f"   Total: ${api_stats['total_cost']:.4f}")
                    
                    return {
                        "username": username,
                        "image_usage_count": api_stats['total_image_count'],
                        "video_usage_count": api_stats['total_video_count'],
                        "total_image_cost": api_stats['total_image_cost'],
                        "total_video_cost": api_stats['total_video_cost'],
                        "total_cost": api_stats['total_cost'],
                        "last_updated": result['data'].get('last_updated', datetime.now().isoformat()),
                        "filter_info": result['data'].get('filter', {}),
                        "source": "api"
                    }
                else:
                    print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                if response.status_code == 404:
                    print("   User not found or not a seller")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching stats from API: {e}")
            return None
    
    def initialize_user_stats_from_api(self, username: str = None) -> bool:
        """Initialize local user stats from API data (called once when tool opens)"""
        if not username:
            username = self.current_user
        
        if not username:
            print("❌ No user logged in for initialization")
            return False
        
        try:
            # Fetch stats from API
            api_stats = self.fetch_stats_from_api(username)
            if not api_stats:
                print("⚠️ Could not fetch stats from API, using local data")
                return False
            
            # Update local user data with API stats as baseline
            users_data = self._load_users_data()
            if username not in users_data:
                print(f"❌ User {username} not found in local data")
                return False
            
            user_data = users_data[username]
            
            # Store API stats as baseline (these are the "official" numbers)
            user_data["api_baseline"] = {
                "image_usage_count": api_stats["image_usage_count"],
                "video_usage_count": api_stats["video_usage_count"],
                "total_image_cost": api_stats["total_image_cost"],
                "total_video_cost": api_stats["total_video_cost"],
                "total_cost": api_stats["total_cost"],
                "fetched_at": datetime.now().isoformat()
            }
            
            # Reset local counters to 0 (will accumulate new usage from this session)
            user_data["image_usage_count"] = 0
            user_data["video_usage_count"] = 0
            user_data["total_image_cost"] = 0.0
            user_data["total_video_cost"] = 0.0
            
            # Clear usage history (start fresh)
            user_data["usage_history"] = []
            
            self._save_users_data(users_data)
            
            print(f"✅ User stats initialized from API!")
            print(f"   API Baseline - Images: {api_stats['image_usage_count']}, Videos: {api_stats['video_usage_count']}")
            print(f"   Local Session - Reset to 0")
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing stats from API: {e}")
            return False
    
    def get_display_stats(self, username: str = None) -> Optional[Dict]:
        """Get stats for display (API baseline + local session)"""
        if not username:
            username = self.current_user
        
        if not username:
            return None
        
        try:
            users_data = self._load_users_data()
            if username not in users_data:
                return None
            
            user_data = users_data[username]
            
            # Get API baseline (official numbers)
            api_baseline = user_data.get("api_baseline", {
                "image_usage_count": 0,
                "video_usage_count": 0,
                "total_image_cost": 0.0,
                "total_video_cost": 0.0,
                "total_cost": 0.0
            })
            
            # Get local session usage
            local_image_count = user_data.get("image_usage_count", 0)
            local_video_count = user_data.get("video_usage_count", 0)
            local_image_cost = user_data.get("total_image_cost", 0.0)
            local_video_cost = user_data.get("total_video_cost", 0.0)
            
            # Calculate total display stats (API + Local)
            total_image_count = api_baseline["image_usage_count"] + local_image_count
            total_video_count = api_baseline["video_usage_count"] + local_video_count
            total_image_cost = api_baseline["total_image_cost"] + local_image_cost
            total_video_cost = api_baseline["total_video_cost"] + local_video_cost
            total_cost = total_image_cost + total_video_cost
            
            return {
                "username": username,
                "image_usage_count": total_image_count,
                "video_usage_count": total_video_count,
                "total_image_cost": total_image_cost,
                "total_video_cost": total_video_cost,
                "total_cost": total_cost,
                "api_baseline": api_baseline,
                "local_session": {
                    "image_usage_count": local_image_count,
                    "video_usage_count": local_video_count,
                    "total_image_cost": local_image_cost,
                    "total_video_cost": local_video_cost
                },
                "last_login": user_data.get("last_login"),
                "created_at": user_data.get("created_at")
            }
            
        except Exception as e:
            print(f"❌ Error getting display stats: {e}")
            return None
    
    def force_sync_unsynced_records(self, username: str = None) -> bool:
        """Force sync all unsynced records immediately (not via background queue)"""
        if not username:
            username = self.current_user
        
        if not username:
            print("❌ No user logged in for force sync")
            return False
        
        try:
            users_data = self._load_users_data()
            if username not in users_data:
                print(f"❌ User {username} not found")
                return False
            
            user_data = users_data[username]
            usage_history = user_data.get("usage_history", [])
            unsynced_records = [record for record in usage_history if not record.get("synced", False)]
            
            if not unsynced_records:
                print("✅ No unsynced records to force sync")
                return True
            
            print(f"🔄 Force syncing {len(unsynced_records)} unsynced records...")
            
            success_count = 0
            for record in unsynced_records:
                # Create API payload in format expected by _send_usage_to_api
                api_item = {
                    "id": record["id"],
                    "userName": username,
                    "type": record["type"],
                    "count": record["count"],
                    "cost": record["cost"],
                    "timestamp": record["timestamp"],
                    "created_at": record["created_at"]
                }
                
                # Send to API immediately
                if self._send_usage_to_api(api_item):
                    success_count += 1
                    print(f"✅ Synced: {record['id']} - {record['type']} x{record['count']}")
                else:
                    print(f"❌ Failed to sync: {record['id']} - {record['type']} x{record['count']}")
            
            print(f"📊 Force sync completed: {success_count}/{len(unsynced_records)} records synced")
            return success_count == len(unsynced_records)
            
        except Exception as e:
            print(f"❌ Error in force sync: {e}")
            return False
    
    def sync_and_reset_on_close(self, username: str = None) -> bool:
        """Sync local session data to API and reset local counters (called when tool closes)"""
        if not username:
            username = self.current_user
        
        if not username:
            print("❌ No user logged in for sync and reset")
            return False
        
        try:
            print(f"🔄 Syncing and resetting data for {username}...")
            
            # Force sync all unsynced records immediately
            sync_success = self.force_sync_unsynced_records(username)
            if not sync_success:
                print("⚠️ Some records may not have synced properly")
            
            # Reset local session data to 0
            users_data = self._load_users_data()
            if username in users_data:
                user_data = users_data[username]
                
                # Keep API baseline but reset local session
                user_data["image_usage_count"] = 0
                user_data["video_usage_count"] = 0
                user_data["total_image_cost"] = 0.0
                user_data["total_video_cost"] = 0.0
                user_data["usage_history"] = []
                
                # Update last sync time
                user_data["last_sync_reset"] = datetime.now().isoformat()
                
                self._save_users_data(users_data)
                
                print("✅ Local session data reset to 0")
                print("   API baseline preserved for next session")
                
                return sync_success  # Return sync success status
            else:
                print(f"❌ User {username} not found for reset")
                return False
                
        except Exception as e:
            print(f"❌ Error in sync and reset: {e}")
            return False
