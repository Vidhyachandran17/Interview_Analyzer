import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(filename):
    """
    Converts an mp3 file to text using SpeechRecognition.
    """
    recognizer = sr.Recognizer()

    # Convert mp3 to wav first (SpeechRecognition works better with wav)
    audio_wav = filename.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(filename)
    sound.export(audio_wav, format="wav")

    # Load the audio file
    with sr.AudioFile(audio_wav) as source:
        audio_data = recognizer.record(source)
        try:
            # Transcribe using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "[Could not understand audio]"
        except sr.RequestError:
            return "[API unavailable]"
