import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import platform
from datetime import datetime, timedelta
from user_manager import UserManager
from password_change_dialog import PasswordChangeDialog

class AccountTab:
    """
    Account tab for displaying user information and usage statistics
    """
    
    def __init__(self, parent_frame, user_manager: UserManager, colors: dict):
        self.parent_frame = parent_frame
        self.user_manager = user_manager
        self.colors = colors
        
        # Time filter state
        self.current_filter = "All Time"
        
        # Create the account UI
        self.create_account_ui()
        
        # Auto-refresh timer
        self.refresh_timer = None
        self.start_auto_refresh()
    
    def create_account_ui(self):
        """Create the account tab UI"""
        # Main container
        main_container = tk.Frame(self.parent_frame, bg=self.colors['bg_medium'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header_section(main_container)
        
        # Content area with two columns
        content_frame = tk.Frame(main_container, bg=self.colors['bg_medium'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left column - User Info
        self.create_user_info_section(content_frame)
        
        # Right column - Usage Statistics
        self.create_usage_stats_section(content_frame)
        
        # Bottom section - Actions
        self.create_actions_section(main_container)
        
        # Initial data load
        self.refresh_data()
    
    def create_header_section(self, parent):
        """Create header section with user greeting"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=self.colors['bg_light'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # User icon and greeting
        greeting_frame = tk.Frame(header_content, bg=self.colors['bg_light'])
        greeting_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # User icon (emoji)
        icon_label = tk.Label(greeting_frame,
                             text="👨‍💻",
                             font=('Arial', 24),
                             bg=self.colors['bg_light'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Greeting text
        text_frame = tk.Frame(greeting_frame, bg=self.colors['bg_light'])
        text_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.greeting_label = tk.Label(text_frame,
                                      text="Welcome back!",
                                      font=('Arial', 16, 'bold'),
                                      fg=self.colors['text_white'],
                                      bg=self.colors['bg_light'])
        self.greeting_label.pack(anchor='w')
        
        self.user_label = tk.Label(text_frame,
                                  text="Loading user info...",
                                  font=('Arial', 12),
                                  fg=self.colors['text_gray'],
                                  bg=self.colors['bg_light'])
        self.user_label.pack(anchor='w', pady=(2, 0))
        
        # Status indicator
        status_frame = tk.Frame(header_content, bg=self.colors['bg_light'])
        status_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.status_indicator = tk.Label(status_frame,
                                        text="✨ Online",
                                        font=('Arial', 10, 'bold'),
                                        fg=self.colors['accent'],
                                        bg=self.colors['bg_light'])
        self.status_indicator.pack(anchor='e')
        
        self.last_update_label = tk.Label(status_frame,
                                         text="Last updated: --",
                                         font=('Arial', 8),
                                         fg=self.colors['text_gray'],
                                         bg=self.colors['bg_light'])
        self.last_update_label.pack(anchor='e', pady=(2, 0))
    
    def create_user_info_section(self, parent):
        """Create user information section"""
        info_frame = tk.Frame(parent, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        info_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Header
        info_header = tk.Frame(info_frame, bg=self.colors['bg_light'], height=40)
        info_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        info_header.pack_propagate(False)
        
        tk.Label(info_header,
                text="🔍 User Information",
                font=('Arial', 14, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['bg_light']).pack(side=tk.LEFT, anchor='w')
        
        # Content
        info_content = tk.Frame(info_frame, bg=self.colors['bg_light'])
        info_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        # User details
        details = [
            ("Username:", "username_value"),
            ("Account Status:", "status_value"),
            ("Session Expires:", "session_expires_value"),
            ("Member Since:", "member_since_value"),
            ("Last Login:", "last_login_value"),
            ("Device ID:", "device_id_value")
        ]
        
        self.info_labels = {}
        for i, (label_text, value_key) in enumerate(details):
            # Label
            label = tk.Label(info_content,
                           text=label_text,
                           font=('Arial', 10, 'bold'),
                           fg=self.colors['text_white'],
                           bg=self.colors['bg_light'])
            label.grid(row=i, column=0, sticky='w', pady=5, padx=(0, 10))
            
            # Value
            value_label = tk.Label(info_content,
                                 text="--",
                                 font=('Arial', 10),
                                 fg=self.colors['text_gray'],
                                 bg=self.colors['bg_light'])
            value_label.grid(row=i, column=1, sticky='w', pady=5)
            
            self.info_labels[value_key] = value_label
        
        # Configure grid weights
        info_content.grid_columnconfigure(1, weight=1)
    
    def create_usage_stats_section(self, parent):
        """Create usage statistics section"""
        stats_frame = tk.Frame(parent, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        stats_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        # Header
        stats_header = tk.Frame(stats_frame, bg=self.colors['bg_light'], height=40)
        stats_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        stats_header.pack_propagate(False)
        
        tk.Label(stats_header,
                text="📈 Usage Statistics",
                font=('Arial', 14, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['bg_light']).pack(side=tk.LEFT, anchor='w')
        
        
        # Time filter section
        self.create_time_filter_section(stats_frame)
        
        # Content
        stats_content = tk.Frame(stats_frame, bg=self.colors['bg_light'])
        stats_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        # Usage cards
        self.create_usage_card(stats_content, "🎨 Image Processing", "image", 0)
        self.create_usage_card(stats_content, "🎥 Video Generation", "video", 1)
        self.create_total_cost_card(stats_content, 2)
    
    def create_time_filter_section(self, parent):
        """Create time filter dropdown section"""
        filter_frame = tk.Frame(parent, bg=self.colors['bg_light'])
        filter_frame.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        # Filter dropdown
        filter_label = tk.Label(filter_frame,
                               text="⏰ Time Range:",
                               font=('Arial', 10),
                               fg=self.colors['text_white'],
                               bg=self.colors['bg_light'])
        filter_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Dropdown with time options
        self.time_filter_var = tk.StringVar(value=self.current_filter)
        time_options = [
            "All Time",
            "Today", 
            "Yesterday",
            "Last 7 Days",
            "Last 30 Days", 
            "This Month",
            "Last Month"
        ]
        
        self.time_filter_dropdown = ttk.Combobox(filter_frame,
                                               textvariable=self.time_filter_var,
                                               values=time_options,
                                               state="readonly",
                                               width=15,
                                               font=('Arial', 9))
        self.time_filter_dropdown.pack(side=tk.LEFT)
        self.time_filter_dropdown.bind('<<ComboboxSelected>>', self.on_time_filter_changed)
    
    def create_usage_card(self, parent, title: str, usage_type: str, row: int):
        """Create a usage statistics card"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_medium'], relief=tk.RAISED, bd=1)
        card_frame.grid(row=row, column=0, sticky='ew', pady=5)
        parent.grid_columnconfigure(0, weight=1)
        
        card_content = tk.Frame(card_frame, bg=self.colors['bg_medium'])
        card_content.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(card_content,
                              text=title,
                              font=('Arial', 11, 'bold'),
                              fg=self.colors['text_white'],
                              bg=self.colors['bg_medium'])
        title_label.pack(anchor='w')
        
        # Stats frame
        stats_frame = tk.Frame(card_content, bg=self.colors['bg_medium'])
        stats_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Usage count
        count_label = tk.Label(stats_frame,
                              text="Count:",
                              font=('Arial', 9),
                              fg=self.colors['text_gray'],
                              bg=self.colors['bg_medium'])
        count_label.pack(side=tk.LEFT)
        
        count_value = tk.Label(stats_frame,
                              text="0",
                              font=('Arial', 9, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_medium'])
        count_value.pack(side=tk.LEFT, padx=(5, 20))
        
        # Cost
        cost_label = tk.Label(stats_frame,
                             text="Cost:",
                             font=('Arial', 9),
                             fg=self.colors['text_gray'],
                             bg=self.colors['bg_medium'])
        cost_label.pack(side=tk.LEFT)
        
        cost_value = tk.Label(stats_frame,
                             text="$0.00",
                             font=('Arial', 9, 'bold'),
                             fg=self.colors['accent'],
                             bg=self.colors['bg_medium'])
        cost_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Store references
        if not hasattr(self, 'usage_labels'):
            self.usage_labels = {}
        
        self.usage_labels[f"{usage_type}_count"] = count_value
        self.usage_labels[f"{usage_type}_cost"] = cost_value
    
    def create_total_cost_card(self, parent, row: int):
        """Create total cost card"""
        card_frame = tk.Frame(parent, bg=self.colors['accent'], relief=tk.RAISED, bd=1)
        card_frame.grid(row=row, column=0, sticky='ew', pady=(15, 5))
        
        card_content = tk.Frame(card_frame, bg=self.colors['accent'])
        card_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(card_content,
                              text="💎 Total Cost",
                              font=('Arial', 12, 'bold'),
                              fg='white',
                              bg=self.colors['accent'])
        title_label.pack()
        
        # Total amount
        self.total_cost_label = tk.Label(card_content,
                                        text="$0.00",
                                        font=('Arial', 18, 'bold'),
                                        fg='white',
                                        bg=self.colors['accent'])
        self.total_cost_label.pack(pady=(5, 0))
    
    def create_actions_section(self, parent):
        """Create actions section"""
        actions_frame = tk.Frame(parent, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, height=80)
        actions_frame.pack(fill=tk.X, pady=(20, 0))
        actions_frame.pack_propagate(False)
        
        actions_content = tk.Frame(actions_frame, bg=self.colors['bg_light'])
        actions_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Left side - Account actions
        left_actions = tk.Frame(actions_content, bg=self.colors['bg_light'])
        left_actions.pack(side=tk.LEFT, fill=tk.Y)
        
        # Change password button
        change_pwd_btn = tk.Button(left_actions,
                                  text="🔑 Change Password",
                                  command=self.show_change_password_dialog,
                                  font=('Arial', 10, 'bold'),
                                  bg=self.colors['button_bg'],
                                  fg='black',
                                  relief=tk.FLAT,
                                  bd=0,
                                  padx=15,
                                  pady=8,
                                  cursor='hand2')
        change_pwd_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        
        # Right side - Logout
        right_actions = tk.Frame(actions_content, bg=self.colors['bg_light'])
        right_actions.pack(side=tk.RIGHT, fill=tk.Y)
        
        logout_btn = tk.Button(right_actions,
                              text="🔓 Logout",
                              command=self.logout,
                              font=('Arial', 10, 'bold'),
                              bg=self.colors['error'],
                              fg='black',
                              relief=tk.FLAT,
                              bd=0,
                              padx=15,
                              pady=8,
                              cursor='hand2')
        logout_btn.pack(side=tk.RIGHT)
    
    def refresh_data(self):
        """Refresh user data and statistics"""
        if not self.user_manager.is_logged_in():
            return
        
        current_user = self.user_manager.get_current_user()
        
        # Get filtered stats based on current time filter
        stats = self.get_filtered_stats()
        
        if not stats:
            return
        
        # Update greeting
        self.greeting_label.config(text=f"Welcome back, {current_user}!")
        self.user_label.config(text=f"Logged in as: {current_user}")
        
        # Update user info
        self.info_labels["username_value"].config(text=current_user)
        self.info_labels["status_value"].config(text="✅ Active", fg='#28a745')
        
        # Format dates
        try:
            created_date = datetime.fromisoformat(stats['created_at']).strftime("%Y-%m-%d")
            self.info_labels["member_since_value"].config(text=created_date)
        except:
            self.info_labels["member_since_value"].config(text="--")
        
        try:
            if stats['last_login']:
                last_login = datetime.fromisoformat(stats['last_login']).strftime("%Y-%m-%d %H:%M")
                self.info_labels["last_login_value"].config(text=last_login)
            else:
                self.info_labels["last_login_value"].config(text="First login")
        except:
            self.info_labels["last_login_value"].config(text="--")
        
        # Session information
        session_info = self.user_manager.get_session_info()
        if session_info and "time_remaining" in session_info:
            time_remaining = session_info["time_remaining"]
            if time_remaining == "Expired":
                self.info_labels["session_expires_value"].config(text="⚠️ Expired", fg=self.colors['error'])
            else:
                self.info_labels["session_expires_value"].config(text=f"⏰ {time_remaining}", fg=self.colors['accent'])
        else:
            self.info_labels["session_expires_value"].config(text="--", fg=self.colors['text_gray'])
        
        # Device ID (truncated)
        device_id = self.user_manager.device_id[:8] + "..."
        self.info_labels["device_id_value"].config(text=device_id)
        
        # Update usage statistics
        self.usage_labels["image_count"].config(text=str(stats['image_usage_count']))
        self.usage_labels["image_cost"].config(text=f"${stats['total_image_cost']:.4f}")
        
        self.usage_labels["video_count"].config(text=str(stats['video_usage_count']))
        self.usage_labels["video_cost"].config(text=f"${stats['total_video_cost']:.2f}")
        
        # Update total cost
        total_cost = stats['total_cost']
        self.total_cost_label.config(text=f"${total_cost:.4f}")
        
        # Update last update time
        current_time = datetime.now().strftime("%H:%M:%S")
        self.last_update_label.config(text=f"Last updated: {current_time}")
    
    def on_time_filter_changed(self, event=None):
        """Handle time filter dropdown change"""
        selected_filter = self.time_filter_var.get()
        self.current_filter = selected_filter
        
        # Apply the selected filter immediately
        self.apply_time_filter()
    
    def apply_time_filter(self):
        """Apply the selected time filter and refresh data"""
        self.refresh_data()
    
    def get_filtered_stats(self):
        """Get statistics based on current filter"""
        if not self.user_manager.is_logged_in():
            return None
        
        filter_type = self.current_filter
        
        if filter_type == "All Time":
            return self.user_manager.get_user_stats()
        elif filter_type == "Today":
            return self.user_manager.get_stats_today()
        elif filter_type == "Yesterday":
            return self.user_manager.get_stats_yesterday()
        elif filter_type == "Last 7 Days":
            return self.user_manager.get_stats_last_7_days()
        elif filter_type == "Last 30 Days":
            return self.user_manager.get_stats_last_30_days()
        elif filter_type == "This Month":
            return self.user_manager.get_stats_this_month()
        elif filter_type == "Last Month":
            return self.user_manager.get_stats_last_month()
        else:
            return self.user_manager.get_user_stats()
    
    def show_change_password_dialog(self):
        """Show change password dialog"""
        if not self.user_manager.is_logged_in():
            messagebox.showwarning("Warning", "Please login first")
            return
        
        current_user = self.user_manager.get_current_user()
        
        # Create a simplified password change dialog
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Change Password")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.parent_frame)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_dark'])
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"400x250+{x}+{y}")
        
        # Create simple password change form
        main_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="Change Password", font=('Arial', 14, 'bold'),
                fg=self.colors['text_white'], bg=self.colors['bg_dark']).pack(pady=(0, 20))
        
        # Current password
        tk.Label(main_frame, text="Current Password:", font=('Arial', 10),
                fg=self.colors['text_white'], bg=self.colors['bg_dark']).pack(anchor='w')
        current_pwd = tk.Entry(main_frame, show='*', font=('Arial', 11),
                              bg=self.colors['bg_light'], fg=self.colors['text_white'])
        current_pwd.pack(fill=tk.X, pady=(5, 10))
        
        # New password
        tk.Label(main_frame, text="New Password:", font=('Arial', 10),
                fg=self.colors['text_white'], bg=self.colors['bg_dark']).pack(anchor='w')
        new_pwd = tk.Entry(main_frame, show='*', font=('Arial', 11),
                          bg=self.colors['bg_light'], fg=self.colors['text_white'])
        new_pwd.pack(fill=tk.X, pady=(5, 20))
        
        def change_password():
            success, message = self.user_manager.change_password(
                current_user, current_pwd.get(), new_pwd.get()
            )
            if success:
                messagebox.showinfo("Success", "Password changed successfully!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Change", command=change_password,
                 bg=self.colors['button_bg'], fg='black', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 bg=self.colors['error'], fg='black', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
    
    def logout(self):
        """Logout current user"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.user_manager.logout()
            # You would need to implement a way to return to login screen
            messagebox.showinfo("Logout", "You have been logged out successfully.")
    
    def start_auto_refresh(self):
        """Start auto-refresh timer"""
        self.refresh_data()
        # Refresh every 30 seconds
        self.refresh_timer = self.parent_frame.after(30000, self.start_auto_refresh)
    
    def stop_auto_refresh(self):
        """Stop auto-refresh timer"""
        if self.refresh_timer:
            self.parent_frame.after_cancel(self.refresh_timer)
            self.refresh_timer = None
