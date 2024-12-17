import os

from piper.download import get_voices, ensure_voice_exists

DEFAULT_PROMPT = "Hello world ! My name is Alice"

def main(model='en_US-lessac-high', config=None, cache=os.environ.get('PIPER_CACHE'),
         speaker=0, length_scale=1.0, noise_scale=0.667, noise_w=0.8, sentence_silence=0.2,
         prompt=DEFAULT_PROMPT, output='/dev/null', use_cuda=False, use_triton=False,
         runs=5, dump=False, **kwargs):
    
    # Download voice info
    try:
        voices_info = get_voices(download_dir=cache, update_voices=True)
    except Exception as error:
        print(f"Failed to download Piper voice list ({error})")
        voices_info = get_voices(cache)
    
    # Resolve aliases for backwards compatibility with old voice names
    aliases_info = {}
    for voice_info in voices_info.values():
        for voice_alias in voices_info.get("aliases", []):
            aliases_info[voice_alias] = {"_is_alias": True, **voice_info}
        
    voices_info.update(aliases_info)
    
    if not os.path.isfile(os.path.join(cache, model)):
        model_name = model
        ensure_voice_exists(model, cache, cache, voice_info)