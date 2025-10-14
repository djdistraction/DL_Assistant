"""
Metadata extraction for various file types
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from mutagen import File as MutagenFile
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False

try:
    from PyPDF2 import PdfReader
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False


class MetadataExtractor:
    """Extract metadata from various file types"""
    
    @staticmethod
    def extract(file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing metadata
        """
        path = Path(file_path)
        metadata = {
            'filename': path.stem,
            'ext': path.suffix.lower().lstrip('.'),
            'size': path.stat().st_size,
            'created': datetime.fromtimestamp(path.stat().st_ctime),
            'modified': datetime.fromtimestamp(path.stat().st_mtime),
        }
        
        # Add formatted date and time
        metadata['date'] = metadata['modified'].strftime('%Y-%m-%d')
        metadata['time'] = metadata['modified'].strftime('%H-%M-%S')
        
        # Try to extract type-specific metadata
        ext = metadata['ext']
        
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            metadata.update(MetadataExtractor._extract_image_metadata(file_path))
        elif ext in ['mp3', 'wav', 'flac', 'm4a', 'aac', 'ogg']:
            metadata.update(MetadataExtractor._extract_audio_metadata(file_path))
        elif ext == 'pdf':
            metadata.update(MetadataExtractor._extract_pdf_metadata(file_path))
        
        return metadata
    
    @staticmethod
    def _extract_image_metadata(file_path: str) -> Dict[str, Any]:
        """Extract metadata from image files"""
        metadata = {}
        
        if not HAS_PIL:
            return metadata
        
        try:
            with Image.open(file_path) as img:
                metadata['width'] = img.width
                metadata['height'] = img.height
                metadata['format'] = img.format
                
                # Extract EXIF data if available
                exif_data = img.getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == 'DateTime':
                            try:
                                dt = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                                metadata['date'] = dt.strftime('%Y-%m-%d')
                                metadata['time'] = dt.strftime('%H-%M-%S')
                            except:
                                pass
                        elif tag == 'ImageDescription':
                            metadata['title'] = value
        except Exception as e:
            pass
        
        return metadata
    
    @staticmethod
    def _extract_audio_metadata(file_path: str) -> Dict[str, Any]:
        """Extract metadata from audio files"""
        metadata = {}
        
        if not HAS_MUTAGEN:
            return metadata
        
        try:
            audio = MutagenFile(file_path)
            if audio is not None:
                # Common tags across formats
                if hasattr(audio, 'tags') and audio.tags:
                    tags = audio.tags
                    
                    # Try different tag formats
                    for title_tag in ['TIT2', 'title', '\xa9nam']:
                        if title_tag in tags:
                            metadata['title'] = str(tags[title_tag])
                            break
                    
                    for artist_tag in ['TPE1', 'artist', '\xa9ART']:
                        if artist_tag in tags:
                            metadata['artist'] = str(tags[artist_tag])
                            break
                    
                    for album_tag in ['TALB', 'album', '\xa9alb']:
                        if album_tag in tags:
                            metadata['album'] = str(tags[album_tag])
                            break
                    
                    for year_tag in ['TDRC', 'date', '\xa9day']:
                        if year_tag in tags:
                            metadata['year'] = str(tags[year_tag])
                            break
                
                # Duration
                if hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                    metadata['duration'] = int(audio.info.length)
        except Exception as e:
            pass
        
        return metadata
    
    @staticmethod
    def _extract_pdf_metadata(file_path: str) -> Dict[str, Any]:
        """Extract metadata from PDF files"""
        metadata = {}
        
        if not HAS_PYPDF2:
            return metadata
        
        try:
            with open(file_path, 'rb') as f:
                pdf = PdfReader(f)
                
                if pdf.metadata:
                    if pdf.metadata.title:
                        metadata['title'] = pdf.metadata.title
                    if pdf.metadata.author:
                        metadata['author'] = pdf.metadata.author
                    if pdf.metadata.subject:
                        metadata['subject'] = pdf.metadata.subject
                
                metadata['pages'] = len(pdf.pages)
        except Exception as e:
            pass
        
        return metadata
