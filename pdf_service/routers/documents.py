import logging

import pypdfium2 as pdfium
from fastapi import APIRouter, BackgroundTasks, HTTPException, Path, Request, Response, UploadFile
from starlette import status

from pdf_service.dao.crud import get_document_db, get_page_data, insert_document
from pdf_service.pdf_utils import process_document
from pdf_service.schemas import GetDocumentResponse, UploadDocumentResponse

router = APIRouter(tags=["pdf documents"])
logger = logging.getLogger("pdf-service.documents")


# normally add checks to file size, format etc., depends on if it is an internal service or not
@router.post("/documents/", response_model=UploadDocumentResponse)
async def upload_document(request: Request, file: UploadFile, background_tasks: BackgroundTasks):
    # checks for parsable pdf or check if its even pdf (omitted in this assigment)
    # also zip bombs and other nice stuff
    pdf = pdfium.PdfDocument(await file.read())
    num_pages = len(pdf)

    if num_pages < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document!")

    try:
        document_id = await insert_document(request.app.state.db_master, num_pages)

        # I went with background_task, it is also off loading work and does not block execution
        # It is a little less scalable solutions, since you do not run workers and queue in different docker container
        # but it doest the job
        # with dramatiq, function process_document would be dramatiq.actor, but only with json encodable args
        # so process_document.send()
        # db conn would have to be acquired in function, not passed as argument
        background_tasks.add_task(process_document, request.app.state, pdf, document_id)

        return UploadDocumentResponse(id=document_id)
    except Exception as e:
        print(e)
        logger.error("Error while uploading document: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload document"
        ) from e


@router.get("/documents/{document_id}", response_model=GetDocumentResponse)
async def get_document(request: Request, document_id: int = Path(gt=0)):
    res = await get_document_db(request.app.state.db_slave, document_id)
    if res:
        return GetDocumentResponse(status=res["status"], n_pages=res["n_pages"])
    else:
        raise HTTPException(status_code=404, detail="Document not found!")


@router.get("/documents/{document_id}/pages/{page_number}")
async def get_page(request: Request, document_id: int = Path(gt=0), page_number: int = Path(gt=0)):
    res = await get_page_data(request.app.state.db_slave, document_id, page_number)
    if res:
        return Response(content=res["image"], media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Incorrect document id or invalid page!")
