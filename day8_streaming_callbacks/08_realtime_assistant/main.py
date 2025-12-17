"""
Real-time Personal AI Assistant

Day 8 - Program 4: Demonstrates streaming + callbacks + real-time audio

Architecture:
User Question → Groq Streaming → Sentence Detection (Callback)
                    ↓
                Audio Queue
                    ↓
            VibeVoice TTS → Speakers

Result: Audio plays AS text streams in (0.3-0.5s latency!)
"""

import sys
import os

# SUPPRESS ALL OUTPUT IMMEDIATELY (before any imports)
sys.stderr = open(os.devnull, 'w')
sys.stdout = sys.__stdout__  # Keep stdout for our prints

import queue
import warnings

# Additional suppression layers
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

from chain import create_chain, stream_response
from callbacks import SentenceDetectorCallback, TimingCallback
from audio_engine import AudioEngine


def show_progress(percent):
    """Display progress bar"""
    bar_length = 40
    filled = int((percent / 100) * bar_length)
    bar = '█' * filled + '.' * (bar_length - filled)
    print(f"\rAKSA_1.0 Loading [{bar}] {percent}%", end='', flush=True)

def main():
    """Main orchestrator"""
    import time

    # Initial display
    show_progress(0)

    # Step 1: Initialize audio engine (0-60%)
    audio_engine = AudioEngine()
    for i in range(0, 61, 5):
        time.sleep(0.1)
        show_progress(i)

    # Step 2: Start threads (60-75%)
    text_queue = queue.Queue()
    gen_thread, play_thread, audio_queue = audio_engine.start_audio_thread(text_queue)
    for i in range(61, 76):
        time.sleep(0.05)
        show_progress(i)

    # Step 3: Create chain (75-90%)
    chain = create_chain()
    for i in range(76, 91):
        time.sleep(0.05)
        show_progress(i)

    # Step 4: Warmup (90-100%)
    warmup_text = "Hi, I'm AKSA."
    warmup_audio = audio_engine.synthesize(warmup_text)
    for i in range(91, 101):
        time.sleep(0.05)
        show_progress(i)

    # Complete - play sci-fi entry greeting
    print()  # New line after progress bar

    # Generate and play welcome message
    welcome_text = "AKSA online. Ready to make the impossible, possible."
    welcome_audio = audio_engine.synthesize(welcome_text)
    audio_engine.play_audio(welcome_audio)

    while True:
        try:
            # Get user question
            question = input("\n🤔 You: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not question:
                continue

            # Reset stop flag before new response
            audio_engine.resume_audio()

            # Create callbacks for this request
            sentence_callback = SentenceDetectorCallback(text_queue)  # Now uses text_queue
            timing_callback = TimingCallback()
            callbacks = [sentence_callback, timing_callback]

            # Stream response (text appears + audio plays simultaneously!)
            print("\n💬 AKSA: ", end="", flush=True)

            for chunk in stream_response(chain, question, callbacks):
                # Print text as it streams
                print(chunk, end="", flush=True)

            # Wait for BOTH queues to finish (text generation + audio playback)
            text_queue.join()   # Wait for all text chunks to be converted to audio
            audio_queue.join()  # Wait for all audio to finish playing

            print()  # New line after response

        except KeyboardInterrupt:
            # User pressed Ctrl+C during response - skip to next question
            print("\n\n⏭️  Skipped!")
            audio_engine.stop_audio()

            # Clear queues
            while not text_queue.empty():
                try:
                    text_queue.get_nowait()
                    text_queue.task_done()
                except:
                    pass
            while not audio_queue.empty():
                try:
                    audio_queue.get_nowait()
                    audio_queue.task_done()
                except:
                    pass

            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
