import tkinter as tk
from tkinter import messagebox
import platform
from user_manager import UserManager

class PasswordChangeDialog:
    """
    Password change dialog for first-time login
    """
    
    def __init__(self, parent, user_manager: UserManager, username: str):
        self.parent = parent
        self.user_manager = user_manager
        self.username = username
        self.result = False
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Change Password - First Time Login")
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configure colors (match main app theme)
        self.colors = {
            'bg_dark': '#2E2E2E',
            'bg_medium': '#3C3C3C',
            'bg_light': '#4A4A4A',
            'accent': '#0078D4' if platform.system() == "Windows" else '#007AFF',
            'text_white': '#FFFFFF',
            'text_gray': '#AAAAAA',
            'button_bg': '#0078D4' if platform.system() == "Windows" else '#007AFF',
            'button_hover': '#106ebe' if platform.system() == "Windows" else '#005cbf',
            'error': '#DC3545',
            'success': '#28a745'
        }
        
        self.dialog.configure(bg=self.colors['bg_dark'])
        
        self.create_ui()
        self.center_dialog()
        
        # Focus on current password entry
        self.current_password_entry.focus_set()
        
        # Bind Enter key to change password
        self.dialog.bind('<Return>', lambda e: self.change_password())
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def create_ui(self):
        """Create the password change UI"""
        # Main container
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame,
                              text="🔐 Change Password",
                              font=('Arial', 16, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_dark'])
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text=f"Welcome {self.username}! Please change your default password.",
                                 font=('Arial', 10),
                                 fg=self.colors['text_gray'],
                                 bg=self.colors['bg_dark'])
        subtitle_label.pack(pady=(5, 0))
        
        # Info message
        info_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'], relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_content = tk.Frame(info_frame, bg=self.colors['bg_medium'])
        info_content.pack(fill=tk.X, padx=15, pady=10)
        
        info_label = tk.Label(info_content,
                             text="⚠️ This is your first login on this device.\nFor security reasons, please change your password.",
                             font=('Arial', 9),
                             fg=self.colors['text_white'],
                             bg=self.colors['bg_medium'],
                             justify=tk.LEFT)
        info_label.pack(anchor='w')
        
        # Form section
        form_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'], relief=tk.RAISED, bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        form_content = tk.Frame(form_frame, bg=self.colors['bg_medium'])
        form_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Current password field
        current_label = tk.Label(form_content,
                                text="Current Password:",
                                font=('Arial', 10, 'bold'),
                                fg=self.colors['text_white'],
                                bg=self.colors['bg_medium'])
        current_label.pack(anchor='w', pady=(0, 5))
        
        self.current_password_var = tk.StringVar()
        self.current_password_entry = tk.Entry(form_content,
                                              textvariable=self.current_password_var,
                                              font=('Arial', 11),
                                              bg=self.colors['bg_light'],
                                              fg=self.colors['text_white'],
                                              insertbackground=self.colors['text_white'],
                                              relief=tk.FLAT,
                                              bd=5,
                                              show='*')
        self.current_password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # New password field
        new_label = tk.Label(form_content,
                            text="New Password:",
                            font=('Arial', 10, 'bold'),
                            fg=self.colors['text_white'],
                            bg=self.colors['bg_medium'])
        new_label.pack(anchor='w', pady=(0, 5))
        
        self.new_password_var = tk.StringVar()
        self.new_password_entry = tk.Entry(form_content,
                                          textvariable=self.new_password_var,
                                          font=('Arial', 11),
                                          bg=self.colors['bg_light'],
                                          fg=self.colors['text_white'],
                                          insertbackground=self.colors['text_white'],
                                          relief=tk.FLAT,
                                          bd=5,
                                          show='*')
        self.new_password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Confirm password field
        confirm_label = tk.Label(form_content,
                                text="Confirm New Password:",
                                font=('Arial', 10, 'bold'),
                                fg=self.colors['text_white'],
                                bg=self.colors['bg_medium'])
        confirm_label.pack(anchor='w', pady=(0, 5))
        
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = tk.Entry(form_content,
                                              textvariable=self.confirm_password_var,
                                              font=('Arial', 11),
                                              bg=self.colors['bg_light'],
                                              fg=self.colors['text_white'],
                                              insertbackground=self.colors['text_white'],
                                              relief=tk.FLAT,
                                              bd=5,
                                              show='*')
        self.confirm_password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(form_content, bg=self.colors['bg_medium'])
        buttons_frame.pack(fill=tk.X)
        
        # Change password button
        self.change_btn = tk.Button(buttons_frame,
                                   text="Change Password",
                                   command=self.change_password,
                                   font=('Arial', 11, 'bold'),
                                   bg=self.colors['button_bg'],
                                   fg='black',
                                   relief=tk.FLAT,
                                   bd=0,
                                   padx=20,
                                   pady=8,
                                   cursor='hand2')
        self.change_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Skip button
        self.skip_btn = tk.Button(buttons_frame,
                                 text="Skip (Not Recommended)",
                                 command=self.skip_password_change,
                                 font=('Arial', 10),
                                 bg=self.colors['error'],
                                 fg='black',
                                 relief=tk.FLAT,
                                 bd=0,
                                 padx=20,
                                 pady=8,
                                 cursor='hand2')
        self.skip_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(status_frame,
                                    text="",
                                    font=('Arial', 9),
                                    fg=self.colors['error'],
                                    bg=self.colors['bg_dark'])
        self.status_label.pack()
    
    def center_dialog(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def change_password(self):
        """Handle password change"""
        current_password = self.current_password_var.get()
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Validation
        if not current_password:
            self.show_status("Please enter current password", error=True)
            self.current_password_entry.focus_set()
            return
        
        if not new_password:
            self.show_status("Please enter new password", error=True)
            self.new_password_entry.focus_set()
            return
        
        if len(new_password) < 6:
            self.show_status("New password must be at least 6 characters", error=True)
            self.new_password_entry.focus_set()
            return
        
        if new_password != confirm_password:
            self.show_status("New passwords do not match", error=True)
            self.confirm_password_entry.focus_set()
            return
        
        if new_password == current_password:
            self.show_status("New password must be different from current password", error=True)
            self.new_password_entry.focus_set()
            return
        
        # Disable button during change
        self.change_btn.config(state='disabled', text='Changing...')
        self.show_status("Changing password...", error=False)
        
        # Change password
        success, message = self.user_manager.change_password(
            self.username, current_password, new_password
        )
        
        if success:
            self.show_status("Password changed successfully!", error=False)
            self.result = True
            self.dialog.after(1000, self.close_dialog)
        else:
            self.show_status(f"Failed to change password: {message}", error=True)
            self.change_btn.config(state='normal', text='Change Password')
            self.current_password_entry.delete(0, tk.END)
            self.current_password_entry.focus_set()
    
    def skip_password_change(self):
        """Handle skipping password change"""
        result = messagebox.askyesno(
            "Skip Password Change",
            "Are you sure you want to skip changing your password?\n\n"
            "This is not recommended for security reasons.\n"
            "You can change your password later in the Account tab.",
            icon='warning'
        )
        
        if result:
            self.result = True
            self.close_dialog()
    
    def show_status(self, message: str, error: bool = False):
        """Show status message"""
        if error:
            color = self.colors['error']
        else:
            color = self.colors['success']
        self.status_label.config(text=message, fg=color)
    
    def on_cancel(self):
        """Handle dialog cancellation"""
        result = messagebox.askyesno(
            "Cancel",
            "Are you sure you want to cancel?\n\n"
            "You will be logged out and need to login again.",
            icon='question'
        )
        
        if result:
            self.result = False
            self.close_dialog()
    
    def close_dialog(self):
        """Close the dialog"""
        self.dialog.destroy()
    
    def show(self) -> bool:
        """
        Show the password change dialog and return result
        
        Returns:
            bool: True if password changed or skipped, False if cancelled
        """
        # Wait for dialog to close
        self.dialog.wait_window()
        return self.result
