import sqlite3
import os

DB_PATH = "data/warehouse/dw_retailstart.db"

# CREAR DIRECTORIO

def crear_directorio():

    os.makedirs(
        "data/warehouse",
        exist_ok=True
    )

# CONEXIÓN

def conectar():

    return sqlite3.connect(
        DB_PATH
    )

# DIM CLIENTE

def crear_dim_cliente(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Dim_Cliente (

        id_cliente INTEGER PRIMARY KEY,

        nombre TEXT NOT NULL,

        apellido TEXT NOT NULL,

        email TEXT,

        segmento TEXT,

        ciudad TEXT

    )

    """)


# ==================================
# DIM PRODUCTO
# ==================================

def crear_dim_producto(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Dim_Producto (

        id_producto INTEGER PRIMARY KEY,

        nombre_producto TEXT NOT NULL,

        categoria TEXT,

        precio_base REAL,

        proveedor TEXT

    )

    """)


# ==================================
# DIM TIEMPO
# ==================================

def crear_dim_tiempo(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Dim_Tiempo (

        id_tiempo INTEGER PRIMARY KEY AUTOINCREMENT,

        fecha TEXT UNIQUE,

        anio INTEGER,

        mes INTEGER,

        dia INTEGER

    )

    """)


# ==================================
# DIM CANAL
# ==================================

def crear_dim_canal(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Dim_Canal (

        id_canal INTEGER PRIMARY KEY AUTOINCREMENT,

        canal TEXT UNIQUE

    )

    """)


# ==================================
# DIM TIENDA
# ==================================

def crear_dim_tienda(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Dim_Tienda (

        id_tienda INTEGER PRIMARY KEY AUTOINCREMENT,

        tienda TEXT UNIQUE

    )

    """)


# ==================================
# FACT VENTAS
# ==================================

def crear_fact_ventas(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Fact_Ventas (

        id_fact INTEGER PRIMARY KEY AUTOINCREMENT,

        id_venta INTEGER UNIQUE,

        id_cliente INTEGER,

        id_producto INTEGER,

        id_tiempo INTEGER,

        id_canal INTEGER,

        id_tienda INTEGER,

        cantidad INTEGER,

        precio_unitario REAL,

        total REAL,

        FOREIGN KEY(id_cliente)
            REFERENCES Dim_Cliente(id_cliente),

        FOREIGN KEY(id_producto)
            REFERENCES Dim_Producto(id_producto),

        FOREIGN KEY(id_tiempo)
            REFERENCES Dim_Tiempo(id_tiempo),

        FOREIGN KEY(id_canal)
            REFERENCES Dim_Canal(id_canal),

        FOREIGN KEY(id_tienda)
            REFERENCES Dim_Tienda(id_tienda)

    )

    """)
    
# FACT VENTAS ONLINE

def crear_fact_ventas_online(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Fact_Ventas_Online (

        id_orden INTEGER PRIMARY KEY,

        id_cliente INTEGER,

        id_tiempo INTEGER,

        id_canal INTEGER,

        total REAL,

        FOREIGN KEY(id_cliente)
            REFERENCES Dim_Cliente(id_cliente),

        FOREIGN KEY(id_tiempo)
            REFERENCES Dim_Tiempo(id_tiempo),

        FOREIGN KEY(id_canal)
            REFERENCES Dim_Canal(id_canal)

    )

    """)

def crear_fact_eventos(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Fact_Eventos (

        id_evento INTEGER PRIMARY KEY,

        id_cliente INTEGER,

        id_producto INTEGER,

        tipo TEXT,

        FOREIGN KEY(id_cliente)
            REFERENCES Dim_Cliente(id_cliente),

        FOREIGN KEY(id_producto)
            REFERENCES Dim_Producto(id_producto)

    )

    """)


# ==================================
# MAIN
# ==================================

def main():

    print("=" * 50)
    print("CREANDO DATA WAREHOUSE")
    print("=" * 50)

    crear_directorio()

    conexion = conectar()

    cursor = conexion.cursor()

    crear_dim_cliente(cursor)

    crear_dim_producto(cursor)

    crear_dim_tiempo(cursor)

    crear_dim_canal(cursor)

    crear_dim_tienda(cursor)

    crear_fact_ventas(cursor)

    crear_fact_ventas_online(cursor)

    crear_fact_eventos(cursor)

    conexion.commit()

    conexion.close()

    print(
        "\nData Warehouse creado correctamente."
    )


if __name__ == "__main__":
    main()