#!/bin/bash
# Inicia o servidor FastAPI usando uvicorn apontando para app/main.py
uvicorn app.main:app --host 0.0.0.0 --port 10000
