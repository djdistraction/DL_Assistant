# DL_Assistant

An intelligent assistant that monitors your system downloads folder, reads meta-data, renames files according to meta-data, deletes duplicate files, and relocates files to stay more organized. If it isn't clear where the file should be moved to, then it quarantines the file for further direction. Includes a dashboard for setup which allows the user to predesignate naming structure and destination folders.

---

**🚀 New to DL_Assistant?** Check out the [Quick Start Guide](QUICKSTART.md) for a fast, guided installation!

---

## Features

- **Automatic File Monitoring**: Watches your downloads folder for new files in real-time
- **AI Vision Integration**: Uses OpenAI's vision API to analyze images and videos for intelligent naming
- **Metadata Extraction**: Reads metadata from various file types (images, audio, videos, PDFs, etc.)
- **Smart Renaming**: Renames files based on metadata and configurable naming patterns
  - Music files: `Artist(s) - Song Title (Clean/Explicit) (Remix Description).ext`
  - Video files: `Artist - Title (Clean/Explicit) (Video Type).ext`
- **Video Content Recognition**: Automatically identifies video types:
  - Music Video, Karaoke, Lyric Video, Background Video, Background FX Video, Slideshow, Concert, Performance, etc.
- **Content Rating Detection**: Identifies explicit content and marks files as Clean or Explicit
- **Duplicate Detection**: Identifies and removes duplicate files using hash comparison
- **Intelligent Organization**: Automatically moves files to appropriate destination folders
- **Quarantine System**: Files with unclear destinations are quarantined for manual review
- **Web Dashboard**: User-friendly interface for configuration and management

## Installation

### Quick Install (Recommended)

**One-Click Installer** - The easiest way to get started! The installer will:
- Install DL_Assistant and all dependencies
- Automatically open the configuration dashboard
- Guide you through initial setup

**For Linux/Unix/MacOS:**
```bash
git clone https://github.com/djdistraction/DL_Assistant.git
cd DL_Assistant
./install.sh
```

**For Windows:**
```batch
git clone https://github.com/djdistraction/DL_Assistant.git
cd DL_Assistant
install.bat
```

After installation, the dashboard will open automatically at http://127.0.0.1:5000, where you can:
- Configure your downloads and destination folders
- Set up naming patterns for different file types
- Configure duplicate detection settings
- Customize file type classifications

Once configured, close the dashboard (Ctrl+C) and run `dl-assistant` to start monitoring.

### Manual Installation

If you prefer to install manually:

#### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

#### Steps

1. Clone the repository:
```bash
git clone https://github.com/djdistraction/DL_Assistant.git
cd DL_Assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up OpenAI API key for vision features:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Note: Vision features require an OpenAI API key. Without it, the assistant will still work but will only use basic metadata extraction.

4. Install the package:
```bash
pip install -e .
```

5. Start the dashboard for initial configuration:
```bash
dl-assistant --mode dashboard
```

Open http://127.0.0.1:5000 in your browser to configure your preferences.

## Usage

### Monitor Mode (Default)

Start monitoring your downloads folder:
```bash
dl-assistant
```

Or using Python:
```bash
python -m dl_assistant.main
```

The assistant will:
1. Process all existing files in your downloads folder
2. Continue monitoring for new files
3. Automatically organize files based on your configuration

Press `Ctrl+C` to stop monitoring.

### Dashboard Mode

Launch the web dashboard to configure settings:
```bash
dl-assistant --mode dashboard
```

Then open your browser to `http://127.0.0.1:5000`

You can also specify custom host and port:
```bash
dl-assistant --mode dashboard --host 0.0.0.0 --port 8080
```

### Process Mode

Process existing files once without continuous monitoring:
```bash
dl-assistant --mode process
```

## Configuration

Configuration is managed through two files:

1. **default_config.yaml**: Default settings (do not modify)
2. **user_config.json**: User-specific overrides (created automatically)

### Configuration Options

#### Folder Paths
```yaml
downloads_folder: "~/Downloads"
quarantine_folder: "~/Downloads/Quarantine"
```

#### Vision AI Settings

Enable or disable AI vision for intelligent file naming:
```yaml
vision_enabled: true  # Requires OPENAI_API_KEY environment variable
```

When enabled, DL_Assistant uses AI to:
- Analyze images and videos to extract artist and title information
- Detect video content types (Music Video, Karaoke, Lyric Video, etc.)
- Identify explicit content and mark files as Clean or Explicit
- Generate descriptive filenames based on visual content

#### Naming Patterns

Define how files should be renamed using placeholders:
```yaml
naming_patterns:
  images: "{date}_{filename}.{ext}"
  documents: "{date}_{title}.{ext}"
  music: "{artist} - {title}.{ext}"
  videos: "{date}_{title}.{ext}"
  default: "{date}_{filename}.{ext}"
```

**Note:** For music and video files with artist/title metadata, the assistant uses intelligent patterns:
- Music: `Artist(s) - Song Title (Clean/Explicit).ext`
- Videos: `Artist - Title (Clean/Explicit) (Video Type).ext`

Available placeholders:
- `{date}`: File date (YYYY-MM-DD)
- `{time}`: File time (HH-MM-SS)
- `{title}`: Title from metadata or AI vision
- `{artist}`: Artist from metadata or AI vision
- `{album}`: Album from metadata (music files)
- `{year}`: Year from metadata
- `{content_rating}`: Clean or Explicit (from AI vision)
- `{video_type}`: Video content type (Music Video, Karaoke, etc.)
- `{filename}`: Original filename
- `{ext}`: File extension

#### Destination Folders

Specify where different file types should be moved:
```yaml
destinations:
  images:
    - "~/Pictures"
  documents:
    - "~/Documents"
  music:
    - "~/Music"
  videos:
    - "~/Videos"
```

#### File Type Classifications

Define which extensions belong to which category:
```yaml
file_types:
  images:
    - jpg
    - jpeg
    - png
    - gif
  documents:
    - pdf
    - doc
    - docx
    - txt
  music:
    - mp3
    - wav
    - wave
    - flac
  videos:
    - mp4
    - avi
    - mkv
```

#### Duplicate Detection

Configure how duplicates are handled:
```yaml
duplicate_detection:
  enabled: true
  compare_method: "hash"  # hash, size, or both
  keep_newest: true
```

## How It Works

1. **File Detection**: The watchdog library monitors your downloads folder for new files
2. **Metadata Extraction**: Reads metadata using appropriate libraries (PIL for images, mutagen for audio, PyPDF2 for PDFs)
3. **AI Vision Analysis** (Optional): If enabled, uses OpenAI's vision API to:
   - Analyze images and video frames for artist/title information
   - Detect video content types (Music Video, Karaoke, Lyric Video, etc.)
   - Identify explicit content and mark as Clean or Explicit
4. **Type Classification**: Determines file type based on extension
5. **Intelligent Naming**: For music and videos with artist/title metadata:
   - Music: `Artist(s) - Song Title (Clean/Explicit).ext`
   - Videos: `Artist - Title (Clean/Explicit) (Video Type).ext`
6. **Duplicate Check**: Compares with existing files in destination folders
7. **Relocation**: Moves file to appropriate destination folder
8. **Quarantine**: If destination is unclear, moves to quarantine folder for manual review

## Project Structure

```
DL_Assistant/
├── src/
│   └── dl_assistant/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── config.py            # Configuration management
│       ├── metadata.py          # Metadata extraction
│       ├── vision.py            # AI vision analysis
│       ├── file_manager.py      # File operations
│       ├── watcher.py           # File monitoring
│       ├── dashboard.py         # Web dashboard
│       └── templates/
│           └── index.html       # Dashboard UI
├── config/
│   └── default_config.yaml      # Default configuration
├── tests/
│   ├── test_config.py
│   ├── test_file_manager.py
│   ├── test_metadata.py
│   └── test_vision.py
├── requirements.txt
├── setup.py
└── README.md
```

## Testing

Run the test suite:
```bash
python -m unittest discover tests
```

Run specific test file:
```bash
python -m unittest tests.test_config
```

## Dependencies

### Required
- **watchdog**: File system monitoring
- **flask**: Web dashboard
- **PyYAML**: Configuration management
- **Pillow**: Image metadata extraction
- **mutagen**: Audio metadata extraction
- **PyPDF2**: PDF metadata extraction
- **python-magic**: File type detection

### Optional (for AI Vision Features)
- **openai**: OpenAI API client for vision analysis
- **opencv-python**: Video frame extraction for vision analysis

**Note**: Vision features require an OpenAI API key. Without it, the assistant will work with basic metadata extraction only.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

