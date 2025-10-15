# Quick Start Guide - DL_Assistant

Get started with DL_Assistant in just a few steps!

## 🚀 One-Click Installation

### For Linux/Unix/MacOS Users:

```bash
git clone https://github.com/djdistraction/DL_Assistant.git
cd DL_Assistant
./install.sh
```

### For Windows Users:

```batch
git clone https://github.com/djdistraction/DL_Assistant.git
cd DL_Assistant
install.bat
```

## 📋 What Happens Next?

1. **Automatic Installation**: The installer will check your system and install all dependencies
2. **Dashboard Opens**: Your browser will automatically open to http://127.0.0.1:5000
3. **Configure Preferences**: Set up your folders, naming patterns, and preferences
4. **Start Using**: Close the dashboard (Ctrl+C) and run `dl-assistant` to start!

## 🎯 Configuration Dashboard

The dashboard allows you to configure:

- **Folder Paths**: Where to monitor and where to move files
- **Naming Patterns**: How to rename different file types  
- **Duplicate Detection**: Whether to detect and remove duplicates
- **File Classifications**: Which file types go where
- **Monitoring Settings**: What files to ignore

![Dashboard Screenshot](https://github.com/user-attachments/assets/dcaa15c4-44bb-487e-b439-1d9c5c47c923)

## 🎮 After Configuration

Once you've configured your preferences:

### Start Monitoring Your Downloads:
```bash
dl-assistant
```

### Or Process Existing Files Once:
```bash
dl-assistant --mode process
```

### Reopen Dashboard Anytime:
```bash
dl-assistant --mode dashboard
```

Or use the launcher scripts:
- **Linux/Mac**: `./launch-dashboard.sh`
- **Windows**: `launch-dashboard.bat`

## 📚 Need More Help?

- **Full Installation Guide**: See [INSTALL.md](INSTALL.md)
- **Detailed Documentation**: See [README.md](README.md)
- **Usage Examples**: See [EXAMPLES.md](EXAMPLES.md)

## 💡 Quick Tips

1. **Test First**: Use `--mode process` to test on existing files before continuous monitoring
2. **Check Quarantine**: Files that can't be auto-organized go to the quarantine folder
3. **Optional AI**: Set `OPENAI_API_KEY` environment variable for AI-powered file analysis

## 🆘 Troubleshooting

**Python not found?** Install Python 3.8+ from https://www.python.org/downloads/

**pip not found?** It's usually included with Python. On Linux: `sudo apt install python3-pip`

**Dashboard won't open?** Manually visit http://127.0.0.1:5000 in your browser

**Port already in use?** Use a different port: `dl-assistant --mode dashboard --port 5001`

---

**Ready to organize your downloads automatically?** Run the installer now! 🎉
