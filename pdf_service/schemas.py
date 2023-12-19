from enum import Enum

from pydantic import BaseModel


class DocumentState(str, Enum):
    PROCESSING = "processing"
    DONE = "done"


class GetDocumentResponse(BaseModel):
    status: DocumentState
    n_pages: int


class UploadDocumentResponse(BaseModel):
    id: int
