import os
from dotenv import load_dotenv

from typing import List

import requests
import hashlib
import mimetypes
from google.cloud import firestore

from PIL import Image
from io import BytesIO


from google.cloud import storage

from crewai_tools import BaseTool

load_dotenv()

# Connect to Google Cloud Storage
client = storage.Client()
bucket = client.get_bucket(os.getenv("GCLOUD_IMAGE_BUCKET"))
db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"), database=os.getenv("FIRESTORE_DATABASE"))


class ImagesDownloader(BaseTool):
    name: str = "Images Downloader"
    description: str = (
        "Accepts a list of public URLs pointing to images, and uploads them to Google Cloud Storage. \
        Returns the the URLs, file names and image hashes that succeeded and failed as a python dict"
    )


    def download_images(self, urls, file_names) -> List[dict]:

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

        results = []        

        # Retrieve the list of existing image hashes from the bucket
        existing_hashes = set([b.metadata.get("sha256hash") for b in bucket.list_blobs()])

        for url,file_name in zip(urls, file_names):

            try:
                response = requests.get(url, headers=headers)
                
                # Check if the request was successful
                if response.status_code == 200:

                    # Retrieve the image contents 
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))
                    image.verify()
                    image_hash = hashlib.sha256(image_data).hexdigest()

                    # Skip if the image hash exists
                    if image_hash in existing_hashes:
                        results.append({"file_name": file_name, "sha256_hash":image_hash, "success": False, "error_message": "Image already exists"})
                        continue

                    # Create a blob and upload it
                    blob = bucket.blob(file_name)
                    blob.metadata = {
                        "sha256hash": image_hash
                    }
                    mime_type, _ = mimetypes.guess_type(file_name)
                    blob.upload_from_string(image_data, content_type=mime_type)

                    # Make the blob publicly accessible
                    blob.make_public()

                    results.append({"file_name": file_name, "sha256_hash":image_hash, "success": True, "error_message": None})
            except Exception as e:
                results.append({"file_name": file_name, "sha256_hash":None, "success": False, "error_message": e})

                            
        return results


    def _run(self, image_urls: List[str], file_names: List[str]) -> List[dict]:

        return self.download_images(image_urls, file_names)
