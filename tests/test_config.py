"""
Unit tests for ConfigManager
"""
import unittest
import tempfile
import shutil
import os
import json
import yaml
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dl_assistant.config import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test configuration manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        
        # Create test default config
        self.default_config = {
            'downloads_folder': '~/Downloads',
            'monitoring': {
                'enabled': True,
                'check_interval': 5
            }
        }
        
        default_config_path = os.path.join(self.test_dir, 'default_config.yaml')
        with open(default_config_path, 'w') as f:
            yaml.dump(self.default_config, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_load_default_config(self):
        """Test loading default configuration"""
        config = ConfigManager(self.test_dir)
        self.assertEqual(config.get('downloads_folder'), os.path.expanduser('~/Downloads'))
        self.assertTrue(config.get('monitoring.enabled'))
    
    def test_get_nested_value(self):
        """Test getting nested configuration values"""
        config = ConfigManager(self.test_dir)
        self.assertTrue(config.get('monitoring.enabled'))
        self.assertEqual(config.get('monitoring.check_interval'), 5)
    
    def test_get_with_default(self):
        """Test getting with default value"""
        config = ConfigManager(self.test_dir)
        self.assertEqual(config.get('nonexistent.key', 'default'), 'default')
    
    def test_set_value(self):
        """Test setting configuration value"""
        config = ConfigManager(self.test_dir)
        config.set('monitoring.enabled', False)
        self.assertFalse(config.get('monitoring.enabled'))
    
    def test_user_config_persistence(self):
        """Test that user config is saved and loaded"""
        config = ConfigManager(self.test_dir)
        config.set('test_key', 'test_value')
        
        # Create new config manager to test loading
        config2 = ConfigManager(self.test_dir)
        self.assertEqual(config2.get('test_key'), 'test_value')


if __name__ == '__main__':
    unittest.main()
