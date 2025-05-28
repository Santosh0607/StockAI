# StockAI PowerShell Launcher
Write-Host "🚀 StockAI - NEPSE Market Prediction Platform" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Starting secure authentication and AI dashboard..." -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "🔐 Starting Authentication System..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "auth_app.py" -WindowStyle Normal

Write-Host "📊 Waiting for auth system to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "📈 Starting Main Dashboard..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "app.py" -WindowStyle Normal

Write-Host ""
Write-Host "🎉 StockAI is starting!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "📋 Application URLs:" -ForegroundColor White
Write-Host "🔑 Authentication: http://127.0.0.1:8060" -ForegroundColor Cyan
Write-Host "📈 Main Dashboard: http://127.0.0.1:8050" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 How to use:" -ForegroundColor White
Write-Host "1. First, login or create account at the authentication page" -ForegroundColor Gray
Write-Host "2. After successful login, access the main dashboard" -ForegroundColor Gray
Write-Host "3. Upload your NEPSE stock data (Excel format)" -ForegroundColor Gray
Write-Host "4. Configure model parameters and train AI model" -ForegroundColor Gray
Write-Host "5. View predictions and technical analysis" -ForegroundColor Gray
Write-Host ""
Write-Host "🔒 Security Features:" -ForegroundColor White
Write-Host "- SQLite database with encrypted passwords" -ForegroundColor Gray
Write-Host "- Secure session management" -ForegroundColor Gray
Write-Host "- PBKDF2-SHA256 password hashing" -ForegroundColor Gray
Write-Host "- CSRF protection" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  Close the Python windows to stop the applications" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Cyan

# Open authentication page
Write-Host "🌐 Opening authentication page..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:8060"

# Open main dashboard
Write-Host "🌐 Opening main dashboard..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:8050"

Write-Host "✅ Both applications are starting..." -ForegroundColor Green
Write-Host "✅ Browser tabs should open automatically" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit this launcher" 