# Sistema de Control de Acceso - Instrucciones de Instalación

Este sistema permite escanear tickets y gestionar el acceso de invitados. Está diseñado para ser portable y fácil de instalar en cualquier computadora Windows.

## 📁 Estructura de Carpetas

*   **_INSTALAR_PRIMERO.bat**: Ejecute esto PRIMERO en una nueva PC. Instala todo lo necesario.
*   **_INICIAR_SISTEMA.bat**: Ejecute esto para abrir el sistema cuando ya esté instalado.
*   **data/**: Carpeta donde se guardan los archivos de datos (Excel original y lista maestra).
*   **scripts/**: Scripts de utilidad (configuración de firewall, acceso remoto, etc.).
*   **app.py / database.py**: Código fuente del sistema.

## 🚀 Pasos para Instalar en una Nueva PC

1.  **Copiar la carpeta**: Copie toda la carpeta del proyecto al Disco C: o al Escritorio de la nueva PC.
    *   *Nota: No es necesario copiar la carpeta `venv` ni `__pycache__` si existen, ya que se crearán de nuevo.*

2.  **Instalar Python**: Asegúrese de que la PC tenga instalado **Python 3.10 o superior**.
    *   Puede descargarlo gratis en: https://www.python.org/downloads/
    *   **IMPORTANTE**: Al instalar, marque la casilla **"Add Python to PATH"** (Agregar Python al PATH).

3.  **Ejecutar Instalador**:
    *   Haga doble clic en el archivo `_INSTALAR_PRIMERO.bat`.
    *   Espere a que termine el proceso (puede tardar unos minutos descargando librerías).
    *   Si todo sale bien, verá un mensaje de "INSTALACION COMPLETADA CON EXITO".

4.  **Iniciar el Sistema**:
    *   Haga doble clic en `_INICIAR_SISTEMA.bat`.
    *   Se abrirá una ventana negra (el servidor) y automáticamente su navegador web en la dirección del sistema.

## 📋 Gestión de Invitados

*   **Lista Maestra**: El sistema carga inicialmente los invitados desde `data/lista_maestra.csv`.
*   **Reiniciar Base de Datos**: Si desea borrar todo y volver a cargar la lista original, puede ejecutar de nuevo `_INSTALAR_PRIMERO.bat` (esto reiniciará la base de datos) o borrar el archivo `invitados.db` manualmente.

## 🛠 Solución de Problemas

*   **Error "Python no encontrado"**: Verifique que instaló Python y marcó la opción "Add to PATH". Reinicie la PC.
*   **Acceso desde celulares (LAN)**: Si desea escanear con celulares conectados al mismo Wi-Fi:
    1.  Ejecute `scripts/configurar_firewall.bat` como Administrador (clic derecho -> Ejecutar como admin).
    2.  Busque la IP de la PC (ej. `192.168.1.15`) y use esa dirección en el celular: `http://192.168.1.15:8000`.

## 📞 Soporte
Si tiene dudas, contacte al desarrollador.
