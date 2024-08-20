import os
from dotenv import load_dotenv
import re

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


class ContentUploadChecker(BaseTool):
    name: str = "Content Upload Checker"
    description: str = (
        "Accepts a List of sha256 hashes of images and checks if any content associated with them exists in the Firestore collection"
    )

    def check_content(self, hashes: List[str]) -> List[dict]:

        results = []

        for hash in hashes:
            try:
                if not _is_valid_sha256(hash):
                    raise ValueError("Received invalied sha256 hash. Please check that you're sending the correct hash value")
                result = {"sha256_hash": hash}
                doc_ref = db.collection(COLLECTION).document(hash)
                doc = doc_ref.get()
                result["exists"] = doc.exists
                results.append(result)
            except Exception as e:
                return f"Check for hash {hash} failed with exception {e}"

        return results

    def _run(self, hashes: List[str]) -> List[dict]:

        return self.check_content(hashes)



def _is_valid_sha256(hash_str):
    # Define the regex pattern for a valid SHA-256 hash (64 hexadecimal characters)
    sha256_pattern = re.compile(r'^[a-fA-F0-9]{64}$')
    
    # Check if the hash matches the pattern
    if sha256_pattern.match(hash_str):
        return True
    return False