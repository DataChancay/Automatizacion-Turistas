# services/auth/login.py
import os
from dotenv import load_dotenv             # <–– importer de python-dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 0) Cargar .env
load_dotenv()

def iniciar_sesion():
    """Abre Chrome, hace login y devuelve el driver autenticado."""
    # 1) Leer variables desde .env
    usuario    = os.getenv("PORTAL_USER")
    contraseña = os.getenv("PORTAL_PASS")

    # Comprueba que no sean None:
    print("🛠️  Usuario:", usuario, "| Contraseña:", "●" * (len(contraseña) if contraseña else 0))

    # 2) Configurar ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")   # Ejecutar sin interfaz gráfica
    options.add_argument("--no-sandbox")  # Necesario para Linux/EC2
    options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memoria
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
 )


    # 3) Ir a la página de login
    driver.get("http://161.132.243.102:8081/boleteria_v5/login/")

    # 4) Esperar a que el input de DNI exista
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )

    # 5) Verificar que Selenium localiza el elemento correcto
    elem = driver.find_element(By.ID, "user-name")
    print("🔍 HTML del campo DNI:", elem.get_attribute("outerHTML"))

    # 6) Rellenar DNI y contraseña
    elem.send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(contraseña)

    # 7) Pulsar “Ingresar”
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # 8) Esperar a que la URL cambie a /dashboard
    WebDriverWait(driver, 10).until(EC.url_contains("/cajas"))
    print("✅ Login OK, URL actual:", driver.current_url)

    return driver

if __name__ == "__main__":
    iniciar_sesion()
