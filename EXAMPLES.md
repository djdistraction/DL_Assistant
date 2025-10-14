# DL_Assistant Usage Examples

This file contains examples of how to use DL_Assistant.

## Quick Start: Complete Workflow

Here's a complete workflow showing how DL_Assistant intelligently organizes your downloads:

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Enable AI Vision features
export OPENAI_API_KEY='your-api-key-here'

# Start monitoring
dl-assistant
```

### What Happens to Your Downloads

**Scenario 1: Music Video Download**
```
Downloaded: "video_20241015_193042.mp4"
↓ Vision AI analyzes video frame
↓ Detects: Music Video, Artist: "Papa Roach", Title: "Last Resort", Rating: Clean
Renamed: "Papa Roach - Last Resort (Clean) (Music Video).mp4"
Moved to: ~/Videos/
```

**Scenario 2: Karaoke Video**
```
Downloaded: "guilty_conscience_kar.mp4"
↓ Vision AI detects karaoke-style lyrics on screen
↓ Extracts: Artist: "Eminem", Title: "Guilty Conscience", Rating: Explicit
Renamed: "Eminem - Guilty Conscience (Explicit) (Karaoke).mp4"
Moved to: ~/Videos/
```

**Scenario 3: Music File with ID3 Tags**
```
Downloaded: "track01.mp3"
↓ Reads ID3 tags from file
↓ Found: Artist: "Test Artist", Title: "Test Song"
Renamed: "Test Artist - Test Song.mp3"
Moved to: ~/Music/
```

**Scenario 4: Music File without Tags**
```
Downloaded: "unknown_track.mp3"
↓ No ID3 tags found
↓ Vision AI analyzes embedded album art
↓ Extracts artist and title from album art
Renamed: "Artist Name - Song Title (Clean).mp3"
Moved to: ~/Music/
```

## Example 1: Basic Monitoring

Start monitoring with default settings:

```bash
dl-assistant
```

This will:
1. Read configuration from `config/default_config.yaml`
2. Monitor your `~/Downloads` folder
3. Process any new files that appear
4. Organize them based on file type

## Example 2: Using the Dashboard

Start the web dashboard:

```bash
dl-assistant --mode dashboard
```

Then open your browser to http://127.0.0.1:5000

From the dashboard you can:
- Configure folder paths
- Set up naming patterns
- Manage duplicate detection settings
- View quarantined files

## Example 3: One-Time Processing

Process all existing files without continuous monitoring:

```bash
dl-assistant --mode process
```

This is useful for:
- Initial organization of your downloads folder
- Periodic cleanup

## Example 4: Custom Configuration

You can customize the configuration by editing `config/user_config.json` (created automatically) or using the dashboard.

### Custom Naming Pattern Example

To rename music files as "Artist - Title.ext":

1. Edit naming pattern in dashboard or config:
```yaml
naming_patterns:
  music: "{artist} - {title}.{ext}"
```

2. Any MP3 files downloaded will be renamed using metadata

### Custom Destination Example

To organize files into custom folders:

```yaml
destinations:
  images:
    - "/home/user/Photos/Unsorted"
  documents:
    - "/home/user/Documents/Downloads"
```

## Example 5: Python API Usage

You can also use DL_Assistant as a Python library:

```python
from dl_assistant.config import ConfigManager
from dl_assistant.file_manager import FileManager
from dl_assistant.watcher import FileWatcher

# Initialize
config = ConfigManager()
file_manager = FileManager(config)
watcher = FileWatcher(config, file_manager)

# Start monitoring
watcher.start()

# Process existing files
watcher.process_existing_files()

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    watcher.stop()
```

## Example 6: Metadata Extraction

Extract metadata from a file:

```python
from dl_assistant.metadata import MetadataExtractor

metadata = MetadataExtractor.extract("/path/to/file.jpg")
print(metadata)
# Output: {'filename': 'file', 'ext': 'jpg', 'date': '2024-01-15', ...}
```

## Example 7: Duplicate Detection

Find duplicates of a file:

```python
from dl_assistant.config import ConfigManager
from dl_assistant.file_manager import FileManager

config = ConfigManager()
file_manager = FileManager(config)

duplicates = file_manager.find_duplicates(
    "/path/to/file.txt",
    "/path/to/search/directory"
)

for dup in duplicates:
    print(f"Duplicate found: {dup}")
```

## File Type Classification

DL_Assistant automatically classifies files by extension:

- **Images**: jpg, jpeg, png, gif, bmp, svg, webp
- **Documents**: pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx
- **Music**: mp3, wav, flac, m4a, aac, ogg, wma
- **Videos**: mp4, avi, mkv, mov, wmv, flv, webm
- **Archives**: zip, rar, tar, gz, 7z

## Naming Pattern Placeholders

Available placeholders for file naming:

- `{date}`: File modification date (YYYY-MM-DD)
- `{time}`: File modification time (HH-MM-SS)
- `{filename}`: Original filename without extension
- `{ext}`: File extension
- `{title}`: Title from metadata or AI vision (if available)
- `{artist}`: Artist from metadata or AI vision (music/video files)
- `{album}`: Album from metadata (music files)
- `{year}`: Year from metadata
- `{author}`: Author from metadata (documents)
- `{width}`: Image width (images)
- `{height}`: Image height (images)
- `{content_rating}`: Clean or Explicit (from AI vision)
- `{video_type}`: Video content type like Music Video, Karaoke, Lyric Video, etc. (from AI vision)

## Example 8: AI Vision-Based Renaming

Enable AI vision for intelligent file naming (requires OpenAI API key):

```bash
export OPENAI_API_KEY='your-api-key-here'
dl-assistant
```

With vision enabled:

**Music Videos:**
- Downloaded file: `video_2024_01_15.mp4`
- Contains: Music video for "Last Resort" by Papa Roach with censored lyrics
- Renamed to: `Papa Roach - Last Resort (Clean) (Music Video).mp4`

**Karaoke Videos:**
- Downloaded file: `Guilty_Conscience.mp4`
- Contains: Karaoke version with lyrics for Eminem's "Guilty Conscience"
- Renamed to: `Eminem - Guilty Conscience (Explicit) (Karaoke).mp4`

**Music Files with Album Art:**
- Downloaded file: `track01.mp3`
- AI analyzes embedded album art to extract artist/title
- Renamed to: `Artist Name - Song Title (Clean).mp3`

To disable vision features, set in your config:
```yaml
vision_enabled: false
```

## Tips

1. **Test First**: Use `--mode process` to test your configuration on existing files before enabling continuous monitoring

2. **Check Quarantine**: Regularly check the quarantine folder for files that couldn't be automatically organized

3. **Backup**: Always have backups of important files before running automated organization

4. **Gradual Setup**: Start with a simple configuration and gradually add more complex rules

5. **Monitor Logs**: Watch the console output to see what DL_Assistant is doing with your files
