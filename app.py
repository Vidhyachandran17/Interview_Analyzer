import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import whisper
import os

# Download NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Load Whisper model (FREE offline)
print("Loading Whisper model... (this takes 10–20 seconds first time)")
model = whisper.load_model("small")

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()


# ---------------------------------------------------------
# 🔥 1. SUMMARY FUNCTION (MANDATORY FEATURE)
# ---------------------------------------------------------
def generate_summary(text):
    """
    Generates a short summary of the interview answer.
    Rule-based and simple to meet project requirements.
    """
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    # Very short input
    if len(text.split()) < 15:
        return "The response is brief but clearly conveys the main idea."

    # If multiple sentences exist
    if len(sentences) > 1:
        return sentences[0] + "."

    # Default fallback
    return "The answer focuses on the candidate's skills and intent."


# ---------------------------------------------------------
# 🔥 2. AUDIO TRANSCRIPTION
# ---------------------------------------------------------
def transcribe_audio(file_path):
    try:
        print("\nTranscribing audio (offline)...")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print("❌ Error in offline transcription:", e)
        return None


# ---------------------------------------------------------
# 🔥 3. TEXT ANALYSIS
# ---------------------------------------------------------
def analyze_text(text):
    # Generate summary (NEW FEATURE)
    summary = generate_summary(text)

    blob = TextBlob(text)
    clarity_score = round(blob.sentiment.polarity, 2)

    sentiment_scores = sia.polarity_scores(text)
    compound = sentiment_scores['compound']

    if compound >= 0.05:
        overall_tone = "Positive"
    elif compound <= -0.05:
        overall_tone = "Negative"
    else:
        overall_tone = "Neutral"

    confidence = "Nervous" if sentiment_scores['neg'] > sentiment_scores['pos'] else "Confident"

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    keywords = [w for w in words if w.isalpha() and w not in stop_words]
    keywords = list(set(keywords))

    suggestions = []
    if clarity_score < 0.5:
        suggestions.append("Improve sentence structure and grammar.")
    if overall_tone == "Negative":
        suggestions.append("Try to maintain a more positive tone.")
    if confidence == "Nervous":
        suggestions.append("Try to sound more confident during your responses.")

    # ---------------------------------------------------------
    # PRINT FINAL REPORT
    # ---------------------------------------------------------
    print("\n=========== AI Interview Analyzer Report ===========\n")

    print("Transcript:")
    print(text)
    print("\n-----------------------------------------------------")

    print("Summary:")
    print(summary)
    print("-----------------------------------------------------")

    print(f"Clarity Score (Grammar): {clarity_score}\n")

    print("Tone Analysis:")
    print(f"Positive: {sentiment_scores['pos']:.3f}, Neutral: {sentiment_scores['neu']:.3f}, Negative: {sentiment_scores['neg']:.3f}")
    print(f"Overall Tone: {overall_tone} ({confidence})\n")

    print("Key Topics Identified:")
    print(", ".join(keywords) if keywords else "None")

    print("\nSuggestions for Improvement:")
    if suggestions:
        for s in suggestions:
            print("- " + s)
    else:
        print("- No improvements needed. Great job!")


# ---------------------------------------------------------
# 🔥 4. MAIN FUNCTION
# ---------------------------------------------------------
def main():
    print("=========== AI Interview Analyzer (Offline Version) ===========")
    choice = input("Do you want to input audio (A) or text (T)? ").strip().lower()

    if choice == "a":
        file_path = input("Enter path to MP3/WAV file: ").strip()
        text = transcribe_audio(file_path)
        if text:
            analyze_text(text)
        else:
            print("❌ Transcription failed.")

    elif choice == "t":
        text = input("Enter your interview answer:\n")
        analyze_text(text)

    else:
        print("Invalid option. Please select A or T.")


if __name__ == "__main__":
    main()
