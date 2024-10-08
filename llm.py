import json
import logging
from huggingface_hub import InferenceClient 
token = "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"

# SetTING up logging globally
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class LLM:
    """
    This class provides an interface to interact with a Large Language Model (LLM) 
    through the Hugging Face Hub. It includes methods to send queries to the model, 
    receive responses, and handle streaming data.

    Attributes:
        None - Initialization can be extended to include specific settings if required.
    """
    
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
    token=token,
)

def llm(query, prompt, max_tokens=500, split=False):
    """
    Sends a query and prompt to the LLM and returns the model's response.

    Args:
        query (str): The user's query to the model.
        prompt (str): The system's prompt to guide the model's response.
        max_tokens (int): The maximum number of tokens for the model's response.
        split (bool): Whether to return only the first line of the response.

    Returns:
        str: The model's response, potentially split into the first line if `split` is True.
    """
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": query},
    ]

    response = ''
    # retry_attempts
    retry_attempts = 0
    max_retries = 100
    while retry_attempts < max_retries:
        try:
            messages = client.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                stream=True  # Stream is handled internally
            )

            for message in messages:
                if "choices" in message and message.choices[0].delta:
                    response += message.choices[0].delta.get("content", "")
            print("response:", response)
            break
        except Exception as e:
            logging.error(f"Error occurred during chat completion: {str(e)}")
            retry_attempts += 1
    
    # Handle the response, assuming the first line is what you need
    if split:
        response = response.split("\n")[0]

    return response
