# sheets_uploader.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
from gspread_formatting import format_cell_range, CellFormat, NumberFormat

def fecha_a_serial(fecha):
    """Convierte un datetime a número serial de Google Sheets (base 1899-12-30)."""
    epoch = datetime(1899, 12, 30)
    delta = fecha - epoch
    return float(delta.days) + (delta.seconds / 86400)

def exportar_a_sheets(df, nombre_hoja, nombre_worksheet="Sheet1", creds_json_path="clave.json"):
    """Agrega un DataFrame a Google Sheets con formatos aplicados automáticamente."""
    
    # Autenticación con Google
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_path, scope)
    cliente = gspread.authorize(creds)

    # Abrir hoja
    hoja = cliente.open(nombre_hoja).worksheet(nombre_worksheet)

    # Fecha actual como número serial para que Sheets la interprete como fecha
    hoy = fecha_a_serial(datetime.now())

    # Limpiar y convertir columnas numéricas
    if "PrecioUnit" in df.columns:
        df["PrecioUnit"] = (
            df["PrecioUnit"]
            .astype(str)
            .str.replace("S/", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["PrecioUnit"] = pd.to_numeric(df["PrecioUnit"], errors="coerce").fillna(0)

    if "Soles" in df.columns:
        df["Soles"] = (
            df["Soles"]
            .astype(str)
            .str.replace("S/", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["Soles"] = pd.to_numeric(df["Soles"], errors="coerce").fillna(0)

    if "Cantidad" in df.columns:
        df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce").fillna(0).astype(int)

    if "Porcentaje" in df.columns:
        df["Porcentaje"] = pd.to_numeric(df["Porcentaje"], errors="coerce").fillna(0)

    # Insertar la fecha como primera columna
    df.insert(1, "Fecha", hoy)

    # Convertir a lista de listas sin encabezados
    valores = df.values.tolist()

    # Buscar la siguiente fila vacía
    fila_actual = len(hoja.get_all_values()) + 1

    # Insertar filas en Sheets
    hoja.update(f"A{fila_actual}", valores)

    # ========================
    # FORMATEAR COLUMNAS
    # ========================
    # Formato de fecha en columna B
    format_cell_range(hoja, f"B{fila_actual}:B{fila_actual+len(valores)-1}", CellFormat(
        numberFormat=NumberFormat(type="DATE", pattern="yyyy-mm-dd")
    ))

    # Si existe columna Porcentaje, formatear
    if "Porcentaje" in df.columns:
        col_porcentaje = df.columns.get_loc("Porcentaje") + 1  # Índice real en Sheets (1-based)
        letra_col = chr(64 + col_porcentaje)  # Convertir a letra
        format_cell_range(hoja, f"{letra_col}{fila_actual}:{letra_col}{fila_actual+len(valores)-1}", CellFormat(
            numberFormat=NumberFormat(type="PERCENT", pattern="0.00%")
        ))

    print(f"✅ {len(valores)} filas añadidas y formato aplicado en '{nombre_worksheet}'")
