from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import httpx, ssl, socket
from datetime import datetime

app = FastAPI(title="AuditYa Pro")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

APP_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>AuditYa Pro - Auditor Online</title>
<style>
body{font-family:system-ui;background:#0f172a;color:#fff;padding:20px;text-align:center}
.card{background:#1e293b;max-width:600px;margin:20px auto;padding:20px;border-radius:12px}
input{padding:12px;width:90%;max-width:400px;border-radius:8px;border:none;margin:10px;font-size:16px}
.btn{padding:12px 24px;border:none;border-radius:8px;font-weight:bold;cursor:pointer;margin:5px}
.btn-g{background:#22c55e;color:white}.btn-b{background:#3b82f6;color:white}
#res{margin-top:15px;text-align:left;background:#0f172a;padding:15px;border-radius:8px;font-size:14px;word-break:break-all}
h1{color:#22c55e}
a{color:#22c55e}
</style>
</head>
<body>
<h1>🛡️ AuditYa Pro</h1>
<p>Tu SaaS de Auditorias SEO + SSL - ONLINE 24/7</p>
<p><a href="/ventas">Ver planes y precios →</a></p>
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

VENTAS_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AuditYa Pro - Audita webs en 5 segundos | Ecuador</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,system-ui,sans-serif}
body{background:#0f172a;color:#e2e8f0;line-height:1.6}
.container{max-width:1100px;margin:0 auto;padding:20px}
.header{display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-bottom:1px solid rgba(255,255,255,.06)}
.logo{display:flex;align-items:center;gap:10px;font-weight:900;font-size:20px}
.badge{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);color:#22c55e;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:700}
.btn{padding:12px 24px;border-radius:30px;border:none;font-weight:800;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:8px}
.btn-g{background:#22c55e;color:#0f172a}.btn-w{background:#fff;color:#0f172a}
.hero{text-align:center;padding:60px 0 40px}
.hero h1{font-size:48px;line-height:.95;font-weight:900;color:#fff}
.hero span{background:linear-gradient(to right,#fff,#94a3b8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{margin-top:20px;color:#94a3b8;font-size:18px;max-width:600px;margin-left:auto;margin-right:auto}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin:40px 0}
.card{background:#1e293b;border:1px solid rgba(255,255,255,.06);border-radius:20px;padding:24px;position:relative}
.card.popular{border:2px solid #22c55e;box-shadow:0 0 30px rgba(34,197,94,.2)}
.tag{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#22c55e;color:#0f172a;font-size:11px;font-weight:900;padding:4px 12px;border-radius:20px}
.price{font-size:42px;font-weight:900;color:#fff;margin:10px 0}
.price small{font-size:16px;color:#94a3b8}
ul{list-style:none;margin:16px 0}
li{padding:6px 0;font-size:14px;color:#cbd5e1}li:before{content:"✅ ";color:#22c55e}
.cta{display:block;width:100%;text-align:center;margin-top:16px}
.demo{background:rgba(255,255,255,.03);border:1px dashed rgba(255,255,255,.1);border-radius:16px;padding:30px;text-align:center;margin:50px 0}
@media(max-width:600px){.hero h1{font-size:32px}}
</style>
</head>
<body>
<div class="container">
<div class="header">
<div class="logo">🛡️ AuditYa <span style="color:#22c55e">Pro</span></div>
<div class="badge">● ONLINE 24/7</div>
</div>

<div class="hero">
<h1>Audita cualquier web<br><span>en 5 segundos</span></h1>
<p>Detecta problemas de SSL, SEO y seguridad que tus clientes no ven. Reporte PDF PRO listo para vender en Ecuador.</p>
<br>
<a href="/" class="btn btn-w">Probar Gratis Ahora →</a>
<a href="https://wa.me/593997687995?text=Hola%20Cristhoper%20quiero%20AuditYa%20Pro" class="btn btn-g">Comprar por WhatsApp</a>
</div>

<div class="cards">
<div class="card">
<h3>🟦 Básico</h3>
<div class="price">$27 <small>/mes</small></div>
<ul>
<li>10 auditorías / mes</li>
<li>Reporte PDF PRO</li>
<li>Check SSL + Online</li>
<li>Soporte por WhatsApp</li>
</ul>
<a href="https://wa.me/593997687995?text=Hola%20Cristhoper%20quiero%20el%20Plan%20Basico%20de%20%2427%20de%20AuditYa%20Pro" class="btn btn-w cta">Comprar Básico $27</a>
</div>

<div class="card popular">
<div class="tag">MÁS POPULAR</div>
<h3>🟩 Pro</h3>
<div class="price">$47 <small>/mes</small></div>
<ul>
<li>50 auditorías / mes</li>
<li>PDF con tu logo</li>
<li>Recomendación IA</li>
<li>Prioridad WhatsApp</li>
<li>Acceso 24/7</li>
</ul>
<a href="https://wa.me/593997687995?text=Hola%20Cristhoper%20quiero%20el%20Plan%20Pro%20de%20%2447%20de%20AuditYa%20Pro%20-%20El%20mas%20popular" class="btn btn-g cta">Comprar Pro $47 🔥</a>
</div>

<div class="card">
<h3>🟨 Agencia</h3>
<div class="price">$97 <small>/mes</small></div>
<ul>
<li>Auditorías ilimitadas</li>
<li>White Label total</li>
<li>Vende a tus clientes</li>
<li>Soporte 1 a 1</li>
<li>Grupo VIP</li>
</ul>
<a href="https://wa.me/593997687995?text=Hola%20Cristhoper%20quiero%20el%20Plan%20Agencia%20de%20%2497%20de%20AuditYa%20Pro%20-%20Ilimitado" class="btn btn-w cta">Comprar Agencia $97</a>
</div>
</div>

<div class="demo">
<h2 style="color:#fff">🚀 Demo en vivo</h2>
<p style="color:#94a3b8;margin:10px 0">Tu app ya está funcionando 24/7 en Render</p>
<p style="margin-top:10px"><a href="/" style="color:#22c55e;font-weight:800">auditya-pro.onrender.com → Probar Ahora</a></p>
<p style="margin-top:8px;font-size:12px;color:#64748b">Hecho en Ecuador 🇪🇨 · WhatsApp: 0997687995 · @cristhoperpinos</p>
</div>
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return APP_HTML

@app.get("/ventas", response_class=HTMLResponse)
async def ventas():
    return VENTAS_HTML

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
    except:
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
        recomendacion = "CRITICO: Sitio offline"
    elif not valido:
        recomendacion = "CRITICO: SSL invalido o expirado"
    elif 0 < dias < 30:
        recomendacion = f"ATENCION: SSL expira en {dias} dias"
    return {"dominio":dominio,"online":online,"status_code":status_code,"ssl":{"valido":valido,"dias_restantes":dias},"valido":valido,"dias_restantes":dias,"recomendacion":recomendacion}

@app.get("/health")
def health():
    return {"status":"ok"}
