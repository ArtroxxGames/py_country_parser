"""
Archivo de configuración de ejemplo para el cargador de datos geográficos.
Copia este archivo como config.py y actualiza con tus credenciales reales.
"""

# Configuración de base de datos
DATABASE_CONFIG = {
    'host': 'localhost',          # Cambia por tu host
    'database': 'mi_database',    # Cambia por tu database
    'user': 'mi_usuario',         # Cambia por tu usuario
    'password': 'mi_password',    # Cambia por tu password
    'port': 5432,                 # Puerto de PostgreSQL (por defecto 5432)
    'connect_timeout': 30         # Timeout de conexión en segundos
}

# Configuración de archivos
CSV_FILE_PATH = './datos.csv'    # Ruta al archivo CSV
CSV_ENCODING = 'latin-1'         # Codificación del archivo CSV
CSV_DELIMITER = ';'              # Delimitador del CSV

# Configuración de procesamiento
BATCH_SIZE = 100                 # Cantidad de registros por lote
LOG_LEVEL = 'INFO'               # Nivel de logging (DEBUG, INFO, WARNING, ERROR)

# Configuración de tablas
SCHEMA_NAME = 'identidades'      # Esquema de la base de datos
TABLES = {
    'departamentos': 'departamentos',
    'ciudades': 'ciudades',
    'barrios': 'barrios'
}
