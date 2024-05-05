import requests
import json

def send_to_llama_api(text, llama_api_url, stream=True):
    # Prepare the request payload
    payload = {
        # "model": "llama3",
        "model": "gemma:2b",
        "system": "You are a helpful, smart, kind, and efficient real-time conversational AI assistant. You always fulfill the users requests to the best of your ability. Basically, keep your responses short.",
        "prompt": text,
        "stream": stream
    }

    # Send the request to the Llama API
    response = requests.post(llama_api_url, json=payload, stream=stream)

    # Check if the request was successful
    if response.status_code == 200:
        if stream:
            # Process the response as a stream
            generated_text = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    # Parse the JSON object
                    json_data = json.loads(chunk)
                    # Extract the generated text
                    generated_text += json_data["response"]
                    # Check if the response is complete
                    if json_data["done"]:
                        return generated_text
        else:
            # Process the response as a single JSON object
            json_data = response.json()
            # Extract the generated text
            generated_text = json_data["response"]
            return generated_text
    else:
        raise Exception(f"Request failed with status code: {response.status_code}")
