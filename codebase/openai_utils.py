# openai_utils.py

import openai
import time
from config import openai_config
from prompt_library import prompts

def parse_response(response_str):
    """
    Parses the response string and extracts the alt text and image description.

    Args:
        response_str (str): The response string from the AI assistant.

    Returns:
        dict: A dictionary containing the parsed alt text and image description.
    """
    parsed_responses = {
        'alt_text_short': '',
        'alt_text_long': '',
        'image_description': ''
    }

    current_section = None
    lines = response_str.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('Alt Text (Short):'):
            current_section = 'alt_text_short'
        elif line.startswith('Alt Text (Long):'):
            current_section = 'alt_text_long'
        elif line.startswith('Image Description:'):
            current_section = 'image_description'
        else:
            if current_section:
                parsed_responses[current_section] += ' ' + line

    for key in parsed_responses:
        parsed_responses[key] = ' '.join(parsed_responses[key].split())

    return parsed_responses

def call_openai_assistant(image_url, max_retries=openai_config['max_retries'], 
retry_delay=openai_config['retry_delay']):
    """
    Calls the OpenAI assistant to generate alt text and image description for the given image URL.

    Args:
        image_url (str): The URL of the image.
        max_retries (int, optional): The maximum number of retries for API errors. Defaults to the value in openai_config.
        retry_delay (float, optional): The delay in seconds between retries. Defaults to the value in openai_config.

    Returns:
        str: The generated alt text and image description, or None if an error occurs.
    """
    openai.api_key = openai_config['api_key']
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            prompt_version = openai_config['prompt_version']
            instructions = prompts[prompt_version]
            formatted_instructions = ''.join([f'"{line}"\n' for line in instructions.split('\n')])

            response = openai.ChatCompletion.create(
                model=openai_config['model_name'],
                messages=[
                    {"role": "system", "content": formatted_instructions},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    }
                ],
                max_tokens=openai_config['max_tokens'],
            )

            # print("OpenAI API Response:", response)

            if 'choices' in response and response['choices']:
                choice = response['choices'][0]
                if 'message' in choice and 'content' in choice['message']:
                    return choice['message']['content'].strip()
            return None
        except openai.error.RateLimitError as e:
            print(f"OpenAI API error: {e}")
            wait_time = openai_config['rate_limit_wait_time']
            print(f"Rate limit reached, waiting for {wait_time} seconds.")
            time.sleep(wait_time)
            retry_count += 1
        except openai.error.OpenAIError as e:
            print(f"OpenAI API error: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_count += 1
    
    print(f"OpenAI API error after {max_retries} retries. Moving on to the next image.")
    return None