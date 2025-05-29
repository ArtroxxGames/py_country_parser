# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Sin liberar]

### Agregado
- Estructura inicial del proyecto
- Documentación completa en README.md
- Scripts de configuración de base de datos
- Sistema de logging detallado
- Manejo robusto de errores

## [1.0.0] - 2024-05-29

### Agregado
- Script principal para carga de datos geográficos desde CSV
- Soporte para datos de Paraguay (departamentos, ciudades, barrios)
- Integración con PostgreSQL usando psycopg2
- Manejo de duplicados con ON CONFLICT
- Sistema de cache para optimizar rendimiento
- Validación de datos de entrada
- Estadísticas de procesamiento
- Commits por lotes para mejor rendimiento
- Configuración de entorno virtual
- Archivos de configuración de ejemplo

### Características
- Carga jerárquica de datos (Departamentos → Ciudades → Barrios)
- Logging con diferentes niveles (INFO, WARNING, ERROR)
- Manejo de errores con rollback automático
- Soporte para archivos CSV con encoding latin-1
- Delimitador de punto y coma (;)
- Transacciones seguras con commits periódicos

### Técnico
- Python 3.12+
- PostgreSQL 12+
- psycopg2 2.9.10
- Estructura de proyecto lista para GitHub
