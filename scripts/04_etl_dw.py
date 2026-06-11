import sqlite3
import pandas as pd
import os

DB_PATH = "data/warehouse/dw_retailstart.db"
PROCESSED_PATH = "data/data_lake/processed"

# CONEXIÓN SQLITE

def conectar():
    return sqlite3.connect(DB_PATH)

# OBTENER TODOS LOS CSV

def obtener_todos_los_csv(carpeta):

    ruta = os.path.join(
        PROCESSED_PATH,
        carpeta
    )

    if not os.path.exists(ruta):
        return []

    archivos = [

        os.path.join(ruta, archivo)

        for archivo in os.listdir(ruta)

        if archivo.endswith(".csv")

    ]

    return sorted(archivos)

# DIM CLIENTE

def cargar_clientes(conn):

    archivos = obtener_todos_los_csv(
        "clientes"
    )

    for archivo in archivos:

        df = pd.read_csv(archivo)

        for _, row in df.iterrows():

            conn.execute("""

            INSERT OR IGNORE INTO Dim_Cliente
            (
                id_cliente,
                nombre,
                apellido,
                email,
                segmento,
                ciudad
            )

            VALUES (?, ?, ?, ?, ?, ?)

            """,

            (
                row["id_cliente"],
                row["nombre"],
                row["apellido"],
                row["email"],
                row["segmento"],
                row["ciudad"]
            ))

    conn.commit()

# DIM PRODUCTO

def cargar_productos(conn):

    archivos = obtener_todos_los_csv(
        "productos"
    )

    for archivo in archivos:

        df = pd.read_csv(archivo)

        for _, row in df.iterrows():

            conn.execute("""

            INSERT OR IGNORE INTO Dim_Producto
            (
                id_producto,
                nombre_producto,
                categoria,
                precio_base,
                proveedor
            )

            VALUES (?, ?, ?, ?, ?)

            """,

            (
                row["id_producto"],
                row["nombre_producto"],
                row["categoria"],
                row["precio_base"],
                row["proveedor"]
            ))

    conn.commit()

# DIM TIEMPO

def insertar_fecha(conn, fecha):

    fecha = str(fecha)

    anio = int(fecha[0:4])
    mes = int(fecha[5:7])
    dia = int(fecha[8:10])

    conn.execute("""

    INSERT OR IGNORE INTO Dim_Tiempo
    (
        fecha,
        anio,
        mes,
        dia
    )

    VALUES (?, ?, ?, ?)

    """,

    (
        fecha,
        anio,
        mes,
        dia
    ))

    conn.commit()

# DIM CANAL

def cargar_canales(conn):

    canales = [
        "POS",
        "WEB",
        "APP"
    ]

    for canal in canales:

        conn.execute("""

        INSERT OR IGNORE INTO
        Dim_Canal(canal)

        VALUES(?)

        """,

        (canal,))

    conn.commit()

# DIM TIENDA

def cargar_tiendas(conn):

    archivos = obtener_todos_los_csv(
        "ventas"
    )

    for archivo in archivos:

        df = pd.read_csv(archivo)

        tiendas = df["tienda"].unique()

        for tienda in tiendas:

            conn.execute("""

            INSERT OR IGNORE INTO
            Dim_Tienda(tienda)

            VALUES(?)

            """,

            (tienda,))

    conn.commit()

# FACT VENTAS POS

def cargar_ventas(conn):

    archivos = obtener_todos_los_csv(
        "ventas"
    )

    for archivo in archivos:

        df = pd.read_csv(archivo)

        for _, row in df.iterrows():

            insertar_fecha(
                conn,
                row["fecha"]
            )

            id_tiempo = conn.execute("""

            SELECT id_tiempo
            FROM Dim_Tiempo
            WHERE fecha = ?

            """,

            (row["fecha"],)
            ).fetchone()[0]

            id_canal = conn.execute("""

            SELECT id_canal
            FROM Dim_Canal
            WHERE canal = 'POS'

            """

            ).fetchone()[0]

            id_tienda = conn.execute("""

            SELECT id_tienda
            FROM Dim_Tienda
            WHERE tienda = ?

            """,

            (row["tienda"],)
            ).fetchone()[0]

            total = (
                row["cantidad"]
                *
                row["precio_unitario"]
            )

            conn.execute("""

            INSERT OR IGNORE INTO Fact_Ventas
            (
                id_venta,
                id_cliente,
                id_producto,
                id_tiempo,
                id_canal,
                id_tienda,
                cantidad,
                precio_unitario,
                total
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

            """,

            (
                row["id_venta"],
                row["id_cliente"],
                row["id_producto"],
                id_tiempo,
                id_canal,
                id_tienda,
                row["cantidad"],
                row["precio_unitario"],
                total
            ))

    conn.commit()

# FACT VENTAS ONLINE

def cargar_ventas_online(conn):

    archivos = obtener_todos_los_csv(
        "ventas_online"
    )

    if not archivos:
        print("No se encontraron archivos de ventas_online")
        return

    total_ordenes = 0

    for archivo in archivos:

        print(f"\nProcesando ventas online: {archivo}")

        try:

            df = pd.read_csv(archivo)

            print(f"Registros encontrados: {len(df)}")

            for _, row in df.iterrows():

                try:

                    insertar_fecha(
                        conn,
                        row["fecha"]
                    )

                    id_tiempo = conn.execute("""

                    SELECT id_tiempo
                    FROM Dim_Tiempo
                    WHERE fecha = ?

                    """,

                    (row["fecha"],)
                    ).fetchone()[0]

                    canal = str(
                        row["canal"]
                    ).upper()

                    id_canal = conn.execute("""

                    SELECT id_canal
                    FROM Dim_Canal
                    WHERE canal = ?

                    """,

                    (canal,)
                    ).fetchone()[0]

                    conn.execute("""

                    INSERT OR IGNORE INTO
                    Fact_Ventas_Online
                    (
                        id_orden,
                        id_cliente,
                        id_tiempo,
                        id_canal,
                        total
                    )

                    VALUES (?, ?, ?, ?, ?)

                    """,

                    (
                        int(row["id_orden"]),
                        int(row["id_cliente"]),
                        int(id_tiempo),
                        int(id_canal),
                        float(row["total"])
                    ))

                    total_ordenes += 1

                except Exception as e:

                    print("\nError insertando venta online:")
                    print(row)
                    print(e)

        except Exception as e:

            print(f"\nError leyendo archivo {archivo}")
            print(e)

    conn.commit()

    print(f"\nVentas online procesadas: {total_ordenes}")

# FACT EVENTOS

def cargar_eventos(conn):

    archivos = obtener_todos_los_csv(
        "eventos_app"
    )

    if not archivos:
        print("No se encontraron archivos de eventos_app")
        return

    total_eventos = 0

    for archivo in archivos:

        print(f"\nProcesando eventos: {archivo}")

        try:

            df = pd.read_csv(archivo)

            print(f"Registros encontrados: {len(df)}")

            for _, row in df.iterrows():

                try:

                    conn.execute("""

                    INSERT OR IGNORE INTO Fact_Eventos
                    (
                        id_evento,
                        id_cliente,
                        id_producto,
                        tipo
                    )

                    VALUES (?, ?, ?, ?)

                    """,

                    (
                        int(row["id_evento"]),
                        int(row["id_cliente"]),
                        int(row["producto"]),
                        str(row["tipo"])
                    ))

                    total_eventos += 1

                except Exception as e:

                    print("\nError insertando evento:")
                    print(row)
                    print(e)

        except Exception as e:

            print(f"\nError leyendo archivo {archivo}")
            print(e)

    conn.commit()

    print(f"\nEventos procesados: {total_eventos}")

# MAIN

def main():

    print("=" * 50)
    print("ETL HACIA DATA WAREHOUSE")
    print("=" * 50)

    conn = conectar()

    print("\nCargando clientes...")
    cargar_clientes(conn)

    print("\nCargando productos...")
    cargar_productos(conn)

    print("\nCargando canales...")
    cargar_canales(conn)

    print("\nCargando tiendas...")
    cargar_tiendas(conn)

    print("\nCargando ventas físicas...")
    cargar_ventas(conn)

    print("\nCargando ventas online...")
    cargar_ventas_online(conn)

    print("\nCargando eventos...")
    cargar_eventos(conn)

    conn.close()

    print("\nCarga completada correctamente.")


if __name__ == "__main__":
    main()