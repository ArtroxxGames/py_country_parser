# Guía de Instalación

Esta guía te ayudará a configurar el proyecto paso a paso.

## Requisitos del Sistema

### Software Requerido

1. **Python 3.8 o superior**
   - Descargar desde: https://python.org/downloads/
   - Verificar instalación: `python --version`

2. **PostgreSQL 12 o superior**
   - Descargar desde: https://postgresql.org/download/
   - Servicios requeridos: PostgreSQL Database Server

3. **Git** (opcional, para clonar el repositorio)
   - Descargar desde: https://git-scm.com/downloads/

### Hardware Recomendado

- **RAM**: Mínimo 4GB, recomendado 8GB
- **Almacenamiento**: Al menos 1GB de espacio libre
- **Procesador**: Cualquier procesador moderno

## Instalación Paso a Paso

### 1. Obtener el Código

#### Opción A: Clonar desde GitHub
```bash
git clone https://github.com/ArtroxxGames/py_country_parser.git
cd cargador-datos-geograficos-py
```

#### Opción B: Descargar ZIP
1. Ir a la página del repositorio en GitHub
2. Hacer clic en "Code" → "Download ZIP"
3. Extraer el archivo ZIP
4. Navegar al directorio extraído

### 2. Configurar Python

#### Windows
```cmd
# Verificar Python
python --version

# Crear entorno virtual
python -m venv env

# Activar entorno virtual
env\Scripts\activate

# Actualizar pip
python -m pip install --upgrade pip
```

#### Linux/macOS
```bash
# Verificar Python
python3 --version

# Crear entorno virtual
python3 -m venv env

# Activar entorno virtual
source env/bin/activate

# Actualizar pip
python -m pip install --upgrade pip
```

### 3. Instalar Dependencias

```bash
# Instalar desde requirements.txt
pip install -r requirements.txt

# Verificar instalación
pip list
```

### 4. Configurar Base de Datos

#### Crear Base de Datos
```sql
-- Conectar a PostgreSQL como superusuario
CREATE DATABASE mi_database;
CREATE USER mi_usuario WITH ENCRYPTED PASSWORD 'mi_password';
GRANT ALL PRIVILEGES ON DATABASE mi_database TO mi_usuario;
```

#### Crear Tablas
```bash
# Ejecutar script de esquema
psql -h localhost -U mi_usuario -d mi_database -f database_schema.sql
```

### 5. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# Usar tu editor favorito: nano, vim, code, etc.
nano .env
```

Actualizar el archivo `.env`:
```env
DB_HOST=localhost
DB_NAME=mi_database
DB_USER=mi_usuario
DB_PASSWORD=mi_password_real
DB_PORT=5432
```

### 6. Preparar Datos

1. Colocar el archivo CSV en la raíz del proyecto
2. Asegurarse de que el archivo se llame `datos.csv`
3. Verificar que el formato sea correcto (delimitador `;`)

### 7. Probar la Instalación

```bash
# Activar entorno virtual si no está activo
# Windows: env\Scripts\activate
# Linux/Mac: source env/bin/activate

# Ejecutar el script
python main.py
```

## Verificación de la Instalación

### Comprobar Python y Dependencias
```bash
python --version
pip list | grep psycopg2
```

### Comprobar Conexión a Base de Datos
```python
import psycopg2
try:
    conn = psycopg2.connect(
        host="localhost",
        database="mi_database",
        user="mi_usuario",
        password="mi_password"
    )
    print("✅ Conexión exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")
```

### Comprobar Estructura de Tablas
```sql
-- Verificar que las tablas existen
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'identidades';
```

## Solución de Problemas Comunes

### Error: "python no es reconocido"
- **Windows**: Asegúrate de que Python esté en el PATH
- **Linux/Mac**: Usa `python3` en lugar de `python`

### Error de conexión a PostgreSQL
1. Verificar que PostgreSQL esté ejecutándose
2. Comprobar credenciales en `.env`
3. Verificar permisos del usuario de base de datos

### Error: "No module named 'psycopg2'"
```bash
# Activar entorno virtual primero
# Luego instalar dependencias
pip install -r requirements.txt
```

### Error: "Permission denied" en PostgreSQL
```sql
-- Otorgar permisos al usuario
GRANT CREATE ON SCHEMA identidades TO mi_usuario;
GRANT USAGE ON SCHEMA identidades TO mi_usuario;
```

### Error: "File not found: datos.csv"
- Verificar que el archivo existe en la raíz del proyecto
- Comprobar el nombre exacto del archivo
- Verificar permisos de lectura

## Configuración Avanzada

### Variables de Entorno Adicionales
```env
# Configuración de logging
LOG_LEVEL=DEBUG
LOG_FILE=./logs/app.log

# Configuración de procesamiento
BATCH_SIZE=50
CSV_ENCODING=utf-8
```

### Configuración de Producción
- Usar un usuario de base de datos con permisos limitados
- Configurar logging en archivos
- Establecer timeouts apropiados
- Configurar backups automáticos

## Próximos Pasos

Después de completar la instalación:

1. **Ejecutar una prueba**: `python main.py`
2. **Revisar logs**: Verificar que no haya errores
3. **Validar datos**: Consultar las tablas en PostgreSQL
4. **Configurar backups**: Establecer rutinas de respaldo
5. **Monitoreo**: Configurar alertas si es necesario
