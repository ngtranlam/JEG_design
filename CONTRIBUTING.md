# 🤝 Contributing to JEG Design Extract

Thank you for your interest in contributing to JEG Design Extract! We welcome contributions from developers of all skill levels.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Setup](#-development-setup)
- [Making Changes](#-making-changes)
- [Submitting Changes](#-submitting-changes)
- [Reporting Issues](#-reporting-issues)
- [Feature Requests](#-feature-requests)

## 🤝 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:

- **Be respectful** - Treat everyone with respect and kindness
- **Be inclusive** - Welcome newcomers and help them learn
- **Be constructive** - Provide helpful feedback and suggestions
- **Be patient** - Remember that everyone is learning

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Basic knowledge of Python and GUI development
- Familiarity with AI/ML concepts (helpful but not required)

### Development Environment

We recommend using:
- **IDE**: VS Code, PyCharm, or similar
- **OS**: Windows 10+, macOS 10.15+, or Linux
- **Hardware**: 8GB+ RAM, dedicated GPU (optional but helpful)

## 🛠️ Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/jeg-design-extract.git
   cd jeg-design-extract
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys** (Optional for basic development)
   ```bash
   # Copy example config
   cp config.example.json config.json
   
   # Edit config.json with your API keys
   # - Gemini API key (for AI processing)
   # - PhotoRoom API key (for background removal)
   ```

5. **Run the Application**
   ```bash
   python jeg_design_extract.py
   ```

## 🔧 Making Changes

### Branch Naming Convention

Use descriptive branch names:
- `feature/add-new-upscaling-model`
- `bugfix/fix-memory-leak`
- `docs/update-readme`
- `refactor/improve-error-handling`

### Code Style

We follow PEP 8 with some modifications:

```python
# Good
def process_image(image_path: str, output_size: tuple) -> bool:
    """Process an image with the specified output size."""
    try:
        # Implementation here
        return True
    except Exception as e:
        logger.error(f"Failed to process image: {e}")
        return False

# Use type hints
# Add docstrings for functions
# Handle exceptions gracefully
# Use descriptive variable names
```

### Testing

Before submitting changes:

1. **Manual Testing**
   ```bash
   # Test basic functionality
   python jeg_design_extract.py
   
   # Test different modes
   # - Extract Design (Print mode)
   # - Extract Design (Embroidery mode)
   # - Video Generation
   # - Upscaling
   ```

2. **Code Quality**
   ```bash
   # Check for common issues
   python -m py_compile jeg_design_extract.py
   python -m py_compile gemini_client.py
   python -m py_compile photoroom_client.py
   ```

3. **Build Testing**
   ```bash
   # Test build process
   python build_exe.py
   ```

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add PhotoRoom background removal for embroidery mode"
git commit -m "Fix memory leak in video generation"
git commit -m "Update README with new installation instructions"

# Bad
git commit -m "fix bug"
git commit -m "update"
git commit -m "changes"
```

## 📤 Submitting Changes

1. **Create Pull Request**
   - Push your changes to your fork
   - Create a PR from your branch to `main`
   - Use the PR template (auto-filled)

2. **PR Requirements**
   - [ ] Clear description of changes
   - [ ] Screenshots/videos for UI changes
   - [ ] Testing instructions
   - [ ] Updated documentation if needed
   - [ ] No merge conflicts

3. **Review Process**
   - Maintainers will review your PR
   - Address any feedback promptly
   - Be patient - reviews may take 1-3 days

## 🐛 Reporting Issues

### Bug Reports

Use the bug report template and include:

- **Environment**: OS, Python version, app version
- **Steps to Reproduce**: Clear, numbered steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Screenshots**: If applicable
- **Logs**: Error messages or console output

### Example Bug Report

```markdown
**Environment:**
- OS: Windows 11
- Python: 3.11.5
- App Version: 2.2.0

**Steps to Reproduce:**
1. Load image with embroidery mode
2. Select design area
3. Click "Extract Design"
4. PhotoRoom processing fails

**Expected:** Background should be removed
**Actual:** Error message appears, original image returned

**Error Log:**
```
❌ PhotoRoom API error: 401 - Unauthorized
⚠️ PhotoRoom background removal failed, using original Gemini result
```
```

## 💡 Feature Requests

### Before Requesting

- Check existing [issues](https://github.com/ngtranlam/jeg-design-extract/issues)
- Search [discussions](https://github.com/ngtranlam/jeg-design-extract/discussions)
- Consider if it fits the project scope

### Feature Request Template

```markdown
**Feature Description:**
Brief description of the feature

**Use Case:**
Why is this feature needed? Who would use it?

**Proposed Solution:**
How should this feature work?

**Alternatives Considered:**
Other ways to solve this problem

**Additional Context:**
Screenshots, mockups, or examples
```

## 🏗️ Architecture Overview

### Project Structure

```
jeg-design-extract/
├── jeg_design_extract.py      # Main application
├── gemini_client.py           # Gemini AI integration
├── photoroom_client.py        # PhotoRoom API client
├── upscayl_processor.py       # Image upscaling
├── upscayl_core/              # Upscaling models and binaries
├── .github/workflows/         # CI/CD pipelines
├── requirements.txt           # Python dependencies
└── build_exe.py              # Build script
```

### Key Components

- **Main GUI** (`jeg_design_extract.py`) - Tkinter-based interface
- **AI Processing** (`gemini_client.py`) - Gemini API integration
- **Background Removal** (`photoroom_client.py`) - PhotoRoom API
- **Upscaling** (`upscayl_processor.py`) - Real-ESRGAN integration
- **Build System** (`.github/workflows/`) - Automated builds

## 📚 Resources

### Documentation
- [Python Tkinter Guide](https://docs.python.org/3/library/tkinter.html)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [PhotoRoom API Docs](https://www.photoroom.com/api/)

### Learning Resources
- [Python Best Practices](https://realpython.com/python-code-quality/)
- [GUI Development with Tkinter](https://realpython.com/python-gui-tkinter/)
- [Working with Images in Python](https://realpython.com/image-processing-with-the-python-pillow-library/)

## 🎯 Areas for Contribution

### High Priority
- **Performance Optimization** - Improve processing speed
- **Error Handling** - Better user feedback and recovery
- **UI/UX Improvements** - More intuitive interface
- **Documentation** - Code comments and user guides

### Medium Priority
- **New AI Models** - Additional upscaling options
- **File Format Support** - More input/output formats
- **Batch Processing** - Enhanced multi-file handling
- **Localization** - Multi-language support

### Low Priority
- **Plugin System** - Extensible architecture
- **Cloud Integration** - Online storage options
- **Mobile App** - Companion mobile application
- **Web Interface** - Browser-based version

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** - Contributors section
- **Release Notes** - Feature acknowledgments
- **GitHub** - Contributor graphs and statistics

## 📞 Getting Help

If you need help with contributing:

- 💬 [Discord Community](https://discord.gg/jeg-design) - Real-time chat
- 📧 [Email](mailto:dev@jeg-design.com) - Direct developer contact
- 📖 [Discussions](https://github.com/ngtranlam/jeg-design-extract/discussions) - GitHub discussions

---

Thank you for contributing to JEG Design Extract! 🎨✨
