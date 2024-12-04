"""Piper configuration"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Mapping, Sequence

class PhonemeType(str, Enum):
    ESPEAK = "espeak"
    TEXT = "text"
    
@dataclass
class PiperConfig:
    """Piper configuration"""
    
    num_symbols: int # number of phonemes
    num_speakers: int # number of speakers
    sample_rate: int  # sample rate of output audio
    espeak_voice: str # Name of espeak-ng voice or alphabet
    length_scale: float
    noise_scale: float
    noise_w: float
    phoneme_id_map: Mapping[str, Sequence[int]]
    phoneme_type: PhonemeType
    
    @staticmethod
    def from_dict(config: Dict[str, Any]) -> "PiperConfig":
        inference = config.get("inference", {})
        
        return PiperConfig(
            num_symbols=config["num_symbols"],
            num_speakers=config["num_speakers"],
            sample_rate=config["audio"]["sample_rate"],
            noise_scale=inference.get("noise_scale", 0.667),
            length_scale=inference.get("length_scale", 1.0),
            noise_w=inference.get("noise_w", 0.8),
            #
            espeak_voice=config["espeak"]["voice"],
            phoneme_id_map=config["phoneme_id_map"],
            phoneme_type=PhonemeType(config.get("phoneme_type", PhonemeType.ESPEAK)),
        )