from fastapi import HTTPException, APIRouter, status
from fastapi.responses import RedirectResponse

from market.auth.token import create_access_token, decode_token

router = APIRouter()


@router.get("/auth")
async def root_page(token: str):
    if not (payload := decode_token(token)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Link expired"
        )

    response = RedirectResponse(url="/")
    response.set_cookie(key="token", value=create_access_token(payload))

    return response
