import os
import pathlib
from typing import List


class AudioScanner:
    """Handles scanning the filesystem for audio files."""

    AUDIO_EXTENSIONS = {'.mp3', '.wav', '.ogg'}

    def __init__(self, root_dir: str):
        """Initialize with the root directory to scan."""
        self.root_dir = os.path.expanduser(root_dir)
        self.audio_files = []

    def scan(self) -> List[str]:
        """Recursively scan the filesystem for audio files."""
        self.audio_files = []
        try:
            for path in pathlib.Path(self.root_dir).rglob('*'):
                if self._is_valid_audio_file(path):
                    self.audio_files.append(str(path))
        except PermissionError:
            pass  # Skip inaccessible files/directories
        except Exception as e:
            print(f"Error during scan: {e}")
        return sorted(self.audio_files)

    def _is_valid_audio_file(self, path: pathlib.Path) -> bool:
        """Check if a path is a valid audio file."""
        return path.is_file() and path.suffix.lower() in self.AUDIO_EXTENSIONS

    def get_audio_files(self) -> List[str]:
        """Return the list of found audio files."""
        return self.audio_files