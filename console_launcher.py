#!/usr/bin/env python3
"""
Facebook Unfriend Tracker - Simple Console Launcher
Alternative launcher for systems without working Tkinter/GUI support
"""

import subprocess
import time
import os
import webbrowser
import threading
from datetime import datetime

class ConsoleTrackerLauncher:
    def __init__(self):
        self.flask_process = None
        self.server_running = False
        self.start_time = None
        
    def print_header(self):
        print("\n" + "="*60)
        print("     FACEBOOK UNFRIEND TRACKER - CONSOLE LAUNCHER")
        print("="*60)
        print("Web-based unfriend tracking with console controls")
        print("="*60)
    
    def show_menu(self):
        print("\nOptions:")
        print("[1] Start Web Server")
        print("[2] Open Web Interface (http://127.0.0.1:5000)")
        print("[3] Stop Server")
        print("[4] Server Status")
        print("[5] Exit")
        return input("\nSelect option (1-5): ").strip()
    
    def start_server(self):
        if self.server_running:
            print("Server is already running!")
            return
            
        try:
            app_dir = os.path.dirname(os.path.abspath(__file__))
            python_exe = os.path.join(app_dir, ".venv", "Scripts", "python.exe")
            if not os.path.exists(python_exe):
                python_exe = "python"
            
            app_file = os.path.join(app_dir, "app.py")
            
            print("Starting Flask server...")
            self.flask_process = subprocess.Popen(
                [python_exe, app_file],
                cwd=app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            time.sleep(3)  # Wait for server to start
            
            self.server_running = True
            self.start_time = datetime.now()
            
            print("✅ Server started successfully!")
            print("🌐 Web interface: http://127.0.0.1:5000")
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
    
    def stop_server(self):
        if not self.server_running:
            print("Server is not running!")
            return
            
        try:
            if self.flask_process:
                self.flask_process.terminate()
                time.sleep(1)
                if self.flask_process.poll() is None:
                    self.flask_process.kill()
            
            self.server_running = False
            self.start_time = None
            print("⏹️ Server stopped successfully!")
            
        except Exception as e:
            print(f"❌ Error stopping server: {e}")
    
    def open_browser(self):
        if self.server_running:
            webbrowser.open("http://127.0.0.1:5000")
            print("🌐 Opened web interface in browser")
        else:
            print("❌ Server is not running! Start the server first (option 1)")
    
    def show_status(self):
        if self.server_running:
            uptime = datetime.now() - self.start_time if self.start_time else None
            if uptime:
                hours, remainder = divmod(uptime.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                uptime_str = "Unknown"
                
            print(f"✅ Server Status: Running")
            print(f"⏱️  Uptime: {uptime_str}")
            print(f"🌐 URL: http://127.0.0.1:5000")
        else:
            print("⏹️ Server Status: Stopped")
    
    def run(self):
        self.print_header()
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == "1":
                    self.start_server()
                elif choice == "2":
                    self.open_browser()
                elif choice == "3":
                    self.stop_server()
                elif choice == "4":
                    self.show_status()
                elif choice == "5":
                    if self.server_running:
                        print("Stopping server before exit...")
                        self.stop_server()
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice! Please select 1-5.")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Interrupted by user")
                if self.server_running:
                    print("Stopping server...")
                    self.stop_server()
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    launcher = ConsoleTrackerLauncher()
    launcher.run()
