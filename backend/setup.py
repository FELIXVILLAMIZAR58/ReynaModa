#!/usr/bin/env python
"""
🚀 Script de inicialización de REYNA MODA v2.0

Este script verifica la configuración y prepara el sistema.
"""

import os
import sys
from pathlib import Path

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_header():
    print(f"""
    {BLUE}╔════════════════════════════════════════╗{END}
    {BLUE}║  🏪 REYNA MODA API v2.0 - SETUP       ║{END}
    {BLUE}╚════════════════════════════════════════╝{END}
    """)

def check_python():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"{GREEN}✅{END} Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"{RED}❌{END} Python 3.9+ requerido")
        return False

def check_venv():
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"{GREEN}✅{END} Virtual environment activado")
        return True
    else:
        print(f"{YELLOW}⚠️{END}  Sin virtual environment")
        return True

def check_dependencies():
    deps = ['fastapi', 'uvicorn', 'pydantic', 'motor', 'pymongo']
    missing = []
    
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            missing.append(dep)
    
    if not missing:
        print(f"{GREEN}✅{END} Todas las dependencias instaladas")
        return True
    else:
        print(f"{RED}❌{END} Faltan: {', '.join(missing)}")
        print(f"   Ejecutar: pip install -r requirements.txt")
        return False

def check_env():
    env_file = Path('.env')
    if env_file.exists():
        print(f"{GREEN}✅{END} Archivo .env encontrado")
        return True
    else:
        print(f"{YELLOW}⚠️{END}  .env no encontrado")
        print(f"   Copiar: cp .env.example .env")
        return True

def check_structure():
    required_dirs = [
        'app',
        'app/routes',
        'app/services',
        'app/models',
        'app/utils'
    ]
    
    all_exist = True
    for dir in required_dirs:
        if Path(dir).exists():
            print(f"{GREEN}✅{END} {dir}/")
        else:
            print(f"{RED}❌{END} Falta: {dir}/")
            all_exist = False
    
    return all_exist

def main():
    print_header()
    
    print(f"{BLUE}📋 Verificaciones:{END}")
    print()
    
    checks = [
        ("Python", check_python),
        ("Virtual Environment", check_venv),
        ("Dependencias", check_dependencies),
        ("Archivo .env", check_env),
        ("Estructura", check_structure)
    ]
    
    results = []
    for name, func in checks:
        print(f"{name}:")
        result = func()
        results.append(result)
        print()
    
    print(f"{BLUE}📊 Resumen:{END}")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{GREEN}✅ Todo verificado correctamente!{END}")
        print()
        print(f"{YELLOW}Para iniciar el servidor:{END}")
        print(f"  python -m uvicorn app.main:app --reload")
        print()
        print(f"{YELLOW}API disponible en:{END}")
        print(f"  http://localhost:8000")
        print(f"  Docs: http://localhost:8000/api/docs")
        return 0
    else:
        print(f"{RED}❌ {total - passed} verificación(es) fallida(s){END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
