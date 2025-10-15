"""
Vision analysis for images and videos using AI
"""
import os
import base64
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import json

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


class VisionAnalyzer:
    """Analyze images and videos using AI vision capabilities"""
    
    def __init__(self):
        """Initialize vision analyzer"""
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.client = None
        if self.api_key and HAS_OPENAI:
            self.client = OpenAI(api_key=self.api_key)
    
    def analyze_media(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze an image or video file using AI vision
        
        Args:
            file_path: Path to the media file
            
        Returns:
            Dictionary containing analysis results
        """
        if not self.client:
            return {}
        
        ext = Path(file_path).suffix.lower().lstrip('.')
        
        # For videos, extract a frame first
        if ext in ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm']:
            return self._analyze_video(file_path)
        elif ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
            return self._analyze_image(file_path)
        
        return {}
    
    def _analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze an image file
        
        Args:
            image_path: Path to the image
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Encode image to base64
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this image and provide information in JSON format:
{
  "description": "Brief description of the image",
  "artist": "Artist name if visible (or null)",
  "title": "Title/song name if visible (or null)",
  "content_type": "Type: Photo, Album Art, Concert, etc.",
  "is_explicit": false or true if explicit content detected
}"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            # Parse response
            result_text = response.choices[0].message.content
            # Try to extract JSON from the response
            if '{' in result_text and '}' in result_text:
                json_start = result_text.find('{')
                json_end = result_text.rfind('}') + 1
                json_str = result_text[json_start:json_end]
                result = json.loads(json_str)
                return self._normalize_metadata(result)
            
        except Exception as e:
            # Silently fail and return empty dict
            pass
        
        return {}
    
    def _analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Analyze a video file by extracting frames and analyzing them
        
        Args:
            video_path: Path to the video
            
        Returns:
            Dictionary with analysis results
        """
        if not HAS_CV2:
            return {}
        
        try:
            # Extract a frame from the video (at 10% position)
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return {}
            
            # Get total frames and seek to 10% position
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            target_frame = int(total_frames * 0.1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return {}
            
            # Save frame to temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                tmp_path = tmp_file.name
                cv2.imwrite(tmp_path, frame)
            
            try:
                # Encode frame to base64
                with open(tmp_path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                
                # Call OpenAI Vision API with video-specific prompt
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": """Analyze this video frame and provide information in JSON format:
{
  "description": "Brief description of what's in the video",
  "artist": "Artist/performer name if visible (or null)",
  "title": "Song/video title if visible (or null)",
  "content_type": "One of: Music Video, Karaoke, Lyric Video, Background Video, Background FX Video, Slideshow, Concert, Performance, Tutorial, Other",
  "is_explicit": false or true if explicit content/language visible,
  "video_category": "More specific category if applicable"
}

Look for text, artist names, song titles, karaoke-style lyrics, or music video characteristics.
Note: Background FX Video refers to videos with visual effects, animations, or motion graphics typically used as background content."""
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_data}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500
                )
                
                # Parse response
                result_text = response.choices[0].message.content
                # Try to extract JSON from the response
                if '{' in result_text and '}' in result_text:
                    json_start = result_text.find('{')
                    json_end = result_text.rfind('}') + 1
                    json_str = result_text[json_start:json_end]
                    result = json.loads(json_str)
                    return self._normalize_metadata(result)
                
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
        except Exception as e:
            # Silently fail and return empty dict
            pass
        
        return {}
    
    def _normalize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize metadata from vision analysis
        
        Args:
            metadata: Raw metadata from vision API
            
        Returns:
            Normalized metadata dictionary
        """
        result = {}
        
        # Extract artist
        if metadata.get('artist'):
            result['artist'] = str(metadata['artist'])
        
        # Extract title
        if metadata.get('title'):
            result['title'] = str(metadata['title'])
        
        # Extract content type and normalize it
        if metadata.get('content_type'):
            content_type = str(metadata['content_type'])
            result['content_type'] = content_type
            
            # Also set a sanitized version for filenames
            result['video_type'] = self._sanitize_content_type(content_type)
        
        # Extract explicit flag
        if 'is_explicit' in metadata:
            result['is_explicit'] = bool(metadata['is_explicit'])
            result['content_rating'] = 'Explicit' if result['is_explicit'] else 'Clean'
        
        # Extract description
        if metadata.get('description'):
            result['description'] = str(metadata['description'])
        
        return result
    
    def _sanitize_content_type(self, content_type: str) -> str:
        """
        Sanitize content type for use in filenames
        
        Args:
            content_type: Raw content type string
            
        Returns:
            Sanitized content type
        """
        # Map common variations to standard names
        type_map = {
            'music video': 'Music Video',
            'musicvideo': 'Music Video',
            'karaoke': 'Karaoke',
            'lyric video': 'Lyric Video',
            'lyrics video': 'Lyric Video',
            'background video': 'Background Video',
            'background fx video': 'Background FX',
            'background fx': 'Background FX',
            'backgroundfx': 'Background FX',
            'slideshow': 'Slideshow',
            'concert': 'Concert',
            'performance': 'Performance',
            'live performance': 'Live',
            'tutorial': 'Tutorial',
        }
        
        lower_type = content_type.lower().strip()
        return type_map.get(lower_type, content_type)
