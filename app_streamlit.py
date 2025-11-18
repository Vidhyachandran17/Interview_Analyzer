import streamlit as st
from faster_whisper import WhisperModel
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import tempfile

# Ensure NLTK data
nltk.download("punkt")
nltk.download("vader_lexicon")

# Sentiment analyzer
sia = SentimentIntensityAnalyzer()

st.set_page_config(page_title="AI Interview Analyzer", page_icon="🎤", layout="wide")

st.title("🎤 AI Interview Analyzer (Simple Dashboard)")
st.write("Upload an audio file and get instant transcription + tone + clarity + summary!")

# Load Whisper model
@st.cache_resource
def load_model():
    return WhisperModel("small", device="cpu", compute_type="int8")

model = load_model()

# File uploader
uploaded = st.file_uploader("Upload audio file (mp3/wav)", type=["mp3", "wav", "m4a"])

if uploaded:

    st.audio(uploaded)

    with st.spinner("Transcribing (using CPU)..."):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded.read())
            temp_path = tmp.name
        
        segments, info = model.transcribe(temp_path)
        text = " ".join([s.text for s in segments])

    st.subheader("📝 Transcription")
    st.text(text)

    # ------- Tone Analysis -------
    st.subheader("📊 Tone & Sentiment")
    scores = sia.polarity_scores(text)
    tone = "Positive" if scores["pos"] > scores["neg"] else "Negative" if scores["neg"] > 0.3 else "Neutral"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Positive", round(scores["pos"], 3))
    col2.metric("Neutral", round(scores["neu"], 3))
    col3.metric("Negative", round(scores["neg"], 3))
    col4.metric("Overall Tone", tone)

    # ------- Clarity Score -------
    st.subheader("🧠 Clarity Score")

    words = word_tokenize(text)
    filler_words = ["um", "uh", "like", "basically", "you know"]
    filler_count = sum(text.lower().count(w) for w in filler_words)

    clarity = max(0, 1 - (filler_count / max(1, len(words))))

    st.metric("Clarity Score", round(clarity, 2))

    # ------- Summary -------
    st.subheader("📝 Summary")

    if len(text.split()) < 30:
        summary = "The response is short. Main idea: " + text[:150] + "..."
    else:
        # simple split summary
        sentences = text.split(".")
        summary = ". ".join(sentences[:2]) + "."

    st.write(summary)

    # ------- Improvement Tips -------
    st.subheader("✨ Suggestions for Improvement")

    tips = []

    if clarity < 0.7:
        tips.append("Reduce filler words for clearer communication.")

    if scores["neg"] > 0.3:
        tips.append("Try to sound more positive and confident.")

    if len(text.split()) < 50:
        tips.append("Give longer and better structured answers.")

    if not tips:
        tips.append("Great job! Your communication is clear and confident.")

    for t in tips:
        st.write("- " + t)

