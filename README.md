# Screenshot Analyzer 📸🤖

A powerful Windows desktop application that captures screenshots, takes user questions, and provides detailed AI-powered analysis using OpenAI's GPT-4 Vision model.

## ✨ Features

- **🔥 Global Hotkey**: Press `Ctrl+Shift+S` anywhere in Windows to instantly capture a screenshot
- **🖼️ Smart Capture**: Automatic screenshot capture with real-time preview
- **🤖 AI Analysis**: Powered by OpenAI's GPT-4 Vision for intelligent image understanding
- **💭 Interactive Q&A**: Ask specific questions about your screenshots
- **📝 Detailed Explanations**: Get comprehensive analysis with specific observations
- **💾 Auto-Save**: Results automatically saved with timestamps
- **🎨 Modern GUI**: Clean, intuitive interface built with tkinter

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** installed on your system
- **OpenAI API Key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys))

### Installation

1. **Clone/Download** this project to your desired location
2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Configure API**:
   
   **For Azure OpenAI (Recommended):**
   - Open `config.ini`
   - Set `api_type = azure`
   - Fill in your Azure OpenAI details:
     - `azure_api_key` - Your Azure OpenAI API key
     - `azure_endpoint` - Your Azure OpenAI endpoint (e.g., https://your-resource.openai.azure.com/)
     - `azure_deployment_name` - Your deployed model name
   
   **For Regular OpenAI:**
   - Open `config.ini`
   - Set `api_type = openai`
   - Set `openai_api_key` to your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)

4. **Run the application**:
   ```powershell
   # Option 1: PowerShell (recommended)
   .\run.ps1
   
   # Option 2: Batch file
   .\run.bat
   
   # Option 3: Direct Python
   python main.py
   ```

## 🎯 How to Use

### Method 1: Global Hotkey (Recommended)
1. Start the application
2. Press `Ctrl+Shift+S` anywhere in Windows
3. The screenshot will be captured and the app window will appear
4. Type your question in the text area
5. Click "Analyze" to get AI-powered insights

### Method 2: Manual Capture
1. Start the application and show the window
2. Click "Capture Screenshot"
3. Enter your question
4. Click "Analyze"

### Example Questions
- "What is the main purpose of this interface?"
- "Identify any errors or issues in this screenshot"
- "Explain what this graph/chart shows"
- "What text is visible in this image?"
- "Describe the layout and design elements"

## ⚙️ Configuration

Edit `config.ini` to customize:

**For Azure OpenAI:**
```ini
[API]
api_type = azure
azure_api_key = your-azure-api-key-here
azure_endpoint = https://your-resource.openai.azure.com/
azure_api_version = 2024-02-15-preview
azure_deployment_name = your-deployment-name

[SHORTCUTS]
capture_hotkey = ctrl+shift+s

[UI]
window_width = 800
window_height = 600
```

**For Regular OpenAI:**
```ini
[API]
api_type = openai
openai_api_key = your-api-key-here
model = gpt-4-vision-preview

[SHORTCUTS]
capture_hotkey = ctrl+shift+s

[UI]
window_width = 800
window_height = 600
```

## 📁 Project Structure

```
screenshot-analyzer/
├── main.py              # Main application
├── config.ini           # Configuration file
├── requirements.txt     # Python dependencies
├── run.ps1             # PowerShell launcher
├── run.bat             # Batch launcher
├── README.md           # This file
└── .github/
    └── copilot-instructions.md
```

## 🔧 Dependencies

- **tkinter**: GUI framework (built into Python)
- **pyautogui**: Screenshot capture
- **Pillow**: Image processing
- **keyboard**: Global hotkey support
- **requests**: API communication
- **configparser**: Configuration management

## 🛠️ Building Executable

To create a standalone executable:

```powershell
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## 🔒 Security & Privacy

- Screenshots are processed locally and only sent to OpenAI's API for analysis
- API keys are stored in local configuration files
- No data is permanently stored on external servers
- Results are saved locally as text files

## 🐛 Troubleshooting

### Common Issues

**"Failed to register hotkey"**
- Make sure no other application is using `Ctrl+Shift+S`
- Try running as administrator
- Change the hotkey in `config.ini`

**"API Error 401"**
- Check your OpenAI API key in `config.ini`
- Ensure you have credits in your OpenAI account

**"Screenshot capture failed"**
- Ensure pyautogui has permission to capture screenshots
- On some systems, you may need to disable "Use Windows Ink" in Windows settings

**Import errors**
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.7+

## 💡 Tips

- Use specific questions for better analysis results
- The app works best with clear, high-contrast screenshots
- Results are automatically saved in the project directory
- You can run multiple instances for different workflows

## 🤝 Contributing

Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Verify your OpenAI API key is valid
4. Check that Python 3.7+ is installed

---

**Made with ❤️ for Windows users who want smarter screenshot analysis**
