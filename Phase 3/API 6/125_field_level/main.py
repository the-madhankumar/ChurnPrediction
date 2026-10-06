from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import ErrorResponse

from routes.customer import router
from database import Base, engine

import os

API_KEY = os.getenv("API_KEY")

Base.metadata.create_all(
    bind=engine
)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    error = ErrorResponse(
        detail="Validation Error",
        status_code=422
    )

    return JSONResponse(
        status_code=422,
        content=error.model_dump()
    )

#129. Add a 404 handler for all routes using @app.exception_handler(404) 
@app.exception_handler(404)
async def not_found_handler(
    request: Request,
    exc
):
    error = ErrorResponse(
        detail="Resource not found",
        status_code=404
    )

    return JSONResponse(
        status_code=404,
        content=error.model_dump()
    )

#131. Add a basic token check: read an API_KEY from environment variable; any request without matching X-API-Key header gets 401 
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):

    if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
        return await call_next(request)

    provided_key = request.headers.get("X-API-Key")

    if provided_key != API_KEY:
        error = ErrorResponse(
            detail="Invalid or missing API key",
            status_code=401
        )

        return JSONResponse(
            status_code=401,
            content=error.model_dump()
        )

    return await call_next(request)

app.include_router(
    router=router
)