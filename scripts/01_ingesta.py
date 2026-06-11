import os
import shutil
from datetime import datetime

# CONFIGURACIÓN GENERAL

FUENTES = [
    "ventas_pos",
    "clientes_crm",
    "productos_erp",
    "ventas_online",
    "eventos_app"
]

ORIGEN_BASE = "data/origen"
RAW_BASE = "data/data_lake/raw"

LOG_FILE = "logs/ingesta.log"

# CREAR DIRECTORIOS

def crear_directorios():
    """
    Crea automáticamente las carpetas RAW
    para cada fuente de datos.
    """

    for fuente in FUENTES:
        ruta = os.path.join(RAW_BASE, fuente)
        os.makedirs(ruta, exist_ok=True)

# REGISTRO DE LOGS

def escribir_log(mensaje):

    os.makedirs("logs", exist_ok=True)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}] {mensaje}\n")

# COPIAR ARCHIVOS A RAW

def copiar_archivos(dia):

    print(f"\nProcesando datos del {dia}...\n")

    for fuente in FUENTES:

        carpeta_origen = os.path.join(
            ORIGEN_BASE,
            fuente,
            dia
        )

        carpeta_destino = os.path.join(
            RAW_BASE,
            fuente
        )

        if not os.path.exists(carpeta_origen):

            mensaje = f"No existe carpeta: {carpeta_origen}"

            print(mensaje)
            escribir_log(mensaje)

            continue

        for archivo in os.listdir(carpeta_origen):

            ruta_origen = os.path.join(
                carpeta_origen,
                archivo
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            nombre, extension = os.path.splitext(
                archivo
            )

            nuevo_nombre = (
                f"{nombre}_{timestamp}{extension}"
            )

            ruta_destino = os.path.join(
                carpeta_destino,
                nuevo_nombre
            )

            shutil.copy2(
                ruta_origen,
                ruta_destino
            )

            mensaje = (
                f"Archivo copiado: "
                f"{ruta_origen} -> {ruta_destino}"
            )

            print(mensaje)

            escribir_log(mensaje)

# PROGRAMA PRINCIPAL

def main():

    print("=" * 50)
    print("INGESTA DE DATOS RETAILSTART")
    print("=" * 50)

    crear_directorios()

    dia = input(
        "Ingrese carga a procesar "
        "(dia_1 o dia_2): "
    )

    copiar_archivos(dia)

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()