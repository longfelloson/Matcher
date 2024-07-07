from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

import database
from config import settings
from market.router import router as market_router

app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/static', StaticFiles(directory='../static'), name='static')
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
    """
    Startup function for web app
    """
    await database.create_tables()


@app.get('/')
async def root_page(request: Request):
    """
    Root page for web app
    """
    return templates.TemplateResponse('index.html', {'request': request})
