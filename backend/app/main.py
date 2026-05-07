from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import auth, contacts, companies, deals, pipelines, analytics, automation, integrations
from app.core.config import settings


app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"]
    ,
    allow_headers=["*"]
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["contacts"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(deals.router, prefix="/api/deals", tags=["deals"])
app.include_router(pipelines.router, prefix="/api/pipelines", tags=["pipelines"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(automation.router, prefix="/api/automation", tags=["automation"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["HubSpot Integration"])
