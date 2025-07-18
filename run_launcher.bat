@echo off
title Facebook Unfriend Tracker - All-in-One Launcher
chcp 65001 >nul
color 0b
echo.
echo  ███████╗██████╗     ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
echo  ██╔════╝██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
echo  █████╗  ██████╔╝       ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
echo  ██╔══╝  ██╔══██╗       ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
echo  ██║     ██████╔╝       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
echo  ╚═╝     ╚═════╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
echo.
echo                    Facebook Unfriend Tracker - All-in-One Launcher
echo                          Compact Edition with GUI and Web Interface
echo.
echo ================================================================================
cd /d "%~dp0"

:MENU
echo.
echo [1] 🚀 Launch GUI Application (Recommended)
echo [2] 🌐 Start Web Server Only
echo [3] 📊 Open Web Interface (if server running)
echo [4] 🖥️  Console Launcher (Tkinter-free)
echo [5] 📥 Facebook Data Helper Guide
echo [6] 📋 View Project Info & README
echo [7] 🔧 Build Executable (PyInstaller)
echo [8] 📦 Install Dependencies
echo [9] 🧹 Clean Project Files
echo [10] 💾 Backup Database & Data
echo [11] 📈 Show Database Statistics
echo [12] 📤 Export All Data to CSV
echo [13] 🔍 Check Database Integrity
echo [14] 🚀 Auto Setup (Complete Installation)
echo [15] 🧪 Run Test Suite
echo [16] ❌ Exit
echo.
set /p choice="Select option (1-16): "

if "%choice%"=="1" goto GUI_LAUNCHER
if "%choice%"=="2" goto WEB_SERVER
if "%choice%"=="3" goto OPEN_BROWSER
if "%choice%"=="4" goto CONSOLE_LAUNCHER
if "%choice%"=="5" goto FACEBOOK_HELP
if "%choice%"=="6" goto PROJECT_INFO
if "%choice%"=="7" goto BUILD_EXE
if "%choice%"=="8" goto INSTALL_DEPS
if "%choice%"=="9" goto CLEAN_PROJECT
if "%choice%"=="10" goto BACKUP_DATA
if "%choice%"=="11" goto SHOW_STATS
if "%choice%"=="12" goto EXPORT_DATA
if "%choice%"=="13" goto CHECK_INTEGRITY
if "%choice%"=="14" goto AUTO_SETUP
if "%choice%"=="15" goto RUN_TESTS
if "%choice%"=="16" goto EXIT
echo Invalid choice! Please select 1-16.
goto MENU

:GUI_LAUNCHER
echo.
echo Starting GUI Launcher...
echo ========================
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" launcher.py
) else (
    echo Virtual environment not found. Using system Python...
    python launcher.py
)
goto MENU

:WEB_SERVER
echo.
echo Starting Web Server...
echo ======================
echo Server will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" app.py
) else (
    echo Virtual environment not found. Using system Python...
    python app.py
)
goto MENU

:OPEN_BROWSER
echo.
echo Opening Web Interface...
echo ========================
start http://127.0.0.1:5000
echo Web interface opened in your default browser.
echo If the page doesn't load, make sure the server is running (option 2).
pause
goto MENU

:CONSOLE_LAUNCHER
echo.
echo Starting Console Launcher...
echo ===========================
echo Alternative launcher for systems with Tkinter/GUI issues.
echo.
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" console_launcher.py
) else (
    echo Virtual environment not found. Using system Python...
    python console_launcher.py
)
goto MENU

:FACEBOOK_HELP
echo.
echo ╔═══════════════════════════════════════════════════════════════════════════════╗
echo ║                        FACEBOOK DATA DOWNLOAD GUIDE                          ║
echo ╚═══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 📥 STEP-BY-STEP GUIDE TO GET YOUR FACEBOOK FRIENDS DATA:
echo.
echo 1️⃣  GO TO FACEBOOK SETTINGS
echo    • Open Facebook.com and log in
echo    • Click the dropdown arrow (top right)
echo    • Select "Settings & Privacy" → "Settings"
echo.
echo 2️⃣  ACCESS YOUR INFORMATION
echo    • In the left sidebar, click "Your Facebook Information"
echo    • Click "Download Your Information"
echo.
echo 3️⃣  CONFIGURE DOWNLOAD SETTINGS
echo    • Date Range: Choose "All time" or your preferred period
echo    • Format: Select "JSON" (IMPORTANT!)
echo    • Media Quality: Choose "Low" to reduce file size
echo.
echo 4️⃣  SELECT DATA TO INCLUDE
echo    • UNCHECK ALL items first
echo    • CHECK ONLY: "Friends and Followers"
echo    • This reduces download size significantly
echo.
echo 5️⃣  CREATE DOWNLOAD
echo    • Click "Create File"
echo    • Facebook will prepare your data (may take hours/days)
echo    • You'll get an email when notified
echo.
echo 6️⃣  DOWNLOAD AND EXTRACT
echo    • Download the ZIP file when notified
echo    • Extract it to a folder
echo    • Look for: friends/your_friends.json
echo.
echo 7️⃣  UPLOAD TO TRACKER
echo    • Use this launcher (option 1 or 2)
echo    • Upload the your_friends.json file
echo    • Start tracking!
echo.
echo 🔄 FREQUENCY RECOMMENDATIONS:
echo    • Download data monthly for regular tracking
echo    • Compare with previous downloads
echo    • Keep old files for historical analysis
echo.
echo ⚠️  IMPORTANT NOTES:
echo    • Only YOUR friends data is included (privacy compliant)
echo    • Data reflects friends at time of download
echo    • No automatic/real-time collection possible
echo    • This is the ONLY legitimate method
echo.
echo 💡 WHY NO AUTOMATIC COLLECTION?
echo    • Facebook API restrictions (privacy protection)
echo    • Legal compliance (GDPR, CCPA)
echo    • Terms of Service protection
echo    • Anti-scraping measures
echo.
echo 🚀 ONCE YOU HAVE THE DATA:
echo    • Upload via web interface
echo    • View in spreadsheet format
echo    • Export to CSV for analysis
echo    • Compare multiple downloads over time
echo.
pause
goto MENU

:PROJECT_INFO
echo.
echo ╔═══════════════════════════════════════════════════════════════════════════════╗
echo ║                           PROJECT INFORMATION & GUIDE                        ║
echo ╚═══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 📋 PROJECT DETAILS:
echo ==================
echo Name: Facebook Unfriend Tracker - Compact Edition
echo Version: 2.0 Compact
echo Type: Web Application with GUI Launcher
echo Purpose: Track changes in your Facebook friends list over time
echo.
echo 🚀 FEATURES:
echo ============
echo ✅ Clean web interface with Bootstrap styling
echo ✅ 400x400 GUI launcher with start/stop controls
echo ✅ Spreadsheet view for friends data analysis
echo ✅ CSV export functionality for data analysis
echo ✅ SQLite database for secure local storage
echo ✅ Facebook JSON data processing and comparison
echo ✅ Historical tracking of friend list changes
echo ✅ Identify who unfriended you between downloads
echo.
echo 📁 PROJECT FILES:
echo =================
echo • launcher.py: GUI application (Tkinter-based)
echo • app.py: Flask web server (main application)
echo • templates/: Web interface HTML files
echo • uploads/: Facebook data storage directory
echo • data/: CSV export and database folder
echo • requirements.txt: Python dependencies
echo • run_launcher.bat: This all-in-one launcher
echo.
echo 🔧 SYSTEM REQUIREMENTS:
echo =======================
echo • Windows 7/8/10/11 (PowerShell support)
echo • Python 3.7+ (with pip package manager)
echo • Flask 2.3+ web framework
echo • Modern web browser (Chrome, Firefox, Edge)
echo • 50MB free disk space
echo • Internet connection (for initial setup only)
echo.
echo 📥 HOW TO GET FACEBOOK FRIENDS DATA:
echo ====================================
echo ⚠️  IMPORTANT: There is NO automatic way to get this data!
echo.
echo 🔹 STEP 1: Go to Facebook Settings
echo    • Login to Facebook.com
echo    • Click profile dropdown (top right)
echo    • Select "Settings & Privacy" → "Settings"
echo.
echo 🔹 STEP 2: Download Your Information
echo    • Left sidebar: "Your Facebook Information"
echo    • Click "Download Your Information"
echo.
echo 🔹 STEP 3: Configure Download (IMPORTANT!)
echo    • Date Range: Select "All time" or preferred period
echo    • Format: Choose "JSON" (NOT HTML!)
echo    • Media Quality: Select "Low" (faster download)
echo.
echo 🔹 STEP 4: Select ONLY Friends Data
echo    • UNCHECK all items first
echo    • CHECK ONLY: "Friends and Followers"
echo    • This keeps file size manageable
echo.
echo 🔹 STEP 5: Create and Wait
echo    • Click "Create File"
echo    • Facebook prepares data (can take hours/days)
echo    • You'll receive email notification when ready
echo.
echo 🔹 STEP 6: Download and Extract
echo    • Download the ZIP file
echo    • Extract to a folder
echo    • Find: friends_and_followers/friends.json
echo.
echo 📊 HOW TO USE THIS PROJECT:
echo ===========================
echo 1️⃣  FIRST TIME SETUP:
echo    • Run this launcher (option 6) to install dependencies
echo    • Download your Facebook data as described above
echo.
echo 2️⃣  START THE APPLICATION:
echo    • Option 1: GUI launcher (recommended for beginners)
echo    • Option 2: Web server only (for advanced users)
echo.
echo 3️⃣  UPLOAD YOUR DATA:
echo    • Open web interface (automatically opens with option 1)
echo    • Click "Upload Facebook Data"
echo    • Select your friends.json file
echo.
echo 4️⃣  VIEW RESULTS:
echo    • Browse friends list in spreadsheet format
echo    • Export to CSV for Excel analysis
echo    • Upload new data periodically to track changes
echo.
echo 5️⃣  TRACK CHANGES OVER TIME:
echo    • Download Facebook data monthly
echo    • Upload each new dataset
echo    • Compare results to see who unfriended you
echo.
echo 🚫 WHY NO AUTOMATION IS POSSIBLE:
echo =================================
echo 🔒 FACEBOOK API LIMITATIONS:
echo    • Friends list API removed in 2014 for privacy
echo    • Only basic public profile data available
echo    • No programmatic access to friends lists
echo.
echo ⚖️  LEGAL RESTRICTIONS:
echo    • GDPR (Europe): Requires explicit user consent
echo    • CCPA (California): Strict privacy regulations
echo    • Facebook Terms of Service prohibit scraping
echo    • Computer Fraud and Abuse Act (CFAA) violations
echo.
echo 🛡️  TECHNICAL BARRIERS:
echo    • Anti-scraping: Rate limits, IP blocking, CAPTCHA
echo    • Dynamic content: JavaScript-heavy, encrypted data
echo    • 2FA requirements: Additional security layers
echo    • Constantly changing: HTML structure updates frequently
echo.
echo 💀 RISKS OF "AUTOMATIC" TOOLS:
echo    • Account suspension or permanent ban
echo    • Credential theft and security breaches
echo    • Legal liability for ToS violations
echo    • Malware and data compromise
echo.
echo 💡 WHY OUR APPROACH IS BETTER:
echo ==============================
echo ✅ 100%% Legal and compliant with Facebook ToS
echo ✅ No risk of account suspension
echo ✅ Uses official Facebook data export feature
echo ✅ Your data stays on your computer (privacy)
echo ✅ No credentials required by our application
echo ✅ Works reliably without breaking
echo.
echo 🔄 RECOMMENDED USAGE PATTERN:
echo =============================
echo • Download Facebook data monthly
echo • Keep previous downloads for comparison
echo • Upload new data to track changes
echo • Export CSV reports for detailed analysis
echo • Share results with friends (optional)
echo.
echo 📞 TROUBLESHOOTING:
echo ==================
echo • If GUI won't start: Try option 2 (web server only)
echo • If browser won't open: Manually go to http://127.0.0.1:5000
echo • If upload fails: Ensure you selected the correct JSON file
echo • If no data shows: Check that friends.json contains friend data
echo.
echo 🎯 NEXT STEPS:
echo =============
echo 1. Press any key to return to main menu
echo 2. Use option 6 to install dependencies (if first time)
echo 3. Download your Facebook data following the guide above
echo 4. Use option 1 to start the application
echo 5. Upload your data and start tracking!
echo.
pause
goto MENU

:BUILD_EXE
echo.
echo Building Executable...
echo ======================
echo Installing PyInstaller...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m pip install pyinstaller pillow
) else (
    python -m pip install pyinstaller pillow
)
echo.
echo Building executable with icon...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\pyinstaller.exe" --onefile --windowed --icon=icon.ico --name="FacebookUnfriendTracker" launcher.py
) else (
    pyinstaller --onefile --windowed --icon=icon.ico --name="FacebookUnfriendTracker" launcher.py
)
echo.
echo Copying required files to dist folder...
if not exist "dist\templates" mkdir "dist\templates"
if not exist "dist\data" mkdir "dist\data"
if not exist "dist\uploads" mkdir "dist\uploads"
copy app.py dist\ >nul 2>&1
copy console_launcher.py dist\ >nul 2>&1
copy requirements.txt dist\ >nul 2>&1
copy README.md dist\ >nul 2>&1
copy icon.ico dist\ >nul 2>&1
copy run_launcher.bat dist\ >nul 2>&1
xcopy templates dist\templates\ /E /Y >nul 2>&1
if exist uploads xcopy uploads dist\uploads\ /E /Y >nul 2>&1
if exist data xcopy data dist\data\ /E /Y >nul 2>&1
if exist friends_tracker.db copy friends_tracker.db dist\ >nul 2>&1
echo.
echo ✅ Build complete! 
echo 📁 Check the 'dist' folder for FacebookUnfriendTracker.exe
echo 🚀 You can now distribute the entire 'dist' folder as a standalone application
pause
goto MENU

:INSTALL_DEPS
echo.
echo Installing Dependencies...
echo =========================
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)
echo Activating virtual environment and installing packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
echo.
echo ✅ Dependencies installed successfully!
echo Virtual environment created at: .venv\
pause
goto MENU

:CLEAN_PROJECT
echo.
echo Cleaning Project Files...
echo ========================
echo Removing temporary files, cache, and build artifacts...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"
if exist ".mypy_cache" rmdir /s /q ".mypy_cache"
if exist "*.pyc" del /q "*.pyc"
if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
if exist "*.log" del /q "*.log"
echo Using utility script for advanced cleanup...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" utils.py cleanup
) else (
    python utils.py cleanup
)
echo.
echo ✅ Project cleaned successfully!
echo 🗑️  Removed: Cache files, build artifacts, temporary files
echo 📁 Kept: Source code, database, templates, user data
pause
goto MENU

:BACKUP_DATA
echo.
echo Creating Backup...
echo ==================
echo Creating backup of database and data files...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" utils.py backup
) else (
    python utils.py backup
)
echo.
pause
goto MENU

:SHOW_STATS
echo.
echo Database Statistics...
echo =====================
echo Showing comprehensive database statistics...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" utils.py stats
) else (
    python utils.py stats
)
echo.
pause
goto MENU

:EXPORT_DATA
echo.
echo Exporting All Data...
echo ====================
echo Exporting all data to CSV files...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" utils.py export
) else (
    python utils.py export
)
echo.
pause
goto MENU

:CHECK_INTEGRITY
echo.
echo Checking Database Integrity...
echo =============================
echo Verifying database consistency and integrity...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" utils.py integrity
) else (
    python utils.py integrity
)
echo.
pause
goto MENU

:AUTO_SETUP
echo.
echo Automated Setup...
echo ==================
echo Running complete automated setup process...
echo This will create virtual environment, install dependencies, and initialize database.
echo.
python setup.py
echo.
pause
goto MENU

:RUN_TESTS
echo.
echo Running Test Suite...
echo ====================
echo Running comprehensive tests to verify installation...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" test_suite.py
) else (
    python test_suite.py
)
echo.
pause
goto MENU

:EXIT
echo.
echo Thank you for using Facebook Unfriend Tracker!
echo ==============================================
echo 👋 Goodbye!
timeout 2 >nul
exit

:ERROR
echo.
echo ❌ An error occurred. Please check the above messages.
pause
goto MENU
