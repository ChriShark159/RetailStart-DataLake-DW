# RetailStart - Data Lake y Data Warehouse

Proyecto desarrollado para la asignatura **Arquitectura y Almacenamiento de Datos**.

La solución implementa una arquitectura de datos completa basada en:

**Fuente → Ingesta → Data Lake → Procesamiento ELT → Data Warehouse → Consumo Analítico**

---

# Tecnologías Utilizadas

- Python 3.12+
- SQLite3
- Pandas
- JSON
- CSV

---

# Requisitos Previos

Antes de ejecutar el proyecto se debe tener instalado:

## Python

Descargar desde:

https://www.python.org/downloads/

Verificar instalación:

```bash
python --version
```

o

```bash
py --version
```

---

## Git (Opcional)

Descargar desde:

https://git-scm.com/downloads

Clonar repositorio:

```bash
git clone https://github.com/ChriShark159/RetailStart-DataLake-DW
```

---

# Instalación

Ingresar al directorio del proyecto:

```bash
cd RetailStart
```

### Crear entorno virtual (Opcional)

```bash
python -m venv venv
```

### Activar entorno virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no existe el archivo requirements.txt:

```bash
pip install pandas
```

---

# Estructura del Proyecto

```text
RetailStart/

│
├── data/
│   ├── origen/
│   │   ├── clientes/
│   │   ├── productos/
│   │   ├── ventas/
│   │   ├── ventas_online/
│   │   └── eventos_app/
│   │
│   ├── data_lake/
│   │   ├── raw/
│   │   └── processed/
│   │
│   └── warehouse/
│       └── dw_retailstart.db
│
├── scripts/
│   ├── 01_ingesta.py
│   ├── 02_elt.py
│   ├── 03_crear_dw.py
│   ├── 04_etl_dw.py
│   └── 05_consultas.py
│
├── requirements.txt
│
└── README.md
```

---

# Flujo de Ejecución

## Paso 1 - Ingesta de Datos

Ejecutar:

```bash
python scripts/01_ingesta.py
```

Este script:

- Lee los datos de origen.
- Genera archivos en la capa RAW.
- Organiza la información por fuente.
- Mantiene histórico mediante timestamps.

---

## Paso 2 - Procesamiento ELT

Ejecutar:

```bash
python scripts/02_elt.py
```

Este script:

- Lee los datos desde RAW.
- Limpia registros.
- Elimina duplicados.
- Normaliza datos.
- Genera archivos en la capa Processed.

---

## Paso 3 - Crear Data Warehouse

Ejecutar:

```bash
python scripts/03_crear_dw.py
```

Este script:

- Crea la base de datos SQLite.
- Genera tablas de dimensiones.
- Genera tablas de hechos.
- Configura las relaciones entre tablas.

---

## Paso 4 - Cargar Data Warehouse

Ejecutar:

```bash
python scripts/04_etl_dw.py
```

Este script:

- Lee archivos Processed.
- Inserta datos en SQLite.
- Mantiene cargas incrementales.
- Conserva datos históricos.

---

## Paso 5 - Ejecutar Consultas

Ejecutar:

```bash
python scripts/05_consultas.py
```

Este script:

- Ejecuta consultas SQL.
- Valida la carga de información.
- Muestra métricas básicas del Data Warehouse.

---

# Base de Datos

La base de datos se almacena en:

```text
data/warehouse/dw_retailstart.db
```

Puede abrirse utilizando herramientas como:

- DB Browser for SQLite
- SQLiteStudio
- DBeaver

---

# Modelo de Datos

## Dimensiones

- Dim_Cliente
- Dim_Producto
- Dim_Tiempo
- Dim_Canal
- Dim_Tienda

## Tablas de Hechos

- Fact_Ventas
- Fact_Eventos

> Dependiendo de futuras mejoras del proyecto, las ventas online pueden integrarse dentro de Fact_Ventas o mantenerse en una tabla independiente según los requerimientos analíticos.

---

# Cargas Incrementales

El sistema soporta:

- Procesamiento de Día 1.
- Procesamiento de Día 2.
- Crecimiento de archivos RAW.
- Crecimiento de archivos Processed.
- Preservación de datos históricos.
- Incremento de registros en el Data Warehouse.
- Trazabilidad mediante archivos versionados.

---

# Dependencias

Archivo `requirements.txt`:

```text
pandas
```

Instalación:

```bash
pip install -r requirements.txt
```

---

# Autor

Proyecto académico desarrollado para la asignatura **Arquitectura y Almacenamiento de Datos**.

Implementación basada en los conceptos de:

- Data Lake
- Data Warehouse
- Procesos ELT
- Procesos ETL
- Modelado Estrella (Star Schema)
- Cargas Incrementales
- Análisis de Datos