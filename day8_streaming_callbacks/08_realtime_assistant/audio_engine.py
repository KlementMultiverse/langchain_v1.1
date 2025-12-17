"""
Audio Engine - VibeVoice TTS Integration

Handles text-to-speech generation and playback using VibeVoice-Realtime-0.5B
"""

import torch
import queue
import threading
import os
import glob
import copy
from vibevoice.modular.modeling_vibevoice_streaming_inference import VibeVoiceStreamingForConditionalGenerationInference
from vibevoice.processor.vibevoice_streaming_processor import VibeVoiceStreamingProcessor
import config


class AudioEngine:
    """
    Manages VibeVoice TTS model and audio playback.

    Runs in separate thread, consuming text chunks from queue
    and generating + playing audio in real-time.
    """

    def __init__(self):
        """Initialize VibeVoice model (silent loading)"""
        import warnings
        import os
        import sys

        # Suppress all warnings and progress bars
        warnings.filterwarnings("ignore")
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

        # Redirect stderr temporarily to hide progress bars
        old_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')

        try:
            # Load processor
            self.processor = VibeVoiceStreamingProcessor.from_pretrained(config.VIBEVOICE_MODEL)

            # Load model with CUDA settings
            self.model = VibeVoiceStreamingForConditionalGenerationInference.from_pretrained(
                config.VIBEVOICE_MODEL,
                torch_dtype=torch.bfloat16,
                device_map="cuda",
                attn_implementation="sdpa"
            )

            self.model.eval()
            self.model.set_ddpm_inference_steps(num_steps=3)  # Reduced from 5 to 3 for speed

            # Load Soother voice
            self.voice_sample = self._load_default_voice()

            # Stop flag for interrupting playback
            self.stop_playback = False
        finally:
            # Restore stderr
            sys.stderr.close()
            sys.stderr = old_stderr

    def _load_default_voice(self):
        """Load default voice preset - Grace (sweet female voice)"""
        voices_dir = "/tmp/VibeVoice/demo/voices/streaming_model"

        # Priority: Soother voice (your choice!)
        preferred_voices = [
            "experimental_voices/en/en-Soother_woman.pt",     # Calm, soothing female voice (SELECTED)
            "en-Soother_woman.pt",     # Fallback path
            "en-Grace_woman.pt",      # Backup option
            "en-Emma_woman.pt",        # Backup option
        ]

        # Try preferred voices first (silent loading)
        for voice_name in preferred_voices:
            voice_path = os.path.join(voices_dir, voice_name)
            if os.path.exists(voice_path):
                voice_sample = torch.load(voice_path, map_location="cuda", weights_only=False)
                return voice_sample

        # Fallback: Find any woman voice
        voice_files = glob.glob(os.path.join(voices_dir, "**", "*woman*.pt"), recursive=True)
        if voice_files:
            voice_path = voice_files[0]
            voice_sample = torch.load(voice_path, map_location="cuda", weights_only=False)
            return voice_sample

        # Last resort: any voice
        voice_files = glob.glob(os.path.join(voices_dir, "**", "*.pt"), recursive=True)
        if not voice_files:
            raise FileNotFoundError(f"No voice files found in {voices_dir}")

        voice_path = voice_files[0]
        voice_sample = torch.load(voice_path, map_location="cuda", weights_only=False)
        return voice_sample

    def synthesize(self, text: str):
        """
        Convert text to speech (silent - no progress bars).

        Args:
            text: Text to synthesize

        Returns:
            Audio waveform (numpy array)
        """
        import sys
        import os

        # Suppress progress bars completely
        old_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')

        try:
            with torch.no_grad():
                # Prepare inputs
                inputs = self.processor.process_input_with_cached_prompt(
                    text=text,
                    cached_prompt=self.voice_sample,
                    padding=True,
                    return_tensors="pt",
                    return_attention_mask=True,
                )

                # Move to CUDA
                for k, v in inputs.items():
                    if torch.is_tensor(v):
                        inputs[k] = v.to("cuda")

                # Generate audio (silent) with higher CFG scale for stronger output
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=None,
                    cfg_scale=2.0,  # Increased from 1.0 for stronger/louder voice
                    tokenizer=self.processor.tokenizer,
                    generation_config={'do_sample': False},
                    verbose=False,
                    all_prefilled_outputs=copy.deepcopy(self.voice_sample)
                )

                # Extract audio waveform
                audio_waveform = outputs.speech_outputs[0]

            return audio_waveform
        finally:
            # Restore stderr
            sys.stderr.close()
            sys.stderr = old_stderr

    def play_audio(self, audio):
        """
        Play audio waveform through speakers (non-blocking for smooth transitions).

        Args:
            audio: Audio waveform tensor
        """
        import sounddevice as sd
        import numpy as np
        import time

        # Convert to numpy and play
        # Convert bfloat16 → float32 for sounddevice compatibility
        audio_np = audio.cpu().float().numpy() if torch.is_tensor(audio) else audio

        # Ensure correct shape for mono audio (1D array)
        if audio_np.ndim > 1:
            audio_np = audio_np.squeeze()

        # Trim silence from end to reduce gaps between chunks
        # Find last non-silent sample (threshold = 0.01)
        silence_threshold = 0.01
        non_silent = np.abs(audio_np) > silence_threshold
        if non_silent.any():
            last_sound_idx = np.where(non_silent)[0][-1]
            # Keep a tiny bit of trailing (50ms) for natural sound
            trailing_samples = int(24000 * 0.05)  # 50ms
            trim_point = min(last_sound_idx + trailing_samples, len(audio_np))
            audio_np = audio_np[:trim_point]

        # Apply MASSIVE volume boost (300% louder = multiply by 4.0)
        audio_np = audio_np * 4.0

        # Clip to prevent distortion (keep within -1 to 1 range)
        audio_np = np.clip(audio_np, -1.0, 1.0)

        # Play at slightly faster speed
        playback_speed = 1.05  # 5% faster
        sd.play(audio_np, samplerate=int(24000 * playback_speed), blocking=True)
        # blocking=True ensures audio finishes before returning

    def generation_worker(self, text_queue: queue.Queue, audio_queue: queue.Queue):
        """
        Generation thread: converts text chunks to audio.
        Runs in parallel with playback thread!
        """
        while True:
            chunk = text_queue.get()

            if chunk == "STOP":
                audio_queue.put("STOP")
                text_queue.task_done()
                continue

            try:
                # Generate audio (non-blocking for playback)
                audio = self.synthesize(chunk)
                audio_queue.put(audio)
            except Exception as e:
                print(f"⚠️  Generation error: {e}")
            finally:
                text_queue.task_done()

    def playback_worker(self, audio_queue: queue.Queue):
        """
        Playback thread: plays generated audio.
        Runs in parallel with generation thread!
        """
        import sounddevice as sd

        while True:
            audio = audio_queue.get()

            if audio == "STOP":
                audio_queue.task_done()
                continue

            try:
                # Check if stop flag is set, skip audio if true
                if self.stop_playback:
                    audio_queue.task_done()
                    continue

                # Play audio
                self.play_audio(audio)
            except KeyboardInterrupt:
                # User pressed Ctrl+C, stop current playback
                sd.stop()
                audio_queue.task_done()
                break
            except Exception as e:
                print(f"⚠️  Playback error: {e}")
            finally:
                audio_queue.task_done()

    def stop_audio(self):
        """Stop current audio playback and clear queues"""
        import sounddevice as sd
        sd.stop()  # Stop current audio immediately
        self.stop_playback = True

    def resume_audio(self):
        """Resume audio playback"""
        self.stop_playback = False

    def start_audio_thread(self, text_queue: queue.Queue):
        """
        Start DUAL-THREADED audio processing (generation + playback in parallel).

        Args:
            text_queue: Queue to consume text chunks from

        Returns:
            Tuple of (generation_thread, playback_thread, audio_queue)
        """
        # Create internal audio queue
        audio_queue = queue.Queue()

        # Start generation thread
        gen_thread = threading.Thread(
            target=self.generation_worker,
            args=(text_queue, audio_queue),
            daemon=True
        )
        gen_thread.start()

        # Start playback thread
        play_thread = threading.Thread(
            target=self.playback_worker,
            args=(audio_queue,),
            daemon=True
        )
        play_thread.start()

        return (gen_thread, play_thread, audio_queue)
