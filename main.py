import speech_recognition as sr
from gtts import gTTS
import requests
import os

# Initialize speech recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Llama API endpoint (replace with your own)
llama_api_url = "https://your-llama-api-url"

def send_to_llama_api(text, llama_api_url, stream=True):
    # Prepare the request payload
    payload = {
        "model": "gemma:2b",
        "prompt": text,
        "stream": stream
    }

    # Send the request to the Llama API
    response = requests.post(llama_api_url, json=payload, stream=stream)

    # Check if the request was successful
    if response.status_code == 200:
        if stream:
            # Process the response as a stream
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    # Parse the JSON object
                    json_data = json.loads(chunk)
                    # Extract the generated text
                    generated_text = json_data["response"]
                    # Check if the response is complete
                    if json_data["done"]:
                        return generated_text
                    else:
                        # Optionally, you can yield the partial response for real-time display
                        yield generated_text
        else:
            # Process the response as a single JSON object
            json_data = response.json()
            # Extract the generated text
            generated_text = json_data["response"]
            return generated_text
    else:
        raise Exception(f"Request failed with status code: {response.status_code}")

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

        # Convert response to speech
        tts = gTTS(response)
        tts.save("response.mp3")
        os.system("mpg321 response.mp3")

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
