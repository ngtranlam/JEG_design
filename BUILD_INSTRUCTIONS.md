# 🔨 Build Instructions - JEG Design Extract v2.2.0

## 📋 Overview

Hướng dẫn build executable cho JEG Design Extract với tất cả tính năng mới nhất:
- ✅ Account System với API integration
- ✅ Gemini AI Integration
- ✅ PhotoRoom Background Removal
- ✅ Video Generation với Veo3
- ✅ Time Filter cho usage statistics

---

## 🛠️ Prerequisites

### System Requirements
- **Python**: 3.8+ (recommended: 3.10+)
- **RAM**: Minimum 4GB (recommended: 8GB+)
- **Storage**: 2GB free space for build process
- **Internet**: Required for downloading dependencies

### Platform Support
- ✅ **Windows 10/11** (x64)
- ✅ **macOS 10.15+** (Intel/Apple Silicon)
- ❌ Linux (not officially supported)

---

## 🚀 Quick Build

### Windows
```bash
# Method 1: Use batch script (recommended)
build.bat

# Method 2: Manual build
pip install -r requirements.txt
python build_exe.py
```

### macOS
```bash
# Install dependencies
pip install -r requirements.txt

# Build
python build_exe.py
```

---

## 📦 Dependencies

### Core Dependencies
```
opencv-python>=4.8.0          # Image processing
Pillow>=9.0.0                 # Image handling
numpy>=1.21.0                 # Numerical operations
requests>=2.28.0              # HTTP requests
scikit-learn>=1.3.0           # ML algorithms
pyinstaller>=5.13.0           # Executable builder
```

### AI/API Dependencies
```
google-genai>=0.3.0           # Gemini AI client
google-generativeai>=0.3.0    # Gemini API
grpcio>=1.50.0                # gRPC communication
protobuf>=4.21.0              # Protocol buffers
google-auth>=2.15.0           # Google authentication
google-auth-oauthlib>=0.7.0   # OAuth support
google-auth-httplib2>=0.1.0   # HTTP transport
```

---

## 🔧 Build Process Details

### Pre-build Validation
Build script tự động kiểm tra:
1. **Required Files**: Tất cả Python modules cần thiết
2. **Dependencies**: Tất cả packages đã cài đặt
3. **PyInstaller**: Build tool availability

### Build Configuration

#### Windows Build (windows_build.spec)
- **Output**: `dist/JEGDesignExtract.exe`
- **Mode**: Windowed (no console)
- **Icon**: `app_icon.ico` (if available)
- **Resources**: Upscayl core, all Python modules
- **Hidden Imports**: 150+ modules for compatibility

#### macOS Build
- **Output**: `dist/JEGDesignExtract`
- **Mode**: App bundle (windowed)
- **Icon**: `app.icns` (if available)
- **Resources**: Upscayl core, all Python modules
- **Hidden Imports**: Google AI, OpenCV, PIL modules

---

## 📁 Build Output

### File Structure
```
dist/
├── JEGDesignExtract.exe     # Windows executable
├── JEGDesignExtract         # macOS executable
└── [dependencies]           # Runtime libraries
```

### File Sizes (Approximate)
- **Windows**: 150-200 MB
- **macOS**: 120-180 MB

---

## 🧪 Testing Build

### Pre-distribution Testing
```bash
# Test executable
cd dist
./JEGDesignExtract           # macOS
JEGDesignExtract.exe         # Windows

# Test core features
1. Login with test account
2. Extract design (Print mode)
3. Extract design (Embroidery mode)
4. Generate video
5. Check Account tab statistics
```

### Common Issues & Solutions

#### "Module not found" errors
```bash
# Solution: Add to hidden imports in spec file
--hidden-import=missing_module_name
```

#### "DLL load failed" (Windows)
```bash
# Solution: Install Visual C++ Redistributable
# Or add to excludes if not needed
```

#### Large file size
```bash
# Solution: Add unused modules to excludes
excludes=['matplotlib', 'PyQt5', 'jupyter']
```

---

## 🔍 Troubleshooting

### Build Fails

#### Missing Dependencies
```bash
# Check what's missing
python -c "import PIL, cv2, numpy, requests, sklearn, google.genai"

# Install missing packages
pip install -r requirements.txt
```

#### PyInstaller Issues
```bash
# Clear cache and rebuild
pyinstaller --clean windows_build.spec

# Or delete build folders
rm -rf build/ dist/ *.spec
```

#### Import Errors
```bash
# Test imports manually
python -c "from jeg_design_extract import *"

# Check module paths
python -c "import sys; print(sys.path)"
```

### Runtime Issues

#### "Failed to execute script"
- **Cause**: Missing runtime dependencies
- **Solution**: Include in hidden imports or data files

#### Antivirus False Positives
- **Cause**: PyInstaller executables flagged as suspicious
- **Solution**: Add to antivirus whitelist, use code signing

#### Slow Startup
- **Cause**: Large executable with many dependencies
- **Solution**: Normal behavior, optimize excludes if needed

---

## 📊 Build Optimization

### Reduce File Size
```python
# Add to excludes in spec file
excludes = [
    'matplotlib',      # Plotting library
    'PyQt5', 'PyQt6',  # GUI frameworks
    'jupyter',         # Notebook environment
    'pytest',          # Testing framework
    'sphinx',          # Documentation
    'babel',           # Internationalization
]
```

### Improve Performance
```python
# Use onefile for distribution
--onefile

# Disable UPX compression (faster startup)
upx=False

# Optimize imports
--optimize=2
```

---

## 🚀 Distribution

### Windows Distribution
1. **Test executable** on clean Windows machine
2. **Create installer** (optional): Use NSIS or Inno Setup
3. **Code signing** (recommended): For enterprise distribution
4. **Antivirus scanning**: Submit to VirusTotal

### macOS Distribution
1. **Test executable** on clean macOS machine
2. **Code signing**: Required for Gatekeeper bypass
3. **Notarization**: Required for macOS 10.15+
4. **DMG creation**: For professional distribution

---

## 📝 Build Checklist

### Pre-build
- [ ] All source files present
- [ ] Dependencies installed
- [ ] PyInstaller available
- [ ] Icon files available
- [ ] Upscayl core resources present

### Post-build
- [ ] Executable created successfully
- [ ] File size reasonable (<300MB)
- [ ] Test on build machine
- [ ] Test on clean target machine
- [ ] All features working
- [ ] No console errors

### Distribution
- [ ] Antivirus scan clean
- [ ] Code signing (if applicable)
- [ ] Documentation included
- [ ] Installation instructions
- [ ] Support contact information

---

## 🆘 Support

### Build Issues
1. **Check console output** for detailed error messages
2. **Run with verbose**: `python build_exe.py --verbose`
3. **Check dependencies**: `pip list | grep -E "(opencv|PIL|numpy|google)"`
4. **Clear cache**: Delete `build/`, `dist/`, `__pycache__/`

### Contact
- **Developer**: Lam Nguyen
- **Project**: JEG Design Extract v2.2.0
- **Build System**: PyInstaller + Custom Scripts

---

## 📈 Version History

### v2.2.0 (Current)
- ✅ Account system integration
- ✅ Gemini AI support
- ✅ PhotoRoom API integration
- ✅ Video generation with Veo3
- ✅ Time-based usage filtering
- ✅ API sync functionality

### Build Improvements
- ✅ Pre-build validation
- ✅ Dependency checking
- ✅ Enhanced error handling
- ✅ Comprehensive hidden imports
- ✅ Optimized file inclusion

**🎉 Build system ready for production deployment!**
