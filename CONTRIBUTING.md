# Guía de Contribución 🤝

¡Gracias por tu interés en contribuir al Cargador de Datos Geográficos de Paraguay! Esta guía te ayudará a entender cómo puedes ayudar a mejorar el proyecto.

## 📋 Código de Conducta

Al participar en este proyecto, te comprometes a mantener un ambiente acogedor y libre de acoso. Lee nuestro [Código de Conducta](CODE_OF_CONDUCT.md) completo.

## 🚀 Formas de Contribuir

### 🐛 Reportando Bugs
- Usa el template de bug report en GitHub Issues
- Incluye información detallada del sistema
- Proporciona pasos claros para reproducir el problema
- Incluye logs de error relevantes

### 💡 Sugiriendo Features
- Usa el template de feature request en GitHub Issues
- Explica claramente el caso de uso
- Describe los beneficios esperados
- Considera la compatibilidad hacia atrás

### 📚 Mejorando Documentación
- Corrige errores tipográficos
- Mejora explicaciones existentes
- Agrega ejemplos útiles
- Traduce documentación a otros idiomas

### 💻 Contribuyendo Código
- Arregla bugs reportados
- Implementa nuevas funcionalidades
- Mejora el rendimiento
- Agrega pruebas

## 🛠️ Configuración del Entorno de Desarrollo

### Prerrequisitos
- Python 3.8+
- PostgreSQL 12+
- Git

### Setup Local
```bash
# 1. Fork y clonar el repositorio
git clone https://github.com/ArtroxxGames/py_country_parser.git
cd cargador-datos-geograficos-py

# 2. Crear y activar entorno virtual
python -m venv env
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate

# 3. Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Si existe

# 4. Configurar base de datos de prueba
createdb test_database
psql -d test_database -f database_schema.sql

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con configuración de prueba
```

## 📝 Estándares de Código

### Estilo de Python
- Seguir PEP 8
- Usar type hints cuando sea posible
- Máximo 88 caracteres por línea (compatible con Black)
- Usar docstrings para funciones y clases

### Ejemplo de función bien documentada:
```python
def procesar_fila_csv(row: List[str], row_num: int) -> Optional[Dict[str, Any]]:
    """
    Procesa una fila del CSV y extrae los datos geográficos.
    
    Args:
        row: Lista con los valores de la fila CSV
        row_num: Número de fila para logging de errores
        
    Returns:
        Diccionario con los datos procesados o None si hay error
        
    Raises:
        ValueError: Si los datos no tienen el formato esperado
    """
    # Implementación...
    pass
```

### Convenciones de Naming
- Funciones y variables: `snake_case`
- Clases: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Archivos: `snake_case.py`

### Commits
- Usar conventional commits: `type(scope): description`
- Tipos válidos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Ejemplos:
  ```
  feat(csv): agregar soporte para encoding UTF-8
  fix(db): corregir error en inserción de departamentos
  docs(readme): actualizar instrucciones de instalación
  ```

## 🧪 Testing

### Ejecutar Pruebas
```bash
# Todas las pruebas
python -m pytest

# Con cobertura
python -m pytest --cov=main

# Pruebas específicas
python -m pytest tests/test_csv_processing.py
```

### Escribir Pruebas
- Cada nueva función debe tener pruebas
- Usar pytest como framework
- Mockear conexiones de base de datos en unit tests
- Incluir pruebas de edge cases

### Ejemplo de test:
```python
def test_procesar_fila_csv_valida():
    """Test que procesa correctamente una fila válida del CSV."""
    row = ['1', '0', 'ASUNCION', '0', 'ASUNCION', '1', '1', 'SAJONIA']
    result = procesar_fila_csv(row, 1)
    
    assert result is not None
    assert result['codigo_departamento'] == 0
    assert result['desc_departamento'] == 'ASUNCION'
```

## 🔄 Proceso de Pull Request

### 1. Preparación
- Crea una rama desde `main`: `git checkout -b feature/nueva-funcionalidad`
- Haz commits pequeños y frecuentes
- Escribe tests para tu código
- Actualiza documentación si es necesario

### 2. Antes de Enviar
```bash
# Verificar estilo de código
flake8 .
black --check .

# Ejecutar tests
python -m pytest

# Verificar que no hay errores de importación
python -c "import main; print('✅ Imports OK')"
```

### 3. Enviar PR
- Usa el template de pull request
- Describe claramente los cambios
- Referencia issues relacionados
- Incluye capturas de pantalla si es relevante

### 4. Revisión
- Responde a feedback constructivamente
- Haz cambios solicitados en la misma rama
- Mantén la discusión enfocada en el código

## 🏷️ Versionado

Seguimos [Semantic Versioning](https://semver.org/):
- `MAJOR`: Cambios incompatibles de API
- `MINOR`: Nueva funcionalidad compatible hacia atrás
- `PATCH`: Bug fixes compatibles hacia atrás

## 📚 Documentación

### Actualizar Documentación
Cuando hagas cambios, actualiza:
- `README.md`: Para cambios en funcionalidad principal
- `CHANGELOG.md`: Para todos los cambios visibles al usuario
- `docs/`: Para documentación técnica detallada
- Docstrings: Para cambios en código

### Escribir Documentación
- Usa Markdown para formateo
- Incluye ejemplos de código cuando sea útil
- Mantén explicaciones claras y concisas
- Usa emojis para hacer la documentación más amigable

## 🆘 Necesitas Ayuda?

### Dónde Preguntar
- **GitHub Discussions**: Para preguntas generales y discusiones
- **GitHub Issues**: Para bugs y feature requests
- **Email**: [tu-email@ejemplo.com] para asuntos privados

### Recursos Útiles
- [Documentación de psycopg2](https://www.psycopg.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python CSV Module](https://docs.python.org/3/library/csv.html)

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] Soporte para múltiples formatos de CSV
- [ ] Interfaz web para visualizar datos
- [ ] API REST para consultar datos
- [ ] Soporte para otros países de Latinoamérica
- [ ] Dashboard de monitoreo de carga

### Cómo Contribuir al Roadmap
1. Revisa issues etiquetados como `roadmap`
2. Comenta en el issue si quieres trabajar en algo
3. Propón nuevas ideas a través de feature requests

## 🙏 Reconocimientos

Los contribuidores serán reconocidos en:
- `README.md`
- Releases notes
- `CONTRIBUTORS.md` (si aplicable)

### Tipos de Contribución Reconocidas
- 💻 Código
- 📖 Documentación
- 🐛 Bug reports
- 💡 Ideas
- 🤔 Feedback
- 🎨 Diseño
- 📋 Gestión de proyecto

¡Gracias por hacer este proyecto mejor! 🚀
