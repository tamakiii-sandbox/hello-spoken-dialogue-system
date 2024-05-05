# main.py
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from utility import send_to_llama_api

# Initialize speech recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Llama API endpoint (replace with your own)
llama_api_url = "http://localhost:11434/api/generate"

def synthesize_speech(text):
    tts = gTTS(text)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio_segment = AudioSegment.from_file(fp, format="mp3")
    play(audio_segment)

while True:
    with mic as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        # Convert speech to text
        text = r.recognize_google(audio)
        print("You said:", text)

        # Send text to Llama API and get the response
        response = send_to_llama_api(text, llama_api_url)
        print("Llama response:", response)

        # Synthesize speech using gTTS
        synthesize_speech(response)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
