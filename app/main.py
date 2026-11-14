import os
from datetime import date
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from app.service import SERVICE_INTERVALS_MONTHS, service_status

# Sätts vid Docker-build i pipelinen (steg 4). Lokalt blir det "dev".
APP_VERSION = os.getenv("APP_VERSION", "dev")
APP_ENV = os.getenv("APP_ENV", "local")

app = FastAPI(title="Servicekoll")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": APP_VERSION, "environment": APP_ENV}


@app.get("/types")
def types():
    return {"intervals_months": SERVICE_INTERVALS_MONTHS}


@app.get("/service-status")
def get_service_status(
    extinguisher_type: Annotated[str, Query(alias="type")],
    last_service: date,
):
    try:
        return service_status(extinguisher_type, last_service, today=date.today())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error