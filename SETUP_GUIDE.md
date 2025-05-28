# 🚀 StockAI Setup Guide

## ✅ **Quick Start (Recommended)**

### **Option 1: Using Batch File (Windows)**
1. Double-click `run_stockai.bat` in the StockAI-master folder
2. Wait for both applications to start
3. Browser tabs will open automatically

### **Option 2: Using PowerShell Script**
1. Right-click `run_stockai.ps1` → "Run with PowerShell"
2. If prompted about execution policy, type `Y` and press Enter
3. Wait for both applications to start

### **Option 3: Manual Start**
1. Open two Command Prompt or PowerShell windows
2. Navigate to the StockAI-master folder in both
3. In first window: `python auth_app.py`
4. In second window: `python app.py`
5. Open browser to:
   - Authentication: http://127.0.0.1:8060
   - Dashboard: http://127.0.0.1:8050

## 📋 **Prerequisites**

- **Python 3.8+** (Check: `python --version`)
- **pip** (Check: `pip --version`)
- **Internet connection** (for package installation)
- **Modern web browser** (Chrome, Firefox, Edge)

## 🔧 **Detailed Setup Steps**

### Step 1: Verify Python Installation
```bash
python --version
# Should show Python 3.8.x or higher
```

### Step 2: Install Dependencies
```bash
cd StockAI-master
pip install -r requirements.txt
```

### Step 3: Start Applications
**Option A - All-in-one:**
```bash
run_stockai.bat
# or
powershell -ExecutionPolicy Bypass -File run_stockai.ps1
```

**Option B - Manual:**
```bash
# Terminal 1 - Authentication
python auth_app.py

# Terminal 2 - Dashboard  
python app.py
```

### Step 4: Access Applications
- 🔑 **Login/Signup**: http://127.0.0.1:8060
- 📈 **Dashboard**: http://127.0.0.1:8050

## 🛠️ **Troubleshooting**

### **Issue: "Python is not recognized"**
**Solution:**
1. Install Python from https://python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt and try again

### **Issue: "pip is not recognized"**
**Solution:**
```bash
python -m pip --version
# Use "python -m pip" instead of "pip"
```

### **Issue: "Port already in use"**
**Solution:**
```bash
# Kill processes on ports
netstat -ano | findstr :8060
netstat -ano | findstr :8050
# Note the PID and kill with: taskkill /PID <PID> /F
```

### **Issue: "ModuleNotFoundError"**
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **Issue: "DLL load failed" or bcrypt errors**
**Solution:**
- Already fixed! We removed bcrypt dependency
- If still occurs, try: `pip uninstall bcrypt && pip install werkzeug`

### **Issue: Authentication not working**
**Solution:**
1. Check both applications are running
2. Clear browser cookies/cache
3. Try incognito/private browsing mode
4. Verify URLs are correct

### **Issue: CSS not loading (plain white page)**
**Solution:**
1. Ensure `assets/style.css` file exists
2. Restart both applications
3. Hard refresh browser (Ctrl+F5)

## 📊 **Test Data Format**

Create an Excel file (.xlsx) with these columns:

| Column | Example | Description |
|--------|---------|-------------|
| Symbol | NEPSE | Stock symbol |
| Date | 2024-01-15 | Trading date |
| Open | 2677.58 | Opening price |
| High | 2687.92 | Highest price |
| Low | 2667.00 | Lowest price |
| Close | 2670.77 | Closing price |
| Volume | 5637981250.23 | Trading volume |

## 🔒 **Security Features Included**

✅ **Password Security:**
- PBKDF2-SHA256 hashing with salt
- Minimum 8 characters with mixed case/numbers
- No plain text storage

✅ **Session Security:**
- 24-hour automatic timeout
- Secure session tokens
- CSRF protection

✅ **Database Security:**
- SQLite with encrypted storage
- SQL injection protection
- Input validation

## 🎯 **Usage Workflow**

1. **Start Applications** → Use batch file or manual start
2. **Create Account** → Visit auth page, sign up with strong password
3. **Login** → Use your credentials to access dashboard
4. **Upload Data** → Excel file with stock data
5. **Configure Model** → Set parameters (time step: 60, prediction days: 30)
6. **Train Model** → Click "Train Model & Predict"
7. **View Results** → Explore charts in different tabs

## 📁 **File Structure**
```
StockAI-master/
├── auth.py              # Authentication core
├── auth_app.py          # Login/signup interface
├── app.py               # Main dashboard
├── run_stockai.bat      # Windows launcher
├── run_stockai.ps1      # PowerShell launcher
├── requirements.txt     # Dependencies
├── assets/
│   └── style.css       # Modern UI styles
├── models/             # AI model files
├── utils/              # Data processing
└── output/             # Generated files
```

## 🆘 **Getting Help**

1. **Check Console Logs** - Look for error messages in terminal
2. **Browser Developer Tools** - F12 → Console tab for JavaScript errors
3. **Restart Applications** - Close and restart both Python processes
4. **Clear Data** - Delete `stockai_users.db` to reset users
5. **Check File Permissions** - Ensure write access to project folder

## 🎉 **Success Indicators**

✅ No error messages in terminal  
✅ Both URLs accessible in browser  
✅ Modern dark theme visible  
✅ Can create account and login  
✅ Can upload file and see preview  
✅ Can train model and see charts  

---

**🎯 You're all set! Enjoy using StockAI for NEPSE market analysis!** 