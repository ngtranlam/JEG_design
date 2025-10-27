"""
Account Integration Module for JEG Design Extract

This module contains the necessary modifications to integrate the account system
into the main application. Apply these changes to jeg_design_extract.py
"""

# Add these imports at the top of jeg_design_extract.py
IMPORTS_TO_ADD = """
from user_manager import UserManager
from login_dialog import LoginDialog
from account_tab import AccountTab
"""

# Add these lines in the __init__ method of JEGDesignExtractGUI class
INIT_ADDITIONS = """
        # Initialize User Manager
        self.user_manager = UserManager()
        
        # Check if user is already logged in (restore session)
        if not self.user_manager.restore_session():
            # Show login dialog if no valid session
            self.root.after(100, self.show_login_dialog)
        else:
            self.add_log(f"Welcome back, {self.user_manager.get_current_user()}!")
"""

# Modify the setup_ui method to include Account tab
SETUP_UI_MODIFICATION = """
        # In setup_ui method, change this line:
        # page_names = ["extract", "upscale", "video_gen"]
        # To:
        page_names = ["extract", "upscale", "video_gen", "account"]
        
        # And add this after creating other tabs:
        # Create the UI for the Account tab
        self.create_account_ui(self.pages["account"])
"""

# Add these methods to the JEGDesignExtractGUI class
METHODS_TO_ADD = """
    def show_login_dialog(self):
        \"\"\"Show login dialog on startup\"\"\"
        login_dialog = LoginDialog(self.root, self.user_manager)
        
        if login_dialog.show():
            # Login successful
            current_user = self.user_manager.get_current_user()
            self.add_log(f"Welcome, {current_user}!")
            
            # Update window title to include username
            self.root.title(f"JEG Design Studio v2.2.0 - {current_user}")
            
            # Refresh account tab if it exists
            if hasattr(self, 'account_tab'):
                self.account_tab.refresh_data()
        else:
            # Login cancelled, close application
            self.add_log("Login required. Closing application...")
            self.root.after(2000, self.root.quit)
    
    def create_account_ui(self, parent):
        \"\"\"Create the Account tab UI\"\"\"
        self.account_tab = AccountTab(parent, self.user_manager, self.colors)
    
    def record_image_usage(self, count=1):
        \"\"\"Record image processing usage\"\"\"
        if self.user_manager.is_logged_in():
            self.user_manager.record_image_usage(count=count)
            self.add_log(f"💰 Recorded {count} image processing usage (${self.user_manager.IMAGE_PROCESSING_COST * count:.4f})")
    
    def record_video_usage(self, count=1):
        \"\"\"Record video generation usage\"\"\"
        if self.user_manager.is_logged_in():
            self.user_manager.record_video_usage(count=count)
            self.add_log(f"💰 Recorded {count} video generation usage (${self.user_manager.VIDEO_GENERATION_COST * count:.2f})")
    
    def check_user_authentication(self):
        \"\"\"Check if user is authenticated before allowing operations\"\"\"
        if not self.user_manager.is_logged_in():
            messagebox.showwarning("Authentication Required", 
                                 "Please login to use this feature.")
            return False
        return True
"""

# Modify the sidebar creation to include Account tab
SIDEBAR_MODIFICATION = """
    def create_sidebar(self, parent):
        # In the create_sidebar method, change this:
        # tabs = ["Extract design", "Up scale", "Video gen"]
        # keys = ["extract", "upscale", "video_gen"]
        # To:
        tabs = ["Extract design", "Up scale", "Video gen", "Account"]
        keys = ["extract", "upscale", "video_gen", "account"]
        
        # And update the button creation accordingly
"""

# Add usage tracking to existing methods
USAGE_TRACKING_ADDITIONS = """
# In process_with_gemini_print method, add after successful processing:
self.record_image_usage()

# In process_with_gemini_embroidery method, add after successful processing:
self.record_image_usage()

# In _generate_video_thread method, add after successful video generation:
self.record_video_usage()

# In process_upscale_image method, add after successful upscaling:
self.record_image_usage()
"""

def apply_account_integration():
    """
    This function shows how to integrate the account system.
    You need to manually apply these changes to jeg_design_extract.py
    """
    print("Account Integration Instructions:")
    print("=" * 50)
    print("\n1. Add imports at the top of jeg_design_extract.py:")
    print(IMPORTS_TO_ADD)
    print("\n2. Add initialization code in __init__ method:")
    print(INIT_ADDITIONS)
    print("\n3. Modify setup_ui method:")
    print(SETUP_UI_MODIFICATION)
    print("\n4. Add new methods to JEGDesignExtractGUI class:")
    print(METHODS_TO_ADD)
    print("\n5. Modify sidebar creation:")
    print(SIDEBAR_MODIFICATION)
    print("\n6. Add usage tracking to existing methods:")
    print(USAGE_TRACKING_ADDITIONS)

if __name__ == "__main__":
    apply_account_integration()
