# main.py
import speech_recognition as sr
import pyttsx3
from utility import send_to_llama_api

# Initialize speech recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Llama API endpoint (replace with your own)
llama_api_url = "http://localhost:11434/api/generate"

# Initialize pyttsx3 engine
engine = pyttsx3.init()

def synthesize_speech(text):
    engine.say(text)
    engine.runAndWait()

def process_llama_response(response):
    buffer = []
    for chunk in response:
        if chunk:
            buffer.append(chunk)
            if '.' in chunk or '?' in chunk or '!' in chunk:
                partial_response = ''.join(buffer)
                print("Partial response:", partial_response)
                synthesize_speech(partial_response)
                buffer = []
    if buffer:
        remaining_response = ''.join(buffer)
        print("Remaining response:", remaining_response)
        synthesize_speech(remaining_response)

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

        # Process and synthesize speech for the response
        process_llama_response(response)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
