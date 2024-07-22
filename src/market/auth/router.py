from fastapi import HTTPException, APIRouter
from fastapi.responses import RedirectResponse

from market.auth.token import create_access_token, decode_token

router = APIRouter()


@router.get('/auth')
async def root_page(token: str):
    """
    Root page for web app
    """
    if not (payload := decode_token(token)):
        raise HTTPException(status_code=400, detail="Link expired")

    response = RedirectResponse(url='/')
    response.set_cookie(key='token', value=create_access_token(payload))

    return response
