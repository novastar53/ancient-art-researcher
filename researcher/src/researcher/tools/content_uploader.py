import os
from dotenv import load_dotenv

from typing import List

from google.cloud import firestore

from crewai_tools import BaseTool

from researcher.utils.types import Content

load_dotenv()

# Initialize Gcloud Firestore
GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
DATABASE = os.getenv("FIRESTORE_DATABASE")
COLLECTION = os.getenv("FIRESTORE_IMAGE_COLLECTION")
db = firestore.Client(project=GCLOUD_PROJECT, database=DATABASE)


class ContentUploader(BaseTool):
    name: str = "Content Uploader"
    description: str = (
        "Accepts a List of Content class objects and uploads them to a Firestore database"
    )

    def upload_content(self, content: List[Content]) -> str:

        for item in content:
            doc_ref = db.collection(COLLECTION).document(item.sha256_hash)
            doc_ref.set(item.dict())

        return "Uploads succeeded."


    def _run(self, content: List[Content]) -> str:

        return self.upload_content(content)
