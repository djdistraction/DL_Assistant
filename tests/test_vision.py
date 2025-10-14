"""
Unit tests for VisionAnalyzer
"""
import unittest
import tempfile
import shutil
import os

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dl_assistant.vision import VisionAnalyzer


class TestVisionAnalyzer(unittest.TestCase):
    """Test vision analyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.analyzer = VisionAnalyzer()
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test vision analyzer initialization"""
        # Should initialize without error
        analyzer = VisionAnalyzer()
        self.assertIsNotNone(analyzer)
    
    def test_analyze_without_api_key(self):
        """Test that analyze_media returns empty dict without API key"""
        # Create a dummy image file
        test_file = os.path.join(self.test_dir, 'test.jpg')
        with open(test_file, 'w') as f:
            f.write('dummy image data')
        
        # Save original API key state
        original_key = os.environ.get('OPENAI_API_KEY')
        
        try:
            # Remove API key if present
            if 'OPENAI_API_KEY' in os.environ:
                del os.environ['OPENAI_API_KEY']
            
            # Create analyzer without API key
            analyzer = VisionAnalyzer()
            result = analyzer.analyze_media(test_file)
            
            # Should return empty dict
            self.assertEqual(result, {})
        finally:
            # Restore original API key
            if original_key:
                os.environ['OPENAI_API_KEY'] = original_key
    
    def test_normalize_metadata(self):
        """Test metadata normalization"""
        raw_metadata = {
            'artist': 'Test Artist',
            'title': 'Test Song',
            'content_type': 'Music Video',
            'is_explicit': False,
            'description': 'A test music video'
        }
        
        normalized = self.analyzer._normalize_metadata(raw_metadata)
        
        self.assertEqual(normalized['artist'], 'Test Artist')
        self.assertEqual(normalized['title'], 'Test Song')
        self.assertEqual(normalized['content_type'], 'Music Video')
        self.assertEqual(normalized['video_type'], 'Music Video')
        self.assertEqual(normalized['content_rating'], 'Clean')
        self.assertFalse(normalized['is_explicit'])
    
    def test_normalize_metadata_explicit(self):
        """Test metadata normalization with explicit content"""
        raw_metadata = {
            'artist': 'Test Artist',
            'title': 'Test Song',
            'is_explicit': True
        }
        
        normalized = self.analyzer._normalize_metadata(raw_metadata)
        
        self.assertEqual(normalized['content_rating'], 'Explicit')
        self.assertTrue(normalized['is_explicit'])
    
    def test_sanitize_content_type(self):
        """Test content type sanitization"""
        test_cases = {
            'Music Video': 'Music Video',
            'music video': 'Music Video',
            'musicvideo': 'Music Video',
            'Karaoke': 'Karaoke',
            'karaoke': 'Karaoke',
            'Lyric Video': 'Lyric Video',
            'lyric video': 'Lyric Video',
            'Background Video': 'Background Video',
            'background video': 'Background Video',
            'Slideshow': 'Slideshow',
            'slideshow': 'Slideshow',
            'Concert': 'Concert',
            'Live Performance': 'Live',
            'Tutorial': 'Tutorial',
            'Unknown Type': 'Unknown Type',  # Should return as-is if not in map
        }
        
        for input_type, expected_output in test_cases.items():
            result = self.analyzer._sanitize_content_type(input_type)
            self.assertEqual(result, expected_output, 
                           f"Failed for input: {input_type}")


if __name__ == '__main__':
    unittest.main()
