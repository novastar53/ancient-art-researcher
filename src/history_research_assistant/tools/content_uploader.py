from typing import List

from google.cloud import firestore

from crewai_tools import BaseTool

from history_research_assistant.utils.types import Content

# Initialize Firestore
db = firestore.Client(project="history-research-assistant", database="history-research-database")


class ContentUploader(BaseTool):
    name: str = "Content Uploader"
    description: str = (
        "Accepts a List of Content class objects and uploads them to a Firestore database"
    )

    def upload_content(self, content: List[Content]) -> str:

        for item in content:
            doc_ref = db.collection('found-image-descriptions').document(item.sha256_hash)
            doc_ref.set(item.dict())

        return "Uploads succeeded."


    def _run(self, content: List[Content]) -> str:

        return self.upload_content(content)
