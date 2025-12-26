from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address

from controllers.src.exceptions.handler_exceptions import register_exception_handler
from controllers.src.routes.quote_request import quote_request_router
from settings.env_variables import get_allowed_origins

def create_app() -> FastAPI:
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI()
    app.state.limiter = limiter

    allowed_origins = get_allowed_origins()
    allowed_origins = allowed_origins

    app.add_middleware(
      CORSMiddleware,
      allow_origins=allowed_origins,
      allow_credentials=False,
      allow_methods=["*"],
      allow_headers=["*"],
    )
    
    app.include_router(quote_request_router)

    register_exception_handler(app)
  
    return app
