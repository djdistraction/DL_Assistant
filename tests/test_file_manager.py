"""
Unit tests for FileManager
"""
import unittest
import tempfile
import shutil
import os
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dl_assistant.config import ConfigManager
from dl_assistant.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    """Test file manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = os.path.join(self.test_dir, 'config')
        os.makedirs(self.config_dir)
        
        # Create minimal config
        config_data = {
            'file_types': {
                'images': ['jpg', 'png'],
                'documents': ['pdf', 'txt']
            },
            'naming_patterns': {
                'images': '{filename}.{ext}',
                'default': '{filename}.{ext}'
            },
            'destinations': {
                'images': [os.path.join(self.test_dir, 'Pictures')],
                'documents': [os.path.join(self.test_dir, 'Documents')]
            },
            'duplicate_detection': {
                'enabled': True,
                'compare_method': 'hash'
            }
        }
        
        import yaml
        with open(os.path.join(self.config_dir, 'default_config.yaml'), 'w') as f:
            yaml.dump(config_data, f)
        
        self.config = ConfigManager(self.config_dir)
        self.file_manager = FileManager(self.config)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_get_file_type(self):
        """Test file type detection"""
        self.assertEqual(self.file_manager.get_file_type('test.jpg'), 'images')
        self.assertEqual(self.file_manager.get_file_type('test.png'), 'images')
        self.assertEqual(self.file_manager.get_file_type('test.pdf'), 'documents')
        self.assertEqual(self.file_manager.get_file_type('test.xyz'), 'unknown')
    
    def test_get_destination_folder(self):
        """Test getting destination folder"""
        dest = self.file_manager.get_destination_folder('images')
        self.assertIsNotNone(dest)
        self.assertIn('Pictures', dest)
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        clean = self.file_manager._sanitize_filename('test<>:file.txt')
        self.assertNotIn('<', clean)
        self.assertNotIn('>', clean)
        self.assertNotIn(':', clean)
    
    def test_move_file(self):
        """Test moving files"""
        # Create test file
        source = os.path.join(self.test_dir, 'test.txt')
        with open(source, 'w') as f:
            f.write('test content')
        
        # Move file
        dest_dir = os.path.join(self.test_dir, 'destination')
        result = self.file_manager.move_file(source, dest_dir, 'newname.txt')
        
        self.assertTrue(os.path.exists(result))
        self.assertFalse(os.path.exists(source))
        self.assertEqual(os.path.basename(result), 'newname.txt')
    
    def test_calculate_file_hash(self):
        """Test file hash calculation"""
        # Create test file
        test_file = os.path.join(self.test_dir, 'test.txt')
        content = 'test content for hashing'
        with open(test_file, 'w') as f:
            f.write(content)
        
        # Calculate hash
        hash1 = self.file_manager.calculate_file_hash(test_file)
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 64)  # SHA256 produces 64 hex chars
        
        # Same file should produce same hash
        hash2 = self.file_manager.calculate_file_hash(test_file)
        self.assertEqual(hash1, hash2)
    
    def test_find_duplicates(self):
        """Test duplicate detection"""
        # Create original file
        search_dir = os.path.join(self.test_dir, 'search')
        os.makedirs(search_dir)
        
        original = os.path.join(search_dir, 'original.txt')
        with open(original, 'w') as f:
            f.write('duplicate content')
        
        # Create duplicate
        duplicate = os.path.join(self.test_dir, 'duplicate.txt')
        with open(duplicate, 'w') as f:
            f.write('duplicate content')
        
        # Find duplicates
        duplicates = self.file_manager.find_duplicates(duplicate, search_dir)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0], original)


if __name__ == '__main__':
    unittest.main()
