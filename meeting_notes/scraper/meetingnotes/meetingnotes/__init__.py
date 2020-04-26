

import re, requests

def get_id_from_google_drive_url(url:str) -> str:
    return re.search(r'\?id=(.+)', url)[1]

def download_google_drive_file(file_id:str):
    """Downloads and returns a requests object for the Google Drive associated id."""
    return requests.get(f"https://drive.google.com/uc?export=download&id={file_id}", stream=True)