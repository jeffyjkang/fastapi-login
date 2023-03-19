from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
import config

router = APIRouter()

@router.get('/github-login')
async def github_login(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={settings.github_client_id}", status_code=302)

@router.get('/github-login-success')
async def github_login_success(code: str, settings: Annotated[config.Settings, Depends(config.get_settings)]):
    params = {
        'client_id': settings.github_client_id,
        'client_secret': settings.github_client_secret,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    async with AsyncClient() as ac:
        res = await ac.post(
            'https://github.com/login/oauth/access_token',
            params=params,
            headers=headers
        )
    res_json = res.json()
    access_token = res_json['access_token']
    async with AsyncClient() as ac:
        headers.update({'Authorization': f'Bearer {access_token}'})
        res = await ac.get('https://api.github.com/user', headers=headers)
    return res.json()
