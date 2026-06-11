import os
import pandas as pd
import json
from datetime import datetime

RAW_BASE = "data/data_lake/raw"
PROCESSED_BASE = "data/data_lake/processed"

LOG_FILE = "logs/elt.log"


def escribir_log(mensaje):

    os.makedirs("logs", exist_ok=True)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}] {mensaje}\n")


def crear_directorios():

    carpetas = [
        "ventas",
        "clientes",
        "productos",
        "ventas_online",
        "eventos_app"
    ]

    for carpeta in carpetas:
        ruta = os.path.join(
            PROCESSED_BASE,
            carpeta
        )

        os.makedirs(
            ruta,
            exist_ok=True
        )


def procesar_csv(
    carpeta_raw,
    carpeta_processed,
    nombre_salida
):

    ruta_raw = os.path.join(
        RAW_BASE,
        carpeta_raw
    )

    archivos = [
        archivo
        for archivo in os.listdir(ruta_raw)
        if archivo.endswith(".csv")
    ]

    if not archivos:
        return

    lista_df = []

    for archivo in archivos:

        ruta_archivo = os.path.join(
            ruta_raw,
            archivo
        )

        df = pd.read_csv(
            ruta_archivo
        )

        lista_df.append(df)

    df_final = pd.concat(
        lista_df,
        ignore_index=True
    )

    # Eliminar duplicados
    df_final = df_final.drop_duplicates()

    # Eliminar espacios
    df_final = df_final.apply(
        lambda x:
        x.str.strip()
        if x.dtype == "object"
        else x
    )

    # Completar nulos
    df_final = df_final.fillna(
        "Sin Información"
    )

    fecha = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    ruta_salida = os.path.join(
        PROCESSED_BASE,
        carpeta_processed,
        f"{nombre_salida}_{fecha}.csv"
    )

    df_final.to_csv(
        ruta_salida,
        index=False
    )

    mensaje = (
        f"Archivo procesado: "
        f"{ruta_salida}"
    )

    print(mensaje)
    escribir_log(mensaje)


def procesar_json():

    ruta_raw = os.path.join(
        RAW_BASE,
        "eventos_app"
    )

    archivos = [
        archivo
        for archivo in os.listdir(ruta_raw)
        if archivo.endswith(".json")
    ]

    if not archivos:
        return

    eventos = []

    for archivo in archivos:

        ruta_archivo = os.path.join(
            ruta_raw,
            archivo
        )

        with open(
            ruta_archivo,
            "r",
            encoding="utf-8"
        ) as f:

            datos = json.load(f)

            eventos.extend(datos)

    df = pd.DataFrame(eventos)

    df = df.drop_duplicates()

    fecha = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    ruta_salida = os.path.join(
        PROCESSED_BASE,
        "eventos_app",
        f"eventos_app_{fecha}.csv"
    )

    df.to_csv(
        ruta_salida,
        index=False
    )

    mensaje = (
        f"JSON procesado: "
        f"{ruta_salida}"
    )

    print(mensaje)
    escribir_log(mensaje)


def main():

    print("=" * 50)
    print("PROCESO ELT")
    print("=" * 50)

    crear_directorios()

    procesar_csv(
        "ventas_pos",
        "ventas",
        "ventas"
    )

    procesar_csv(
        "clientes_crm",
        "clientes",
        "clientes"
    )

    procesar_csv(
        "productos_erp",
        "productos",
        "productos"
    )

    procesar_csv(
        "ventas_online",
        "ventas_online",
        "ventas_online"
    )

    procesar_json()

    print("\nELT Finalizado")


if __name__ == "__main__":
    main()