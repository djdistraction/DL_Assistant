"""
File system monitoring for DL_Assistant
"""
import os
import time
import logging
from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from .file_manager import FileManager

logger = logging.getLogger(__name__)


class DownloadHandler(FileSystemEventHandler):
    """Handles file system events in the downloads folder"""
    
    def __init__(self, config, file_manager: FileManager, process_callback: Optional[Callable] = None):
        """
        Initialize download handler
        
        Args:
            config: ConfigManager instance
            file_manager: FileManager instance
            process_callback: Optional callback function for processing files
        """
        super().__init__()
        self.config = config
        self.file_manager = file_manager
        self.process_callback = process_callback
        self.processing = set()  # Track files being processed
    
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        # Ignore hidden and temp files if configured
        file_path = event.src_path
        filename = os.path.basename(file_path)
        
        if self.config.get('monitoring.ignore_hidden', True) and filename.startswith('.'):
            return
        
        if self.config.get('monitoring.ignore_temp', True):
            if filename.endswith('.tmp') or filename.endswith('.crdownload') or filename.endswith('.part'):
                return
        
        # Wait a bit for the file to finish writing
        self._wait_for_file_ready(file_path)
        
        # Process the file
        if file_path not in self.processing:
            self.processing.add(file_path)
            try:
                self.process_file(file_path)
            finally:
                self.processing.discard(file_path)
    
    def _wait_for_file_ready(self, file_path: str, timeout: int = 30) -> bool:
        """
        Wait for a file to be fully written
        
        Args:
            file_path: Path to the file
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if file is ready, False if timeout
        """
        start_time = time.time()
        last_size = -1
        
        while time.time() - start_time < timeout:
            try:
                current_size = os.path.getsize(file_path)
                if current_size == last_size and current_size > 0:
                    # Size hasn't changed, file is likely ready
                    time.sleep(0.5)  # Extra wait to be safe
                    return True
                last_size = current_size
                time.sleep(1)
            except (OSError, FileNotFoundError):
                time.sleep(1)
        
        return False
    
    def process_file(self, file_path: str) -> None:
        """
        Process a new file
        
        Args:
            file_path: Path to the file
        """
        logger.info(f"Processing file: {file_path}")
        
        try:
            # Check if file still exists
            if not os.path.exists(file_path):
                return
            
            # Get file type
            file_type = self.file_manager.get_file_type(file_path)
            logger.info(f"File type: {file_type}")
            
            # Check for duplicates
            if self.config.get('duplicate_detection.enabled', True):
                destination = self.file_manager.get_destination_folder(file_type)
                if destination:
                    duplicates = self.file_manager.find_duplicates(file_path, destination)
                    if duplicates:
                        logger.info(f"Duplicate found: {duplicates[0]}")
                        if self.config.get('duplicate_detection.keep_newest', True):
                            # Keep the newer file
                            if os.path.getmtime(file_path) > os.path.getmtime(duplicates[0]):
                                self.file_manager.delete_file(duplicates[0])
                                logger.info(f"Deleted older duplicate: {duplicates[0]}")
                            else:
                                self.file_manager.delete_file(file_path)
                                logger.info(f"Deleted older file: {file_path}")
                                return
                        else:
                            # Delete the new file
                            self.file_manager.delete_file(file_path)
                            logger.info(f"Deleted duplicate: {file_path}")
                            return
            
            # Generate new filename
            new_filename = self.file_manager.generate_new_filename(file_path, file_type)
            logger.info(f"New filename: {new_filename}")
            
            # Get destination
            destination = self.file_manager.get_destination_folder(file_type)
            
            if destination:
                # Move file to destination
                new_path = self.file_manager.move_file(file_path, destination, new_filename)
                logger.info(f"Moved to: {new_path}")
            elif self.config.get('quarantine.enabled', True):
                # Quarantine if destination not clear
                new_path = self.file_manager.quarantine_file(file_path)
                logger.info(f"Quarantined to: {new_path}")
            
            # Call callback if provided
            if self.process_callback:
                self.process_callback(file_path, new_path if destination else None)
                
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")


class FileWatcher:
    """Monitors the downloads folder for new files"""
    
    def __init__(self, config, file_manager: FileManager):
        """
        Initialize file watcher
        
        Args:
            config: ConfigManager instance
            file_manager: FileManager instance
        """
        self.config = config
        self.file_manager = file_manager
        self.observer = None
        self.handler = None
    
    def start(self, process_callback: Optional[Callable] = None) -> None:
        """
        Start monitoring the downloads folder
        
        Args:
            process_callback: Optional callback function for processing files
        """
        downloads_folder = self.config.get('downloads_folder')
        
        # Create downloads folder if it doesn't exist
        os.makedirs(downloads_folder, exist_ok=True)
        
        # Set up event handler
        self.handler = DownloadHandler(self.config, self.file_manager, process_callback)
        
        # Set up observer
        self.observer = Observer()
        self.observer.schedule(self.handler, downloads_folder, recursive=False)
        self.observer.start()
        
        logger.info(f"Started monitoring: {downloads_folder}")
    
    def stop(self) -> None:
        """Stop monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Stopped monitoring")
    
    def process_existing_files(self) -> None:
        """Process all existing files in the downloads folder"""
        downloads_folder = self.config.get('downloads_folder')
        
        if not os.path.exists(downloads_folder):
            return
        
        for filename in os.listdir(downloads_folder):
            file_path = os.path.join(downloads_folder, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Skip hidden files if configured
            if self.config.get('monitoring.ignore_hidden', True) and filename.startswith('.'):
                continue
            
            # Process the file
            if self.handler:
                self.handler.process_file(file_path)
