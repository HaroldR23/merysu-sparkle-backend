from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.src.routes.quote_request import quote_request_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
			CORSMiddleware,
			allow_origins=["*"],
			allow_credentials=False,
			allow_methods=["*"],
			allow_headers=["*"],
		)
    app.include_router(quote_request_router)

    return app
