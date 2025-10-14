"""
Unit tests for MetadataExtractor
"""
import unittest
import tempfile
import shutil
import os

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dl_assistant.metadata import MetadataExtractor


class TestMetadataExtractor(unittest.TestCase):
    """Test metadata extraction"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.extractor = MetadataExtractor(use_vision=False)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_extract_basic_metadata(self):
        """Test extracting basic file metadata"""
        # Create test file
        test_file = os.path.join(self.test_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        # Extract metadata
        metadata = self.extractor.extract(test_file)
        
        # Check basic fields
        self.assertEqual(metadata['filename'], 'test')
        self.assertEqual(metadata['ext'], 'txt')
        self.assertIn('date', metadata)
        self.assertIn('time', metadata)
        self.assertIn('size', metadata)
        self.assertIn('created', metadata)
        self.assertIn('modified', metadata)
    
    def test_extract_from_different_extensions(self):
        """Test metadata extraction from various file types"""
        extensions = ['txt', 'jpg', 'pdf', 'mp3', 'wave']
        
        for ext in extensions:
            test_file = os.path.join(self.test_dir, f'test.{ext}')
            with open(test_file, 'w') as f:
                f.write('dummy content')
            
            metadata = self.extractor.extract(test_file)
            self.assertEqual(metadata['ext'], ext)


if __name__ == '__main__':
    unittest.main()
