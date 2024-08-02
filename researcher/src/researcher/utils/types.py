
from pydantic.v1 import BaseModel 


class Content(BaseModel):
    file_name: str 
    generated_description: str
    original_url: str
    source_url: str
    sha256_hash: str
    source: str
    title: str

