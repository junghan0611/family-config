#!/usr/bin/env python3
"""
Denote Namer Module
Converts filenames to Denote naming convention for family photos/videos
Format: YYYYMMDDTHHMMSS--original-name__tag1_tag2.ext
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple


class DenoteNamer:
    """Handle Denote-style file naming for family media files"""

    def __init__(self):
        self.photo_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.gif', '.bmp', '.webp'}
        self.video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.m4v', '.3gp'}
        self.document_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx'}

    def extract_datetime(self, filepath: str, fallback_to_mtime: bool = True) -> Optional[datetime]:
        """
        Extract datetime from various sources:
        1. Filename patterns (YYYYMMDD_HHMMSS, IMG_YYYYMMDD_HHMMSS, etc.)
        2. Unix timestamp in filename (13-digit milliseconds)
        3. File modification time as fallback
        """
        filename = os.path.basename(filepath)

        # Pattern 1: YYYYMMDD_HHMMSS or similar
        patterns = [
            r'(\d{8})_(\d{6})',  # 20191215_124225
            r'IMG_(\d{8})_(\d{6})',  # IMG_20191215_124225
            r'VID_(\d{8})_(\d{6})',  # VID_20191215_124225
            r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})',  # 2019-12-15_12-42-25
        ]

        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                groups = match.groups()
                if len(groups) == 2:  # YYYYMMDD_HHMMSS
                    date_str = groups[0]
                    time_str = groups[1]
                    try:
                        dt = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                        return dt
                    except ValueError:
                        continue
                elif len(groups) == 6:  # YYYY-MM-DD_HH-MM-SS
                    try:
                        dt = datetime.strptime(
                            f"{groups[0]}-{groups[1]}-{groups[2]}_{groups[3]}-{groups[4]}-{groups[5]}",
                            "%Y-%m-%d_%H-%M-%S"
                        )
                        return dt
                    except ValueError:
                        continue

        # Pattern 2: Unix timestamp (13 digits = milliseconds)
        timestamp_match = re.search(r'^(\d{13})', filename)
        if timestamp_match:
            try:
                timestamp = int(timestamp_match.group(1)) / 1000  # Convert to seconds
                dt = datetime.fromtimestamp(timestamp)
                # Sanity check: between 2000 and 2030
                if 2000 <= dt.year <= 2030:
                    return dt
            except (ValueError, OSError):
                pass

        # Pattern 3: Unix timestamp (10 digits = seconds)
        timestamp_match = re.search(r'^(\d{10})', filename)
        if timestamp_match:
            try:
                timestamp = int(timestamp_match.group(1))
                dt = datetime.fromtimestamp(timestamp)
                # Sanity check: between 2000 and 2030
                if 2000 <= dt.year <= 2030:
                    return dt
            except (ValueError, OSError):
                pass

        # Fallback to file modification time
        if fallback_to_mtime and os.path.exists(filepath):
            mtime = os.path.getmtime(filepath)
            return datetime.fromtimestamp(mtime)

        return None

    def sanitize_filename(self, name: str) -> str:
        """
        Sanitize filename for Denote convention:
        - Replace underscores with hyphens
        - Remove special characters
        - Convert to lowercase (except for original case preservation)
        """
        # Remove file extension if present
        name = os.path.splitext(name)[0]

        # Replace underscores with hyphens
        name = name.replace('_', '-')

        # Keep only alphanumeric, hyphens, and dots
        name = re.sub(r'[^a-zA-Z0-9\-\.]', '-', name)

        # Remove multiple consecutive hyphens
        name = re.sub(r'-+', '-', name)

        # Remove leading/trailing hyphens
        name = name.strip('-')

        return name

    def determine_tags(self, filepath: str, folder_path: str = "") -> List[str]:
        """
        Determine tags based on file type and location
        """
        tags = []
        ext = Path(filepath).suffix.lower()
        folder_name = os.path.basename(os.path.dirname(filepath)).lower()

        # File type tags
        if ext in self.photo_extensions:
            tags.append("photo")
        elif ext in self.video_extensions:
            tags.append("video")
        elif ext in self.document_extensions:
            tags.append("document")

        # Location-based tags
        if 'screenshot' in folder_name:
            tags.append("screenshot")
        elif '내사랑baron' in folder_name or 'baron' in folder_name:
            tags.append("baron")
        elif '서류' in folder_name:
            tags.append("document")
        elif 'restored' in folder_name:
            tags.append("restored")
        elif 'message' in folder_name:
            tags.append("message")
        elif 'camera' in folder_name:
            tags.append("camera")

        # Check parent folders for restored tag
        if 'Restored' in filepath or 'restored' in filepath:
            if 'restored' not in tags:
                tags.append("restored")

        return tags

    def generate_denote_name(self, filepath: str, custom_tags: List[str] = None) -> str:
        """
        Generate Denote-style filename
        Format: YYYYMMDDTHHMMSS--original-name__tag1_tag2.ext
        """
        # Extract datetime
        dt = self.extract_datetime(filepath)
        if not dt:
            # Use current time if cannot extract
            dt = datetime.now()

        # Format timestamp
        timestamp = dt.strftime("%Y%m%dT%H%M%S")

        # Get original filename and sanitize
        original = os.path.basename(filepath)
        original_sanitized = self.sanitize_filename(original)

        # Determine tags
        tags = custom_tags if custom_tags else self.determine_tags(filepath)
        tags_str = "_".join(tags) if tags else ""

        # Get file extension
        ext = Path(filepath).suffix.lower()

        # Construct Denote name
        if tags_str:
            denote_name = f"{timestamp}--{original_sanitized}__{tags_str}{ext}"
        else:
            denote_name = f"{timestamp}--{original_sanitized}{ext}"

        return denote_name

    def parse_denote_name(self, filename: str) -> Tuple[Optional[datetime], str, List[str], str]:
        """
        Parse a Denote-style filename and extract components
        Returns: (datetime, original_name, tags, extension)
        """
        # Pattern: YYYYMMDDTHHMMSS--original-name__tag1_tag2.ext
        pattern = r'^(\d{8}T\d{6})--([^_]+?)(?:__([^\.]+))?(\.[^\.]+)$'
        match = re.match(pattern, filename)

        if match:
            timestamp_str = match.group(1)
            original_name = match.group(2)
            tags_str = match.group(3) or ""
            extension = match.group(4)

            # Parse timestamp
            try:
                dt = datetime.strptime(timestamp_str, "%Y%m%dT%H%M%S")
            except ValueError:
                dt = None

            # Parse tags
            tags = tags_str.split('_') if tags_str else []

            return dt, original_name, tags, extension

        return None, "", [], ""


# Testing function
if __name__ == "__main__":
    namer = DenoteNamer()

    # Test cases
    test_files = [
        "/media/goqual/T7 Shield/SmartSwitchBackup2/SM-S921N_e74608c6b851cb3e/1757590576343/PHOTO/DCIM/Restored/20190803_123204.jpg",
        "/media/goqual/T7 Shield/SmartSwitchBackup2/SM-S921N_e74608c6b851cb3e/1757590576343/PHOTO/DCIM/Screenshots/Screenshot_20210315_142035.png",
        "/media/goqual/T7 Shield/SmartSwitchBackup2/SM-S921N_e74608c6b851cb3e/1757590576343/MESSAGE/1613911426199-26.jpg",
    ]

    for filepath in test_files:
        if os.path.exists(filepath):
            new_name = namer.generate_denote_name(filepath)
            print(f"Original: {os.path.basename(filepath)}")
            print(f"Denote:   {new_name}")
            print()