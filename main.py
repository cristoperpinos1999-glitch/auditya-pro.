from fastapi import FastAPI, Query, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
import httpx, ssl, socket, json, os, random, string
from datetime import datetime

app = FastAPI(title="AuditYa Pro - SEO + Licencias")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

CODES_FILE = "codes.json"
ADMIN_PASS = "Cristhoper2025"
WHATSAPP = "593997687995"
BASE_URL = "https://auditya-pro.onrender.com"

def load_codes():
    if os.path.exists(CODES_FILE):
        try:
            with open(CODES_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_codes(codes):
    try:
        with open(CODES_FILE, "w") as f:
            json.dump(codes, f, indent=2)
    except:
        pass

def gen_code(plan):
    prefix = {"Basico":"BAS","Pro":"PRO","Agencia":"AGY"}.get(plan, "PRO")
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{rand[:4]}-{rand[4:]}"

codes_db = load_codes()
if not codes_db:
    codes_db = {
        "PRO-TEST-CRISTHOPER": {"plan":"Pro","limite":50,"usados":0,"email":"cristhoperpinos@test.com","activo":True,"creado": str(datetime.now())},
    }
    save_codes(codes_db)

# --- SEO ROUTES ---
@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return f"""User-agent: *
Allow: /
Disallow: /admin
Sitemap: {BASE_URL}/sitemap.xml
"""

@app.get("/sitemap.xml")
async def sitemap():
    now = datetime.now().strftime("%Y-%m-%d")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{BASE_URL}/</loc><lastmod>{now}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>
  <url><loc>{BASE_URL}/ventas</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>{BASE_URL}/activar</loc><lastmod>{now}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
</urlset>"""
    return Response(content=xml, media_type="application/xml")

HOME_HTML = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>AuditYa Pro - Auditor Web SSL y SEO en 5 segundos | Ecuador</title>
<meta name="description" content="Audita cualquier web en 5 segundos. Detecta SSL expirado, web caída y errores SEO. Reporte PDF PRO listo para vender. Desde $27. WhatsApp 0997687995">
<meta name="keywords" content="auditor web, auditor ssl, revisar ssl, seo ecuador, auditor web ecuador, auditya pro, check ssl, web caida">
<meta name="author" content="Cristhoper Pinos - AuditYa Pro">
<meta property="og:title" content="AuditYa Pro - Auditor Web en 5s">
<meta property="og:description" content="Detecta problemas de SSL y SEO que tus clientes no ven. Reporte PDF PRO">
<meta property="og:url" content="{BASE_URL}">
<meta property="og:type" content="website">
<link rel="canonical" href="{BASE_URL}/">
<style>body{{font-family:system-ui;background:#0f172a;color:#fff;padding:20px;text-align:center}}
.card{{background:#1e293b;max-width:650px;margin:20px auto;padding:20px;border-radius:12px;border:1px solid rgba(255,255,255,.08)}}
input{{padding:12px;width:90%;max-width:400px;border-radius:8px;border:1px solid rgba(255,255,255,.1);background:#0f172a;color:#fff;margin:8px;font-size:15px}}
.btn{{padding:12px 22px;border:none;border-radius:30px;font-weight:800;cursor:pointer;margin:5px}}
.btn-g{{background:#22c55e;color:#0f172a}} .btn-w{{background:#fff;color:#0f172a}} .btn-b{{background:#3b82f6;color:#fff}}
#res{{margin-top:15px;text-align:left;background:#0f172a;padding:15px;border-radius:10px;font-size:14px;word-break:break-all;border:1px solid rgba(255,255,255,.06)}}
.badge{{display:inline-block;background:rgba(34,197,94,.15);border:1px solid rgba(34,197,94,.3);color:#22c55e;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:800}}
a{{color:#22c55e;text-decoration:none;font-weight:700}}
.code-ok{{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);color:#86efac;padding:10px;border-radius:8px;margin:10px 0}}
</style>
</head>
<body>
<h1>🛡️ AuditYa Pro</h1>
<p><span class="badge">● ONLINE 24/7</span> · Auditor Web #1 Ecuador 🇪🇨</p>
<p><a href="/ventas">Ver planes $27/$47/$97 →</a> | <a href="/activar">Activar código →</a></p>
<div class="card">
<h3>🔍 Audita tu web gratis</h3>
<input id="url" placeholder="https://ejemplo.com">
<input id="codigo" placeholder="Código PRO (opcional) Ej: PRO-8X2J-99A1">
<br>
<button class="btn btn-g" onclick="auditar()">AUDITAR AHORA</button>
<button class="btn btn-b" onclick="pdf()">📄 PDF PRO</button>
<div id="info"></div>
<div id="res">Ingresa una URL para auditar...<br><br>💡 Tip: Sin código 1 demo gratis. Con código Pro 50 auditorías.<br><br><small style="color:#64748b">Indexado en Google · sitemap.xml · robots.txt</small></div>
</div>
<script>
let lastData=null;
async function auditar(){{
 let u=document.getElementById('url').value;
 let c=document.getElementById('codigo').value.trim().toUpperCase();
 if(!u){{alert('Pon una URL');return}}
 document.getElementById('res').innerHTML='⏳ Auditando '+u+'...';
 try{{
  let url='/auditar?url='+encodeURIComponent(u);
  if(c) url+='&codigo='+encodeURIComponent(c);
  let r=await fetch(url);
  let d=await r.json();
  if(d.error){{document.getElementById('res').innerHTML='❌ '+d.error; return;}}
  lastData=d;
  let html='<b>Dominio:</b> '+d.dominio+'<br><b>Online:</b> '+(d.online?'✅ Si':'❌ No')+' ('+d.status_code+')<br><b>SSL:</b> '+(d.ssl.valido?'✅ Valido':'❌ Invalido')+'<br><b>Dias:</b> '+d.ssl.dias_restantes+'<br><b>Recomendacion:</b> '+d.recomendacion;
  if(d.licencia){{html='<div class=code-ok>✅ '+d.licencia.plan+' | Usados: '+d.licencia.usados+'/'+d.licencia.limite+' | Restan: '+(d.licencia.limite-d.licencia.usados)+'</div>'+html;}}
  document.getElementById('res').innerHTML=html;
 }}catch(e){{document.getElementById('res').innerHTML='❌ Error: '+e}}
}}
function pdf(){{
 if(!lastData){{alert('Primero audita');return}}
 let d=lastData;
 let w=window.open('','_blank');
 w.document.write('<html><head><title>Reporte '+d.dominio+'</title></head><body style="font-family:Arial;padding:30px"><h1>Reporte AuditYa Pro</h1><p><b>Dominio:</b> '+d.dominio+'</p><p><b>Online:</b> '+d.online+'</p><p><b>SSL Valido:</b> '+d.ssl.valido+'</p><p><b>Dias restantes:</b> '+d.ssl.dias_restantes+'</p><p><b>Recomendacion:</b> '+d.recomendacion+'</p>'+(d.licencia?'<p><b>Licencia:</b> '+d.licencia.plan+' - '+d.licencia.codigo+'</p>':'')+'<p><b>Fecha:</b> '+new Date().toLocaleString()+'</p><hr><p>Generado por AuditYa Pro - {BASE_URL} | WhatsApp 0997687995</p><script>window.print();<\\/script></body></html>');
}}
</script>
</body>
</html>
"""

VENTAS_HTML = f"""
<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AuditYa Pro - Planes $27 $47 $97 | Auditor Web Ecuador</title>
<meta name="description" content="Auditor web en 5 segundos. Planes desde $27. Detecta SSL expirado y errores SEO. Código automático por WhatsApp 0997687995">
<meta name="keywords" content="auditor web precio, auditor ssl ecuador, comprar auditor web, auditya pro precio">
<link rel="canonical" href="{BASE_URL}/ventas">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}}
body{{background:#0f172a;color:#e2e8f0}} .container{{max-width:1100px;margin:0 auto;padding:20px}}
.header{{display:flex;justify-content:space-between;padding:16px 0;border-bottom:1px solid rgba(255,255,255,.06)}} .logo{{font-weight:900;font-size:20px}} .badge{{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);color:#22c55e;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:800}}
.btn{{padding:12px 24px;border-radius:30px;border:none;font-weight:800;cursor:pointer;text-decoration:none;display:inline-block}} .btn-g{{background:#22c55e;color:#0f172a}} .btn-w{{background:#fff;color:#0f172a}}
.hero{{text-align:center;padding:50px 0}} .hero h1{{font-size:42px;font-weight:900;color:#fff;line-height:.95}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin:40px 0}}
.card{{background:#1e293b;border:1px solid rgba(255,255,255,.06);border-radius:20px;padding:24px;position:relative}}
.card.popular{{border:2px solid #22c55e}} .tag{{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#22c55e;color:#0f172a;font-size:11px;font-weight:900;padding:4px 12px;border-radius:20px}}
.price{{font-size:40px;font-weight:900;color:#fff;margin:10px 0}} .price small{{font-size:15px;color:#94a3b8}}
ul{{list-style:none;margin:14px 0}} li{{padding:5px 0;font-size:14px}} li:before{{content:"✅ "}} .cta{{width:100%;text-align:center;margin-top:14px}}
.flujo{{background:rgba(255,255,255,.03);border-radius:16px;padding:24px;margin:40px 0;text-align:center}}
.paso{{display:inline-block;background:#1e293b;padding:10px 16px;border-radius:30px;margin:6px;font-size:13px;border:1px solid rgba(255,255,255,.08)}}
@media(max-width:600px){{.hero h1{{font-size:28px}}}}
</style>
</head>
<body><div class="container">
<div class="header"><div class="logo">🛡️ AuditYa Pro</div><div class="badge">● ONLINE 24/7</div></div>
<div class="hero">
<h1>Audita webs en 5s<br><span style="color:#94a3b8">y cobra $27-$97</span></h1>
<p style="margin-top:16px;color:#94a3b8">Sistema automático de licencias + SEO Google listo</p><br>
<a href="/" class="btn btn-w">Probar Gratis</a>
<a href="#planes" class="btn btn-g">Ver Planes</a>
</div>
<div class="flujo">
<h3 style="color:#fff;margin-bottom:12px">🔄 Cómo funciona después de pagar:</h3>
<div><span class="paso">1️⃣ Cliente paga → WhatsApp 0997687995</span><br>
<span class="paso">2️⃣ Tú generas código en /admin?pass=Cristhoper2025</span><br>
<span class="paso">3️⃣ Cliente activa en /activar → ✅ Plan listo</span></div>
</div>
<div id="planes" class="cards">
<div class="card"><h3>🟦 Básico</h3><div class="price">$27 <small>/mes</small></div><ul><li>10 auditorías</li><li>PDF PRO</li><li>SSL + Online</li></ul><a href="https://wa.me/{WHATSAPP}?text=Hola%20quiero%20Plan%20Basico%20%2427" class="btn btn-w cta">Comprar $27</a></div>
<div class="card popular"><div class="tag">MÁS POPULAR</div><h3>🟩 Pro</h3><div class="price">$47 <small>/mes</small></div><ul><li>50 auditorías</li><li>PDF con logo</li><li>Soporte WhatsApp</li><li>Código automático</li></ul><a href="https://wa.me/{WHATSAPP}?text=Hola%20quiero%20Plan%20Pro%20%2447" class="btn btn-g cta">Comprar $47 🔥</a></div>
<div class="card"><h3>🟨 Agencia</h3><div class="price">$97 <small>/mes</small></div><ul><li>Ilimitado</li><li>White Label</li><li>Vende a clientes</li></ul><a href="https://wa.me/{WHATSAPP}?text=Hola%20quiero%20Plan%20Agencia%20%2497" class="btn btn-w cta">Comprar $97</a></div>
</div>
<p style="text-align:center;color:#64748b;font-size:12px;margin:20px 0">WhatsApp: 0997687995 · @cristhoperpinos · Ecuador 🇪🇨 · <a href="/sitemap.xml" style="color:#64748b">sitemap.xml</a> | <a href="/robots.txt" style="color:#64748b">robots.txt</a></p>
</div></body></html>
"""

ACTIVAR_HTML = """
<!DOCTYPE html>
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Activar Código - AuditYa Pro</title>
<style>body{font-family:system-ui;background:#0f172a;color:#fff;display:flex;min-height:100vh;align-items:center;justify-content:center;padding:20px}
.card{background:#1e293b;max-width:450px;width:100%;padding:30px;border-radius:16px;border:1px solid rgba(255,255,255,.08);text-align:center}
input{padding:14px;width:100%;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:#0f172a;color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase;text-align:center;margin:12px 0}
.btn{padding:14px 24px;border:none;border-radius:30px;font-weight:800;cursor:pointer;width:100%;font-size:15px}
.btn-g{background:#22c55e;color:#0f172a} .ok{background:rgba(34,197,94,.15);border:1px solid rgba(34,197,94,.3);color:#86efac;padding:12px;border-radius:10px;margin:12px 0}
.err{background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.3);color:#fca5a5;padding:12px;border-radius:10px;margin:12px 0}
a{color:#22c55e}
</style>
</head>
<body>
<div class="card">
<h2>🔑 Activar mi Código</h2>
<p style="color:#94a3b8;font-size:14px;margin:8px 0">Te llegó por WhatsApp después de pagar</p>
<input id="codigo" placeholder="Ej: PRO-8X2J-99A1">
<button class="btn btn-g" onclick="activar()">ACTIVAR AHORA</button>
<div id="res"></div>
<p style="margin-top:20px;font-size:13px;color:#64748b">¿No tienes código? <a href="/ventas">Compra aquí</a> · WhatsApp 0997687995</p>
</div>
<script>
async function activar(){
 let c=document.getElementById('codigo').value.trim().toUpperCase();
 if(!c){alert('Pon tu código');return}
 document.getElementById('res').innerHTML='⏳ Verificando...';
 try{
  let r=await fetch('/activar/validar?codigo='+encodeURIComponent(c));
  let d=await r.json();
  if(d.valido){
    document.getElementById('res').innerHTML='<div class=ok>✅ CÓDIGO VÁLIDO<br><b>'+d.plan+'</b> - '+d.limite+' auditorías<br>Usados: '+d.usados+' | Restan: '+(d.limite-d.usados)+'<br><br>Ya puedes usarlo en la <a href=/>app principal</a><br>Pon tu código en el campo Código PRO</div>';
  }else{
    document.getElementById('res').innerHTML='<div class=err>❌ '+d.error+'</div>';
  }
 }catch(e){document.getElementById('res').innerHTML='<div class=err>Error: '+e+'</div>'}
}
</script>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html>
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Admin - AuditYa Pro</title>
<style>body{font-family:system-ui;background:#0f172a;color:#fff;padding:20px}
.container{max-width:800px;margin:0 auto}
.card{background:#1e293b;padding:20px;border-radius:12px;margin:15px 0;border:1px solid rgba(255,255,255,.06)}
input,select{padding:10px;border-radius:8px;border:1px solid rgba(255,255,255,.1);background:#0f172a;color:#fff;margin:5px;width:200px}
.btn{padding:10px 18px;border:none;border-radius:8px;font-weight:800;cursor:pointer}
.btn-g{background:#22c55e;color:#0f172a}.btn-b{background:#3b82f6;color:#fff}
table{width:100%;border-collapse:collapse;margin-top:15px;font-size:13px}
th,td{padding:8px;text-align:left;border-bottom:1px solid rgba(255,255,255,.08)}
th{color:#94a3b8;font-size:11px}
.code{font-family:monospace;background:rgba(34,197,94,.15);padding:4px 8px;border-radius:6px;color:#86efac}
</style>
</head>
<body><div class="container">
<h1>🔐 Admin AuditYa Pro</h1>
<p style="color:#94a3b8">WhatsApp: 0997687995 · Genera códigos después de cobrar</p>
<div class="card">
<h3>➕ Generar Nuevo Código</h3>
<form onsubmit="generar(event)">
<input id="email" placeholder="Email cliente" required>
<select id="plan"><option value="Basico">Básico $27 - 10 audits</option><option value="Pro" selected>Pro $47 - 50 audits</option><option value="Agencia">Agencia $97 - 999 audits</option></select>
<button type="submit" class="btn btn-g">Generar Código</button>
</form>
<div id="nuevo"></div>
</div>
<div class="card">
<h3>📋 Códigos Generados (<span id="total">0</span>)</h3>
<div id="lista">Cargando...</div>
</div>
<script>
async function load(){
 let r=await fetch('/admin/lista?pass={{PASS}}');
 let d=await r.json();
 document.getElementById('total').innerText=d.total;
 let html='<table><tr><th>Código</th><th>Plan</th><th>Email</th><th>Usados/Limite</th><th>Estado</th></tr>';
 d.codigos.forEach(c=>{
   html+=`<tr><td><span class=code>${c.codigo}</span></td><td>${c.plan}</td><td>${c.email}</td><td>${c.usados}/${c.limite}</td><td>${c.activo?'✅':'❌'}</td></tr>`;
 });
 html+='</table>';
 document.getElementById('lista').innerHTML=html;
}
async function generar(e){
 e.preventDefault();
 let email=document.getElementById('email').value;
 let plan=document.getElementById('plan').value;
 let r=await fetch('/admin/generar?pass={{PASS}}&email='+encodeURIComponent(email)+'&plan='+encodeURIComponent(plan),{method:'POST'});
 let d=await r.json();
 if(d.ok){
   document.getElementById('nuevo').innerHTML='<p style=color:#86efac;margin-top:10px>✅ Código: <span class=code>'+d.codigo.codigo+'</span> para '+plan+'<br>Mensaje para WhatsApp: <br><textarea style=width:100%;margin-top:6px;padding:8px;background:#0f172a;color:#fff;border-radius:8px>¡Gracias por tu compra! 🎉 Tu código AuditYa Pro '+plan+' es: '+d.codigo.codigo+' Actívalo aquí: https://auditya-pro.onrender.com/activar WhatsApp: 0997687995</textarea></p>';
   load();
 }else{alert(d.error)}
}
load();
</script>
</div></body></html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HOME_HTML

@app.get("/ventas", response_class=HTMLResponse)
async def ventas():
    return VENTAS_HTML

@app.get("/activar", response_class=HTMLResponse)
async def activar_page():
    return ACTIVAR_HTML

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(pass_: str = Query(None, alias="pass")):
    if pass_ != ADMIN_PASS:
        return HTMLResponse("""
        <body style="background:#0f172a;color:#fff;font-family:system-ui;display:flex;align-items:center;justify-content:center;min-height:100vh">
        <div style="text-align:center"><h2>🔐 Admin Privado</h2><p>Acceso solo para Cristhoper</p>
        <form method="get"><input type="password" name="pass" placeholder="Contraseña" style="padding:10px;border-radius:8px"><button style="padding:10px 20px;border:none;background:#22c55e;border-radius:8px;font-weight:800;margin-left:6px">Entrar</button></form>
        <p style="font-size:12px;color:#64748b;margin-top:10px">Contraseña: Cristhoper2025</p></div></body>
        """, status_code=401)
    html = ADMIN_HTML.replace("{{PASS}}", ADMIN_PASS)
    return HTMLResponse(html)

@app.get("/admin/lista")
async def admin_lista(pass_: str = Query(None, alias="pass")):
    if pass_ != ADMIN_PASS:
        return JSONResponse({"error":"No autorizado"}, status_code=401)
    codes = load_codes()
    lista = []
    for k,v in codes.items():
        lista.append({"codigo":k, **v})
    return {"total": len(lista), "codigos": lista[::-1]}

@app.post("/admin/generar")
async def admin_generar(pass_: str = Query(None, alias="pass"), email: str = Query(...), plan: str = Query(...)):
    if pass_ != ADMIN_PASS:
        return JSONResponse({"error":"No autorizado"}, status_code=401)
    limite = {"Basico":10,"Pro":50,"Agencia":999}.get(plan, 50)
    codigo = gen_code(plan)
    codes = load_codes()
    codes[codigo] = {"plan":plan,"limite":limite,"usados":0,"email":email,"activo":True,"creado":str(datetime.now())}
    save_codes(codes)
    return {"ok":True,"codigo":{"codigo":codigo,"plan":plan,"limite":limite,"email":email}}

@app.get("/activar/validar")
async def activar_validar(codigo: str = Query(...)):
    codigo = codigo.strip().upper()
    codes = load_codes()
    if codigo not in codes:
        return {"valido":False,"error":"Código no existe. Compra en /ventas"}
    c = codes[codigo]
    if not c.get("activo"):
        return {"valido":False,"error":"Código desactivado"}
    if c["usados"] >= c["limite"]:
        return {"valido":False,"error":f"Agotado {c['usados']}/{c['limite']}. Renueva en /ventas"}
    return {"valido":True, **c, "codigo":codigo}

@app.get("/auditar")
async def auditar(url: str = Query(...), codigo: str = Query(None)):
    codes = load_codes()
    licencia_info = None
    if codigo:
        codigo = codigo.strip().upper()
        if codigo not in codes:
            return JSONResponse({"error": f"Código {codigo} no existe. Compra en /ventas"}, status_code=402)
        c = codes[codigo]
        if not c.get("activo"):
            return JSONResponse({"error":"Código desactivado"}, status_code=402)
        if c["usados"] >= c["limite"]:
            return JSONResponse({"error":f"Límite {c['usados']}/{c['limite']}. Renueva en /ventas WhatsApp 0997687995"}, status_code=402)
        codes[codigo]["usados"] += 1
        save_codes(codes)
        licencia_info = {"codigo":codigo,"plan":c["plan"],"limite":c["limite"],"usados":codes[codigo]["usados"]}

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
    recomendacion = "TODO BIEN"
    if not online:
        recomendacion = "CRITICO: Offline"
    elif not valido:
        recomendacion = "CRITICO: SSL invalido"
    elif 0 < dias < 30:
        recomendacion = f"ATENCION: SSL expira en {dias} dias"
    result = {"dominio":dominio,"online":online,"status_code":status_code,"ssl":{"valido":valido,"dias_restantes":dias},"recomendacion":recomendacion}
    if licencia_info:
        result["licencia"] = licencia_info
    return result

@app.get("/health")
def health():
    return {"status":"ok","codes":len(load_codes())}
