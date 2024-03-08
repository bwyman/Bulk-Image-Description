# claude_utils.py
import anthropic
import time
from config import claude_config

def parse_response(response_str):
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

def call_claude_assistant(image_url, max_retries=claude_config['max_retries'], retry_delay=claude_config['retry_delay']):
    client = anthropic.Client(api_key=claude_config['api_key'])
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            prompt_version = claude_config['prompt_version']
            instructions = prompts[prompt_version]

            message_list = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": image_media_type, "data": image_data}},
                        {"type": "text", "text": "What's in this image?"}
                    ]
                }
            ]

            response = client.messages.create(
                model=claude_config['model_name'],
                max_tokens=claude_config['max_tokens'],
                messages=message_list
            )

            if response.content:
                return response.content[0].text.strip()
            return None
        except anthropic.APIError as e:
            print(f"Anthropic API error: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_count += 1
    
    print(f"Anthropic API error after {max_retries} retries. Moving on to the next image.")
    return None