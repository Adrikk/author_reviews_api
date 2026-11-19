import logging

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from exceptions import (
    AppExceptions,
)
from routers import authors, books, reviews

app = FastAPI(title="My Pet Project")
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(reviews.router)

logger = logging.getLogger("PET_CRUD_APP")


# Root
@app.get("/", tags=["ROOT"], summary="Root endpoint")
def root():
    return {"msg": "Hello from ROOT"}


@app.exception_handler(AppExceptions)
def app_exceptions_handler(request: Request, exc: AppExceptions):
    if exc.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error(
            "Server error on %s %s: %s",
            request.method,
            request.url.path,
            exc.message,
            exc_info=True,
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
