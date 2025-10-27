# 📋 Changelog

All notable changes to JEG Design Extract will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2024-10-16

### 🎉 Added
- **PhotoRoom Background Removal** - Professional background removal for Embroidery mode
- **Enhanced Embroidery Flow** - New 5-step processing pipeline with background removal
- **Debug Logging** - Comprehensive logging for troubleshooting
- **Build Improvements** - Updated GitHub Actions workflows with caching and verification

### 🔧 Changed
- **Embroidery Processing** - Updated prompts for better chromakey background generation
- **Workflow Optimization** - Improved CI/CD pipeline with dependency caching
- **Error Handling** - Better fallback mechanisms for API failures

### 🐛 Fixed
- **Background Removal** - Improved transparency detection and handling
- **Build Process** - Fixed missing module imports in PyInstaller builds
- **UI Responsiveness** - Better progress indicators for multi-step processes

### 📦 Dependencies
- Added `pyinstaller>=5.13.0` to requirements
- Updated `google-genai>=0.3.0` for latest features

## [2.1.0] - 2024-10-01

### 🎉 Added
- **Video Generation** - Create TikTok-ready videos with Gemini Veo3
- **Dual Camera Angles** - Close-up and full-body video generation
- **16s Merged Videos** - Automatic video concatenation with ffmpeg
- **9:16 Aspect Ratio** - Perfect for TikTok and social media

### 🔧 Changed
- **UI Layout** - New tabbed interface for Extract, Upscale, and Video Gen
- **Script Generation** - AI-powered video script creation
- **Video Quality** - Full frame 9:16 without black borders

### 🐛 Fixed
- **Memory Management** - Better handling of large video files
- **API Timeouts** - Increased timeout for video generation
- **Cross-platform** - Improved compatibility across Windows and macOS

## [2.0.0] - 2024-09-15

### 🎉 Added
- **Gemini AI Integration** - Advanced design processing with Google Gemini
- **Embroidery Mode** - Specialized processing for embroidery designs
- **Mockup Generation** - Create realistic product mockups
- **Batch Processing** - Handle multiple images efficiently
- **Cache System** - Faster repeated operations

### 🔧 Changed
- **Complete UI Overhaul** - Modern dark theme interface
- **Processing Pipeline** - Multi-step AI-enhanced workflow
- **Output Quality** - Professional-grade results with 4x upscaling

### 🐛 Fixed
- **Memory Leaks** - Improved memory management
- **File Handling** - Better support for various image formats
- **Error Recovery** - Robust error handling and user feedback

### 💔 Breaking Changes
- **API Changes** - New Gemini API integration requires API key
- **File Structure** - Updated project organization
- **Dependencies** - New requirements for AI processing

## [1.5.0] - 2024-08-01

### 🎉 Added
- **AI Upscaling** - Real-ESRGAN integration for image enhancement
- **Custom Models** - Support for different upscaling models
- **Progress Tracking** - Real-time processing progress indicators
- **Multi-format Support** - Extended file format compatibility

### 🔧 Changed
- **Performance** - Optimized processing algorithms
- **UI/UX** - Improved user interface and experience
- **File Management** - Better organization of processed files

### 🐛 Fixed
- **Stability** - Reduced crashes and improved error handling
- **Compatibility** - Better cross-platform support
- **Resource Usage** - Optimized memory and CPU usage

## [1.0.0] - 2024-06-01

### 🎉 Initial Release
- **Basic Design Extraction** - Core functionality for design processing
- **Background Removal** - Simple background removal capabilities
- **Cross-platform Support** - Windows and macOS compatibility
- **User-friendly Interface** - Intuitive GUI for easy operation

---

## 📝 Notes

### Version Numbering
- **Major** (X.0.0) - Breaking changes, major new features
- **Minor** (0.X.0) - New features, backwards compatible
- **Patch** (0.0.X) - Bug fixes, small improvements

### Support
For questions about specific versions or upgrade paths, please:
- Check our [Documentation](https://docs.jeg-design.com)
- Visit [GitHub Issues](https://github.com/ngtranlam/jeg-design-extract/issues)
- Join our [Discord Community](https://discord.gg/jeg-design)

---

[⬆️ Back to README](README.md)
