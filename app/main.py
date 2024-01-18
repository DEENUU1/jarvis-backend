from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config.settings import settings
from routers import health, chat, media

# from config.database import engine, Base
# Base.metadata.create_all(bind=engine)


app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(media.router)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
