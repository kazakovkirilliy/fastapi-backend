from curses.ascii import CR
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from api.routers import post
from api.routers import user
from api.routers import auth
from api.routers import like
from api.database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["http://localhost:8000/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(post.router)
v1_router.include_router(user.router)
v1_router.include_router(auth.router)
v1_router.include_router(like.router)
app.include_router(v1_router)


@app.get("/")
async def index():
    return {"message": "Hello world!"}
