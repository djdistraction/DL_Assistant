"""
Main entry point for DL_Assistant
"""
import sys
import logging
import argparse
import time
from pathlib import Path

from .config import ConfigManager
from .file_manager import FileManager
from .watcher import FileWatcher
from .dashboard import run_dashboard


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='DL Assistant - Download Folder Management Assistant'
    )
    parser.add_argument(
        '--mode',
        choices=['monitor', 'dashboard', 'process'],
        default='monitor',
        help='Operation mode: monitor (watch folder), dashboard (web UI), or process (one-time processing)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration directory'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Dashboard host (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Dashboard port (default: 5000)'
    )
    
    args = parser.parse_args()
    
    # Initialize configuration
    config = ConfigManager(args.config)
    file_manager = FileManager(config)
    
    try:
        if args.mode == 'dashboard':
            # Run web dashboard
            logger.info("Starting dashboard...")
            run_dashboard(config, host=args.host, port=args.port)
        
        elif args.mode == 'process':
            # Process existing files once
            logger.info("Processing existing files...")
            watcher = FileWatcher(config, file_manager)
            watcher.start()
            watcher.process_existing_files()
            watcher.stop()
            logger.info("Processing complete")
        
        else:  # monitor mode
            # Start file watcher
            logger.info("Starting file watcher...")
            watcher = FileWatcher(config, file_manager)
            watcher.start()
            
            # Process existing files first if configured
            logger.info("Processing existing files...")
            watcher.process_existing_files()
            
            logger.info("Monitoring downloads folder. Press Ctrl+C to stop.")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Stopping...")
                watcher.stop()
    
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
