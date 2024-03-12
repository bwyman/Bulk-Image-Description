# claude_utils.py
import anthropic
import time
import base64
import httpx
import requests
import mimetypes
import re
from PIL import Image
from io import BytesIO
from config import claude_config
from prompt_library import prompts
from image_processing import download_and_resize_image

def parse_response(response_str):
    parsed_responses = {
        'alt_text_short': '',
        'alt_text_long': '',
        'image_description': ''
    }

    sections = re.split(r'(Alt Text \(Short\):|Alt Text \(Long\):|Image Description:)', response_str)
    sections = [section.strip() for section in sections if section.strip()]

    for i in range(0, len(sections), 2):
        title = sections[i].lower().replace(':', '').replace(' ', '_')
        content = sections[i + 1].replace('\n', ' ').strip()

        if title in parsed_responses:
            parsed_responses[title] = content

    return parsed_responses

def call_claude_assistant(image_url, source_image_path=None, resized_image_path=None, max_retries=claude_config['max_retries'], retry_delay=claude_config['retry_delay']):
    client = anthropic.Client(api_key=claude_config['api_key'])

    retry_count = 0
    while retry_count < max_retries:
        try:
            prompt_version = claude_config['prompt_version']
            if prompt_version not in prompts:
                raise ValueError(f"Prompt '{prompt_version}' not found in the prompt library.")
            
            instructions = prompts[prompt_version].replace('\n', ' ')
            # print("Claude Instructions:", instructions)

            if resized_image_path:
                with open(resized_image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("utf-8")
                    
                    # Determine the media type based on the file extension
                    media_type, _ = mimetypes.guess_type(resized_image_path)
                    if media_type is None:
                        media_type = "application/octet-stream"  # Default media type if not determined

                    message_list = [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": instructions
                                },
                                {
                                    "type": "image",
                                    "source": {
                                    	"type": "base64",
                                    	"media_type": media_type,
                                    	"data": image_data,
                                    },
                                }
                            ],
                        }
                    ]
            else:
                message_list = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Here is the image URL: {image_url}"
                            },
                            {
                                "type": "text",
                                "text": instructions
                            }
                        ],
                    }
                ]
            
            response = client.messages.create(
                model=claude_config['model_name'],
                max_tokens=claude_config['max_tokens'],
                messages=message_list
            )

            # print("Claude Response:", response)
            if response.content:
                return response.content[0].text.strip()
            return None
        except anthropic.APIError as e:
            print(f"Anthropic API error: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_count += 1
    
    print(f"Anthropic API error after {max_retries} retries. Moving on to the next image.")
    return None

