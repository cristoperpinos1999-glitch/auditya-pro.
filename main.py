from fastapi import FastAPI
import requests
import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry - datetime.now()).days
                return {"valido": True, "dias_restantes": days_left}
    except Exception as e:
        return {"valido": False, "error": str(e)}

@app.get("/auditar")
def auditar(url: str):
    if not url.startswith("http"):
        url = "https://" + url
    
    dominio = urlparse(url).netloc or urlparse(url).path
    
    # 1. ¿Está online?
    try:
        r = requests.get(url, timeout=5)
        online = r.status_code == 200
        status_code = r.status_code
    except:
        online = False
        status_code = 0

    # 2. ¿SSL?
    ssl_info = check_ssl(dominio)

    return {
        "dominio": dominio,
        "online": online,
        "status_code": status_code,
        "ssl": ssl_info,
        "recomendacion": "TODO BIEN" if online and ssl_info.get("valido") else "ALERTA - Revisar"
    }
@app.get("/")
def home():
    return {"mensaje": "AuditYa API está corriendo! Ve a /docs"}