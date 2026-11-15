import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import (
    AppExceptions,
)
from routers import authors, books

app = FastAPI(title="My Pet Project")
app.include_router(authors.router)
app.include_router(books.router)


# Root
@app.get("/", tags=["ROOT"], summary="Root endpoint")
def root():
    return {"msg": "Hello from ROOT"}


@app.exception_handler(AppExceptions)
def app_exceptions_handler(request: Request, exc: AppExceptions):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
