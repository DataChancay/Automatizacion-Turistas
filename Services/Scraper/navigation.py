# services/scraper/navigation.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ir_a_taquilla(driver, timeout=15):
    """Clic en Taquilla y espera que cargue /reportes/."""
    print("🚀 Navegando a Taquilla…")
    boton = driver.find_element(
        By.XPATH,
        "//div[contains(@class,'btn-success') and normalize-space(.)='Taquilla']"
    )
    print("🔍 HTML botón Taquilla:", boton.get_attribute("outerHTML"))
    boton.click()

    # Opcional: espera a que desaparezca el preloader (si existe)
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.ID, "preloader"))
        )
    except:
        pass

    # Esperar que la URL cambie realmente
    WebDriverWait(driver, timeout).until(
        EC.url_contains("/reportes/")
    )
    print("✅ URL Taquilla:", driver.current_url)

def ir_a_comercial(driver, timeout=15):
    """Clic en Comercial y espera que cargue /reportes_comercial/."""
    print("🚀 Navegando a Comercial…")
    boton = driver.find_element(
        By.XPATH,
        "//div[contains(@class,'btn-success') and normalize-space(.)='Comercial']"
    )
    print("🔍 HTML botón Comercial:", boton.get_attribute("outerHTML"))
    boton.click()

    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.ID, "preloader"))
        )
    except:
        pass

    WebDriverWait(driver, timeout).until(
        EC.url_contains("/reportes_comercial/")
    )
    print("✅ URL Comercial:", driver.current_url)

