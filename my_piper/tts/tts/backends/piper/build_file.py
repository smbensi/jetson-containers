import os
import wave
import time
from pathlib import Path
from typing import Union

from piper.downloads import get_voices, ensure_voice_exists, find_voice

from tts.utils import LOGGER


"""
steps :
 - load the model
 - build the file 
 - play the file with options for stopping in the middle

"""
DEFAULT_PROMPT="This is a default prompt"

def load_model(model,
               config, 
               use_cuda:bool = False, 
               cache:Union[str, Path]=None):
    
    from .voice import PiperVoice
    return PiperVoice.load(model, config, use_cuda)    


def build_file(model:str = 'en_US_lessac_high',
               config=None,
               cache=os.environ.get('PIPER_CACHE'),
               speaker=0,
               length_scale=1.0,
               noise_scale=0.667,
               noise_w=0.8,
               sentence_silence=0.2,
               prompt=DEFAULT_PROMPT,
               output:str|Path = '/dev/null',
               use_cuda=False,
               use_triton=False,
               runs=5,
               dump=False,
               **kwargs):
    with wave.open(output, "wb") as wav_file:
        wav_file.setnchannels(1)
        start = time.perf_counter()
        voice.synthesize(prompt, wav_file, **synthesize_args)
        end = time.perf_counter()
        
        inference_duration = end - start
        
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        audio_duration = frames / float(rate)
        
        print(f"Piper TTS model:    {model}")
        print(f"Output saved to:    {output}")
        print(f"Inference duration: {inference_duration:.3f} sec")
        print(f"Audio duration:     {audio_duration:.3f} sec")
        print(f"Realtime factor:    {inference_duration/audio_duration:.3f}")
        print(f"Inverse RTF (RTFX): {audio_duration/inference_duration:.3f}\n")
        
    
    
def voice_choice(model: str,cache=os.environ.get('PIPER_CACHE'),):
    try:
        voices_info = get_voices(cache, update_voices=True)
    except Exception as error:
        LOGGER.error(f'Failed to download Piper voice list ({error})')
        voices_info = get_voices(cache)
        
    # Resolve aliases for backwards compatibility with old voice names
    aliases_info = {}
    for voice_info in voices_info.values():
        for voice_alias in voice_info.get("aliases", []):
            aliases_info[voice_alias] = {"_is_alias": True, **voice_info}
    
    voices_info.update(aliases_info)
    if not os.path.isfile(os.path.join(cache, model)):
        model_name = model
        ensure_voice_exists(model, cache, cache, voices_info)
        model, config = find_voice(model, [cache])
    else:
        model_name = os.path.splitext(os.path.basename(model))[0]
        
    