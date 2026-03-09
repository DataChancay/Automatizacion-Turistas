# main.py
from Services.Auth.login import iniciar_sesion
from Services.Scraper.navigation import ir_a_taquilla, ir_a_comercial
from Services.Scraper.scraper import obtener_datos_tabla
from Services.Uploader.sheets_uploader import exportar_a_sheets

def main():
    driver = iniciar_sesion()

    # --- Taquilla ---
    ir_a_taquilla(driver)
    df_taq = obtener_datos_tabla(driver)
    df_taq.insert(0, "Proviene", "Taquilla")

    # --- Comercial ---
    ir_a_comercial(driver)
    df_com = obtener_datos_tabla(driver)
    df_com.insert(0, "Proviene", "Comercial")

    driver.quit()

    # Reordenar columnas antes de subir
    columnas_deseadas = ["Proviene", "Taquilla", "Cantidad", "PrecioUnit", "Soles", "Porcentaje"]
    df_taq = df_taq[columnas_deseadas]
    df_com = df_com[columnas_deseadas]

    print("\n============================== TAQUILLA ==============================")
    print(df_taq)
    print("\n============================== COMERCIAL ==============================")
    print(df_com)

    exportar_a_sheets(df_taq, "Reporte Automatizado", "Taquilla")
    exportar_a_sheets(df_com, "Reporte Automatizado", "Comercial")

if __name__ == "__main__":
    main()

