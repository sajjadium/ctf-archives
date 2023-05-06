from pydantic import BaseModel, validator

class UploadedModel(BaseModel):
    source: str
    file_name: str
    file_size: int