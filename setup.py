#!/usr/bin/env python3
"""
Script de configuración inicial para el proyecto.
Ejecuta este script después de clonar el repositorio.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Ejecuta un comando y maneja errores."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"   {e.stderr}")
        return False

def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.8+")
        return False

def setup_virtual_environment():
    """Configura el entorno virtual."""
    if not os.path.exists('env'):
        if not run_command('python -m venv env', 'Creando entorno virtual'):
            return False
    else:
        print("✅ Entorno virtual ya existe")
    
    # Activar entorno virtual e instalar dependencias
    if os.name == 'nt':  # Windows
        activate_cmd = 'env\\Scripts\\activate && pip install -r requirements.txt'
    else:  # Linux/Mac
        activate_cmd = 'source env/bin/activate && pip install -r requirements.txt'
    
    return run_command(activate_cmd, 'Instalando dependencias')

def setup_env_file():
    """Configura el archivo de variables de entorno."""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            if os.name == 'nt':  # Windows
                run_command('copy .env.example .env', 'Creando archivo .env')
            else:  # Linux/Mac
                run_command('cp .env.example .env', 'Creando archivo .env')
            print("⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales reales")
        else:
            print("❌ No se encontró .env.example")
            return False
    else:
        print("✅ Archivo .env ya existe")
    return True

def main():
    """Función principal del setup."""
    print("🚀 Configuración inicial del proyecto - Cargador de Datos Geográficos")
    print("=" * 60)
    
    # Verificar versión de Python
    if not check_python_version():
        print("\n❌ Setup fallido: Versión de Python incompatible")
        sys.exit(1)
    
    # Configurar entorno virtual
    if not setup_virtual_environment():
        print("\n❌ Setup fallido: Error configurando entorno virtual")
        sys.exit(1)
    
    # Configurar archivo .env
    if not setup_env_file():
        print("\n❌ Setup fallido: Error configurando archivo .env")
        sys.exit(1)
    
    print("\n🎉 ¡Setup completado exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Edita el archivo .env con tus credenciales de base de datos")
    print("2. Ejecuta el script database_schema.sql en tu base de datos PostgreSQL")
    print("3. Coloca tu archivo CSV en la raíz del proyecto")
    print("4. Ejecuta: python main.py")
    
    if os.name == 'nt':  # Windows
        print("\n💡 Para activar el entorno virtual manualmente:")
        print("   env\\Scripts\\activate")
    else:  # Linux/Mac
        print("\n💡 Para activar el entorno virtual manualmente:")
        print("   source env/bin/activate")

if __name__ == "__main__":
    main()
