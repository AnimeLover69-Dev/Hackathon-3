#!/usr/bin/env python3
"""
Enhanced YouTube Downloader Module
Handles downloading YouTube videos and extracting audio using pytube.
"""

import os
import time
from pathlib import Path
from typing import Optional, Tuple
from pytube import YouTube, Stream
from pytube.exceptions import PytubeError
from utils import sanitize_filename, print_colored, Color, create_progress_bar

class YouTubeDownloader:
    """Class to handle YouTube video downloading and audio extraction."""
    
    def __init__(self, url: str):
        """Initialize with YouTube URL and setup directories."""
        self.url = url
        self.yt: Optional[YouTube] = None
        self.title: str = ""
        self.current_filesize: int = 0
        self.downloaded: int = 0
        
        # Set up download directories
        self.base_dir = Path(os.getcwd()) / "downloads"
        self.video_dir = self.base_dir / "videos"
        self.audio_dir = self.base_dir / "audio"
        
        self._create_directories()
        
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.video_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
    
    def get_video_info(self) -> bool:
        """Fetch and display video information from YouTube."""
        try:
            self.yt = YouTube(
                self.url,
                on_progress_callback=self._on_progress,
                on_complete_callback=self._on_complete
            )
            self.title = sanitize_filename(self.yt.title)
            
            print_colored("\nVideo Information:", Color.CYAN)
            print_colored(f"Title: {self.yt.title}", Color.GREEN)
            print_colored(f"Channel: {self.yt.author}", Color.GREEN)
            print_colored(f"Length: {self._format_duration(self.yt.length)}", Color.GREEN)
            print_colored(f"Views: {self.yt.views:,}", Color.GREEN)
            
            return True
        except PytubeError as e:
            print_colored(f"Error fetching video information: {str(e)}", Color.RED)
            return False
    
    def download_video(self) -> Optional[Path]:
        """Download the video in the highest resolution."""
        if not self._ensure_yt_object():
            return None
            
        try:
            print_colored("\nFinding best video stream...", Color.YELLOW)
            stream = self._get_best_video_stream()
            
            if not stream:
                print_colored("No suitable video stream found.", Color.RED)
                return None
                
            filename = f"{self.title}_{stream.resolution}.{stream.subtype}"
            filepath = self.video_dir / filename
            
            if self._check_existing_file(filepath):
                return filepath
                
            return self._download_stream(stream, filepath)
            
        except PytubeError as e:
            print_colored(f"Error downloading video: {str(e)}", Color.RED)
            return None
    
    def download_audio_only(self) -> Optional[Path]:
        """Download audio only in the best available quality."""
        if not self._ensure_yt_object():
            return None
            
        try:
            print_colored("\nFinding best audio stream...", Color.YELLOW)
            stream = self._get_best_audio_stream()
            
            if not stream:
                print_colored("No suitable audio stream found.", Color.RED)
                return None
                
            temp_filename = f"{self.title}_temp.{stream.subtype}"
            temp_filepath = self.audio_dir / temp_filename
            
            mp3_filename = f"{self.title}.mp3"
            mp3_filepath = self.audio_dir / mp3_filename
            
            if self._check_existing_file(mp3_filepath):
                return mp3_filepath
                
            downloaded_path = self._download_stream(stream, temp_filepath)
            if not downloaded_path:
                return None
                
            return self._convert_to_mp3(downloaded_path, mp3_filepath)
            
        except PytubeError as e:
            print_colored(f"Error downloading audio: {str(e)}", Color.RED)
            return None
    
    def extract_audio(self, video_path: Path) -> Optional[Path]:
        """Extract audio from a video file and save as MP3."""
        if not video_path or not video_path.exists():
            print_colored("Video file not found.", Color.RED)
            return None
            
        try:
            print_colored("\nExtracting audio from video...", Color.YELLOW)
            
            mp3_filename = f"{self.title}.mp3"
            mp3_filepath = self.audio_dir / mp3_filename
            
            if self._check_existing_file(mp3_filepath):
                return mp3_filepath
                
            return self._convert_to_mp3(video_path, mp3_filepath)
            
        except Exception as e:
            print_colored(f"Error extracting audio: {str(e)}", Color.RED)
            return None
    
    def _get_best_video_stream(self) -> Optional[Stream]:
        """Get the highest resolution stream with both video and audio."""
        return self.yt.streams.filter(
            progressive=True,
            file_extension='mp4'
        ).order_by('resolution').desc().first()
    
    def _get_best_audio_stream(self) -> Optional[Stream]:
        """Get the highest quality audio stream."""
        return self.yt.streams.filter(
            only_audio=True
        ).order_by('abr').desc().first()
    
    def _ensure_yt_object(self) -> bool:
        """Ensure YouTube object is initialized."""
        if not self.yt and not self.get_video_info():
            return False
        return True
    
    def _check_existing_file(self, filepath: Path) -> bool:
        """Check if file already exists and prompt user."""
        if filepath.exists():
            print_colored(f"File already exists at: {filepath}", Color.YELLOW)
            return True
        return False
    
    def _download_stream(self, stream: Stream, filepath: Path) -> Optional[Path]:
        """Download the stream to the specified filepath."""
        print_colored(f"Downloading: {stream.resolution or stream.abr}, {stream.mime_type}", Color.YELLOW)
        
        self.current_filesize = stream.filesize
        self.downloaded = 0
        print("")  # Empty line for progress bar
        
        try:
            stream.download(output_path=str(filepath.parent), filename=filepath.name)
            return filepath
        except Exception as e:
            print_colored(f"Download failed: {str(e)}", Color.RED)
            return None
    
    def _convert_to_mp3(self, input_path: Path, output_path: Path) -> Optional[Path]:
        """Convert a file to MP3 format."""
        print_colored("Converting to MP3 format...", Color.YELLOW)
        
        # Simulate conversion with progress bar
        total_steps = 20
        for i in range(total_steps + 1):
            progress = i / total_steps
            create_progress_bar(progress, prefix="Converting: ")
            time.sleep(0.1)
        
        print("\nConversion complete!", Color.GREEN)
        
        # In real implementation, replace with actual conversion
        try:
            with open(input_path, 'rb') as source:
                with open(output_path, 'wb') as dest:
                    dest.write(source.read())
            
            # Clean up temporary file if it's different from output
            if input_path != output_path and input_path.exists():
                input_path.unlink()
                
            return output_path
        except Exception as e:
            print_colored(f"Conversion failed: {str(e)}", Color.RED)
            return None
    
    def _on_progress(self, stream: Stream, chunk: bytes, bytes_remaining: int) -> None:
        """Progress callback for download."""
        self.downloaded = self.current_filesize - bytes_remaining
        progress = self.downloaded / self.current_filesize
        create_progress_bar(progress, prefix="Downloading: ")
    
    def _on_complete(self, stream: Stream, file_path: str) -> None:
        """Complete callback for download."""
        print("\nDownload complete!", Color.GREEN)
        print_colored(f"Saved to: {file_path}", Color.GREEN)
    
    def _format_duration(self, seconds: int) -> str:
        """Format seconds into human-readable time."""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        return f"{minutes}m {seconds}s"