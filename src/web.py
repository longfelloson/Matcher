import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
from config import settings
from market.auth.router import router as auth_router
from market.auth.utils import auth_guard
from market.router import router as market_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='../static'), name='static')

app.include_router(market_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=settings.MARKET.TEMPLATES_PATH)


@app.on_event("startup")
async def startup():
    """
    Startup function for web app
    """
    await database.create_tables()


@app.get('/', dependencies=[Depends(auth_guard)])
async def root_page(request: Request):
    """
    Root page for web app
    """
    return templates.TemplateResponse('index.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run(app)
