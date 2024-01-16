from fastapi import FastAPI
from config.settings import settings
from routers import health

# from config.database import engine, Base
# Base.metadata.create_all(bind=engine)


app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
)

app.include_router(health.router)
