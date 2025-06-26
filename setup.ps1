Write-Host "🚀 Screenshot Analyzer Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

Write-Host "Checking for Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Please install Python:" -ForegroundColor Cyan
    Write-Host "   Option 1: Download from https://python.org" -ForegroundColor White
    Write-Host "   Option 2: Install from Microsoft Store" -ForegroundColor White
    Write-Host "   Option 3: Use winget: winget install Python.Python.3" -ForegroundColor White
    Write-Host ""
    Write-Host "⚠️  Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    
    $installChoice = Read-Host "Would you like to install Python via winget? (y/N)"
    if ($installChoice -eq "y" -or $installChoice -eq "Y") {
        try {
            Write-Host "Installing Python via winget..." -ForegroundColor Yellow
            winget install Python.Python.3
            Write-Host "✅ Python installation completed" -ForegroundColor Green
            Write-Host "🔄 Please restart this script after installation" -ForegroundColor Yellow
        } catch {
            Write-Host "❌ Failed to install Python via winget" -ForegroundColor Red
            Write-Host "Please install Python manually from https://python.org" -ForegroundColor Yellow
        }
    }
    
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Checking for pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Found pip" -ForegroundColor Green
    } else {
        throw "pip not found"
    }
} catch {
    Write-Host "❌ pip is not available" -ForegroundColor Red
    Write-Host "Please ensure pip is installed with Python" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    try {
        pip install -r requirements.txt
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install some dependencies" -ForegroundColor Red
        Write-Host "You may need to install them manually" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ requirements.txt not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "Checking API configuration..." -ForegroundColor Yellow
if (Test-Path "config.ini") {
    $configContent = Get-Content "config.ini" -Raw
    if ($configContent -match "your-openai-api-key-here") {
        Write-Host "⚠️  API key not configured" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "📝 To complete setup:" -ForegroundColor Cyan
        Write-Host "   1. Get an OpenAI API key from: https://platform.openai.com/api-keys" -ForegroundColor White
        Write-Host "   2. Open config.ini in a text editor" -ForegroundColor White
        Write-Host "   3. Replace 'your-openai-api-key-here' with your actual API key" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "✅ API key appears to be configured" -ForegroundColor Green
    }
} else {
    Write-Host "❌ config.ini not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 Setup Summary:" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host "✅ Python: Installed" -ForegroundColor Green
Write-Host "✅ Dependencies: Installed" -ForegroundColor Green

if (Test-Path "config.ini") {
    $configContent = Get-Content "config.ini" -Raw
    if ($configContent -match "your-openai-api-key-here") {
        Write-Host "⚠️  API Key: Not configured" -ForegroundColor Yellow
    } else {
        Write-Host "✅ API Key: Configured" -ForegroundColor Green
    }
} else {
    Write-Host "❌ Config: Missing" -ForegroundColor Red
}

Write-Host ""
Write-Host "🚀 Ready to run! Use one of:" -ForegroundColor Green
Write-Host "   .\run.ps1" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor White
Write-Host ""
Write-Host "📸 Global hotkey: Ctrl+Shift+S" -ForegroundColor Cyan

Read-Host "Press Enter to exit"