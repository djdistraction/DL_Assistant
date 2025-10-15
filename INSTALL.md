# DL_Assistant Installation Guide

## One-Click Installation

DL_Assistant provides easy-to-use installer scripts that handle the entire installation process and automatically open the configuration dashboard.

### For Linux/Unix/MacOS

1. **Clone the repository:**
   ```bash
   git clone https://github.com/djdistraction/DL_Assistant.git
   cd DL_Assistant
   ```

2. **Run the installer:**
   ```bash
   ./install.sh
   ```

The installer will:
- Check for Python 3.8+ installation
- Install DL_Assistant and all required dependencies
- Automatically open the configuration dashboard in your browser
- Guide you through the setup process

### For Windows

1. **Clone the repository:**
   ```batch
   git clone https://github.com/djdistraction/DL_Assistant.git
   cd DL_Assistant
   ```

2. **Run the installer:**
   ```batch
   install.bat
   ```

The installer will:
- Check for Python 3.8+ installation
- Install DL_Assistant and all required dependencies
- Automatically open the configuration dashboard in your browser
- Guide you through the setup process

## Configuration Dashboard

After installation, the dashboard will open automatically at http://127.0.0.1:5000

### What You Can Configure:

1. **Folder Paths**
   - Downloads folder location
   - Quarantine folder location
   - Destination folders for different file types

2. **Naming Patterns**
   - Music files: `{artist} - {title} ({content_rating}) ({remix}).{ext}`
   - Video files: `{artist} - {title} ({content_rating}) ({video_type}).{ext}`
   - Images: `{title}.{ext}`
   - Documents: `{title}.{ext}`

3. **File Type Classifications**
   - Define which file extensions belong to which category
   - Add custom extensions for your needs

4. **Duplicate Detection**
   - Enable/disable duplicate detection
   - Choose comparison method (hash, size, or both)
   - Configure whether to keep newest or oldest files

5. **AI Vision Settings**
   - Enable/disable AI vision features (requires OpenAI API key)
   - Configure vision-based file analysis

## After Configuration

Once you've configured your preferences in the dashboard:

1. **Close the dashboard** by pressing `Ctrl+C` in the terminal

2. **Start monitoring** your downloads folder:
   ```bash
   dl-assistant
   ```

3. **Or run one-time processing** of existing files:
   ```bash
   dl-assistant --mode process
   ```

## Quick Launcher Scripts

For convenience, you can use the launcher scripts to quickly open the dashboard again:

**Linux/Unix/MacOS:**
```bash
./launch-dashboard.sh
```

**Windows:**
```batch
launch-dashboard.bat
```

## Command Line Options

After installation, the `dl-assistant` command is available with these options:

```
dl-assistant [options]

Options:
  --mode {monitor,dashboard,process}
                        Operation mode (default: monitor)
  --config CONFIG       Path to configuration directory
  --host HOST          Dashboard host (default: 127.0.0.1)
  --port PORT          Dashboard port (default: 5000)
  -h, --help           Show help message
```

### Modes:

- **monitor** (default): Watch downloads folder continuously
- **dashboard**: Open the web-based configuration interface
- **process**: Process existing files once without continuous monitoring

## Optional: AI Vision Features

For enhanced file analysis and naming, you can enable AI vision features:

1. Get an OpenAI API key from https://platform.openai.com/api-keys

2. Set the environment variable:
   
   **Linux/Unix/MacOS:**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
   
   **Windows:**
   ```batch
   set OPENAI_API_KEY=your-api-key-here
   ```

3. Enable vision in the dashboard configuration

With AI vision enabled, DL_Assistant can:
- Analyze image and video content
- Identify artists and song titles from visual content
- Detect video types (Music Video, Karaoke, Lyric Video, etc.)
- Identify explicit content automatically

## Troubleshooting

### Python Not Found

**Error:** "Python is not installed" or command not found

**Solution:** Install Python 3.8 or higher from:
- **Linux:** Use your package manager (e.g., `sudo apt install python3`)
- **MacOS:** Download from https://www.python.org/downloads/ or use `brew install python3`
- **Windows:** Download from https://www.python.org/downloads/ (check "Add Python to PATH")

### pip Not Found

**Error:** "pip is not installed" or command not found

**Solution:** 
- Usually pip is included with Python 3.4+
- On Linux: `sudo apt install python3-pip`
- On MacOS: `python3 -m ensurepip --upgrade`
- On Windows: Reinstall Python with pip included

### Permission Denied (Linux/Mac)

**Error:** Permission denied when running scripts

**Solution:** Make the script executable:
```bash
chmod +x install.sh
```

### Dashboard Won't Open

**Error:** Dashboard doesn't open in browser

**Solution:** Manually open http://127.0.0.1:5000 in your web browser

### Port Already in Use

**Error:** Port 5000 is already in use

**Solution:** Use a different port:
```bash
dl-assistant --mode dashboard --port 5001
```

## Uninstallation

To remove DL_Assistant:

```bash
pip uninstall dl-assistant
```

## Getting Help

If you encounter any issues:

1. Check the [README.md](README.md) for detailed documentation
2. Review [EXAMPLES.md](EXAMPLES.md) for usage examples
3. Open an issue on GitHub: https://github.com/djdistraction/DL_Assistant/issues

## Next Steps

After installation:

1. Configure your preferences in the dashboard
2. Test with `dl-assistant --mode process` on existing files
3. Start continuous monitoring with `dl-assistant`
4. Regularly check the quarantine folder for files needing manual sorting
5. Adjust configuration as needed via the dashboard
