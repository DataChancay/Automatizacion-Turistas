# 📋 Guía: Desplegar Automatización en EC2 (Linux)

## 1️⃣ REQUISITOS EN EC2

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias del navegador
sudo apt install -y python3 python3-pip chromium-browser chromium-chromedriver

# Verificar versiones
python3 --version
chromium --version
chromedriver --version
```

## 2️⃣ CONFIGURAR LA APLICACIÓN

```bash
# Clonar o copiar los archivos a EC2
# (Usando SCP desde tu máquina local)
scp -r /ruta/local/Automatización\ sistema\ castillo ec2-user@tu-ec2:/home/ec2-user/

# Entrar a la carpeta
cd ~/Automatización\ sistema\ castillo/

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r Requirements.txt
```

## 3️⃣ CONFIGURAR VARIABLES DE ENTORNO

```bash
# Crear archivo .env en la raíz del proyecto
echo "PORTAL_USER=tu_usuario" > .env
echo "PORTAL_PASS=tu_contraseña" >> .env
echo "GOOGLE_SHEETS_CREDENTIALS=/home/ec2-user/clave.json" >> .env

# Dar permisos
chmod 600 .env
```

## 4️⃣ CONFIGURAR CRON JOB (Ejecución Diaria)

```bash
# Editar crontab
crontab -e

# Agregar esta línea para ejecutar DIARIAMENTE a las 9:00 AM
0 9 * * * cd /home/ec2-user/Automatización\ sistema\ castillo && source venv/bin/activate && python3 run_automation.py

# Otras opciones comunes:
# 0 */6 * * *    → Cada 6 horas
# 0 9,14,18 * * * → A las 9 AM, 2 PM y 6 PM
# */30 * * * *   → Cada 30 minutos
```

## 5️⃣ MONITOREAR EJECUCIONES

```bash
# Ver logs de la última ejecución
tail -f ~/castillo_logs/castillo_*.log

# Ver historial de cron
grep CRON /var/log/syslog
```

## 6️⃣ VERIFICAR FUNCIONALIDAD

```bash
# Ejecutar manualmente para probar
cd ~/Automatización\ sistema\ castillo
source venv/bin/activate
python3 run_automation.py

# Debería crear un archivo de log y completarse sin errores
```

## ⚠️ NOTAS IMPORTANTES

- **Headless Mode**: Ya está activado en `login.py`, no se abrirán ventanas
- **Logs**: Se guardan en `~/castillo_logs/` para debugging
- **Credenciales**: Mantén `.env` seguro con permisos 600
- **Google Sheets**: Asegúrate de que `clave.json` esté en la carpeta raíz
- **Zona Horaria**: Configura correctamente en EC2 con `timedatectl`

## 🔧 SOLUCIONAR PROBLEMAS

```bash
# Si falla el chromedriver:
sudo apt install -y chromium-chromedriver

# Si hay problema con permisos:
sudo chmod +x chromedriver

# Verificar que Chrome esté funcionando:
chromium-browser --headless --dump-dom https://www.google.com
```
