import os
import requests
import pickle
import hashlib

from typing import List

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


from crewai_tools import BaseTool

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveUploader(BaseTool):
    name: str = "Google Drive Uploader"
    description: str = (
        "Accepts a list of filepaths on disk and uploads them to Google Drive."
    )

    def authenticate(self):
        """Authenticate the user and return the Google Drive API service."""

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_drive_client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service
    
    def find_folder(self, folder_name, parent_id=None):
        """Find a folder in Google Drive by name and return its ID."""

        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = self._service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            pageSize=10
        ).execute()
        
        items = results.get('files', [])
        if items:
            return items[0]['id']
        return None
    
    def create_folder(self, folder_name, parent_id=None):
        """Creates a folder in Google Drive and returns the folder ID."""

        folder_id = self.find_folder(folder_name, parent_id)

        if folder_id:
            print(f"Folder '{folder_name}' already exists with ID: {folder_id}")
            return folder_id 

        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = self._service.files().create(body=file_metadata, fields='id').execute()
        print(f'Folder ID: {folder.get("id")}')
        return folder.get('id')
    

    def compute_file_hash(self, file_path):
        """Computes the SHA-256 hash of the specified file."""

        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


    def find_file_by_hash(self, folder_id, file_hash):
        """Finds a file in Google Drive by its hash in the specified folder."""

        #query = f"properties has {{ key='sha256Checksum' and value='{file_hash}' }}"
        query = ""

        results = self._service.files().list(
            q=query,
            spaces='drive',
            #fields='*',
            fields='files(id, name, sha256Checksum, properties)',
            pageSize=10
        ).execute()
        
        items = results.get('files', [])
        for item in items:
            if item["sha256Checksum"] == file_hash:
                return item["id"] 
        return None


    def upload_files(self, file_paths, folder_id):
        """Uploads a list of files to Google Drive in the specified folder."""

        successes = []
        failures = []

        for file_path in file_paths:

            try:

                file_name = os.path.basename(file_path)

                file_hash = self.compute_file_hash(f"downloads/{file_path}")
                if self.find_file_by_hash(folder_id, file_hash):
                    raise Exception(f"This file already exists on Google Drive in the folder {folder_id} with {file_hash}. Skipping...")

                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id],
                    'hash': file_hash
                }
                media = MediaFileUpload(f"downloads/{file_path}", resumable=True)
                file = self._service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                successes.append(file_path)
            except Exception as e:
                failures.append({"file":file_path, "error_message":e})
        
        return successes, failures

            

    def _run(self, file_paths: List[str]):
        
        self._service = self.authenticate()

        folder_id = self.create_folder("test-folder-1")
        s,f = self.upload_files(file_paths, folder_id)

        return {"successes": s, "failures": f}




