import asyncio
import logging

from fastapi import FastAPI

from pdf_service.app_state import AppState
from pdf_service.routers import documents, internal

tags_metadata = [
    {
        "name": "PDF service",
        "description": "Server for rendering of PDFs",
    },
]

app = FastAPI(title="PDF service", description="Server for rendering of PDFs", openapi_tags=tags_metadata)
app.state = AppState()
# this would be a Flask blueprints - basically the same
app.include_router(documents.router)
app.include_router(internal.router)


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("pdf-service")
    await app.state.setup()
    print("started")
    logger.info("Started")


@app.on_event("shutdown")
async def shutdown():
    logger = logging.getLogger("pdf-service")
    logger.info("Shutting down")
    # don't forget to close pools :)
    await asyncio.gather(app.state.db_master.close(), app.state.db_slave.close())
    logger.info("Shutdown end")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "pdf_service.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
        timeout_keep_alive=10,
    )
