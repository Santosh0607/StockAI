"""
StockAI Application Runner
Starts both authentication system and main dashboard
"""

import os
import sys
import time
import subprocess
import webbrowser
from threading import Timer
import psutil

def check_port(port):
    """Check if a port is already in use"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False

def kill_port(port):
    """Kill process using a specific port"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    proc.kill()
                    print(f"✅ Killed process on port {port}")
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def open_auth_page():
    """Open authentication page in browser"""
    time.sleep(2)
    webbrowser.open_new("http://127.0.0.1:8060/")

def open_main_page():
    """Open main dashboard in browser"""
    time.sleep(4)
    webbrowser.open_new("http://127.0.0.1:8050/")

def main():
    print("🚀 StockAI - NEPSE Market Prediction Platform")
    print("=" * 60)
    print("🎯 Initializing secure authentication and AI dashboard...")
    print()
    
    # Check if ports are available
    auth_port = 8060
    main_port = 8050
    
    if check_port(auth_port):
        print(f"⚠️  Port {auth_port} is already in use")
        response = input(f"Kill process on port {auth_port}? (y/n): ")
        if response.lower() == 'y':
            kill_port(auth_port)
        else:
            print("❌ Cannot start authentication system")
            return
    
    if check_port(main_port):
        print(f"⚠️  Port {main_port} is already in use")
        response = input(f"Kill process on port {main_port}? (y/n): ")
        if response.lower() == 'y':
            kill_port(main_port)
        else:
            print("❌ Cannot start main dashboard")
            return
    
    try:
        # Start authentication system
        print("🔐 Starting Authentication System...")
        auth_process = subprocess.Popen([
            sys.executable, "auth_app.py"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # Wait a bit for auth to start
        time.sleep(3)
        
        # Start main dashboard
        print("📊 Starting Main Dashboard...")
        main_process = subprocess.Popen([
            sys.executable, "app.py"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # Open browsers
        Timer(2, open_auth_page).start()
        Timer(5, open_main_page).start()
        
        print()
        print("🎉 StockAI is now running!")
        print("=" * 60)
        print("📋 Application URLs:")
        print(f"🔑 Authentication: http://127.0.0.1:{auth_port}")
        print(f"📈 Main Dashboard: http://127.0.0.1:{main_port}")
        print()
        print("📖 How to use:")
        print("1. First, login or create account at the authentication page")
        print("2. After successful login, access the main dashboard")
        print("3. Upload your NEPSE stock data (Excel format)")
        print("4. Configure model parameters and train AI model")
        print("5. View predictions and technical analysis")
        print()
        print("🔒 Security Features:")
        print("- SQLite database with encrypted passwords")
        print("- Secure session management")
        print("- PBKDF2-SHA256 password hashing")
        print("- CSRF protection")
        print()
        print("⚠️  Press Ctrl+C to stop both applications")
        print("=" * 60)
        
        # Wait for processes
        try:
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                if auth_process.poll() is not None:
                    print("❌ Authentication system stopped")
                    break
                if main_process.poll() is not None:
                    print("❌ Main dashboard stopped")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down StockAI...")
            
            # Terminate processes
            try:
                auth_process.terminate()
                main_process.terminate()
                
                # Wait for clean shutdown
                auth_process.wait(timeout=5)
                main_process.wait(timeout=5)
                
            except subprocess.TimeoutExpired:
                # Force kill if needed
                auth_process.kill()
                main_process.kill()
                
            print("✅ StockAI stopped successfully")
            
    except Exception as e:
        print(f"❌ Error starting StockAI: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 