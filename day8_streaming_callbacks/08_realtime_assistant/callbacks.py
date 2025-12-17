"""
LangChain Callbacks for Real-time Sentence Detection

Custom callbacks that detect sentence boundaries during streaming
and push chunks to audio queue for immediate playback.
"""

from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List
import queue
import config


class SentenceDetectorCallback(BaseCallbackHandler):
    """
    Detects complete sentences during LLM streaming.

    Strategy: Buffer tokens until we hit punctuation or word limit,
    then push to audio queue for immediate TTS generation.

    This creates the "real-time" effect: audio plays AS text streams in!
    """

    def __init__(self, audio_queue: queue.Queue):
        """
        Args:
            audio_queue: Thread-safe queue for audio chunks
        """
        self.audio_queue = audio_queue
        self.buffer = ""
        self.word_count = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        """Reset state when LLM starts"""
        self.buffer = ""
        self.word_count = 0

    def on_llm_new_token(self, token: str, **kwargs):
        """
        Called for EVERY token during streaming.

        This is where the magic happens:
        1. Add token to buffer
        2. Count words
        3. Detect sentence boundaries
        4. Push complete chunks to audio queue
        """
        # Add token to buffer
        self.buffer += token

        # Count words (spaces indicate word boundaries)
        if token.strip() == ' ':
            self.word_count += 1

        # Check if we should send this chunk to audio
        should_send = False

        # Strategy 1: Hit sentence ending punctuation
        if any(ending in token for ending in config.SENTENCE_ENDINGS):
            should_send = True

        # Strategy 2: Hit mini-pause (for natural flow)
        elif any(pause in token for pause in config.MINI_PAUSES):
            if self.word_count >= config.MIN_CHUNK_WORDS:
                should_send = True

        # Strategy 3: Buffer is getting too long
        elif self.word_count >= config.MAX_CHUNK_WORDS:
            should_send = True

        # Send chunk to audio queue
        if should_send and self.buffer.strip():
            chunk = self.buffer.strip()
            self.audio_queue.put(chunk)

            # Reset buffer
            self.buffer = ""
            self.word_count = 0

    def on_llm_end(self, response, **kwargs):
        """Send any remaining buffer when LLM finishes"""
        if self.buffer.strip():
            self.audio_queue.put(self.buffer.strip())

        # Signal audio thread to stop
        self.audio_queue.put("STOP")

    def on_llm_error(self, error: Exception, **kwargs):
        """Handle errors gracefully"""
        self.audio_queue.put("STOP")


class TimingCallback(BaseCallbackHandler):
    """
    Tracks timing metrics for observability.

    Shows how fast tokens are streaming (demonstrates Groq's speed!)
    """

    def __init__(self):
        import time
        self.start_time = None
        self.token_count = 0
        self.time_module = time

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        """Start timer"""
        self.start_time = self.time_module.time()
        self.token_count = 0

    def on_llm_new_token(self, token: str, **kwargs):
        """Count tokens"""
        self.token_count += 1

    def on_llm_end(self, response, **kwargs):
        """Calculate metrics (silent - for observability if needed)"""
        duration = self.time_module.time() - self.start_time
        tokens_per_sec = self.token_count / duration if duration > 0 else 0
        # Metrics available but not printed (clean chat experience)
