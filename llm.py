import json
import logging
from huggingface_hub import InferenceClient # type: ignore

# Set up logging globally
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class LLM:
    def __init__(self):
        # Initialize anything needed for the class here if required
        pass

    def log_and_decode_stream(self, byte_payload):
        # Log the raw byte payload
        logging.info(f"Raw byte payload: {byte_payload}")

        # Proceed with the decoding process
        try:
            json_payload = json.loads(byte_payload.decode("utf-8").lstrip("data:").rstrip("/n"))
            return json_payload
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding failed: {str(e)}")
            return None

# Initialize the client
client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token="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",
)

def llm(query, prompt, max_tokens=500, split=False):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": query},
    ]

    response = ''
    try:
        messages = client.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            stream=True  # Stream is handled internally
        )

        for message in messages:
            if "choices" in message and message.choices[0].delta:
                response += message.choices[0].delta.get("content", "")

    except Exception as e:
        logging.error(f"Error occurred during chat completion: {str(e)}")

    # Handle the response, assuming the first line is what you need
    if split:
        response = response.split("\n")[0]

    return response
