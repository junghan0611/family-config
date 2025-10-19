#!/usr/bin/env python3
"""
Duplicate Checker Module
Efficiently detect duplicate files using size and hash comparison
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import json


class DuplicateChecker:
    """Handle duplicate detection for media files"""

    def __init__(self, cache_file: str = None):
        """
        Initialize duplicate checker with optional cache file
        """
        self.cache_file = cache_file
        self.hash_cache = {}
        self.size_groups = defaultdict(list)
        self.duplicates = defaultdict(list)

        # Load cache if exists
        if cache_file and os.path.exists(cache_file):
            self.load_cache()

    def load_cache(self):
        """Load hash cache from file"""
        try:
            with open(self.cache_file, 'r') as f:
                self.hash_cache = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cache: {e}")
            self.hash_cache = {}

    def save_cache(self):
        """Save hash cache to file"""
        if self.cache_file:
            try:
                with open(self.cache_file, 'w') as f:
                    json.dump(self.hash_cache, f, indent=2)
            except Exception as e:
                print(f"Warning: Could not save cache: {e}")

    def calculate_hash(self, filepath: str, quick: bool = False) -> Optional[str]:
        """
        Calculate MD5 hash of a file
        If quick=True, only hash first and last 64KB for large files
        """
        if not os.path.exists(filepath):
            return None

        # Check cache first
        cache_key = f"{filepath}:{os.path.getmtime(filepath)}"
        if cache_key in self.hash_cache:
            return self.hash_cache[cache_key]

        try:
            hasher = hashlib.md5()
            file_size = os.path.getsize(filepath)

            with open(filepath, 'rb') as f:
                if quick and file_size > 131072:  # 128KB
                    # Hash first 64KB
                    hasher.update(f.read(65536))
                    # Hash last 64KB
                    f.seek(-65536, os.SEEK_END)
                    hasher.update(f.read(65536))
                else:
                    # Hash entire file in chunks
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        hasher.update(chunk)

            file_hash = hasher.hexdigest()
            self.hash_cache[cache_key] = file_hash
            return file_hash

        except Exception as e:
            print(f"Error calculating hash for {filepath}: {e}")
            return None

    def group_by_size(self, filepaths: List[str]) -> Dict[int, List[str]]:
        """
        Group files by size - first step in duplicate detection
        """
        size_groups = defaultdict(list)

        for filepath in filepaths:
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                size_groups[size].append(filepath)

        # Only keep groups with more than one file
        return {size: files for size, files in size_groups.items() if len(files) > 1}

    def find_duplicates_in_group(self, filepaths: List[str]) -> List[List[str]]:
        """
        Find duplicates within a group of same-sized files
        Returns list of duplicate groups
        """
        if len(filepaths) < 2:
            return []

        # First, quick hash to narrow down
        quick_hashes = defaultdict(list)
        for filepath in filepaths:
            quick_hash = self.calculate_hash(filepath, quick=True)
            if quick_hash:
                quick_hashes[quick_hash].append(filepath)

        # Then, full hash for potential duplicates
        duplicate_groups = []
        for quick_hash, files in quick_hashes.items():
            if len(files) > 1:
                full_hashes = defaultdict(list)
                for filepath in files:
                    full_hash = self.calculate_hash(filepath, quick=False)
                    if full_hash:
                        full_hashes[full_hash].append(filepath)

                # Add duplicate groups
                for file_hash, dup_files in full_hashes.items():
                    if len(dup_files) > 1:
                        duplicate_groups.append(dup_files)

        return duplicate_groups

    def find_duplicates(self, filepaths: List[str], min_size: int = 10240) -> Dict[str, List[str]]:
        """
        Find all duplicate files in the given list
        min_size: Minimum file size to consider (default 10KB to skip thumbnails)
        Returns: Dictionary with hash as key and list of duplicate files as value
        """
        # Filter by minimum size
        valid_files = []
        for filepath in filepaths:
            if os.path.exists(filepath) and os.path.getsize(filepath) >= min_size:
                valid_files.append(filepath)

        print(f"Checking {len(valid_files)} files for duplicates...")

        # Step 1: Group by size
        size_groups = self.group_by_size(valid_files)
        print(f"Found {len(size_groups)} size groups with potential duplicates")

        # Step 2: Check hash within each size group
        all_duplicates = {}
        for size, files in size_groups.items():
            duplicate_groups = self.find_duplicates_in_group(files)
            for dup_group in duplicate_groups:
                # Use the first file's hash as the key
                file_hash = self.calculate_hash(dup_group[0], quick=False)
                if file_hash:
                    all_duplicates[file_hash] = dup_group

        # Save cache
        self.save_cache()

        return all_duplicates

    def check_duplicate(self, source_file: str, target_directory: str) -> Optional[str]:
        """
        Check if a file already exists in the target directory
        Returns the path of the duplicate if found, None otherwise
        """
        if not os.path.exists(source_file):
            return None

        source_size = os.path.getsize(source_file)
        source_hash = None

        # Check all files in target directory
        for root, dirs, files in os.walk(target_directory):
            for filename in files:
                target_file = os.path.join(root, filename)

                # Quick check: size must match
                if os.path.getsize(target_file) != source_size:
                    continue

                # Calculate source hash if not done yet
                if source_hash is None:
                    source_hash = self.calculate_hash(source_file)
                    if source_hash is None:
                        return None

                # Check hash
                target_hash = self.calculate_hash(target_file)
                if target_hash == source_hash:
                    return target_file

        return None

    def get_duplicate_stats(self, duplicates: Dict[str, List[str]]) -> Dict:
        """
        Get statistics about duplicates
        """
        stats = {
            'total_duplicate_groups': len(duplicates),
            'total_duplicate_files': sum(len(files) for files in duplicates.values()),
            'total_duplicate_size': 0,
            'space_saveable': 0
        }

        for file_hash, files in duplicates.items():
            if files:
                file_size = os.path.getsize(files[0]) if os.path.exists(files[0]) else 0
                stats['total_duplicate_size'] += file_size * len(files)
                stats['space_saveable'] += file_size * (len(files) - 1)

        # Convert to human-readable sizes
        for key in ['total_duplicate_size', 'space_saveable']:
            size = stats[key]
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    stats[f'{key}_human'] = f"{size:.2f} {unit}"
                    break
                size /= 1024.0

        return stats


# Testing function
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = "/media/goqual/T7 Shield/SmartSwitchBackup2/SM-S921N_e74608c6b851cb3e/1757590576343/PHOTO"

    # Find all image files
    test_files = []
    for root, dirs, files in os.walk(test_dir):
        for filename in files[:100]:  # Limit to 100 files for testing
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4')):
                test_files.append(os.path.join(root, filename))

    print(f"Testing with {len(test_files)} files from {test_dir}")

    # Check for duplicates
    checker = DuplicateChecker(cache_file="/tmp/duplicate_cache.json")
    duplicates = checker.find_duplicates(test_files)

    # Print results
    if duplicates:
        print(f"\nFound {len(duplicates)} groups of duplicates:")
        for file_hash, files in duplicates.items():
            print(f"\nHash: {file_hash}")
            for filepath in files:
                print(f"  - {filepath}")

        # Print statistics
        stats = checker.get_duplicate_stats(duplicates)
        print("\nDuplicate Statistics:")
        for key, value in stats.items():
            if not key.endswith('_human'):
                print(f"  {key}: {value}")