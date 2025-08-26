import os
import json
import time
import requests
from pydantic import BaseModel, validator

from typing import Optional as OptionalType

from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header, HTTPException, Request

from starlette.middleware.base import BaseHTTPMiddleware
import logging

import hashlib

from google.cloud import bigquery
from datetime import datetime

from utils import FirestoreLogs

app = FastAPI(title="Hashing API",
              description="""Convertir a hash un RUC""",
              version="0.0.1"
             )

# Reemplaza con tu IP fija.
class IPRestrictionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, authorized_ips: list[str]):
        super().__init__(app)
        self.authorized_ips = authorized_ips

    async def dispatch(self, request: Request, call_next):
        # Imprimimos todas las posibles fuentes de IP
        print("X-Forwarded-For:", request.headers.get("X-Forwarded-For"))
        print("X-Real-IP:", request.headers.get("X-Real-IP"))
        print("client.host:", request.client.host)
        
        client_ip = request.headers.get("X-Forwarded-For", request.client.host)
        if isinstance(client_ip, str) and "," in client_ip:
            client_ip = client_ip.split(",")[0].strip()
        
        print("IP detectada:", client_ip)
        print("IPs autorizadas:", self.authorized_ips)

        if client_ip not in self.authorized_ips:
            raise HTTPException(
                status_code=403,
                detail=f"Acceso denegado para IP: {client_ip}"
            )

        return await call_next(request)

# Uso con múltiples IPs

# IPs de prueba en local
#AUTHORIZED_IPS = ["127.0.0.1", "190.239.73.213"]

# AUTHORIZED_IPS = ["PRD OM", "OM DEV CHATBOT"]
AUTHORIZED_IPS = ["35.232.156.102", "190.113.29.10", "192.168.110.209", "192.168.110.127", "192.168.100.190"]
origins = ["*"]

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    IPRestrictionMiddleware,
    authorized_ips=AUTHORIZED_IPS
)

class RequestChatModel(BaseModel):
    input: str 

# @app.before_request
# def restrict_ip():
#     # Obtén la IP del cliente (usa X-Forwarded-For si estás detrás de un proxy)
#     client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
#     # Verifica si la IP es autorizada
#     if client_ip != AUTHORIZED_IP:
#         return jsonify({"error": "Acceso denegado"}, 403)

# Home page
@app.get("/")
def home( token: str = Header(None)):
    if token is None or token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"message": "API Hashing Ruc Izipay", "model_version": 0.1}

@app.post("/hashing")
def api_hashing(payload: RequestChatModel, token: str = Header(None)):
    
    if token is None or token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Get Data
    data = payload.dict()
    # print('Payload:', data)
    
    data_input = data.get('input')
    
    try:
        response = {}
        
        ruc_hasheado, _ = api_logger.store_log(ruc=data_input)        
        
        response["ruc_hash"] = ruc_hasheado
        
        return response
    except Exception as e:
        print("error-> ",str(e))
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/unhashing")
def api_unhushing(payload: RequestChatModel, token: str = Header(None)):
    
    if token is None or token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Get Data
    data = payload.dict()
    # print('Payload:', data)
    
    data_input = data.get('input')
    
    try:
        response = {}
        
        ruc = api_logger.get_latest_ruc_by_hash(ruc_hash=data_input)        
        
        response["ruc"] = ruc
        
        return response
    except Exception as e:
        print("error-> ",str(e))
        raise HTTPException(status_code=401, detail=str(e))

# Startup
async def startup_event():
    global SECRET_TOKEN    
    global GCP_PROJECT_ID
    global api_logger
    
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', "my-secret-token")
    SECRET_TOKEN = os.getenv('SECRET_TOKEN', "my-secret-token")
    
    api_logger = FirestoreLogs(project_id=GCP_PROJECT_ID, database_id='logs-hushing-ruc',collection_name="collection-logs-hushing-ruc")
    
    # Inicializar el cliente
    #client = bigquery.Client(project=GCP_PROJECT_ID)

    # cred = credentials.ApplicationDefault()
    # firebase_admin.initialize_app(cred, {'projectId': GCP_PROJECT_ID,})
    # FS_CLIENT = firestore.client()
    print("La aplicación se está iniciando")    
    
app.add_event_handler("startup", startup_event)
