# main.py
from fastapi import FastAPI
from app.ui.ui_cli import router

app = FastAPI()
app.include_router(router)
