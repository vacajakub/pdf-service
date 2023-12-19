import logging

from fastapi import APIRouter, Path, UploadFile, Request, HTTPException, Response, BackgroundTasks
import pypdfium2 as pdfium
from starlette import status

from pdf_service.dao.crud import insert_document, get_document_db, get_page_data
from pdf_service.pdf_utils import process_document
from pdf_service.schemas import GetDocumentResponse, UploadDocumentResponse

router = APIRouter(tags=["pdf documents"])
logger = logging.getLogger("pdf-service.documents")


# normally add checks to file size, format etc., depends on if it is an internal service or not
@router.post("/documents/", response_model=UploadDocumentResponse)
async def upload_file(request: Request, file: UploadFile, background_tasks: BackgroundTasks):
    # checks for parsable pdf or check if its even pdf (omitted in this assigment)
    # also zip bombs and other nice stuff
    pdf = pdfium.PdfDocument(await file.read())
    num_pages = len(pdf)

    if num_pages < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document!")

    try:
        document_id = await insert_document(request.app.state.db_master, num_pages)
        background_tasks.add_task(process_document, request.app.state, pdf, document_id)

        return UploadDocumentResponse(id=document_id)
    except Exception as e:
        print(e)
        logger.error("Error while uploading document: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to upload document") from e


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
