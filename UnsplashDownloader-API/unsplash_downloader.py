import os
import requests
from bs4 import BeautifulSoup

def download_images(query, count=10, download_folder="downloads"):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    url = f"https://unsplash.com/s/photos/{query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img', {'data-test': 'photo-grid-masonry-img'})[:count]

    downloaded = []
    for idx, img in enumerate(images):
        img_url = img['src'].split('?')[0]
        try:
            img_data = requests.get(img_url).content
            filename = f"{query}_{idx}.jpg"
            path = os.path.join(download_folder, filename)
            with open(path, 'wb') as f:
                f.write(img_data)
            downloaded.append(filename)
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")

    return downloaded
