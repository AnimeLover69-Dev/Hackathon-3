"""
Utility functions for the YouTube Downloader application.
"""

import os
import re
from enum import Enum

class Color:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_colored(text, color):
    """Print text in specified color."""
    print(f"{color}{text}{Color.END}")

def create_progress_bar(progress, prefix="", length=50):
    """Create a progress bar string."""
    filled_length = int(length * progress)
    bar = "█" * filled_length + "░" * (length - filled_length)
    percentage = int(progress * 100)
    print(f"\r{prefix}|{bar}| {percentage}%", end="", flush=True)

def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove or replace other problematic characters
    filename = re.sub(r'[\x00-\x1f]', '', filename)
    # Limit length
    return filename[:200].strip()

def setup_environment():
    """Create necessary directories for downloads."""
    # Create base downloads directory
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    
    # Create subdirectories for videos and audio
    video_dir = os.path.join(downloads_dir, "videos")
    audio_dir = os.path.join(downloads_dir, "audio")
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)