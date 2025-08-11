# services/scraper/scraper.py

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obtener_datos_tabla(driver, timeout=15):
    """
    1) Asume que driver ya está en la página de reportes (Taquilla/Comercial).
    2) Pulsa el botón Filtrar.
    3) Espera a que cargue la PRIMERA tabla dentro de #imp.
    4) Extrae solo esa tabla, descarta la fila “Total” y devuelve un DataFrame
       con las 5 columnas: Taquilla, Cantidad, PrecioUnit, Soles, Porcentaje.
    """
    wait = WebDriverWait(driver, timeout)

    # 1) Pulsar Filtrar dentro de #imp
    boton = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//div[@id='imp']//button[contains(normalize-space(.), 'Filtrar')]"
    )))
    print("👉 Pulsando Filtrar:", boton.get_attribute("outerHTML"))
    boton.click()

    # 2) Esperar a que reaparezca la PRIMERA tabla en #imp
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR,
        "#imp table:first-of-type tbody tr"
    )))

    # 3) Localizar esa tabla y sus filas
    tabla = driver.find_element(By.CSS_SELECTOR, "#imp table:first-of-type")
    filas = tabla.find_elements(By.CSS_SELECTOR, "tbody tr")
    print(f"🗂️ Filas en PRIMERA tabla (incluye “Total”): {len(filas)}")

    # 4) Extraer datos y descartar la fila “Total”
    data = []
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if not celdas:
            continue
        textos = [td.text.strip() for td in celdas]
        # Saltar la fila cuyo primer campo empiece por “Total”
        if textos[0].lower().startswith("total"):
            continue
        data.append(textos)

    print(f"↪ Filas útiles (sin “Total”): {len(data)}")

    # 5) Crear DataFrame con esas 5 columnas
    df = pd.DataFrame(data, columns=[
        "Taquilla", "Cantidad", "PrecioUnit", "Soles", "Porcentaje"
    ])

    # Convertir 'Cantidad' a número
    df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce").fillna(0).astype(int)

     # Convertir 'Porcentaje' a número decimal
    df["Porcentaje"] = (
        df["Porcentaje"]
          .str.replace("%", "", regex=False)
          .str.strip()
    )
    df["Porcentaje"] = pd.to_numeric(df["Porcentaje"], errors="coerce").fillna(0) / 100

    # Eliminar última fila (siempre, por si es un resumen)
    if not df.empty:
        df = df.iloc[:-1]

    print("📊 Primeras filas del DataFrame:")
    print(df.head())
    return df
