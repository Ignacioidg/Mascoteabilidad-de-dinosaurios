import sqlite3
import os
import urllib.request
import urllib.parse
import json
import time
from typing import List, Dict, Any, Optional

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'dinomascota.db')
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')
SEEDS_PATH = os.path.join(DB_DIR, 'seeds.sql')

CUSTOM_WIKI_MAP = {
    "Yi qi": "Yi_(dinosaur)",
    "Tyrannosaurus rex": "Tyrannosaurus",
    "Mussaurus": "Mussaurus",
    "Lesothosaurus": "Lesothosaurus",
    "Pisanosaurus": "Pisanosaurus",
    "Liliensternus": "Liliensternus",
    "Gojirasaurus": "Gojirasaurus",
    "Marasuchus": "Marasuchus",
}

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def fetch_wiki_thumbnail(nombre: str) -> Optional[str]:
    queries = []
    if nombre in CUSTOM_WIKI_MAP:
        queries.append(CUSTOM_WIKI_MAP[nombre])
    genus = nombre.split()[0]
    if genus not in queries:
        queries.append(genus)
    if nombre not in queries:
        queries.append(nombre.replace(" ", "_"))

    for q in queries:
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(q)}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "DinoMascotaApp/1.0 (academic-project@uai.edu.ar)"}
            )
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    thumb = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
                    if thumb:
                        return thumb
        except Exception:
            continue
    return None

def fetch_jurassic_park_image(nombre: str) -> Optional[str]:
    clean_title = nombre.split()[0]
    for q in [nombre, clean_title]:
        url = f"https://jurassicpark.fandom.com/api.php?action=query&titles={urllib.parse.quote(q)}&prop=pageimages&format=json&pithumbsize=800"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DinoMascotaApp/1.0 (academic-project@uai.edu.ar)"}
            )
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                pages = data.get("query", {}).get("pages", {})
                for pid, pdata in pages.items():
                    if pid != "-1" and "thumbnail" in pdata:
                        src = pdata["thumbnail"]["source"]
                        if "PictureNotFound" not in src and "No_image" not in src:
                            return src
        except Exception:
            pass

    try:
        url = f"https://jurassicpark.fandom.com/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(nombre)}&gsrlimit=1&prop=pageimages&format=json&pithumbsize=800"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DinoMascotaApp/1.0 (academic-project@uai.edu.ar)"}
        )
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get("query", {}).get("pages", {})
            for pid, pdata in pages.items():
                if pid != "-1" and "thumbnail" in pdata:
                    src = pdata["thumbnail"]["source"]
                    if "PictureNotFound" not in src and "No_image" not in src:
                        return src
    except Exception:
        pass

    return None

def fetch_dino_best_image(nombre: str) -> Optional[str]:
    # 1. Prioridad: Render 3D vivo de Jurassic Park Wiki
    jp_img = fetch_jurassic_park_image(nombre)
    if jp_img:
        return jp_img
    # 2. Respaldo: Paleoarte de Wikipedia / Wikimedia
    return fetch_wiki_thumbnail(nombre)

def sync_wikipedia_images(conn: Optional[sqlite3.Connection] = None, force_refresh: bool = False):
    should_close = False
    if conn is None:
        conn = get_connection()
        should_close = True
        
    cursor = conn.cursor()
    if force_refresh:
        cursor.execute("SELECT id_dinosaurio, nombre FROM dinosaurios")
    else:
        cursor.execute("SELECT id_dinosaurio, nombre FROM dinosaurios WHERE imagen_url IS NULL OR imagen_url = ''")
        
    rows = cursor.fetchall()
    if not rows:
        print("[DB] Todas las imagenes de dinosaurios ya se encuentran sincronizadas.")
        if should_close:
            conn.close()
        return
        
    print(f"[DB] Sincronizando imagenes (Jurassic Park Wiki + Wikipedia) para {len(rows)} especies...")
    updated_count = 0
    for row in rows:
        dino_id = row["id_dinosaurio"]
        nombre = row["nombre"]
        time.sleep(0.04) # Evitar rate limit
        thumb_url = fetch_dino_best_image(nombre)
        if thumb_url:
            cursor.execute("UPDATE dinosaurios SET imagen_url = ? WHERE id_dinosaurio = ?", (thumb_url, dino_id))
            updated_count += 1
            print(f"  [OK] {nombre} -> Imagen obtenida correctamente.")
        else:
            print(f"  [WARN] No se encontro imagen para: {nombre}")
            
    conn.commit()
    print(f"[DB] Sincronizacion finalizada: {updated_count}/{len(rows)} imagenes actualizadas.")
    if should_close:
        conn.close()

def init_db(force_reload: bool = False):
    db_exists = os.path.exists(DB_PATH)
    if force_reload or not db_exists:
        conn = get_connection()
        cursor = conn.cursor()
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        with open(SEEDS_PATH, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        conn.commit()
        print('[DB] Base de datos dinomascota.db inicializada con exito.')
        sync_wikipedia_images(conn, force_refresh=True)
        conn.close()
    else:
        print('[DB] Base de datos existente encontrada.')
        # Verificar si hay imágenes pendientes de sincronizar
        sync_wikipedia_images(force_refresh=False)

def query_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result

def query_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

if __name__ == '__main__':
    init_db(force_reload=True)
