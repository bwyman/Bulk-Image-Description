import requests
from bs4 import BeautifulSoup

def extract_image_url(obj_url):
    """
    Extracts the image URL from the CMA artwork page.

    Args:
        obj_url (str): The URL of the CMA artwork page.

    Returns:
        str: The extracted image URL, or None if not found.
    """
    try:
        # Construct the print URL from the object URL
        print_url = obj_url.replace('/art/', '/print/art/')

        response = requests.get(print_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the <link> tag with rel="preload" and extract the href attribute
        link_tag = soup.find('link', rel='preload', attrs={'as': 'image'})
        if link_tag and 'href' in link_tag.attrs:
            return link_tag['href'].replace('&amp;', '&')
    except requests.RequestException:
        return None