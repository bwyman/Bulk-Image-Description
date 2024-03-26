# image_processing.py

import requests
from PIL import Image

def download_and_resize_image(image_url, source_image_path, resized_image_path, target_size=1568):
    """
    Downloads an image from the given URL, saves it to the source image path, resizes it to the target size,
    and saves the resized image to the resized image path.

    Args:
        image_url (str): The URL of the image to download.
        source_image_path (str): The path to save the downloaded source image.
        resized_image_path (str): The path to save the resized image.
        target_size (int, optional): The target size for the long side of the resized image. Defaults to 1568.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        with open(source_image_path, 'wb') as file:
            file.write(response.content)

        # Resize the image
        with Image.open(source_image_path) as img:
            width, height = img.size
            if width > height:
                new_width = target_size
                new_height = int(height * (target_size / width))
            else:
                new_height = target_size
                new_width = int(width * (target_size / height))

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            resized_img.save(resized_image_path)

    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
    except Exception as e:
        print(f"Error resizing image: {e}")