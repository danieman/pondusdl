import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve


WEBPAGE   = "https://www.adressa.no/kultur/tegneserier/pondus/"
DIRECTORY = Path.home() / "pondus"


def find_images(url):
    """Takes a web page URL as input, and returns a list of relevant image URLs."""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    img_tags = soup.find_all("img")
    image_urls = [img["src"] for img in img_tags]
    return image_urls


def download_image(url, filename):
    """Downloads image and prints a confirmation to stdout."""
    urlretrieve(url, filename)
    time_str = datetime.now().strftime("[%Y-%m-%d %H:%M]")
    print(f"{time_str} Downloaded {filename}!")


if __name__ == "__main__":
    images = find_images(WEBPAGE)
    
    # Create ./striper/ if necessary
    if not (DIRECTORY / "striper").is_dir():
        Path.mkdir(DIRECTORY / "striper")

    # Download all new images to ./striper/
    for image in images:
        filename = DIRECTORY / "striper" / f"{image.split('/')[-1]}"
        if not Path.is_file(filename) and "_pon_" in str(filename):
            download_image(image, str(filename))