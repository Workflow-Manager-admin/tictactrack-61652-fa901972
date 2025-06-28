from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    """
    PUBLIC_INTERFACE
    FastAPI dependency that yields a SQLAlchemy session.
    Ensures session is closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    """
    Initialize database and create tables if they don't exist at startup.
    """
    init_db()


@app.get("/")
def health_check():
    return {"message": "Healthy"}
