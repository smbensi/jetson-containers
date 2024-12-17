import json
from typing import Any, Dict, Iterable, Set, Union
from pathlib import Path
import logging
import shutil
from urllib.request import urlopen


URL_FORMAT = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/{file}"

_DIR = Path(__file__).parent
_LOGGER = logging.getLogger(__name__)

class VoiceNotFoundError(Exception):
    pass

def get_voices(
    download_dir: Union[str, Path], update_voice: bool = False
) -> Dict[str, Any]:
    """Load available voices from downloaded or embedded JSON files"""
    download_dir = Path(download_dir)
    voices_download = download_dir / "voices.json"
    
    if update_voice:
        # Download latest voices.json
        voices_url = URL_FORMAT.format(file="voices.json")
        _LOGGER.debug(f"Downloading {voices_url} to {voices_download}")
        with urlopen(voices_url) as response, open(
            voices_download, "wb"
        ) as download_file:
            shutil.copyfileobj(response, download_file) 
            # function to copy the content of a file object to another file object
            
    # Perfer downloded files to embedded
    voices_embedded = _DIR / "voices.json"
    voices_path = voices_download if voices_download.exists() else voices_embedded
    
    _LOGGER.debug("Loading %s", voices_path)
    with open(voices_path, "r", encoding="utf-8") as voices_file:
        return json.load(voices_file)
    
    
def ensure_voice_exist(
    name: str,
    data_dirs: Iterable[Union[str, Path]],
    download_dir: Union[str, Path],
    voices_info: Dict[str, Any]
):
    assert data_dirs, "No data dirs"
    if name not in voices_info:
        raise VoiceNotFoundError
    
    voice_info = voices_info[name]
    voice_files = voice_info["files"]
    files_to_download: Set[str] = set()
    
    for data_dir in data_dirs:
        
    
    