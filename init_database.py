# -*- coding: utf-8 -*-
"""
====================================================================
DinoMascota Dashboard — Script de Inicialización de Base de Datos
Materia: Bases de Datos Aplicada — UAI
====================================================================

Uso:
    python init_database.py
    python init_database.py --sync-images  (descarga paleoarte de Wikipedia/JP Wiki)

Este script:
1. Crea/resetea la base de datos SQLite dinomascota.db por separado del backend.
2. Ejecuta el DDL (schema.sql) creando las 5 tablas normalizadas.
3. Ejecuta el DML (seeds.sql) poblando períodos, hábitats, dietas, especies y usuarios iniciales.
4. Verifica la integridad y conteo de registros.
"""

import os
import sys
import argparse
import sqlite3

# Configurar encoding seguro para terminales Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'backend', 'database')
DB_PATH = os.path.join(DB_DIR, 'dinomascota.db')
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')
SEEDS_PATH = os.path.join(DB_DIR, 'seeds.sql')

# Agregar directorio al sys.path para poder importar módulos del backend si es necesario
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def main():
    parser = argparse.ArgumentParser(description="Inicializador independiente de Base de Datos SQLite para DinoMascota")
    parser.add_argument("--sync-images", action="store_true", help="Descargar y sincronizar imágenes online de especies")
    parser.add_argument("--force", action="store_true", default=True, help="Sobrescribir tablas existentes")
    args = parser.parse_args()

    print("=" * 70)
    print(" [DINO] DINOMASCOTA DASHBOARD -- INICIALIZACION DE BASE DE DATOS (UAI)")
    print("=" * 70)
    print(f"[*] Archivo destino: {DB_PATH}")

    if not os.path.exists(SCHEMA_PATH):
        print(f"[ERROR] No se encontró el esquema DDL en: {SCHEMA_PATH}")
        sys.exit(1)

    if not os.path.exists(SEEDS_PATH):
        print(f"[ERROR] No se encontró el archivo DML en: {SEEDS_PATH}")
        sys.exit(1)

    # 1. Conexión y ejecución de scripts SQL
    print("\n[1/3] Creando tablas normalizadas desde schema.sql...")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("  [OK] 5 Entidades creadas: usuarios, periodos, habitats, dietas, dinosaurios.")
    except Exception as e:
        print(f"[ERROR] Falló la creación del esquema: {e}")
        conn.close()
        sys.exit(1)

    # 2. Carga de datos iniciales
    print("\n[2/3] Insertando datos iniciales desde seeds.sql...")
    try:
        with open(SEEDS_PATH, 'r', encoding='utf-8') as f:
            seeds_sql = f.read()
        cursor.executescript(seeds_sql)
        conn.commit()
        print("  [OK] Datos maestros insertados correctamente.")
    except Exception as e:
        print(f"[ERROR] Falló la inserción de seeds: {e}")
        conn.close()
        sys.exit(1)

    # 3. Verificación de conteos e integridad
    print("\n[3/3] Verificando conteo de registros...")
    tablas = ["usuarios", "periodos", "habitats", "dietas", "dinosaurios"]
    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        cnt = cursor.fetchone()[0]
        print(f"  - Tabla '{tabla}': {cnt} registros.")

    # 4. Sincronización opcional de imágenes
    if args.sync_images:
        print("\n[*] Sincronizando paleoarte e imágenes online...")
        try:
            from backend.database.db import sync_wikipedia_images
            sync_wikipedia_images(conn, force_refresh=True)
        except Exception as e:
            print(f"[WARN] No se pudo completar la sincronización online de imágenes: {e}")

    conn.close()

    print("\n" + "=" * 70)
    print(" BASE DE DATOS INICIALIZADA CON EXITO!")
    print("=" * 70)
    print("\nYa puedes iniciar el backend FastAPI en cualquier momento:")
    print("python -m uvicorn backend.app:app --reload --port 8000\n")

if __name__ == '__main__':
    main()
