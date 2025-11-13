#!/usr/bin/env python3
"""
Universal build script cho JEG Design Extract
Hỗ trợ cả macOS và Windows
"""

import os
import subprocess
import sys
import platform
from pathlib import Path

def build_macos():
    """Build macOS app bundle using PyInstaller"""
    
    print("🍎 Building cho macOS...")
    
    # PyInstaller command cho macOS với tất cả dependencies
    cmd = [
        "pyinstaller",
        "--onefile",                    # Tạo 1 executable file
        "--windowed",                   # Ẩn terminal
        "--name=JEGDesignExtract",      # Tên app
        "--add-data=jeglogo.png:.",        # Thêm logo file
        "--add-data=upscayl_core:upscayl_core",  # Thêm upscayl resources
        # Hidden imports cho các module mới
        "--hidden-import=google.genai",
        "--hidden-import=google.generativeai",
        "--hidden-import=requests",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=threading",
        "--hidden-import=json",
        "--hidden-import=hashlib",
        "--hidden-import=pathlib",
        "--hidden-import=datetime",
        "--hidden-import=numpy",
        "--hidden-import=cv2",
        # Collect submodules
        "--collect-submodules=google.genai",
        "--collect-submodules=google.generativeai",
        "--collect-submodules=PIL",
        "--collect-submodules=cv2",
        "jeg_design_extract.py"
    ]
    
    # Thêm icon nếu có
    if os.path.exists("app_icon.png"):
        cmd.insert(-1, "--icon=app_icon.png")
        print("✅ Sử dụng icon app_icon.png")
    elif os.path.exists("app.icns"):
        cmd.insert(-1, "--icon=app.icns")
        print("✅ Sử dụng icon app.icns (fallback)")
    else:
        print("⚠️  Không tìm thấy icon, build không có icon")
    
    print("🔧 Đang build macOS app...")
    print(f"📝 Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build macOS thành công!")
        
        # Kiểm tra file output
        exe_path = Path("dist/JEGDesignExtract")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 macOS executable: {exe_path}")
            print(f"📊 Kích thước: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Không tìm thấy executable trong dist/")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi build macOS: {e}")
        return False

def build_windows():
    """Build Windows .exe file using PyInstaller"""
    
    print("🪟 Building cho Windows...")
    
    # PyInstaller command cho Windows - sử dụng spec file tối ưu
    cmd = [
        "pyinstaller",
        "windows_build.spec",           # Sử dụng spec file tối ưu với full config
        "--distpath=dist"               # Output directory
    ]
    
    # Icon đã được handle trong spec file
    if os.path.exists("app_icon.png"):
        print("✅ Icon app_icon.png sẽ được sử dụng (configured trong spec file)")
    elif os.path.exists("app.ico"):
        print("✅ Icon app.ico sẽ được sử dụng (fallback)")
    else:
        print("⚠️  Không tìm thấy icon, build sẽ không có icon")
    
    print("🔧 Đang build Windows .exe...")
    print(f"📝 Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build Windows thành công!")
        
        # Kiểm tra file output
        exe_path = Path("dist/JEGDesignExtract.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Windows executable: {exe_path}")
            print(f"📊 Kích thước: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Không tìm thấy .exe trong dist/")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi build Windows: {e}")
        return False

def detect_and_build():
    """Tự động detect platform và build"""
    current_platform = platform.system()
    
    print(f"🔍 Detected platform: {current_platform}")
    
    if current_platform == "Darwin":  # macOS
        return build_macos()
    elif current_platform == "Windows":
        return build_windows()
    else:
        print(f"❌ Platform {current_platform} không được hỗ trợ!")
        print("💡 Script này chỉ hỗ trợ macOS và Windows")
        return False

def build_both():
    """Build cho cả macOS và Windows (nếu có thể)"""
    success_count = 0
    
    print("🚀 Attempting to build cho cả hai platform...")
    
    # Thử build cho platform hiện tại trước
    if detect_and_build():
        success_count += 1
    
    # Có thể mở rộng để build cross-platform ở đây
    # (cần docker hoặc CI/CD pipeline)
    
    return success_count > 0

def check_dependencies():
    """Kiểm tra tất cả dependencies cần thiết"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        ('PIL', 'Pillow'),
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('sklearn', 'scikit-learn'),
        ('google.genai', 'google-genai'),
        ('google.generativeai', 'google-generativeai'),
    ]
    
    missing_modules = []
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - OK")
        except ImportError:
            print(f"❌ {module_name} - MISSING")
            missing_modules.append(package_name)
    
    if missing_modules:
        print(f"\n❌ Missing dependencies: {', '.join(missing_modules)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies OK")
    return True

def check_required_files():
    """Kiểm tra các file cần thiết cho build"""
    print("🔍 Checking required files...")
    
    required_files = [
        'jeg_design_extract.py',
        'gemini_client.py',
        'photoroom_client.py',
        'user_manager.py',
        'login_dialog.py',
        'password_change_dialog.py',
        'account_tab.py',
        'upscayl_processor.py',
        'image_processor.py',
    ]
    
    missing_files = []
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} - OK")
        else:
            print(f"❌ {file_name} - MISSING")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files OK")
    return True

def setup_pyinstaller():
    """Kiểm tra và cài đặt PyInstaller"""
    try:
        import PyInstaller
        print("✅ PyInstaller đã có sẵn")
        return True
    except ImportError:
        print("❌ Chưa có PyInstaller. Đang cài đặt...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ Đã cài PyInstaller")
            return True
        except:
            print("❌ Không thể cài PyInstaller!")
            return False

def cleanup():
    """Dọn dẹp file tạm"""
    import shutil
    
    # Xóa thư mục build và file .spec
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("🗑️  Đã xóa thư mục build")
    
    spec_file = "JEGDesignExtract.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print("🗑️  Đã xóa file .spec")

def show_instructions():
    """Hiển thị hướng dẫn sau build"""
    current_platform = platform.system()
    
    print("\n📋 Hướng dẫn:")
    if current_platform == "Darwin":  # macOS
        print("   🍎 macOS Executable:")
        print("   1. File ở trong thư mục 'dist/JEGDesignExtract'")
        print("   2. Copy sang máy Mac khác")
        print("   3. chmod +x JEGDesignExtract (nếu cần)")
        print("   4. ./JEGDesignExtract để chạy")
        print("   5. Nếu gặp Gatekeeper: Right-click → Open")
    elif current_platform == "Windows":
        print("   🪟 Windows Executable:")
        print("   1. File ở trong thư mục 'dist/JEGDesignExtract.exe'")
        print("   2. Copy sang máy Windows khác")
        print("   3. Double-click để chạy")
    
    print("\n💡 Tips:")
    print("   - Copy toàn bộ thư mục 'dist/' để đảm bảo")
    print("   - Test trên máy target trước khi phân phối")

if __name__ == "__main__":
    print("=" * 60)
    print("    JEG DESIGN EXTRACT - UNIVERSAL BUILDER v2.2.0")
    print("=" * 60)
    
    # Hiển thị thông tin platform
    print(f"🖥️  Platform: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print()
    
    # Pre-build checks
    print("🔍 Pre-build validation...")
    
    # Check required files
    if not check_required_files():
        print("❌ Missing required files. Cannot proceed.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Missing dependencies. Cannot proceed.")
        print("💡 Install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    # Setup PyInstaller
    if not setup_pyinstaller():
        print("❌ Cannot proceed without PyInstaller")
        sys.exit(1)
    
    print("\n✅ All pre-build checks passed!")
    
    # Build
    print("\n🚀 Bắt đầu build process...")
    if detect_and_build():
        print("\n🔧 Dọn dẹp file tạm...")
        cleanup()
        print("\n✨ Build hoàn tất!")
        show_instructions()
    else:
        print("\n❌ Build thất bại!")
        sys.exit(1) 