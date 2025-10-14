# DL_Assistant

An intelligent assistant that monitors your system downloads folder, reads meta-data, renames files according to meta-data, deletes duplicate files, and relocates files to stay more organized. If it isn't clear where the file should be moved to, then it quarantines the file for further direction. Includes a dashboard for setup which allows the user to predesignate naming structure and destination folders.

## Features

- **Automatic File Monitoring**: Watches your downloads folder for new files in real-time
- **Metadata Extraction**: Reads metadata from various file types (images, audio, PDFs, etc.)
- **Smart Renaming**: Renames files based on metadata and configurable naming patterns
- **Duplicate Detection**: Identifies and removes duplicate files using hash comparison
- **Intelligent Organization**: Automatically moves files to appropriate destination folders
- **Quarantine System**: Files with unclear destinations are quarantined for manual review
- **Web Dashboard**: User-friendly interface for configuration and management

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/djdistraction/DL_Assistant.git
cd DL_Assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

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

Available placeholders:
- `{date}`: File date (YYYY-MM-DD)
- `{time}`: File time (HH-MM-SS)
- `{title}`: Title from metadata
- `{artist}`: Artist from metadata (music files)
- `{album}`: Album from metadata (music files)
- `{year}`: Year from metadata
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
3. **Type Classification**: Determines file type based on extension
4. **Duplicate Check**: Compares with existing files in destination folders
5. **Renaming**: Generates new filename based on metadata and naming patterns
6. **Relocation**: Moves file to appropriate destination folder
7. **Quarantine**: If destination is unclear, moves to quarantine folder for manual review

## Project Structure

```
DL_Assistant/
├── src/
│   └── dl_assistant/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── config.py            # Configuration management
│       ├── metadata.py          # Metadata extraction
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
│   └── test_metadata.py
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

- **watchdog**: File system monitoring
- **flask**: Web dashboard
- **PyYAML**: Configuration management
- **Pillow**: Image metadata extraction
- **mutagen**: Audio metadata extraction
- **PyPDF2**: PDF metadata extraction
- **python-magic**: File type detection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

