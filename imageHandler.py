"""
ImageDownloader will be given all of the image urls with names attached.
It will handle downloading and converting them into the proper formats
"""

import requests
import os
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

    def convertWEBPBackgroundToPNG(self,filename,newFilepath):
        image = Image.open(filename)
        # Get the new filepath for the name
        filepathParts = os.path.split(newFilepath)
        print("filepathParts")
        print(filepathParts)
        if(filepathParts[0] != ""):
            os.makedirs(filepathParts[0],exist_ok=True)
        #image.save(filename[:-4]+'jpg', 'JPEG')
        image.save(newFilepath)

        
