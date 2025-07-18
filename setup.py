#!/usr/bin/env python3
"""
Facebook Unfriend Tracker - Setup and Installation Script
Automates the complete setup process for the application
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class FacebookTrackerSetup:
    def __init__(self):
        self.python_executable = sys.executable
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / '.venv'
        self.requirements_file = self.project_dir / 'requirements.txt'
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print("❌ Python 3.7 or higher is required")
            print(f"Current version: {version.major}.{version.minor}.{version.micro}")
            return False
        
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    
    def check_system_requirements(self):
        """Check system requirements and dependencies"""
        print("\n🔍 Checking System Requirements...")
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Check pip
        try:
            import pip
            print("✅ pip is available")
        except ImportError:
            print("❌ pip is not available")
            return False
        
        # Check tkinter (for GUI)
        try:
            import tkinter
            print("✅ tkinter is available (GUI will work)")
        except ImportError:
            print("⚠️  tkinter is not available (GUI may not work, console mode available)")
        
        # Check operating system
        os_name = platform.system()
        print(f"✅ Operating System: {os_name}")
        
        return True
    
    def create_virtual_environment(self):
        """Create a virtual environment"""
        print("\n📦 Creating Virtual Environment...")
        
        if self.venv_dir.exists():
            print("⚠️  Virtual environment already exists")
            return True
        
        try:
            subprocess.run([
                self.python_executable, '-m', 'venv', str(self.venv_dir)
            ], check=True)
            print("✅ Virtual environment created")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    def get_venv_python(self):
        """Get the Python executable from virtual environment"""
        if platform.system() == 'Windows':
            return self.venv_dir / 'Scripts' / 'python.exe'
        else:
            return self.venv_dir / 'bin' / 'python'
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("\n📥 Installing Dependencies...")
        
        venv_python = self.get_venv_python()
        
        if not venv_python.exists():
            print("❌ Virtual environment Python not found")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([
                str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'
            ], check=True)
            
            # Install requirements
            subprocess.run([
                str(venv_python), '-m', 'pip', 'install', '-r', str(self.requirements_file)
            ], check=True)
            
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_directories(self):
        """Create necessary directories"""
        print("\n📁 Creating Directories...")
        
        directories = ['uploads', 'data', 'backups', 'templates']
        
        for directory in directories:
            dir_path = self.project_dir / directory
            dir_path.mkdir(exist_ok=True)
            print(f"✅ Directory created/verified: {directory}")
    
    def initialize_database(self):
        """Initialize the application database"""
        print("\n💾 Initializing Database...")
        
        venv_python = self.get_venv_python()
        
        try:
            # Import and initialize database
            result = subprocess.run([
                str(venv_python), '-c', 
                'from app import init_db; init_db(); print("Database initialized")'
            ], capture_output=True, text=True, cwd=str(self.project_dir))
            
            if result.returncode == 0:
                print("✅ Database initialized successfully")
                return True
            else:
                print(f"❌ Database initialization failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            return False
    
    def create_sample_data(self):
        """Create sample data for testing"""
        print("\n📋 Creating Sample Data...")
        
        sample_data = {
            "friends": [
                {"name": "Sample Friend 1", "timestamp": 1640995200},
                {"name": "Sample Friend 2", "timestamp": 1640995300},
                {"name": "Sample Friend 3", "timestamp": 1640995400}
            ]
        }
        
        uploads_dir = self.project_dir / 'uploads'
        sample_file = uploads_dir / 'sample_friends.json'
        
        with open(sample_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"✅ Sample data created: {sample_file}")
    
    def test_installation(self):
        """Test the installation"""
        print("\n🧪 Testing Installation...")
        
        venv_python = self.get_venv_python()
        
        try:
            # Test imports
            result = subprocess.run([
                str(venv_python), '-c', 
                'import flask, app; print("All imports successful")'
            ], capture_output=True, text=True, cwd=str(self.project_dir))
            
            if result.returncode == 0:
                print("✅ Installation test passed")
                return True
            else:
                print(f"❌ Installation test failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Installation test error: {e}")
            return False
    
    def show_next_steps(self):
        """Show next steps to the user"""
        print("\n🎉 Setup Complete!")
        print("=" * 50)
        print("Next steps:")
        print("1. Run the launcher: run_launcher.bat")
        print("2. Choose option 1 for GUI or option 2 for web server")
        print("3. Download your Facebook data following the guide (option 5)")
        print("4. Upload your Facebook data through the web interface")
        print("\nQuick start:")
        print("• Windows: Double-click run_launcher.bat")
        print("• Command line: run_launcher.bat")
        print("\nFor help:")
        print("• Option 5: Facebook data download guide")
        print("• Option 6: Complete project information")
        print("\nSample data for testing:")
        print("• uploads/sample_friends.json")
        print("\n🚀 Happy tracking!")
    
    def setup(self):
        """Run the complete setup process"""
        print("🚀 Facebook Unfriend Tracker - Setup")
        print("=" * 40)
        
        steps = [
            ("Checking system requirements", self.check_system_requirements),
            ("Creating virtual environment", self.create_virtual_environment),
            ("Installing dependencies", self.install_dependencies),
            ("Creating directories", self.create_directories),
            ("Initializing database", self.initialize_database),
            ("Creating sample data", self.create_sample_data),
            ("Testing installation", self.test_installation)
        ]
        
        for step_name, step_func in steps:
            print(f"\n⏳ {step_name}...")
            if not step_func():
                print(f"\n❌ Setup failed at: {step_name}")
                return False
        
        self.show_next_steps()
        return True

def main():
    """Main setup function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Facebook Unfriend Tracker Setup Script")
        print("Usage: python setup.py")
        print("\nThis script will:")
        print("• Check system requirements")
        print("• Create virtual environment")
        print("• Install dependencies")
        print("• Initialize database")
        print("• Create sample data")
        print("• Test installation")
        return
    
    setup = FacebookTrackerSetup()
    success = setup.setup()
    
    if not success:
        print("\n💡 Troubleshooting tips:")
        print("• Ensure Python 3.7+ is installed")
        print("• Check internet connection for package downloads")
        print("• Run as administrator if permission errors occur")
        print("• Try manual installation: run_launcher.bat -> option 8")
        sys.exit(1)

if __name__ == '__main__':
    main()
