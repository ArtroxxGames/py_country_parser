#!/usr/bin/env python3
"""
Script de desarrollo para el Cargador de Datos Geográficos.
Proporciona comandos útiles para desarrollo y testing.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, cwd=None):
    """Ejecuta un comando y maneja el resultado."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print(f"✅ {description} completado")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"   {e.stderr}")
        return False

def setup_dev_env():
    """Configura el entorno de desarrollo."""
    print("🚀 Configurando entorno de desarrollo...")
    
    commands = [
        ("python -m pip install --upgrade pip", "Actualizando pip"),
        ("pip install -r requirements.txt", "Instalando dependencias principales"),
        ("pip install pytest pytest-cov flake8 black bandit safety", "Instalando herramientas de desarrollo"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("✅ Entorno de desarrollo configurado correctamente")
    return True

def run_tests():
    """Ejecuta todas las pruebas."""
    print("🧪 Ejecutando pruebas...")
    
    commands = [
        ("python -m pytest -v", "Ejecutando pruebas unitarias"),
        ("python -m pytest --cov=main --cov-report=html", "Generando reporte de cobertura"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("✅ Todas las pruebas pasaron")
    return True

def lint_code():
    """Ejecuta linters en el código."""
    print("🔍 Analizando código...")
    
    commands = [
        ("flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics", "Verificando errores críticos"),
        ("flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics", "Análisis de estilo"),
        ("black --check .", "Verificando formato de código"),
    ]
    
    for command, description in commands:
        run_command(command, description)  # No fallar en lint warnings
    
    print("✅ Análisis de código completado")
    return True

def format_code():
    """Formatea el código automáticamente."""
    print("✨ Formateando código...")
    
    commands = [
        ("black .", "Formateando con Black"),
        ("isort .", "Organizando imports"),
    ]
    
    for command, description in commands:
        run_command(command, description)
    
    print("✅ Código formateado")
    return True

def security_check():
    """Ejecuta verificaciones de seguridad."""
    print("🔒 Verificando seguridad...")
    
    commands = [
        ("safety check", "Verificando vulnerabilidades en dependencias"),
        ("bandit -r . --skip B101", "Análisis de seguridad del código"),
    ]
    
    for command, description in commands:
        run_command(command, description)
    
    print("✅ Verificación de seguridad completada")
    return True

def validate_project():
    """Valida que el proyecto esté configurado correctamente."""
    print("🔍 Validando proyecto...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "database_schema.sql",
        ".gitignore",
        "LICENSE"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    # Validar sintaxis de Python
    python_files = ["main.py", "setup.py", "config_example.py"]
    for file in python_files:
        if Path(file).exists():
            if not run_command(f"python -m py_compile {file}", f"Validando sintaxis de {file}"):
                return False
    
    print("✅ Proyecto validado correctamente")
    return True

def clean_project():
    """Limpia archivos temporales y cache."""
    print("🧹 Limpiando proyecto...")
    
    import shutil
    
    patterns_to_remove = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".pytest_cache",
        ".coverage",
        "htmlcov",
        "dist",
        "build",
        "*.egg-info"
    ]
    
    removed_count = 0
    for pattern in patterns_to_remove:
        for path in Path(".").rglob(pattern):
            if path.is_file():
                path.unlink()
                removed_count += 1
            elif path.is_dir():
                shutil.rmtree(path)
                removed_count += 1
    
    print(f"✅ Limpieza completada - {removed_count} elementos removidos")
    return True

def create_sample_data():
    """Crea datos de ejemplo para testing."""
    print("📊 Creando datos de ejemplo...")
    
    sample_csv = """Codigo concatenado;Codigo de Departamento;Descripcion de Departamento;Codigo de Distrito;Descripcion de Distrito;Area;Codigo de Barrio/Localidad;Descripcion de Barrio/Localidad
1;0;ASUNCION;0;ASUNCION;1;1;SAJONIA
2;0;ASUNCION;0;ASUNCION;1;2;SAN ANTONIO
3;1;CONCEPCION;1;CONCEPCION;2;1;CENTRO
4;1;CONCEPCION;1;CONCEPCION;2;2;BARRIO OBRERO
"""
    
    with open("datos_ejemplo.csv", "w", encoding="latin-1") as f:
        f.write(sample_csv)
    
    print("✅ Archivo datos_ejemplo.csv creado")
    return True

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Script de desarrollo")
    parser.add_argument(
        "command",
        choices=[
            "setup", "test", "lint", "format", "security", 
            "validate", "clean", "sample-data", "all"
        ],
        help="Comando a ejecutar"
    )
    
    args = parser.parse_args()
    
    commands = {
        "setup": setup_dev_env,
        "test": run_tests,
        "lint": lint_code,
        "format": format_code,
        "security": security_check,
        "validate": validate_project,
        "clean": clean_project,
        "sample-data": create_sample_data,
    }
    
    if args.command == "all":
        print("🚀 Ejecutando pipeline completo de desarrollo...")
        success = True
        for cmd_name, cmd_func in [
            ("setup", setup_dev_env),
            ("validate", validate_project),
            ("format", format_code),
            ("lint", lint_code),
            ("security", security_check),
            ("test", run_tests),
        ]:
            print(f"\n{'='*50}")
            print(f"Ejecutando: {cmd_name}")
            print(f"{'='*50}")
            if not cmd_func():
                success = False
                break
        
        if success:
            print("\n🎉 ¡Pipeline completado exitosamente!")
        else:
            print("\n❌ Pipeline falló")
            sys.exit(1)
    else:
        command_func = commands[args.command]
        if not command_func():
            sys.exit(1)

if __name__ == "__main__":
    main()
