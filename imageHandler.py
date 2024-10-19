"""
ImageDownloader will be given all of the image urls with names attached.
It will handle downloading and converting them into the proper formats
"""

import requests
from PIL import Image

class ImageHandler:

    def downloadImage(self, url, local_filename):
        response = requests.get(url)

        if response.status_code == 200:
            with open(local_filename, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded: {local_filename}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

    def convertWEBPBackgroundToPNG(self,filename):
        image = Image.open(filename)
        image.save(filename[:-4]+'jpg', 'JPEG')

        
