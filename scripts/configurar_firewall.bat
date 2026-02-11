@echo off
echo Solicitando permisos de administrador para abrir el puerto 8000...
PowerShell -Command "Start-Process cmd -Verb RunAs -ArgumentList '/k netsh advfirewall firewall add rule name=\"Ticket Scanner App\" dir=in action=allow protocol=TCP localport=8000'"
echo.
echo Si aparecio una ventana negra y se cerro rapido (o pidio permiso), ya deberia estar listo.
echo Intenta acceder de nuevo desde el celular.
pause
