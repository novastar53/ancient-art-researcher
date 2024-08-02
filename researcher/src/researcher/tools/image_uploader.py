import os
import requests
import pickle
import hashlib
import mimetypes

from typing import List
from PIL import Image
import io

import redis
from google.cloud import storage

from crewai_tools import BaseTool

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Connect to Google Cloud Storage
client = storage.Client()
bucket = client.get_bucket("latest-finds-images-happy-cat-234")

class ImageUploader(BaseTool):
    name: str = "Image Uploader"
    description: str = (
        "Accepts a list of file names and their corresponding hash values. Uploads them to Google Cloud Storage"
    )


    def upload_files(self, file_names, hash_values ) -> List[dict]:
        """Takes a list of file names and their corresponding hash values. Uploads them to Google Cloud Storage."""

        # Get a list of existing files' hash values 
        existing_hashes = set([b.metadata.get("sha256hash") for b in bucket.list_blobs()])

        results = []
        for file_name, file_hash in zip(file_names, hash_values):

            if file_hash in existing_hashes:
                results.append({"file_name": file_name, "success": False, "error_message": "File exists in bucket"})
                continue

            # Upload the file's content to Google Cloud Storage
            blob = bucket.blob(file_name)
            blob.metadata = {
                "sha256hash": file_hash
            }
            image = r.get(file_hash)
            mime_type, _ = mimetypes.guess_type(file_name)
            blob.upload_from_string(image, content_type=mime_type)

            # Make the blob publicly accessible
            blob.make_public()

            results.append({"file_name": file_name, "success": True, "error_message": None})

        return results


    def _run(self, file_names: List[str], hash_values: List[str]) -> List[dict]:

        if len(file_names) == 0 or len(hash_values) == 0:
            return []
        
        return self.upload_files(file_names, hash_values)




