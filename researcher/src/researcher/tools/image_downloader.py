from typing import List

import requests
import hashlib

import redis
from PIL import Image
import io

from crewai_tools import BaseTool

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)


class ImagesDownloader(BaseTool):
    name: str = "Images Downloader"
    description: str = (
        "Accepts a list of public URLs pointing to images, and saves them to a Redis cache. \
        Returns the the URLs, file names and image hashes that succeeded and failed as a python dict"
    )


    def download_images(self, urls, file_names) -> List[dict]:

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

        results = []        

        for url,file_name in zip(urls, file_names):

            try:
                response = requests.get(url, headers=headers)
                
                # Check if the request was successful
                new_image = False
                if response.status_code == 200:
                    # Open a file in binary write mode and write the content of the image
                    image_data = response.content
                    image_hash = hashlib.sha256(image_data).hexdigest()
                    if not r.exists(image_hash):
                        r.set(image_hash, image_data)
                        results.append({"url":url, "file_name":file_name, "hash_value":image_hash, "error_message": None, "new": True, "success": True})
                    else:
                        results.append({"url":url, "file_name":file_name, "hash_value":image_hash, "error_message": None, "new": False, "success": True})
                else:
                    results.append({"url":url, "file_name":file_name, "hash_value": None, "error_message": response.status_code, "new": False, "success": False})
            except ValueError as e:
                results.append({"url":url, "file_name":file_name, "hash_value": None, "error_message": e, "new": False, "success": False})

        
        return results


    def _run(self, image_urls: List[str], file_names: List[str]) -> List[dict]:

        return self.download_images(image_urls, file_names)
