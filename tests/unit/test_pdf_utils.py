from PIL import Image

from pdf_service.pdf_utils import resize_image

# tests to resize, keep ratio, normalization of RGB values etc.
# also possible to test the pdf library to load PDF, check number of pages
# ideally from annotated test set of pdfs


def test_resize_image():
    image = Image.new(mode="RGB", size=(2000, 2000))

    assert image.size[0] == 2000
    assert image.size[1] == 2000

    resize_image(image, 1200, 1600)

    assert image.size[0] <= 1200
    assert image.size[1] <= 1600
