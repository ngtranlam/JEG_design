#!/usr/bin/env python3
"""
Sync Progress Dialog - Hiển thị tiến trình đồng bộ dữ liệu khi đóng tool
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

class SyncProgressDialog:
    """Dialog hiển thị tiến trình đồng bộ dữ liệu"""
    
    def __init__(self, parent, user_manager):
        self.parent = parent
        self.user_manager = user_manager
        self.dialog = None
        self.progress_var = None
        self.status_var = None
        self.sync_completed = False
        self.sync_success = False
        
    def show_and_sync(self):
        """Hiển thị dialog và thực hiện đồng bộ"""
        self.create_dialog()
        
        # Bắt đầu sync trong background thread
        sync_thread = threading.Thread(target=self._perform_sync, daemon=True)
        sync_thread.start()
        
        # Hiển thị dialog (blocking)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("400x200")
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        # Wait for sync to complete
        self._wait_for_sync_completion()
        
        return self.sync_success
    
    def create_dialog(self):
        """Tạo dialog UI"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Đồng bộ dữ liệu")
        self.dialog.resizable(False, False)
        
        # Prevent closing dialog manually
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🔄 Đang đồng bộ dữ liệu lên server...",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=300,
            mode='determinate'
        )
        progress_bar.pack(pady=(0, 15))
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Đang chuẩn bị đồng bộ...")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 10)
        )
        status_label.pack(pady=(0, 10))
        
        # Info label
        info_label = ttk.Label(
            main_frame,
            text="Vui lòng đợi trong giây lát...",
            font=("Arial", 9),
            foreground="gray"
        )
        info_label.pack()
        
    def _perform_sync(self):
        """Thực hiện đồng bộ trong background thread"""
        try:
            # Step 1: Check if user is logged in
            self._update_status("Kiểm tra trạng thái đăng nhập...", 10)
            time.sleep(0.5)
            
            if not self.user_manager.is_logged_in():
                self._update_status("Không có user đăng nhập", 100)
                self.sync_success = True  # No sync needed
                self.sync_completed = True
                return
            
            # Step 2: Check for unsynced records
            self._update_status("Kiểm tra dữ liệu cần đồng bộ...", 20)
            time.sleep(0.5)
            
            username = self.user_manager.get_current_user()
            users_data = self.user_manager._load_users_data()
            
            if username not in users_data:
                self._update_status("Không tìm thấy dữ liệu user", 100)
                self.sync_success = True
                self.sync_completed = True
                return
            
            user_data = users_data[username]
            usage_history = user_data.get("usage_history", [])
            unsynced_records = [record for record in usage_history if not record.get("synced", False)]
            
            if not unsynced_records:
                self._update_status("Không có dữ liệu cần đồng bộ", 50)
                time.sleep(0.5)
                self._update_status("Đang reset dữ liệu local...", 80)
                time.sleep(0.5)
                
                # Still need to reset local data
                success = self.user_manager.sync_and_reset_on_close(username)
                self._update_status("✅ Hoàn tất!", 100)
                self.sync_success = success
                self.sync_completed = True
                return
            
            # Step 3: Force sync unsynced records immediately
            self._update_status(f"Đang đồng bộ {len(unsynced_records)} bản ghi...", 30)
            time.sleep(0.5)
            
            # Use force sync method for immediate sync
            sync_success = self.user_manager.force_sync_unsynced_records(username)
            
            if sync_success:
                self._update_status("✅ Tất cả bản ghi đã được đồng bộ", 80)
            else:
                self._update_status("⚠️ Một số bản ghi không thể đồng bộ", 80)
            
            time.sleep(0.5)
            
            # Step 5: Reset local data
            self._update_status("Đang reset dữ liệu local...", 90)
            time.sleep(0.5)
            
            success = self.user_manager.sync_and_reset_on_close(username)
            
            if success:
                self._update_status("✅ Đồng bộ hoàn tất!", 100)
                self.sync_success = True
            else:
                self._update_status("⚠️ Có lỗi trong quá trình đồng bộ", 100)
                self.sync_success = False
            
            time.sleep(1)  # Show final status
            
        except Exception as e:
            self._update_status(f"❌ Lỗi: {str(e)}", 100)
            self.sync_success = False
            time.sleep(2)
        
        finally:
            self.sync_completed = True
    
    def _update_status(self, message, progress):
        """Cập nhật trạng thái và progress"""
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.after(0, lambda: self._safe_update_status(message, progress))
    
    def _safe_update_status(self, message, progress):
        """Safely update status in main thread"""
        try:
            if self.status_var:
                self.status_var.set(message)
            if self.progress_var:
                self.progress_var.set(progress)
            if self.dialog:
                self.dialog.update_idletasks()
        except:
            pass  # Ignore errors if dialog is destroyed
    
    def _wait_for_sync_completion(self):
        """Đợi sync hoàn tất"""
        while not self.sync_completed:
            try:
                self.dialog.update()
                time.sleep(0.1)
            except:
                break  # Dialog destroyed
        
        # Close dialog after sync completes
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.after(500, self.dialog.destroy)  # Small delay to show final status
