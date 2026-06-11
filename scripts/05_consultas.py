import sqlite3

DB_PATH = "data/warehouse/dw_retailstart.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def ejecutar_consulta(conn, titulo, consulta):

    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)

    cursor = conn.execute(consulta)

    columnas = [desc[0] for desc in cursor.description]

    print(" | ".join(columnas))
    print("-" * 60)

    for fila in cursor.fetchall():
        print(" | ".join(str(valor) for valor in fila))


def main():

    print("=" * 60)
    print("CONSULTAS ANALÍTICAS DATA WAREHOUSE")
    print("=" * 60)

    conn = conectar()

    # Consulta 1
    ejecutar_consulta(
        conn,
        "1. Total de clientes",
        """
        SELECT COUNT(*) AS total_clientes
        FROM Dim_Cliente
        """
    )

    # Consulta 2
    ejecutar_consulta(
        conn,
        "2. Total de productos",
        """
        SELECT COUNT(*) AS total_productos
        FROM Dim_Producto
        """
    )

    # Consulta 3
    ejecutar_consulta(
        conn,
        "3. Total ventas físicas",
        """
        SELECT
            COUNT(*) AS cantidad_ventas,
            SUM(total) AS monto_total
        FROM Fact_Ventas
        """
    )

    # Consulta 4
    ejecutar_consulta(
        conn,
        "4. Total ventas online",
        """
        SELECT
            COUNT(*) AS cantidad_ordenes,
            SUM(total) AS monto_total
        FROM Fact_Ventas_Online
        """
    )

    # Consulta 5
    ejecutar_consulta(
        conn,
        "5. Ventas por ciudad",
        """
        SELECT
            dt.tienda,
            SUM(fv.total) AS total_vendido
        FROM Fact_Ventas fv
        JOIN Dim_Tienda dt
            ON fv.id_tienda = dt.id_tienda
        GROUP BY dt.tienda
        ORDER BY total_vendido DESC
        """
    )

    # Consulta 6
    ejecutar_consulta(
        conn,
        "6. Productos más vendidos",
        """
        SELECT
            dp.nombre_producto,
            SUM(fv.cantidad) AS unidades_vendidas
        FROM Fact_Ventas fv
        JOIN Dim_Producto dp
            ON fv.id_producto = dp.id_producto
        GROUP BY dp.nombre_producto
        ORDER BY unidades_vendidas DESC
        """
    )

    # Consulta 7
    ejecutar_consulta(
        conn,
        "7. Ventas por canal online",
        """
        SELECT
            dc.canal,
            COUNT(*) AS cantidad_ordenes,
            SUM(fvo.total) AS total_vendido
        FROM Fact_Ventas_Online fvo
        JOIN Dim_Canal dc
            ON fvo.id_canal = dc.id_canal
        GROUP BY dc.canal
        """
    )

    # Consulta 8
    ejecutar_consulta(
        conn,
        "8. Eventos por tipo",
        """
        SELECT
            tipo,
            COUNT(*) AS cantidad
        FROM Fact_Eventos
        GROUP BY tipo
        ORDER BY cantidad DESC
        """
    )

    # Consulta 9
    ejecutar_consulta(
        conn,
        "9. Clientes por segmento",
        """
        SELECT
            segmento,
            COUNT(*) AS cantidad_clientes
        FROM Dim_Cliente
        GROUP BY segmento
        """
    )

    # Consulta 10
    ejecutar_consulta(
        conn,
        "10. Ventas por cliente",
        """
        SELECT
            dc.nombre,
            dc.apellido,
            SUM(fv.total) AS total_comprado
        FROM Fact_Ventas fv
        JOIN Dim_Cliente dc
            ON fv.id_cliente = dc.id_cliente
        GROUP BY dc.id_cliente
        ORDER BY total_comprado DESC
        """
    )

    conn.close()

    print("\nConsultas ejecutadas correctamente.")


if __name__ == "__main__":
    main()