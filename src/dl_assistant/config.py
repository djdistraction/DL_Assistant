"""
Configuration manager for DL_Assistant
"""
import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Path to configuration directory (default: ./config)
        """
        if config_dir is None:
            config_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "config"
            )
        
        self.config_dir = Path(config_dir)
        self.default_config_path = self.config_dir / "default_config.yaml"
        self.user_config_path = self.config_dir / "user_config.json"
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from files"""
        # Load default config
        config = {}
        if self.default_config_path.exists():
            with open(self.default_config_path, 'r') as f:
                config = yaml.safe_load(f)
        
        # Override with user config if exists
        if self.user_config_path.exists():
            with open(self.user_config_path, 'r') as f:
                user_config = json.load(f)
                config.update(user_config)
        
        # Expand paths
        config = self._expand_paths(config)
        
        return config
    
    def _expand_paths(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Expand ~ and environment variables in paths"""
        if isinstance(config, dict):
            for key, value in config.items():
                if isinstance(value, str) and ('/' in value or '~' in value):
                    config[key] = os.path.expanduser(os.path.expandvars(value))
                elif isinstance(value, (dict, list)):
                    config[key] = self._expand_paths(value)
        elif isinstance(config, list):
            config = [self._expand_paths(item) if isinstance(item, (dict, list, str)) 
                     else item for item in config]
            config = [os.path.expanduser(os.path.expandvars(item)) if isinstance(item, str) 
                     and ('/' in item or '~' in item) else item for item in config]
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key (supports dot notation like 'monitoring.enabled')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value (saves to user config)
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent dict
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save user config
        self._save_user_config()
    
    def _save_user_config(self) -> None:
        """Save current configuration to user config file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.user_config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self.config.copy()
