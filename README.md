# 🎫 Sistema de Control de Acceso (MVP)

Sistema simple y ligero de control de acceso mediante códigos QR, ideal para eventos en Anfiteatros.

## 🚀 Características
- **Carga Masiva**: Sube listas de invitados desde archivos CSV o Excel (.xlsx).
- **Tickets Personalizados**: Generación automática de tickets con nombre, asiento y código QR.
- **App de Escaneo**: Aplicación web optimizada para móviles para validación rápida en puerta.
- **Validación en Tiempo Real**: Detecta tickets válidos, duplicados o inválidos con feedback visual (verde/rojo) y sonoro.
- **Estadísticas**: Panel con métricas de ingreso en tiempo real.
- **Seguridad**: Configuración HTTPS local para habilitar permisos de cámara en dispositivos móviles.

## 🛠️ Tecnologías
- **Backend**: FastAPI (Python)
- **Base de Datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Librerías**: `html5-qrcode`, `pandas`, `qrcode`

## 📋 Requisitos
- Python 3.10 o superior.

## ⚙️ Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [URL-DEL-REPO]
   cd [NOMBRE-CARPETA]
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generar certificados SSL (Requerido para la cámara en móvil):**
   ```bash
   python generate_cert.py
   ```

4. **Iniciar el servidor:**
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8000 --ssl-keyfile key.pem --ssl-certfile cert.pem
   ```

5. **Acceder:**
   - **Panel Admin**: `https://localhost:8000`
   - **App de Escaneo**: `https://[TU-IP-LOCAL]:8000/scanner`

---
> [!TIP]
> Si el servidor no carga en el móvil, asegúrate de permitir el puerto 8000 en el **Firewall de Windows** o desactivarlo temporalmente para la red privada.
