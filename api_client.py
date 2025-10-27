import requests
import os

IMGBB_API_KEY = "b248161838895d85e5ac6884c5f0de07" 
DYNAMIC_MOCKUPS_API_KEY = "79d70e34-104c-493c-8553-723102e37207:f1afba7b448fe18ec304c8c71a0768f5756e3973b50bcd7745f6815be4e2f1ef"
JEG_API_BASE_URL = "https://jeg-redesign.onrender.com"

# Global auth headers (will be set by AuthManager)
_auth_headers = {}


def set_auth_headers(auth_headers):
    """
    Set authentication headers for API requests
    
    Args:
        auth_headers (dict): Authentication headers from AuthManager
    """
    global _auth_headers
    _auth_headers = auth_headers.copy()

def get_auth_headers():
    """Get current authentication headers"""
    return _auth_headers.copy()

def fetch_mockup_templates():
    """
    Fetches the list of available mockup templates from the JEG backend.
    Now supports authenticated requests for premium templates.
    """
    url = f"{JEG_API_BASE_URL}/mockup-templates"
    headers = _auth_headers.copy()
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mockup templates: {e}")
        return None

def upload_image_to_imgbb(image_base64_data):
    """
    Uploads a base64 encoded image to ImgBB and returns the public URL.
    """
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
        "image": image_base64_data,
    }
    try:
        response = requests.post(url, data=payload, timeout=60) # Longer timeout for uploads
        response.raise_for_status()
        result = response.json()
        if result.get("success"):
            return result["data"]["url"]
        else:
            print(f"ImgBB upload failed: {result.get('error', {}).get('message')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error uploading to ImgBB: {e}")
        return None

def render_mockup(mockup_uuid, smart_object_uuid, image_url):
    """
    Calls the DynamicMockups API to render a mockup.
    """
    url = "https://app.dynamicmockups.com/api/v1/renders"
    headers = {
        "x-api-key": DYNAMIC_MOCKUPS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = {
        "mockup_uuid": mockup_uuid,
        "export_label": f"MOCKUP_{os.urandom(4).hex()}",
        "export_options": {
            "image_format": "jpg",
            "image_size": 1500,
            "mode": "download"
        },
        "smart_objects": [
            {
                "uuid": smart_object_uuid,
                "asset": {
                    "url": image_url,
                    "fit": "contain"
                }
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=body, timeout=120) # Longer timeout for rendering
        response.raise_for_status()
        result = response.json()
        if result.get("success"):
            return result["data"]["export_path"]
        else:
            print(f"DynamicMockups render failed: {result.get('message')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error rendering mockup: {e}")
        return None

def save_user_project(project_data):
    """
    Save user project data to cloud (authenticated endpoint)
    
    Args:
        project_data (dict): Project data to save
        
    Returns:
        dict: Response data or None if failed
    """
    if not _auth_headers:
        print("Not authenticated - cannot save project to cloud")
        return None
        
    url = f"{JEG_API_BASE_URL}/user/projects"
    headers = {
        "Content-Type": "application/json",
        **_auth_headers
    }
    
    try:
        response = requests.post(url, headers=headers, json=project_data, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error saving user project: {e}")
        return None

def get_user_projects():
    """
    Get user's saved projects from cloud
    
    Returns:
        list: List of user projects or empty list if failed
    """
    if not _auth_headers:
        print("Not authenticated - cannot fetch user projects")
        return []
        
    url = f"{JEG_API_BASE_URL}/user/projects"
    headers = _auth_headers.copy()
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('projects', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user projects: {e}")
        return []

def sync_user_settings(settings_data):
    """
    Sync user settings to cloud
    
    Args:
        settings_data (dict): User settings to sync
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not _auth_headers:
        print("Not authenticated - cannot sync settings")
        return False
        
    url = f"{JEG_API_BASE_URL}/user/settings"
    headers = {
        "Content-Type": "application/json",
        **_auth_headers
    }
    
    try:
        response = requests.post(url, headers=headers, json=settings_data, timeout=30)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error syncing user settings: {e}")
        return False

def get_user_settings():
    """
    Get user settings from cloud
    
    Returns:
        dict: User settings or empty dict if failed
    """
    if not _auth_headers:
        print("Not authenticated - cannot fetch user settings")
        return {}
        
    url = f"{JEG_API_BASE_URL}/user/settings"
    headers = _auth_headers.copy()
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('settings', {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user settings: {e}")
        return {}
