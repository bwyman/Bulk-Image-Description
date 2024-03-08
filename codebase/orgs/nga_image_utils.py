# orgs/nga_image_utils.py
import requests
from bs4 import BeautifulSoup
import re

def extract_image_url(page_url):
    """
    Extracts the image URL from the NGA artwork page.

    Args:
        obj_url (str): The URL of the NGA artwork page.

    Returns:
        str: The extracted image URL, or None if not found.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        img_tag = soup.find('img', class_=re.compile('mainImg'))
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']

        print(f"Found img tag: {img_tag}")
    except requests.RequestException as e:
        print(f"Error fetching image URL: {e}")
        return None