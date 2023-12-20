import pytest

# spin up different docker compose for test, with server container, db container and test containter
# which will fire requests (this)
# we can use fixtures to insert some data before test into db


def test_upload_document_simple(test_app):

    response = test_app.get("/history/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) != 0
    for record in data["items"]:
        for key in ("title", "type", "createTime"):
            assert key in record


# tests of simple call os API, we should always test nonsense arguments, like document id < 0
# or non-existing id and test to expect 404
def test_get_document_simple(test_app):
    assert True


# tests of simple call os API, we should always test nonsense arguments, like document id < 0
# or non-existing page_id and test to expect 404
def test_get_page_simple(test_app):
    assert True


def test_get_non_existing_id(test_app):
    response = test_app.get("/documents/9999/pages/9999")
    assert response.status_code == 404


# then more complex scenarios, like
# 1 - insert document
# 2 - check status
# 3 - retrieve pages
# 4 - ideally compare them to precomputed results
# alternatively upload big document and loop on check status, until it switches into processed, then retrieve pages
def test_upload_file(test_app):
    assert True
