from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

router = APIRouter()

@router.get('/google-login')
async def google_login(request: Request):
    redirect_uri = 'http://localhost:8000/google-login-success'
    something = await oauth.google.authorize_redirect(request, redirect_uri)
    return something

@router.get('/google-login-success')
async def google_login_success(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token['userinfo']
    return user
