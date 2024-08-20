
from pydantic.v1 import BaseModel 


class Content(BaseModel):
    """Content and related info to be uploaded to a database"""
    title: str # The title of the image
    file_name: str  # The name of the image file with an extension specifying the image format
    generated_description: str # The generated description of the image contents
    original_url: str # The url from where the image was originally downloaded
    source: str # The name  of the source website for the image
    source_url: str # The url of the source website for the image
    sha256_hash: str # the sha256 hash of the image


class ImageInfo(BaseModel):
    """Information for an image found on the internet"""
    title: str # The title of the image
    source: str # The url from where the image was downloaded
    link: str # The url for the image source
