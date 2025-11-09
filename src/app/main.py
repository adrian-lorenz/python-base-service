from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.domains.user.api.users_contoller import UsersController
from src.app.database import Base, engine

# Datenbanktabellen erstellen
Base.metadata.create_all(bind=engine)

# FastAPI App mit Metadaten
app = FastAPI(
    title="User Service API",
    description="Ein einfacher User-Service mit FastAPI und MySQL",
    version="1.0.0"
)

# CORS-Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router einbinden
app.include_router(UsersController, prefix="/api")


# Root-Endpunkt
@app.get("/")
def read_root():
    return {
        "message": "Willkommen bei der User Service API",
        "docs": "/docs"
    }
