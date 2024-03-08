# sdma_image_utils.py
import requests
from bs4 import BeautifulSoup

def extract_image_url(page_url):
    """
    Extracts the image URL from the SDMA artwork page.

    Args:
        obj_url (str): The URL of the SDMA artwork page.

    Returns:
        str: The extracted image URL, or None if not found.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        a_tag = soup.find('a', class_='highslide')
        if a_tag and 'href' in a_tag.attrs:
            image_url = a_tag['href']
            if image_url.startswith('/'):
                from urllib.parse import urljoin
                image_url = urljoin(page_url, image_url)
            return image_url

        print(f"No 'highslide' link found on page: {page_url}")
        return None
    except requests.RequestException as e:
        print(f"Error fetching page URL: {e}")
        return None