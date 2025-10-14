"""
File management utilities for DL_Assistant
"""
import os
import hashlib
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .metadata import MetadataExtractor


class FileManager:
    """Handles file operations like renaming, moving, and duplicate detection"""
    
    def __init__(self, config):
        """
        Initialize file manager
        
        Args:
            config: ConfigManager instance
        """
        self.config = config
        self.metadata_extractor = MetadataExtractor()
    
    def get_file_type(self, file_path: str) -> str:
        """
        Determine the type of a file based on extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type category (images, documents, music, videos, archives, or unknown)
        """
        ext = Path(file_path).suffix.lower().lstrip('.')
        file_types = self.config.get('file_types', {})
        
        for category, extensions in file_types.items():
            if ext in extensions:
                return category
        
        return 'unknown'
    
    def generate_new_filename(self, file_path: str, file_type: str) -> str:
        """
        Generate new filename based on metadata and naming pattern
        
        Args:
            file_path: Path to the file
            file_type: Type of the file
            
        Returns:
            New filename
        """
        metadata = self.metadata_extractor.extract(file_path)
        
        # Get naming pattern for this file type
        patterns = self.config.get('naming_patterns', {})
        pattern = patterns.get(file_type, patterns.get('default', '{filename}.{ext}'))
        
        # Replace placeholders with metadata
        try:
            new_name = pattern.format(**metadata)
            # Clean up invalid filename characters
            new_name = self._sanitize_filename(new_name)
            return new_name
        except KeyError:
            # If metadata is missing, fall back to original filename
            return Path(file_path).name
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Remove invalid characters from filename
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def get_destination_folder(self, file_type: str) -> Optional[str]:
        """
        Get destination folder for a file type
        
        Args:
            file_type: Type of the file
            
        Returns:
            Destination folder path or None if not configured
        """
        destinations = self.config.get('destinations', {})
        
        if file_type in destinations:
            dest_list = destinations[file_type]
            if dest_list and len(dest_list) > 0:
                return dest_list[0]
        
        return None
    
    def calculate_file_hash(self, file_path: str, chunk_size: int = 8192) -> str:
        """
        Calculate SHA256 hash of a file
        
        Args:
            file_path: Path to the file
            chunk_size: Size of chunks to read
            
        Returns:
            Hexadecimal hash string
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def find_duplicates(self, file_path: str, search_dir: str) -> List[str]:
        """
        Find duplicate files in a directory
        
        Args:
            file_path: Path to the file to check
            search_dir: Directory to search for duplicates
            
        Returns:
            List of paths to duplicate files
        """
        duplicates = []
        
        if not os.path.exists(search_dir):
            return duplicates
        
        compare_method = self.config.get('duplicate_detection.compare_method', 'hash')
        file_size = os.path.getsize(file_path)
        file_hash = None
        
        if compare_method in ['hash', 'both']:
            file_hash = self.calculate_file_hash(file_path)
        
        # Search for duplicates
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                other_path = os.path.join(root, file)
                
                # Skip the file itself
                if os.path.samefile(file_path, other_path):
                    continue
                
                # Check if it's a duplicate
                if compare_method == 'size':
                    if os.path.getsize(other_path) == file_size:
                        duplicates.append(other_path)
                elif compare_method == 'hash':
                    if self.calculate_file_hash(other_path) == file_hash:
                        duplicates.append(other_path)
                elif compare_method == 'both':
                    if (os.path.getsize(other_path) == file_size and
                        self.calculate_file_hash(other_path) == file_hash):
                        duplicates.append(other_path)
        
        return duplicates
    
    def move_file(self, source: str, destination_dir: str, new_filename: Optional[str] = None) -> str:
        """
        Move a file to a destination directory
        
        Args:
            source: Source file path
            destination_dir: Destination directory
            new_filename: Optional new filename
            
        Returns:
            Path to the moved file
        """
        # Create destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)
        
        # Determine destination filename
        if new_filename is None:
            new_filename = Path(source).name
        
        destination = os.path.join(destination_dir, new_filename)
        
        # Handle name conflicts
        if os.path.exists(destination):
            base, ext = os.path.splitext(new_filename)
            counter = 1
            while os.path.exists(destination):
                new_filename = f"{base}_{counter}{ext}"
                destination = os.path.join(destination_dir, new_filename)
                counter += 1
        
        # Move the file
        shutil.move(source, destination)
        return destination
    
    def quarantine_file(self, file_path: str) -> str:
        """
        Move a file to quarantine folder
        
        Args:
            file_path: Path to the file
            
        Returns:
            Path to the quarantined file
        """
        quarantine_dir = self.config.get('quarantine_folder', '~/Downloads/Quarantine')
        return self.move_file(file_path, quarantine_dir)
    
    def delete_file(self, file_path: str) -> None:
        """
        Delete a file
        
        Args:
            file_path: Path to the file
        """
        if os.path.exists(file_path):
            os.remove(file_path)
