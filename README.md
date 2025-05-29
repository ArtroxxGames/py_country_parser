# Cargador de Datos Geográficos de Paraguay 🇵🇾

Un script en Python para cargar datos geográficos de Paraguay (departamentos, ciudades y barrios) desde un archivo CSV a una base de datos PostgreSQL.

## 📋 Descripción

Este proyecto automatiza la carga de datos geográficos de Paraguay en una base de datos PostgreSQL. El script procesa un archivo CSV que contiene información sobre departamentos, ciudades (distritos) y barrios, organizándolos en una estructura jerárquica en la base de datos.

## 🎯 Características

- ✅ Carga masiva de datos geográficos desde CSV
- ✅ Estructura de datos jerárquica (Departamentos → Ciudades → Barrios)
- ✅ Manejo de duplicados con `ON CONFLICT`
- ✅ Logging detallado del proceso
- ✅ Estadísticas de carga
- ✅ Manejo robusto de errores
- ✅ Transacciones por lotes para mejor rendimiento
- ✅ Validación de datos de entrada

## 📊 Estructura de Datos

El CSV contiene las siguientes columnas:
- **Código concatenado**: Identificador único
- **Código de Departamento**: Código numérico del departamento
- **Descripción de Departamento**: Nombre del departamento
- **Código de Distrito**: Código numérico del distrito/ciudad
- **Descripción de Distrito**: Nombre del distrito/ciudad
- **Área**: Código de área
- **Código de Barrio/Localidad**: Código numérico del barrio
- **Descripción de Barrio/Localidad**: Nombre del barrio

## 🛠️ Tecnologías Utilizadas

- **Python 3.12+**
- **PostgreSQL**
- **psycopg2** - Adaptador de PostgreSQL para Python
- **CSV** - Procesamiento de archivos CSV
- **Logging** - Sistema de logs

## 📋 Requisitos Previos

- Python 3.12 o superior
- PostgreSQL 12 o superior
- Acceso a una base de datos PostgreSQL

## 🚀 Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/ArtroxxGames/py_country_parser.git
   cd py_country_parser
   ```

2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv env
   
   # En Windows:
   env\Scripts\activate
   
   # En Linux/Mac:
   source env/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**
   - Crea las tablas necesarias en PostgreSQL (ver sección de Estructura de Base de Datos)
   - Actualiza las credenciales de conexión en `main.py`

## 🗄️ Estructura de Base de Datos

El script espera las siguientes tablas en el esquema `identidades`:

```sql
-- Tabla de departamentos
CREATE TABLE identidades.departamentos (
    id SERIAL PRIMARY KEY,
    codigo INTEGER UNIQUE NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL
);

-- Tabla de ciudades
CREATE TABLE identidades.ciudades (
    id SERIAL PRIMARY KEY,
    codigo INTEGER NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    area INTEGER,
    departamento_id INTEGER REFERENCES identidades.departamentos(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL,
    UNIQUE(codigo, departamento_id)
);

-- Tabla de barrios
CREATE TABLE identidades.barrios (
    id SERIAL PRIMARY KEY,
    codigo INTEGER NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    ciudad_id INTEGER REFERENCES identidades.ciudades(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL,
    UNIQUE(codigo, ciudad_id)
);
```

## ⚙️ Configuración

Antes de ejecutar el script, actualiza las credenciales de conexión en `main.py`:

```python
conexion = psycopg2.connect(
    host="tu-host",
    database="tu-database",
    user="tu-usuario",
    password="tu-password",
    connect_timeout=30
)
```

**⚠️ Importante:** Nunca subas credenciales reales a GitHub. Considera usar variables de entorno o archivos de configuración que estén en `.gitignore`.

## 🏃‍♂️ Uso

1. **Asegúrate de tener el archivo CSV:**
   - El archivo debe llamarse `datos.csv` y estar en el directorio raíz
   - Debe seguir el formato especificado con delimitador `;`

2. **Ejecuta el script:**
   ```bash
   python main.py
   ```

3. **Monitorea la salida:**
   El script mostrará:
   - Progreso de la carga cada 100 registros
   - Errores encontrados
   - Estadísticas finales

## 📈 Ejemplo de Salida

```
2024-05-29 10:30:15,123 - INFO - Iniciando carga de datos geográficos...
2024-05-29 10:30:15,124 - INFO - Procesando archivo CSV con header: ['Codigo concatenado', 'Codigo de Departamento', ...]
2024-05-29 10:30:16,234 - INFO - Procesadas 100 filas...
2024-05-29 10:30:17,345 - INFO - Procesadas 200 filas...
...
2024-05-29 10:30:45,678 - INFO - === ESTADÍSTICAS DE CARGA ===
2024-05-29 10:30:45,679 - INFO - Filas procesadas exitosamente: 8337
2024-05-29 10:30:45,680 - INFO - Errores encontrados: 0
2024-05-29 10:30:45,681 - INFO - Datos cargados exitosamente!
2024-05-29 10:30:45,682 - INFO - === ESTADÍSTICAS FINALES ===
2024-05-29 10:30:45,683 - INFO - Departamentos: 18
2024-05-29 10:30:45,684 - INFO - Ciudades: 254
2024-05-29 10:30:45,685 - INFO - Barrios: 8337
```

## 🔍 Características del Script

### Manejo de Duplicados
- Usa `ON CONFLICT` para manejar duplicados elegantemente
- Actualiza registros existentes con nueva información

### Optimización de Rendimiento
- Commits cada 100 registros para evitar transacciones muy largas
- Cache en memoria para evitar consultas repetidas
- Validación temprana de datos

### Manejo de Errores
- Validación de formato de datos
- Manejo de errores de conexión a la base de datos
- Logging detallado de errores para debugging

### Logging
- Logs con timestamps
- Diferentes niveles de log (INFO, WARNING, ERROR)
- Estadísticas de procesamiento

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

Matias Lopez - [@ArtroxxGames](https://twitter.com/ArtroxxGames)

Link del Proyecto: [https://github.com/ArtroxxGames/py_country_parser](https://github.com/ArtroxxGames/py_country_parser)


