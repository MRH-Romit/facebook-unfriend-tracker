import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import os
import webbrowser
from datetime import datetime
import sys

class FacebookTrackerLauncher:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("Facebook Unfriend Tracker")
            self.root.geometry("400x400")
            self.root.resizable(False, False)
            
            # Try to set icon
            try:
                self.root.iconbitmap("icon.ico")
            except:
                pass
            
            self.flask_process = None
            self.server_running = False
            self.start_time = None
            self.setup_ui()
            
        except Exception as e:
            print(f"Error initializing GUI: {e}")
            print("Tkinter/Tcl is not properly installed or configured.")
            print("Running in fallback mode - starting web server directly...")
            self.fallback_mode()
    
    def fallback_mode(self):
        """Fallback mode when GUI can't be initialized"""
        print("\n" + "="*50)
        print("GUI LAUNCHER - FALLBACK MODE")
        print("="*50)
        print("Starting web server directly...")
        
        try:
            app_dir = os.path.dirname(os.path.abspath(__file__))
            python_exe = os.path.join(app_dir, ".venv", "Scripts", "python.exe")
            if not os.path.exists(python_exe):
                python_exe = "python"
            
            app_file = os.path.join(app_dir, "app.py")
            print(f"Using Python: {python_exe}")
            print(f"Running: {app_file}")
            print("Web server will be available at: http://127.0.0.1:5000")
            print("\nPress Ctrl+C to stop the server")
            print("-" * 50)
            
            # Start Flask app directly
            subprocess.run([python_exe, app_file], cwd=app_dir)
            
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        except Exception as e:
            print(f"Error starting server: {e}")
            input("Press Enter to exit...")
        
        sys.exit(0)
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(main_frame, text="📱 Facebook Unfriend Tracker", 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Server Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Server: Stopped", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.time_label = ttk.Label(status_frame, text="Uptime: --:--:--", font=("Arial", 10))
        self.time_label.grid(row=1, column=0, sticky=tk.W)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="🚀 Start Server", 
                                   command=self.start_server, width=15)
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ Stop Server", 
                                  command=self.stop_server, width=15, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1)
        
        # Web interface
        web_frame = ttk.LabelFrame(main_frame, text="Web Interface", padding="10")
        web_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.url_label = ttk.Label(web_frame, text="http://127.0.0.1:5000", 
                                  font=("Arial", 12, "underline"), 
                                  foreground="blue", cursor="hand2")
        self.url_label.grid(row=0, column=0)
        self.url_label.bind("<Button-1>", self.open_browser)
        
        self.browser_btn = ttk.Button(web_frame, text="🌐 Open Browser", 
                                     command=self.open_browser, state=tk.DISABLED)
        self.browser_btn.grid(row=1, column=0, pady=(10, 0))
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=45, font=("Consolas", 9), state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.update_timer()
        self.log_message("Facebook Unfriend Tracker ready")
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def start_server(self):
        if not self.server_running:
            try:
                app_dir = os.path.dirname(os.path.abspath(__file__))
                python_exe = os.path.join(app_dir, ".venv", "Scripts", "python.exe")
                if not os.path.exists(python_exe):
                    python_exe = "python"
                
                app_file = os.path.join(app_dir, "app.py")
                
                self.flask_process = subprocess.Popen(
                    [python_exe, app_file],
                    cwd=app_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                
                time.sleep(2)
                
                self.server_running = True
                self.start_time = datetime.now()
                
                self.status_label.config(text="Server: Running ✅")
                self.start_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.browser_btn.config(state=tk.NORMAL)
                
                self.log_message("Server started successfully")
                
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to start server: {str(e)}")
    
    def stop_server(self):
        if self.server_running:
            try:
                if self.flask_process:
                    self.flask_process.terminate()
                    time.sleep(1)
                    if self.flask_process.poll() is None:
                        self.flask_process.kill()
                
                self.server_running = False
                self.start_time = None
                
                self.status_label.config(text="Server: Stopped ⏹️")
                self.time_label.config(text="Uptime: --:--:--")
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.browser_btn.config(state=tk.DISABLED)
                
                self.log_message("Server stopped")
                
            except Exception as e:
                self.log_message(f"Error stopping: {str(e)}")
    
    def open_browser(self, event=None):
        if self.server_running:
            webbrowser.open("http://127.0.0.1:5000")
            self.log_message("Opened in browser")
        else:
            messagebox.showwarning("Server Not Running", "Please start the server first")
    
    def update_timer(self):
        if self.server_running and self.start_time:
            uptime = datetime.now() - self.start_time
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=uptime_str)
        
        self.root.after(1000, self.update_timer)
    
    def on_closing(self):
        if self.server_running:
            if messagebox.askokcancel("Quit", "Server is running. Stop and quit?"):
                self.stop_server()
                time.sleep(1)
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    launcher = FacebookTrackerLauncher()
    launcher.run()
