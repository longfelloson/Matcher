from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
from config import settings
from market.auth.router import router as auth_router
from market.auth.utils import auth_guard
from market.router import router as market_router

app = FastAPI(docs_url="", redoc_url="")

app.mount("/static", StaticFiles(directory="../static"), name="static")

app.include_router(market_router)
app.include_router(auth_router)

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
    """Создание таблиц перед запуском"""
    await database.create_tables()


@app.get("/", dependencies=[Depends(auth_guard)])
async def root_page(request: Request):
    """Ручка для получения главной страницы"""
    return templates.TemplateResponse("index.html", {"request": request})
