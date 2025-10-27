import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import platform
from user_manager import UserManager

class LoginDialog:
    """
    Login dialog for JEG Design Extract
    """
    
    def __init__(self, parent, user_manager: UserManager):
        self.parent = parent
        self.user_manager = user_manager
        self.result = None
        self.username = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("JEG Design Extract - Login")
        self.dialog.geometry("450x400")
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
            'error': '#DC3545'
        }
        
        self.dialog.configure(bg=self.colors['bg_dark'])
        
        self.create_ui()
        self.center_dialog()
        
        # Focus on username entry
        self.username_entry.focus_set()
        
        # Bind Enter key to login
        self.dialog.bind('<Return>', lambda e: self.login())
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def create_ui(self):
        """Create the login UI"""
        # Main container
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Logo/Title section
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # App title
        title_label = tk.Label(title_frame, 
                              text="🎨 JEG Design Extract",
                              font=('Arial', 16, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_dark'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Please login to continue",
                                 font=('Arial', 10),
                                 fg=self.colors['text_gray'],
                                 bg=self.colors['bg_dark'])
        subtitle_label.pack(pady=(5, 0))
        
        # Login form
        form_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'], relief=tk.RAISED, bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        form_content = tk.Frame(form_frame, bg=self.colors['bg_medium'])
        form_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Username field
        username_label = tk.Label(form_content,
                                 text="Username:",
                                 font=('Arial', 10, 'bold'),
                                 fg=self.colors['text_white'],
                                 bg=self.colors['bg_medium'])
        username_label.pack(anchor='w', pady=(0, 5))
        
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(form_content,
                                      textvariable=self.username_var,
                                      font=('Arial', 11),
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['text_white'],
                                      insertbackground=self.colors['text_white'],
                                      relief=tk.FLAT,
                                      bd=5)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        password_label = tk.Label(form_content,
                                 text="Password:",
                                 font=('Arial', 10, 'bold'),
                                 fg=self.colors['text_white'],
                                 bg=self.colors['bg_medium'])
        password_label.pack(anchor='w', pady=(0, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(form_content,
                                      textvariable=self.password_var,
                                      font=('Arial', 11),
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['text_white'],
                                      insertbackground=self.colors['text_white'],
                                      relief=tk.FLAT,
                                      bd=5,
                                      show='*')
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Login button
        self.login_btn = tk.Button(form_content,
                                  text="Login",
                                  command=self.login,
                                  font=('Arial', 11, 'bold'),
                                  bg=self.colors['button_bg'],
                                  fg='black',
                                  relief=tk.FLAT,
                                  bd=0,
                                  padx=20,
                                  pady=8,
                                  cursor='hand2')
        self.login_btn.pack(fill=tk.X)
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(status_frame,
                                    text="",
                                    font=('Arial', 9),
                                    fg=self.colors['error'],
                                    bg=self.colors['bg_dark'])
        self.status_label.pack()
        
        # Info text
        info_label = tk.Label(status_frame,
                             text="Default password: jeg@12345",
                             font=('Arial', 8),
                             fg=self.colors['text_gray'],
                             bg=self.colors['bg_dark'])
        info_label.pack(pady=(10, 0))
    
    def center_dialog(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()
        
        try:
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
        except:
            # Fallback to screen center
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width - 450) // 2
            y = (screen_height - 400) // 2
            self.dialog.geometry(f"450x400+{x}+{y}")
    
    def login(self):
        """Handle login attempt"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username:
            self.show_status("Please enter username", error=True)
            self.username_entry.focus_set()
            return
        
        if not password:
            self.show_status("Please enter password", error=True)
            self.password_entry.focus_set()
            return
        
        # Disable login button during authentication
        self.login_btn.config(state='disabled', text='Logging in...')
        self.show_status("Authenticating...", error=False)
        
        # Authenticate
        success, message = self.user_manager.authenticate(username, password)
        
        if success:
            self.username = username
            self.result = True
            self.show_status("Login successful!", error=False)
            
            # Check if this is first login on this device
            if self.user_manager.is_first_login_on_device(username):
                self.dialog.after(500, self.show_password_change_dialog)
            else:
                self.dialog.after(500, self.close_dialog)
        else:
            self.show_status(f"Login failed: {message}", error=True)
            self.login_btn.config(state='normal', text='Login')
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
    
    def show_password_change_dialog(self):
        """Show password change dialog for first-time login"""
        self.dialog.withdraw()  # Hide login dialog
        
        from password_change_dialog import PasswordChangeDialog
        
        change_dialog = PasswordChangeDialog(self.parent, self.user_manager, self.username)
        
        if change_dialog.show():
            # Password changed successfully
            self.user_manager.complete_first_login(self.username)
            self.close_dialog()
        else:
            # User cancelled password change, logout
            self.user_manager.logout()
            self.result = False
            self.close_dialog()
    
    def show_status(self, message: str, error: bool = False):
        """Show status message"""
        color = self.colors['error'] if error else self.colors['accent']
        self.status_label.config(text=message, fg=color)
    
    def on_cancel(self):
        """Handle dialog cancellation"""
        self.result = False
        self.close_dialog()
    
    def close_dialog(self):
        """Close the dialog"""
        self.dialog.destroy()
    
    def show(self) -> bool:
        """
        Show the login dialog and return result
        
        Returns:
            bool: True if login successful, False if cancelled
        """
        # Wait for dialog to close
        self.dialog.wait_window()
        return self.result is True
