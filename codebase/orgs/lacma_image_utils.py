# orgs/lacma_image_utils.py
import requests
from bs4 import BeautifulSoup

def extract_image_url(page_url):
    """
    Extracts the image URL from the LACMA artwork page.

    Args:
        obj_url (str): The URL of the LACMA artwork page.

    Returns:
        str: The extracted image URL, or None if not found.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        media_asset_div = soup.find('div', class_='media-asset-image')
        if media_asset_div:
            img_tag = media_asset_div.find('img')
            if img_tag and 'src' in img_tag.attrs:
                return img_tag['src']

        print(f"Found img tag: {img_tag}")
    except requests.RequestException as e:
        print(f"Error fetching image URL: {e}")
        return None