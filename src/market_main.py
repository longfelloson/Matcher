from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

import database
from config import settings
from market.auth.utils import get_current_user
from market.router import router as market_router

app = FastAPI(docs_url="", redoc_url="", title="Market")

app.mount("/static", StaticFiles(directory="../static"), name="static")

app.include_router(market_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=settings.TEMPLATES_PATH)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    await database.create_tables()


@app.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_class=HTMLResponse,
)
async def root_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_exception_handler(_: Request, __: HTTPException):
    return RedirectResponse("/login")
