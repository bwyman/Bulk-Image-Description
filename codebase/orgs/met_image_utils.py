# orgs/met_image_utils.py
import requests
from bs4 import BeautifulSoup

def extract_image_url(page_url):
    """
    Extracts the image URL from the Met artwork page.

    Args:
        obj_url (str): The URL of the Met artwork page.

    Returns:
        str: The extracted image URL, or None if not found.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        img = soup.find('img', {'id': 'artwork__image'})
        if img and 'src' in img.attrs:
            image_url = img['src']
            return image_url

        print(f"No 'artwork__image' found on page: {page_url}")
        return None
    except requests.RequestException as e:
        print(f"Error fetching page URL: {e}")
        return None