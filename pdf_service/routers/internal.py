import logging

from fastapi import APIRouter, HTTPException, Request

router = APIRouter(tags=["internal"])
logger = logging.getLogger("pdf-service.internal")


# internal routes for example for k8s liveness, readiness, metrics etc. normally should not be exposed to the world
@router.get("/readiness", response_model=str)
async def readiness(request: Request) -> str:
    try:

        async with request.app.state.db_slave.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")

                res = await cur.fetchone()
                if res:
                    return "I'm ready!"
        raise HTTPException(status_code=412, detail="Not Ready")
    except Exception as e:
        logger.error("Server not ready: %s", e)
        raise HTTPException(status_code=412, detail="Not Ready") from e


@router.get("/liveness", response_model=str)
async def liveness() -> str:
    # simply returns 200 if server is running
    return "I'm alive!"
