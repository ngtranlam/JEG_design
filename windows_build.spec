# -*- mode: python ; coding: utf-8 -*-
"""
Optimized PyInstaller spec file for Windows build
Includes all necessary hidden imports and resources
"""

import sys
import os
from pathlib import Path

# Define paths
SCRIPT_DIR = Path('.')
UPSCAYL_CORE = SCRIPT_DIR / 'upscayl_core'

def add_if_exists(path, dest='.'):
    return [(path, dest)] if Path(path).exists() else []

# Data files to include (required + optional)
datas = [
    (str(UPSCAYL_CORE), 'upscayl_core'),  # Upscayl resources (required)
    ('api_client.py', '.'),               # API client module (required)
    ('upscayl_processor.py', '.'),        # Upscayl processor module (required)
    ('image_processor.py', '.'),          # Image processor module (required)
    ('gemini_client.py', '.'),            # Gemini AI client (required)
    ('photoroom_client.py', '.'),         # PhotoRoom client (required)
    ('user_manager.py', '.'),             # User management (required)
    ('login_dialog.py', '.'),             # Login dialog (required)
    ('password_change_dialog.py', '.'),   # Password change dialog (required)
    ('account_tab.py', '.'),              # Account tab (required)
]

# Add OpenCV data files if they exist
try:
    import cv2
    cv2_data_path = Path(cv2.data.haarcascades).parent
    if cv2_data_path.exists():
        datas.append((str(cv2_data_path), 'cv2/data'))
except:
    pass
datas += (
    add_if_exists('README.md') +
    add_if_exists('version.txt') +
    add_if_exists('AUTHENTICATION_README.md') +
    add_if_exists('mockup_cache', 'mockup_cache') +
    add_if_exists('_cache', '_cache') +
    add_if_exists('jeglogo.png') +
    add_if_exists('app_icon.ico') +
    add_if_exists('app_icon.png') +
    add_if_exists('app.ico')
)

# Hidden imports for Windows compatibility
hiddenimports = [
    # Core libraries
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
    'tkinter.font',
    'tkinter.constants',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageDraw',
    'PIL.ImageSequence',
    'PIL.ImageFont',
    'PIL.ImageFilter',
    'PIL.ImageOps',
    'PIL.ImageEnhance',
    'PIL.PngImagePlugin',
    'PIL.JpegImagePlugin',
    'PIL.BmpImagePlugin',
    'PIL.TiffImagePlugin',
    'PIL.WebPImagePlugin',
    'PIL.ImageFile',
    'PIL.ImageMode',
    'PIL.ImagePalette',
    'PIL.ImageStat',
    'PIL.ImageTransform',
    'PIL.ImageWin',
    'PIL.ImageColor',
    'PIL.ImageMath',
    'PIL.ImageGrab',
    'PIL.ImageChops',
    'PIL.ImageMorph',
    'PIL.ImagePath',
    'PIL.ImageShow',
    'PIL.ImageTk',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'PIL.ImageFilter',
    'PIL.ImageSequence',
    'cv2',
    'numpy',
    'requests',
    'scipy',
    'sklearn',
    'sklearn.cluster',
    'joblib',
    'threadpoolctl',
    
    # Requests and HTTP dependencies (CRITICAL!)
    'urllib3',
    'urllib3.util',
    'urllib3.util.retry',
    'urllib3.exceptions',
    'urllib3.poolmanager',
    'certifi',
    'chardet',
    'idna',
    'six',
    'packaging',
    'pyparsing',
    
    # System modules
    'subprocess',
    'tempfile',
    'pathlib',
    'threading',
    'platform',
    'json',
    'datetime',
    're',
    'base64',
    'io',
    'shutil',
    'time',
    'webbrowser',
    'functools',
    'collections',
    'ctypes',  # For Windows DPI awareness
    'os',
    'sys',
    
    # API and processing modules
    'api_client',
    'upscayl_processor',
    'image_processor',
    'gemini_client',
    'photoroom_client',
    'user_manager',
    'login_dialog',
    'password_change_dialog',
    'account_tab',
    
    # Google AI/Gemini dependencies
    'google',
    'google.genai',
    'google.generativeai',
    'google.generativeai.client',
    'google.generativeai.types',
    'google.auth',
    'google.auth.transport',
    'google.auth.transport.requests',
    'google.oauth2',
    'google.protobuf',
    'grpc',
    'grpcio',
    'proto',
    'protobuf',
    
    # Additional security and crypto
    'hashlib',
    'hmac',
    'secrets',
    'ssl',
    'socket',
    
    # OpenCV hidden imports
    'cv2.cv2',
    'cv2.data',
    'cv2.aruco',
    'cv2.bgsegm',
    'cv2.bioinspired',
    'cv2.ccalib',
    'cv2.datasets',
    'cv2.dnn',
    'cv2.face',
    'cv2.freetype',
    'cv2.fuzzy',
    'cv2.hdf',
    'cv2.hfs',
    'cv2.img_hash',
    'cv2.intensity_transform',
    'cv2.line_descriptor',
    'cv2.mcc',
    'cv2.ml',
    'cv2.motempl',
    'cv2.objdetect',
    'cv2.optflow',
    'cv2.phase_unwrapping',
    'cv2.plot',
    'cv2.quality',
    'cv2.rapid',
    'cv2.reg',
    'cv2.rgbd',
    'cv2.saliency',
    'cv2.stereo',
    'cv2.structured_light',
    'cv2.superres',
    'cv2.surface_matching',
    'cv2.text',
    'cv2.tracking',
    'cv2.video',
    'cv2.videoio',
    'cv2.videostab',
    'cv2.wechat_qrcode',
    'cv2.xfeatures2d',
    'cv2.ximgproc',
    'cv2.xobjdetect',
    'cv2.xphoto',
    'numpy.core',
    'numpy.core.multiarray',
    'numpy.lib.format',
    
    # PIL/Pillow hidden imports
    'PIL._tkinter_finder',
    'PIL.ImageQt',
    'PIL._binary',
    
    # Scipy dependencies
    'scipy.sparse',
    'scipy.sparse.csgraph',
    'scipy.spatial',
    'scipy.special',
    
    # Additional modules that might be needed
    'email',
    'email.mime',
    'email.mime.text',
    'email.mime.multipart',
    'html',
    'html.parser',
    'http',
    'http.client',
    'xml',
    'xml.etree',
    'xml.etree.ElementTree',
    'distutils',
    'distutils.version',
    
    # Image processing additional modules
    'PIL._imaging',
    'PIL._imagingft',
    'PIL._imagingmath',
    'PIL._imagingmorph',
    'PIL._imagingtga',
    'PIL._imagingtk',
    'PIL._webp',
    'PIL._util',
    'PIL._version',
    'PIL._deprecate',
    'PIL._deprecate_util',
    'PIL._deprecate_util_2',
    'PIL._deprecate_util_3',
    'PIL._deprecate_util_4',
    'PIL._deprecate_util_5',
    'PIL._deprecate_util_6',
    'PIL._deprecate_util_7',
    'PIL._deprecate_util_8',
    'PIL._deprecate_util_9',
    'PIL._deprecate_util_10',
]

# Binaries to exclude (only exclude what we're sure we don't need)
excludes = [
    'matplotlib',
    'PyQt5',
    'PyQt6',
    'PySide2',
    'PySide6',
    'tornado',
    'zmq',
    'IPython',
    'jupyter',
    'notebook',
    'pytest',
    'sphinx',
    'docutils',
    'babel',
    'jinja2',
    'markupsafe',
    'pytz',
    'unittest',
    'test',
    'tests',
    '_pytest',
]

block_cipher = None

a = Analysis(
    ['jeg_design_extract.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JEGDesignExtract',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX to avoid false positives
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowed mode
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico' if Path('app_icon.ico').exists() else ('app_icon.png' if Path('app_icon.png').exists() else ('app.ico' if Path('app.ico').exists() else None)),
    # Add version info to look more legitimate
    version='version.txt' if Path('version.txt').exists() else None,
)
