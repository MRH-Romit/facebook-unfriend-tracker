# 📱 Facebook Unfriend Tracker - Compact Edition

> **Track changes in your Facebook friends list over time with this privacy-focused, locally-hosted web application.**

## 🌟 Overview

The Facebook Unfriend Tracker is a **privacy-first** tool that helps you monitor changes in your Facebook friends list. Unlike automated scraping tools that violate Facebook's Terms of Service, this application uses Facebook's official "Download Your Information" feature to track friend changes legitimately and safely.

## ✨ Key Features

- 🌐 **Clean Web Interface** - Modern, responsive design with Bootstrap
- 🖥️ **Multiple Launch Options** - GUI launcher, web server, or console mode
- 📊 **Spreadsheet View** - View friends data in an organized table format
- 📈 **CSV Export** - Export data for analysis in Excel or other tools
- 💾 **Local Storage** - All data stays on your computer (SQLite database)
- 🔒 **Privacy Focused** - No credentials required, uses official Facebook data
- 📅 **Historical Tracking** - Compare multiple downloads to see changes over time
- 🚫 **100% Legal** - Complies with Facebook ToS, GDPR, and privacy laws

## 🚨 Important: Why No Automation?

**This tool does NOT automatically collect Facebook data.** Here's why:

### 🔒 **Technical Limitations**
- Facebook removed friends list access from their API in 2014
- Anti-scraping measures: Rate limits, IP blocking, CAPTCHA
- Dynamic, JavaScript-heavy pages that change frequently

### ⚖️ **Legal Requirements**
- **Facebook Terms of Service** prohibit automated data collection
- **GDPR** (Europe) requires explicit consent for data processing
- **CCPA** (California) has strict privacy regulations
- **Computer Fraud and Abuse Act** makes unauthorized access illegal

### 💀 **Risks of "Automatic" Tools**
- Account suspension or permanent ban
- Security breaches and credential theft
- Legal liability for ToS violations
- Malware and data compromise

## 📥 How to Get Facebook Friends Data

### Step-by-Step Guide

1. **Go to Facebook Settings**
   - Login to Facebook.com
   - Click your profile picture (top right)
   - Select "Settings & Privacy" → "Settings"

2. **Access Download Your Information**
   - In the left sidebar, click "Your Facebook Information"
   - Click "Download Your Information"

3. **Configure Download Settings** ⚠️ **IMPORTANT**
   - **Date Range**: Select "All time" or your preferred period
   - **Format**: Choose "JSON" (NOT HTML!)
   - **Media Quality**: Select "Low" (faster download, smaller file)

4. **Select ONLY Friends Data**
   - **UNCHECK ALL** items first
   - **CHECK ONLY**: "Friends and Followers"
   - This keeps the file size manageable

5. **Create and Wait**
   - Click "Create File"
   - Facebook will prepare your data (can take hours or days)
   - You'll receive an email notification when ready

6. **Download and Extract**
   - Download the ZIP file when notified
   - Extract it to a folder on your computer
   - Look for: `friends_and_followers/friends.json`

## 🚀 Installation & Setup

### Prerequisites
- **Windows 7/8/10/11** with PowerShell
- **Python 3.7+** (Download from [python.org](https://www.python.org/downloads/))
- **Modern web browser** (Chrome, Firefox, Edge)
- **50MB free disk space**

### Quick Start

1. **Download this project** to a folder on your computer

2. **Run the launcher**
   ```cmd
   # Double-click or run in command prompt:
   run_launcher.bat
   ```

3. **Install dependencies** (first time only)
   - Choose option `8` from the menu
   - This creates a virtual environment and installs required packages

4. **Download your Facebook data** (follow the guide above)

5. **Start the application**
   - Choose option `1` (GUI launcher) or option `2` (web server only)
   - Your web browser will open automatically

6. **Upload your data**
   - Click "Upload Facebook Data" in the web interface
   - Select your `friends.json` file
   - View your friends list in the application

## 🎮 How to Use

### First Time Setup
```bash
1. Run run_launcher.bat
2. Choose option 8: Install Dependencies
3. Download Facebook data following the guide above
4. Choose option 1: Launch GUI Application
5. Upload your friends.json file
```

### Regular Usage
```bash
1. Download new Facebook data monthly
2. Run run_launcher.bat
3. Choose option 1 or 2 to start the application
4. Upload new data to compare with previous uploads
5. Export CSV reports for detailed analysis
```

### Launcher Options

| Option | Description |
|--------|-------------|
| 1 | 🚀 **Launch GUI Application** (Recommended for beginners) |
| 2 | 🌐 **Start Web Server Only** (For advanced users) |
| 3 | 📊 **Open Web Interface** (If server is already running) |
| 4 | 🖥️ **Console Launcher** (Alternative for Tkinter issues) |
| 5 | 📥 **Facebook Data Helper Guide** (Step-by-step instructions) |
| 6 | 📋 **View Project Info & README** (Comprehensive documentation) |
| 7 | 🔧 **Build Executable** (Create standalone .exe file) |
| 8 | 📦 **Install Dependencies** (Set up Python environment) |
| 9 | 🧹 **Clean Project Files** (Remove temporary files) |
| 10 | ❌ **Exit** |

## 🔧 Advanced Usage

### Building a Standalone Executable
```bash
1. Run run_launcher.bat
2. Choose option 7: Build Executable
3. Find FacebookUnfriendTracker.exe in the dist/ folder
4. Share the entire dist/ folder with others
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| GUI won't start | Try option 2 (web server only) or option 4 (console launcher) |
| Browser won't open | Manually go to http://127.0.0.1:5000 |
| Upload fails | Ensure you selected the correct `friends.json` file |
| No data shows | Check that the JSON file contains friends data |
| Python not found | Install Python from python.org and restart |
| Permission errors | Run as Administrator or check antivirus software |

## 📁 Project Structure

```
📦 Facebook Unfriend Tracker
├── 🚀 run_launcher.bat         # Main launcher (START HERE)
├── 🌐 app.py                   # Flask web server
├── 🖥️ launcher.py              # GUI application
├── 🖥️ console_launcher.py      # Console alternative
├── 📋 README.md                # This file
├── 📦 requirements.txt         # Python dependencies
├── 🎨 icon.ico                 # Application icon
├── 🙈 .gitignore              # Protects your personal data
├── 📁 templates/               # Web interface files
├── 📁 uploads/                 # Your Facebook data (ignored by git)
├── 📁 data/                    # CSV exports (ignored by git)
└── 💾 friends_tracker.db       # Local database (ignored by git)
```

## 🔒 Privacy & Security

### What Data is Collected?
- **NONE** - This application doesn't collect any data from you
- All processing happens locally on your computer
- No internet connection required after initial setup

### What Data is Stored?
- Only the Facebook friends data YOU upload
- Data is stored locally in SQLite database
- No cloud storage, no external servers

### Data Protection
- `.gitignore` protects your personal data from being committed to git
- Database files are excluded from version control
- Upload folders are automatically ignored

## 🔄 Recommended Workflow

1. **Monthly Data Collection**
   - Download Facebook data once per month
   - Keep previous downloads for comparison
   - Store files in organized folders by date

2. **Regular Tracking**
   - Upload new data when available
   - Compare with previous uploads
   - Export CSV reports for detailed analysis

3. **Data Management**
   - Keep backups of your Facebook data downloads
   - Export CSV files for long-term storage
   - Clean up old temporary files regularly

## 📊 Understanding the Results

### Friends List View
- See all your friends in a clean table format
- Sortable by name, date added, etc.
- Search and filter functionality

### Change Detection
- Upload multiple datasets to see changes
- Identify who unfriended you between downloads
- Track new friend additions over time

### CSV Exports
- Detailed spreadsheet with all friend data
- Timestamps for tracking purposes
- Compatible with Excel, Google Sheets, etc.

## 🤝 Contributing

This is a privacy-focused project. If you want to contribute:

1. **Never commit personal data** - Check `.gitignore` is working
2. **Test with sample data** - Don't use real Facebook data for testing
3. **Respect privacy laws** - Ensure all features comply with GDPR/CCPA
4. **No automation** - Don't add features that violate Facebook ToS

## ⚠️ Disclaimer

- This tool uses Facebook's official data export feature
- You are responsible for complying with your local privacy laws
- Only upload data that belongs to you
- This project is not affiliated with Facebook/Meta
- Use at your own discretion and responsibility

## 📞 Support

Having issues? Try these steps:

1. **Check the built-in guide**: Run `run_launcher.bat` → Option 5
2. **View project info**: Run `run_launcher.bat` → Option 6
3. **Try console mode**: Run `run_launcher.bat` → Option 4
4. **Clean and reinstall**: Run `run_launcher.bat` → Option 9, then Option 8

---

**🎯 Quick Start**: Download Facebook data → Run `run_launcher.bat` → Option 8 → Option 1 → Upload data → Start tracking!

**🔒 Remember**: Your privacy is protected - all data stays on your computer, no automation means no ToS violations, and you're in complete control of your data.
