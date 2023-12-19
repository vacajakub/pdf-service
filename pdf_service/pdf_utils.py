import io

import numpy as np
from PIL import Image
from pypdfium2 import PdfDocument, PdfPage

from pdf_service.app_state import AppState
from pdf_service.dao.crud import insert_page, mark_document_as_done


async def process_document(app_state: AppState, pdf: PdfDocument, document_id: int):
    for i, page in enumerate(pdf, 1):
        await process_page(app_state, page, document_id, i)

    await mark_document_as_done(app_state.db_master, document_id)


async def process_page(app_state: AppState, page: PdfPage, document_id: int, page_number: int):
    page_img = page.render().to_pil()

    if page_img.size[0] > app_state.settings.image_max_width or page_img.size[1] > app_state.settings.image_max_width:
        page_img = page_img.resize((app_state.settings.image_max_width, app_state.settings.image_max_width))

    page_image = normalize_image(page_img)
    image_data = io.BytesIO()
    page_image.save(image_data, format="PNG")

    # !!! normally image should be saved in CDN and only an url in db !!! this is only for the assignment
    await insert_page(app_state.db_master, document_id, page_number, image_data)


def normalize_image(page_image: Image) -> Image:
    np_page = np.array(page_image)
    np_page = (np_page / (np_page.max() / 255.0)).astype(np.uint8)
    return Image.fromarray(np_page)
