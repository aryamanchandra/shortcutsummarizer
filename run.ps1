Write-Host "Screenshot Analyzer - Starting..." -ForegroundColor Green
Write-Host ""

try {
    $pythonVersion = python --version
    Write-Host "Found: $pythonVersion" -ForegroundColor Yellow
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Checking dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt --quiet
    Write-Host "Dependencies installed/updated" -ForegroundColor Green
} else {
    Write-Host "Warning: requirements.txt not found" -ForegroundColor Yellow
}

if (Test-Path "config.ini") {
    $configContent = Get-Content "config.ini" -Raw
    if ($configContent -match "your-openai-api-key-here") {
        Write-Host ""
        Write-Host "⚠️  IMPORTANT: Please set your OpenAI API key in config.ini" -ForegroundColor Red
        Write-Host "   1. Open config.ini" -ForegroundColor White
        Write-Host "   2. Replace 'your-openai-api-key-here' with your actual API key" -ForegroundColor White
        Write-Host "   3. Get API key from: https://platform.openai.com/api-keys" -ForegroundColor White
        Write-Host ""
    }
} else {
    Write-Host "Warning: config.ini not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Starting Screenshot Analyzer..." -ForegroundColor Green
Write-Host "📸 Global hotkey: Ctrl+Shift+S" -ForegroundColor Cyan
Write-Host "❌ Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

try {
    python main.py
} catch {
    Write-Host "Error running application: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}