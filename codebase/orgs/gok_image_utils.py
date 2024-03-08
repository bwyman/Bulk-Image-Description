# orgs/gok_image_utils.py
import requests
from bs4 import BeautifulSoup
import json

def extract_image_url(page_url):
    """
    Extracts the image URL from the GOK artwork page.

    Args:
        obj_url (str): The URL of GOK artwork page.

    Returns:
        str: The extracted image URL, or None if not found.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        div = soup.find('div', {'id': 'entityImageViewerRoot'})
        if div and 'data-representation' in div.attrs:
            try:
                json_data = json.loads(div['data-representation'])
                for item in json_data:
                    if 'iiifManifest' in item:
                        manifest_url = item['iiifManifest']
                        image_id = manifest_url.split('/')[-2]
                        image_url = f"https://iiif.okeeffemuseum.org/image/iiif/2/{image_id}/full/pct:10/0/default.jpg"
                        return image_url

            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return None

        print(f"No data-representation found on page: {page_url}")
        return None
    except requests.RequestException as e:
        print(f"Error fetching page URL: {e}")
        return None