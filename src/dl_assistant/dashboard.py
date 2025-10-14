"""
Web dashboard for DL_Assistant configuration
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from pathlib import Path

from .config import ConfigManager


def create_app(config_manager: ConfigManager):
    """
    Create Flask application
    
    Args:
        config_manager: ConfigManager instance
        
    Returns:
        Flask app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    
    # Store config manager in app context
    app.config_manager = config_manager
    
    @app.route('/')
    def index():
        """Dashboard home page"""
        config = config_manager.get_all()
        return render_template('index.html', config=config)
    
    @app.route('/api/config', methods=['GET'])
    def get_config():
        """Get current configuration"""
        return jsonify(config_manager.get_all())
    
    @app.route('/api/config', methods=['POST'])
    def update_config():
        """Update configuration"""
        data = request.json
        
        try:
            for key, value in data.items():
                config_manager.set(key, value)
            return jsonify({'success': True, 'message': 'Configuration updated'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    @app.route('/api/config/<path:key>', methods=['GET'])
    def get_config_value(key):
        """Get specific configuration value"""
        value = config_manager.get(key)
        return jsonify({'key': key, 'value': value})
    
    @app.route('/api/config/<path:key>', methods=['PUT'])
    def set_config_value(key):
        """Set specific configuration value"""
        data = request.json
        
        try:
            config_manager.set(key, data.get('value'))
            return jsonify({'success': True, 'message': f'Updated {key}'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    @app.route('/api/folders/quarantine', methods=['GET'])
    def list_quarantine():
        """List files in quarantine folder"""
        quarantine_folder = config_manager.get('quarantine_folder')
        
        if not os.path.exists(quarantine_folder):
            return jsonify({'files': []})
        
        files = []
        for filename in os.listdir(quarantine_folder):
            file_path = os.path.join(quarantine_folder, filename)
            if os.path.isfile(file_path):
                files.append({
                    'name': filename,
                    'size': os.path.getsize(file_path),
                    'modified': os.path.getmtime(file_path)
                })
        
        return jsonify({'files': files})
    
    return app


def run_dashboard(config_manager: ConfigManager, host: str = '127.0.0.1', port: int = 5000):
    """
    Run the web dashboard
    
    Args:
        config_manager: ConfigManager instance
        host: Host to bind to
        port: Port to bind to
    """
    app = create_app(config_manager)
    app.run(host=host, port=port, debug=False)
