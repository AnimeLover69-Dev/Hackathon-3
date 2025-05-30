#!/usr/bin/env python3
"""
YouTube Video Downloader and Audio Extractor
This script downloads YouTube videos and extracts their audio to MP3 format.
"""

import os
import sys
from enum import Enum, auto
from typing import Optional

class Color(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

class DownloadOption(Enum):
    VIDEO_AND_AUDIO = auto()
    AUDIO_ONLY = auto()
    QUIT = auto()

def print_colored(message: str, color: Color) -> None:
    """Print colored text to the console."""
    print(f"{color.value}{message}{Color.RESET.value}")

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner() -> None:
    """Display the program banner."""
    clear_screen()
    print_colored("\n" + "=" * 50, Color.BLUE)
    print_colored("YouTube Video Downloader & Audio Extractor", Color.CYAN)
    print_colored("=" * 50 + "\n", Color.BLUE)

def get_user_url() -> Optional[str]:
    """Get YouTube URL from user input."""
    while True:
        url = input("Enter YouTube URL (or 'q' to quit): ").strip()
        
        if url.lower() == 'q':
            return None
            
        if not url:
            print_colored("Please enter a valid URL.", Color.RED)
            continue
            
        return url

def get_download_option() -> DownloadOption:
    """Get download option from user."""
    while True:
        print_colored("\nDownload options:", Color.CYAN)
        print_colored("1. Download video and extract audio", Color.CYAN)
        print_colored("2. Download audio only", Color.CYAN)
        print_colored("3. Quit", Color.CYAN)
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            return DownloadOption.VIDEO_AND_AUDIO
        elif choice == '2':
            return DownloadOption.AUDIO_ONLY
        elif choice == '3':
            return DownloadOption.QUIT
        else:
            print_colored("Invalid choice. Please enter 1, 2, or 3.", Color.RED)

def process_download(url: str, option: DownloadOption) -> None:
    """Process the download based on user's option."""
    try:
        downloader = YouTubeDownloader(url)
        print_colored("\nFetching video information...", Color.YELLOW)
        downloader.get_video_info()
        
        if option == DownloadOption.VIDEO_AND_AUDIO:
            video_path = downloader.download_video()
            if video_path:
                audio_path = downloader.extract_audio(video_path)
                if audio_path:
                    print_colored(f"\n✓ Success! Audio saved to: {audio_path}", Color.GREEN)
        elif option == DownloadOption.AUDIO_ONLY:
            audio_path = downloader.download_audio_only()
            if audio_path:
                print_colored(f"\n✓ Success! Audio saved to: {audio_path}", Color.GREEN)
                
    except Exception as e:
        print_colored(f"\nError: {str(e)}", Color.RED)

def main() -> None:
    """Main program loop."""
    display_banner()
    
    while True:
        url = get_user_url()
        if url is None:
            print_colored("\nThank you for using the YouTube Downloader. Goodbye!", Color.GREEN)
            break
            
        option = get_download_option()
        if option == DownloadOption.QUIT:
            print_colored("\nOperation cancelled. Returning to URL input...", Color.YELLOW)
            continue
            
        process_download(url, option)
        print_colored("\n" + "─" * 50 + "\n", Color.BLUE)

if __name__ == "__main__":
    try:
        # Add your imports here (they were missing in the original code)
        from downloader import YouTubeDownloader
        from utils import setup_environment
        
        setup_environment()  # Assuming this sets up necessary directories
        main()
    except KeyboardInterrupt:
        print_colored("\nOperation cancelled by user. Exiting...", Color.YELLOW)
        sys.exit(0)
    except Exception as e:
        print_colored(f"\nFatal error: {str(e)}", Color.RED)
        sys.exit(1)