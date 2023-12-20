import io

import numpy as np
from PIL import Image
from pypdfium2 import PdfDocument, PdfPage

from pdf_service.app_state import AppState
from pdf_service.dao.crud import insert_page, mark_document_as_done


async def process_document(app_state: AppState, pdf: PdfDocument, document_id: int):
    for page_number, page in enumerate(pdf, 1):
        await process_page(app_state, page, document_id, page_number)

    await mark_document_as_done(app_state.db_master, document_id)


async def process_page(app_state: AppState, page: PdfPage, document_id: int, page_number: int):
    page_img = page.render().to_pil()

    resize_image(page_img, app_state.settings.image_max_width, app_state.settings.image_max_height)
    page_image = normalize_image(page_img)

    image_data = io.BytesIO()
    page_image.save(image_data, format="PNG")

    # !!! normally image should be saved in CDN and only an url in db !!! this is only for the assignment
    await insert_page(app_state.db_master, document_id, page_number, image_data)


def resize_image(image: Image, max_width: int, max_height: int):
    # if we want to keep ratio
    # skip this if we check that height and width is below max defined dimensions
    if image.size[0] > max_width or image.size[1] > max_height:
        image.thumbnail((max_width, max_height))

    # also possible to use `resize` this won't preserve ration, if any dimension is higher than specified resize
    # resize returns a new instance so `return image.resize((max_width, max_height))` (after appropriate if)


# I got my answer by phone after I already implemented linear normalization, so I keep it here
# Without it, we just need to crop the page img to specified size
def normalize_image(page_image: Image) -> Image:
    np_page = np.array(page_image)
    np_page = (np_page / (np_page.max() / 255.0)).astype(np.uint8)
    return Image.fromarray(np_page)
