#!/usr/bin/env python3
"""
Utility functions for the YouTube downloader.
"""

import os
import re
import sys

class Color:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_colored(text, color):
    """Print text with specified color."""
    print(f"{color}{text}{Color.RESET}")

def create_progress_bar(progress, width=50, prefix=""):
    """Create a text-based progress bar."""
    filled_length = int(width * progress)
    bar = '█' * filled_length + '░' * (width - filled_length)
    percentage = int(100 * progress)
    
    # Clear the current line and print the progress bar
    sys.stdout.write('\r')
    sys.stdout.write(f"{prefix}|{bar}| {percentage}%")
    sys.stdout.flush()

def setup_environment():
    """Set up the necessary directories for downloads."""
    # Create the main downloads directory
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        
    # Create subdirectories for videos and audio
    video_dir = os.path.join(downloads_dir, "videos")
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
        
    audio_dir = os.path.join(downloads_dir, "audio")
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        
    return downloads_dir, video_dir, audio_dir

def sanitize_filename(filename):
    """Remove illegal characters from filename."""
    # Replace illegal characters with underscore
    sanitized = re.sub(r'[\\/*?:"<>|]', "_", filename)
    # Remove any leading/trailing spaces
    sanitized = sanitized.strip()
    # Limit length to avoid too long filenames
    if len(sanitized) > 100:
        sanitized = sanitized[:97] + "..."
    return sanitized