# analyze.py

import sys
import whisper
from modules.analysis import analyze_text  # IMPORT YOUR MODULE


def transcribe_audio(audio_path):
    """Transcribes audio using Whisper (CPU mode)."""
    print("[INFO] Loading Whisper model...")
    model = whisper.load_model("base")

    print("[INFO] Transcribing audio...")
    result = model.transcribe(audio_path, fp16=False)

    return result["text"]


def generate_report(transcript):
    """Runs your custom analysis module and formats output."""
    analysis_result = analyze_text(transcript)

    print("\n=========== AI Interview Analyzer Report ===========\n")
    print("Transcript:\n")
    print(transcript)
    print("\n-----------------------------------------------------")
    print(f"Word Count: {analysis_result['word_count']}")
    print("Feedback:", analysis_result["feedback"])
    print("-----------------------------------------------------\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <audio_file>")
        return

    audio_path = sys.argv[1]

    print(f"[INFO] Processing: {audio_path}\n")

    # STEP 1 — TRANSCRIBE
    transcript = transcribe_audio(audio_path)

    # STEP 2 — ANALYZE
    generate_report(transcript)


if __name__ == "__main__":
    main()
