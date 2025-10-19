#!/usr/bin/env python3
"""
Family Photo Organizer - SmartSwitch Samsung Backup Processor
Organizes photos/videos from Samsung SmartSwitch backups using Denote naming convention
This is a universal tool for all Samsung SmartSwitch users
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import argparse
import exifread
from PIL import Image

# Import our modules
from denote_namer import DenoteNamer
from duplicate_checker import DuplicateChecker


class FamilyPhotoOrganizer:
    """Main organizer for processing SmartSwitch backups"""

    def __init__(self, source_dir: str, target_dir: str, dry_run: bool = False):
        """
        Initialize the organizer

        Args:
            source_dir: SmartSwitch backup directory (e.g., SM-S921N_xxx)
            target_dir: Target directory for organized files
            dry_run: If True, don't actually move files
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run

        # Initialize modules
        self.namer = DenoteNamer()
        self.duplicate_checker = DuplicateChecker(
            cache_file=str(self.target_dir / "logs" / "duplicate_cache.json")
        )

        # Setup logging
        self.setup_logging()

        # Statistics
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'duplicates': 0,
            'errors': 0,
            'by_type': defaultdict(int),
            'by_year': defaultdict(int),
            'by_folder': defaultdict(int),
            'size_saved': 0
        }

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.target_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"organize_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting photo organization from {self.source_dir} to {self.target_dir}")

    def analyze_smartswitch_structure(self) -> Dict:
        """
        Analyze SmartSwitch backup structure
        Returns a dictionary with structure information
        """
        structure = {
            'backup_info': {},
            'folders': {},
            'total_files': 0,
            'total_size': 0,
            'file_types': defaultdict(int)
        }

        # Common SmartSwitch folders
        known_folders = [
            'PHOTO',          # Photos and videos from gallery
            'MESSAGE',        # Messages with media attachments
            'GALLERYLOCATION',# Gallery location data
            'PHOTO_ORIGIN',   # Original photo data
            'DOWNLOAD',       # Downloaded files
            'DOCUMENTS',      # Documents
            'MUSIC',          # Music files
            'CONTACTS',       # Contact data
            'CALENDAR',       # Calendar data
        ]

        # Find all backup timestamp folders (e.g., 1757590576343)
        backup_folders = []
        for item in self.source_dir.iterdir():
            if item.is_dir() and item.name.isdigit() and len(item.name) == 13:
                backup_folders.append(item)

        self.logger.info(f"Found {len(backup_folders)} backup folders")

        # Analyze each backup folder
        for backup_folder in backup_folders:
            backup_timestamp = int(backup_folder.name) / 1000
            backup_date = datetime.fromtimestamp(backup_timestamp)

            structure['backup_info'][backup_folder.name] = {
                'date': backup_date.strftime('%Y-%m-%d %H:%M:%S'),
                'folders': {}
            }

            # Check known folders
            for folder_name in known_folders:
                folder_path = backup_folder / folder_name
                if folder_path.exists():
                    file_count = sum(1 for _ in folder_path.rglob('*') if _.is_file())
                    folder_size = sum(f.stat().st_size for f in folder_path.rglob('*') if f.is_file())

                    structure['backup_info'][backup_folder.name]['folders'][folder_name] = {
                        'files': file_count,
                        'size': folder_size
                    }

                    structure['total_files'] += file_count
                    structure['total_size'] += folder_size

        # Find backup_media.db if exists
        db_files = list(self.source_dir.glob('**/backup_media.db'))
        if db_files:
            structure['media_db'] = str(db_files[0])
            self.logger.info(f"Found media database: {db_files[0]}")

        return structure

    def get_media_files(self) -> List[Path]:
        """
        Get all media files from SmartSwitch backup
        Filters by size (>100KB) to exclude thumbnails
        """
        media_extensions = {
            # Photos
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif',
            # Videos
            '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.m4v', '.3gp', '.webm',
            # Screenshots (also images but tagged differently)
            # Documents that might be photos of documents
        }

        media_files = []
        min_size = 100 * 1024  # 100KB minimum

        # Search in all backup folders
        for backup_folder in self.source_dir.iterdir():
            if not backup_folder.is_dir():
                continue

            # Search in common media locations
            search_dirs = [
                backup_folder / 'PHOTO',
                backup_folder / 'MESSAGE',
                backup_folder / 'DOWNLOAD',
                backup_folder / 'DOCUMENTS',
            ]

            for search_dir in search_dirs:
                if search_dir.exists():
                    for file_path in search_dir.rglob('*'):
                        if file_path.is_file():
                            # Check extension
                            if file_path.suffix.lower() in media_extensions:
                                # Check size
                                if file_path.stat().st_size >= min_size:
                                    media_files.append(file_path)

        self.logger.info(f"Found {len(media_files)} media files (>100KB)")
        return media_files

    def extract_metadata(self, file_path: Path) -> Dict:
        """
        Extract metadata from file using EXIF and other methods
        """
        metadata = {
            'datetime': None,
            'gps': None,
            'camera': None,
            'original_name': file_path.name,
            'folder_path': str(file_path.parent.relative_to(self.source_dir))
        }

        # Try to extract EXIF data
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')

                # Extract datetime
                for tag in ['EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime']:
                    if tag in tags:
                        dt_str = str(tags[tag])
                        try:
                            metadata['datetime'] = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
                            break
                        except:
                            pass

                # Extract GPS if available
                if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                    metadata['gps'] = {
                        'lat': str(tags['GPS GPSLatitude']),
                        'lon': str(tags['GPS GPSLongitude'])
                    }

                # Extract camera info
                if 'Image Make' in tags and 'Image Model' in tags:
                    metadata['camera'] = f"{tags['Image Make']} {tags['Image Model']}"

        except Exception as e:
            self.logger.debug(f"Could not extract EXIF from {file_path}: {e}")

        # Fallback to filename parsing or file modification time
        if not metadata['datetime']:
            metadata['datetime'] = self.namer.extract_datetime(str(file_path))

        return metadata

    def determine_target_path(self, source_file: Path, metadata: Dict) -> Path:
        """
        Determine target path based on file type and metadata
        """
        # Generate Denote filename
        denote_name = self.namer.generate_denote_name(str(source_file))

        # Determine category folder
        ext = source_file.suffix.lower()
        folder_name = source_file.parent.name.lower()

        # Main category
        if ext in self.namer.video_extensions:
            category = 'videos'
        elif 'screenshot' in folder_name:
            category = 'screenshots'
        elif '서류' in folder_name or 'document' in folder_name:
            category = 'documents'
        else:
            category = 'photos'

        # Year subfolder
        dt = metadata.get('datetime')
        if dt:
            year = str(dt.year)
        else:
            # Fallback to current year if no date found
            year = str(datetime.now().year)

        # Construct target path
        target_path = self.target_dir / category / year / denote_name

        return target_path

    def process_file(self, source_file: Path) -> bool:
        """
        Process a single file
        Returns True if successful, False otherwise
        """
        try:
            # Extract metadata
            metadata = self.extract_metadata(source_file)

            # Determine target path
            target_path = self.determine_target_path(source_file, metadata)

            # Check for duplicates
            if target_path.parent.exists():
                duplicate = self.duplicate_checker.check_duplicate(
                    str(source_file),
                    str(target_path.parent)
                )

                if duplicate:
                    self.logger.info(f"Duplicate found: {source_file.name} -> {duplicate}")
                    self.stats['duplicates'] += 1
                    self.stats['size_saved'] += source_file.stat().st_size
                    return True  # Consider it successful, just skip

            # Create target directory
            if not self.dry_run:
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(source_file, target_path)
                self.logger.info(f"Copied: {source_file.name} -> {target_path}")
            else:
                self.logger.info(f"[DRY RUN] Would copy: {source_file.name} -> {target_path}")

            # Update statistics
            self.stats['processed'] += 1

            # Update by type
            if target_path.suffix.lower() in self.namer.video_extensions:
                self.stats['by_type']['videos'] += 1
            else:
                self.stats['by_type']['photos'] += 1

            # Update by year
            year = target_path.parent.name
            self.stats['by_year'][year] += 1

            # Update by source folder
            source_folder = source_file.parent.name
            self.stats['by_folder'][source_folder] += 1

            return True

        except Exception as e:
            self.logger.error(f"Error processing {source_file}: {e}")
            self.stats['errors'] += 1
            return False

    def process_all(self, limit: int = None):
        """
        Process all media files

        Args:
            limit: Process only this many files (for testing)
        """
        # Get all media files
        media_files = self.get_media_files()

        if limit:
            media_files = media_files[:limit]
            self.logger.info(f"Processing limited to {limit} files")

        self.stats['total_files'] = len(media_files)

        # Process each file
        for i, media_file in enumerate(media_files, 1):
            self.logger.info(f"Processing {i}/{len(media_files)}: {media_file.name}")
            self.process_file(media_file)

            # Progress report every 100 files
            if i % 100 == 0:
                self.print_progress()

        # Final report
        self.print_final_report()

        # Save duplicate cache
        self.duplicate_checker.save_cache()

    def print_progress(self):
        """Print progress report"""
        total = self.stats['total_files']
        processed = self.stats['processed']
        duplicates = self.stats['duplicates']
        errors = self.stats['errors']

        percent = (processed + duplicates + errors) / total * 100 if total > 0 else 0

        self.logger.info(f"""
        Progress: {percent:.1f}%
        Processed: {processed}/{total}
        Duplicates: {duplicates}
        Errors: {errors}
        """)

    def print_final_report(self):
        """Print final report"""
        report = f"""
        ========================================
        FINAL REPORT
        ========================================
        Total Files: {self.stats['total_files']}
        Successfully Processed: {self.stats['processed']}
        Duplicates Skipped: {self.stats['duplicates']}
        Errors: {self.stats['errors']}

        By Type:
        - Photos: {self.stats['by_type']['photos']}
        - Videos: {self.stats['by_type']['videos']}

        By Year:
        """

        for year in sorted(self.stats['by_year'].keys()):
            report += f"\n        - {year}: {self.stats['by_year'][year]}"

        report += f"\n\n        By Source Folder:"
        for folder in sorted(self.stats['by_folder'].keys()):
            report += f"\n        - {folder}: {self.stats['by_folder'][folder]}"

        # Calculate space saved
        size_saved = self.stats['size_saved']
        size_saved_mb = size_saved / (1024 * 1024)
        report += f"\n\n        Space Saved (duplicates): {size_saved_mb:.2f} MB"

        report += "\n        ========================================"

        self.logger.info(report)

        # Save report to file
        report_file = self.target_dir / "logs" / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)


def main():
    parser = argparse.ArgumentParser(
        description='Organize photos/videos from Samsung SmartSwitch backup'
    )
    parser.add_argument('source', help='SmartSwitch backup directory (e.g., SM-S921N_xxx)')
    parser.add_argument('target', help='Target directory for organized files')
    parser.add_argument('--dry-run', action='store_true', help='Run without actually moving files')
    parser.add_argument('--limit', type=int, help='Limit number of files to process (for testing)')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze structure, don\'t process')

    args = parser.parse_args()

    # Initialize organizer
    organizer = FamilyPhotoOrganizer(args.source, args.target, args.dry_run)

    if args.analyze_only:
        # Just analyze structure
        structure = organizer.analyze_smartswitch_structure()
        print(json.dumps(structure, indent=2, default=str))
    else:
        # Process files
        organizer.process_all(limit=args.limit)


if __name__ == "__main__":
    main()