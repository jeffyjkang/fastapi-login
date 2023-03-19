from fastapi import FastAPI
from routes.login import github, google
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config

config = Config('.env')
secret_key = config.get('SESSION_SECRET')

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=secret_key)
app.include_router(github.router)
app.include_router(google.router)
