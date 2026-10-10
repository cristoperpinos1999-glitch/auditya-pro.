from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx, ssl, socket
from datetime import datetime
import os

app = FastAPI(title="AuditYa Pro API", version="2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/auditar")
async def auditar(url: str = Query(...)):
    dominio = url.replace("https://","").replace("http://","").split("/")[0]
    online=False; status_code=0
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            r = await client.get(url if url.startswith("http") else f"https://{url}")
            status_code=r.status_code; online=200 <= status_code < 400
    except: online=False
    valido=False; dias_restantes=0
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=dominio) as s:
            s.settimeout(5); s.connect((dominio,443))
            cert=s.getpeercert(); exp_str=cert['notAfter']
            exp_date=datetime.strptime(exp_str,'%b %d %H:%M:%S %Y %Z')
            dias_restantes=(exp_date-datetime.utcnow()).days; valido=dias_restantes>0
    except: valido=False
    recomendacion="TODO BIEN" if (online and valido) else "Revisar SSL o conectividad"
    if 0<dias_restantes<30: recomendacion=f"ATENCIÓN: SSL expira en {dias_restantes} días"
    return {"dominio":dominio,"online":online,"status_code":status_code,"ssl":{"valido":valido,"dias_restantes":dias_restantes},"valido":valido,"dias_restantes":dias_restantes,"recomendacion":recomendacion}

@app.get("/health")
def health(): return {"status":"ok"}

if os.path.isdir("static"):
    app.mount("/app", StaticFiles(directory="static", html=True), name="static")
    @app.get("/")
    async def root():
        if os.path.exists("static/index.html"): return FileResponse("static/index.html")
        return {"mensaje":"AuditYa API está corriendo! Ve a /docs"}

if __name__ == "__main__":
    import uvicorn; port=int(os.environ.get("PORT",8000)); uvicorn.run(app, host="0.0.0.0", port=port)
