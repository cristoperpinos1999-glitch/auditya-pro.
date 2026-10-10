from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import httpx, ssl, socket
from datetime import datetime
import os

app = FastAPI(title="AuditYa Pro")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>AuditYa Pro</title>
<style>
body{font-family:system-ui;background:#0f172a;color:#fff;padding:20px;text-align:center}
.card{background:#1e293b;max-width:600px;margin:20px auto;padding:20px;border-radius:12px}
input{padding:12px;width:90%;max-width:400px;border-radius:8px;border:none;margin:10px;font-size:16px}
.btn{padding:12px 24px;border:none;border-radius:8px;font-weight:bold;cursor:pointer;margin:5px}
.btn-g{background:#22c55e;color:white}.btn-b{background:#3b82f6;color:white}
#res{margin-top:15px;text-align:left;background:#0f172a;padding:15px;border-radius:8px;font-size:14px;word-break:break-all}
h1{color:#22c55e}
</style>
</head>
<body>
<h1>🛡️ AuditYa Pro</h1>
<p>Tu SaaS de Auditorias SEO + SSL - ONLINE 24/7</p>
<div class="card">
<input id="url" placeholder="https://ejemplo.com">
<br>
<button class="btn btn-g" onclick="auditar()">AUDITAR AHORA</button>
<button class="btn btn-b" onclick="pdf()">📄 PDF PRO</button>
<div id="res">Ingresa una URL para auditar...</div>
</div>
<script>
async function auditar(){
 let u=document.getElementById('url').value;
 if(!u){alert('Pon una URL');return}
 document.getElementById('res').innerHTML='⏳ Auditando '+u+'...';
 try{
  let r=await fetch('/auditar?url='+encodeURIComponent(u));
  let d=await r.json();
  document.getElementById('res').innerHTML='<b>Dominio:</b> '+d.dominio+'<br><b>Online:</b> '+(d.online?'✅ Si':'❌ No')+' ('+d.status_code+')<br><b>SSL:</b> '+(d.ssl.valido?'✅ Valido':'❌ Invalido')+'<br><b>Dias restantes:</b> '+d.ssl.dias_restantes+'<br><b>Recomendacion:</b> '+d.recomendacion;
  window.lastData=d;
 }catch(e){document.getElementById('res').innerHTML='❌ Error: '+e}
}
function pdf(){
 if(!window.lastData){alert('Primero audita una web');return}
 let d=window.lastData;
 let w=window.open('','_blank');
 w.document.write('<html><head><title>Reporte '+d.dominio+'</title></head><body style="font-family:Arial;padding:30px"><h1>Reporte AuditYa Pro</h1><p><b>Dominio:</b> '+d.dominio+'</p><p><b>Online:</b> '+d.online+' - Status '+d.status_code+'</p><p><b>SSL Valido:</b> '+d.ssl.valido+'</p><p><b>Dias restantes SSL:</b> '+d.ssl.dias_restantes+'</p><p><b>Recomendacion:</b> '+d.recomendacion+'</p><p><b>Fecha:</b> '+new Date().toLocaleString()+'</p><hr><p>Generado por AuditYa Pro - https://auditya-pro.onrender.com</p><script>window.print();<\/script></body></html>');
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML

@app.get("/auditar")
async def auditar(url: str = Query(...)):
    dominio = url.replace("https://","").replace("http://","").split("/")[0].split("?")[0]
    online = False
    status_code = 0
    try:
        async with httpx.AsyncClient(timeout=12, follow_redirects=True) as client:
            r = await client.get(url if url.startswith("http") else f"https://{url}", headers={"User-Agent":"AuditYaBot"})
            status_code = r.status_code
            online = 200 <= status_code < 400
    except Exception as e:
        online = False
    valido = False
    dias = 0
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=dominio) as s:
            s.settimeout(6)
            s.connect((dominio, 443))
            cert = s.getpeercert()
            exp_str = cert['notAfter']
            exp_date = datetime.strptime(exp_str, '%b %d %H:%M:%S %Y %Z')
            dias = (exp_date - datetime.utcnow()).days
            valido = dias > 0
    except:
        valido = False
    recomendacion = "TODO BIEN - Sitio seguro y online"
    if not online:
        recomendacion = "CRITICO: Sitio offline o no responde"
    elif not valido:
        recomendacion = "CRITICO: SSL invalido o expirado"
    elif 0 < dias < 30:
        recomendacion = f"ATENCION: SSL expira en {dias} dias - Renovar pronto"
    return {"dominio":dominio,"online":online,"status_code":status_code,"ssl":{"valido":valido,"dias_restantes":dias},"valido":valido,"dias_restantes":dias,"recomendacion":recomendacion}

@app.get("/health")
def health():
    return {"status":"ok"}
 
