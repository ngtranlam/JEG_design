@echo off
echo ========================================
echo  JEG Design Extract v2.2.0 - Windows Builder
echo ========================================

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo.
echo Checking pip...
pip --version
if %errorlevel% neq 0 (
    echo ERROR: pip not found!
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Verifying installation...
python -c "import PIL, cv2, numpy, requests, sklearn; print('All dependencies OK')"
if %errorlevel% neq 0 (
    echo ERROR: Dependencies verification failed!
    pause
    exit /b 1
)

echo.
echo Building executable...
python build_exe.py
if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo.
echo Your executable is ready:
echo   - Location: dist\JEGDesignExtract.exe
echo   - Size: Check file properties
echo   - Ready to distribute!
echo.
echo Next steps:
echo   1. Test the executable on this machine
echo   2. Copy dist\ folder to target machines
echo   3. Run JEGDesignExtract.exe
echo ========================================
pause