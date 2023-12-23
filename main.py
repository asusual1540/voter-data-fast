from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
import os
from starlette.responses import FileResponse, JSONResponse
from app.api.router import router
from app.core.base_model import BaseResponse
from app.core.vdm import vdm


def create_app() -> FastAPI:
    if not vdm.db.database_exists():
        vdm.db.recreate_database()
   #  vdm.db.recreate_database()
    fast_api_app = FastAPI()
    fast_api_app.include_router(router, prefix=vdm.config.API_V1)
    return fast_api_app


app = create_app()

# app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]  # Specify specific origins here
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=400,
        content=BaseResponse(
            status_code=400,
            message=base_error_message
        ).toJson()
    )

@app.get("/{path:path}")
async def root(path: str):
    if path == "" :
        index_path = os.path.join("static", "index.html")
        return FileResponse(index_path)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

   #gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8001 --daemon
