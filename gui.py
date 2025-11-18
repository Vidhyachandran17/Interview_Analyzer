import tkinter as tk
from tkinter import filedialog, scrolledtext
import whisper
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("vader_lexicon")

# Load Whisper model
model = whisper.load_model("small")
sia = SentimentIntensityAnalyzer()

# -----------------------------
# Core Functions
# -----------------------------

def transcribe_audio(path):
    try:
        result = model.transcribe(path)
        return result["text"]
    except Exception as e:
        return f"Error: {e}"

def analyze_text(text):
    blob = TextBlob(text)
    clarity = round(blob.sentiment.polarity, 2)

    sentiment = sia.polarity_scores(text)
    tone = (
        "Positive" if sentiment["compound"] >= 0.05
        else "Negative" if sentiment["compound"] <= -0.05
        else "Neutral"
    )
    confidence = "Confident" if sentiment["pos"] >= sentiment["neg"] else "Nervous"

    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    keywords = [w for w in words if w.isalpha() and w not in stop_words]

    # Summary (simple heuristic)
    sentences = text.split(".")
    summary = sentences[0] if len(sentences) > 0 else "No summary available."

    # Suggestions
    suggestions = []
    if clarity < 0.5:
        suggestions.append("Improve grammar and clarity.")
    if confidence == "Nervous":
        suggestions.append("Try to sound more confident.")
    if tone == "Negative":
        suggestions.append("Try to maintain a positive tone.")
    if len(text.split()) < 10:
        suggestions.append("Give more detailed answers.")

    report = f"""
=========== AI Interview Analyzer Report ===========

Summary:
{summary}

Clarity Score: {clarity}
Tone: {tone}
Confidence Level: {confidence}

Keywords:
{", ".join(set(keywords))}

Suggestions:
{chr(10).join("- " + s for s in suggestions) if suggestions else "No improvements needed!"}
"""

    return report

# -----------------------------
# Tkinter UI
# -----------------------------

def choose_audio():
    filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if filepath:
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "Transcribing audio...\n")
        text = transcribe_audio(filepath)
        report = analyze_text(text)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, report)

def submit_text():
    text = text_input.get("1.0", tk.END).strip()
    if text:
        report = analyze_text(text)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, report)

# Window setup
root = tk.Tk()
root.title("AI Interview Analyzer - Offline UI")
root.geometry("700x600")
root.resizable(False, False)

title = tk.Label(root, text="AI Interview Analyzer (Offline)", font=("Arial", 18))
title.pack(pady=10)

text_input = scrolledtext.ScrolledText(root, height=5, width=70)
text_input.pack(pady=10)

submit_button = tk.Button(root, text="Analyze Text", command=submit_text, width=20)
submit_button.pack(pady=5)

audio_button = tk.Button(root, text="Upload & Analyze Audio", command=choose_audio, width=25)
audio_button.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, height=20, width=70)
output_box.pack(pady=10)

root.mainloop()
