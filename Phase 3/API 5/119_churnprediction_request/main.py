from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routes.customer import router
from database import Base, engine

Base.metadata.create_all(
    bind=engine
)

app = FastAPI()

#124. Verify that submitting wrong types (e.g. tenure as a string) returns a 422 Validation Error automatically from Pydantic 
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        }
    )

app.include_router(
    router=router
)