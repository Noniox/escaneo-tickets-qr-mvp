"""
Event Access Control System - MVP
A simple QR-based check-in system for events

Run with: python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import pandas as pd
import qrcode
from io import BytesIO
import socket
import database as db

def get_local_ip():
    """Get the local IP address of the machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Initialize FastAPI app
app = FastAPI(
    title="Sistema de Control de Acceso",
    description="MVP para escaneo de tickets con QR",
    version="1.0.0"
)

# Setup static files and templates
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ============================================================
# ADMIN ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def admin_panel(request: Request):
    """Main admin panel - upload data and view guests"""
    guests = db.get_all_guests()
    stats = db.get_stats()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "guests": guests,
        "stats": stats
    })


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload CSV or Excel file with guest data"""
    try:
        # Read file content
        content = await file.read()
        
        # Detect file type and parse
        if file.filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(BytesIO(content))
        else:
            raise HTTPException(400, "Formato no soportado. Use CSV o Excel (.xlsx)")
        
        # Normalize column names (case-insensitive)
        df.columns = df.columns.str.strip().str.lower()
        
        # Validate required columns
        required = ['nombre', 'asiento']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise HTTPException(400, f"Columnas faltantes: {', '.join(missing)}")
        
        # Clear existing guests and add new ones
        db.clear_guests()
        
        count = 0
        for _, row in df.iterrows():
            nombre = str(row['nombre']).strip()
            email = str(row.get('email', '')).strip() if 'email' in df.columns else ''
            asiento = str(row['asiento']).strip()
            
            if nombre and asiento:
                db.add_guest(nombre, email, asiento)
                count += 1
        
        return JSONResponse({
            "success": True,
            "message": f"{count} invitados cargados exitosamente",
            "count": count
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error procesando archivo: {str(e)}")


@app.get("/guests")
async def get_guests():
    """Get all guests as JSON"""
    return db.get_all_guests()


@app.get("/stats")
async def get_stats():
    """Get check-in statistics"""
    return db.get_stats()


@app.post("/reset")
async def reset_checkins():
    """Reset all check-ins"""
    count = db.reset_all_checkins()
    return {"success": True, "message": f"{count} check-ins reiniciados"}


# ============================================================
# QR GENERATION
# ============================================================

@app.get("/qr/{guest_uuid}")
async def generate_qr(guest_uuid: str):
    """Generate QR code image for a guest"""
    guest = db.get_guest_by_uuid(guest_uuid)
    if not guest:
        raise HTTPException(404, "Invitado no encontrado")
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(guest_uuid)
    qr.make(fit=True)
    
    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Return as PNG
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="image/png")


@app.get("/ticket/{guest_uuid}", response_class=HTMLResponse)
async def ticket_view(request: Request, guest_uuid: str):
    """Printable ticket view with QR code"""
    guest = db.get_guest_by_uuid(guest_uuid)
    if not guest:
        raise HTTPException(404, "Invitado no encontrado")
    
    return templates.TemplateResponse("ticket.html", {
        "request": request,
        "guest": guest
    })


# ============================================================
# SCANNER (For door staff)
# ============================================================

@app.get("/scanner", response_class=HTMLResponse)
async def scanner_page(request: Request):
    """QR Scanner page for door staff"""
    return templates.TemplateResponse("scanner.html", {"request": request})


@app.post("/scan")
async def validate_scan(request: Request):
    """Validate a scanned QR code"""
    try:
        body = await request.json()
        guest_uuid = body.get("code", "").strip()
        
        if not guest_uuid:
            return JSONResponse({
                "status": "invalid",
                "message": "CÓDIGO VACÍO"
            })
        
        # Find guest
        guest = db.get_guest_by_uuid(guest_uuid)
        
        if not guest:
            return JSONResponse({
                "status": "invalid",
                "message": "CÓDIGO INVÁLIDO",
                "nombre": None,
                "asiento": None
            })
        
        if guest["checked_in"]:
            return JSONResponse({
                "status": "already_used",
                "message": "TICKET YA USADO",
                "nombre": guest["nombre"],
                "asiento": guest["asiento"]
            })
        
        # Mark as checked in
        db.check_in_guest(guest_uuid)
        
        return JSONResponse({
            "status": "valid",
            "message": "¡BIENVENIDO!",
            "nombre": guest["nombre"],
            "asiento": guest["asiento"]
        })
        
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Error: {str(e)}"
        })


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Ensure database is initialized on startup"""
    db.init_db()
    local_ip = get_local_ip()
    print("Sistema de Control de Acceso iniciado")
    print(f"Panel de admin: https://localhost:8000")
    print(f"Panel de admin (Red): https://{local_ip}:8000")
    print(f"Scanner (Móvil): https://{local_ip}:8000/scanner")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
