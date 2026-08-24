# -*- coding: utf-8 -*-
import os
import bcrypt
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from backend.database.db import query_all, query_one, init_db

# Inicializar Base de Datos SQLite
init_db()

app = FastAPI(
    title="DinoMascota API - Tablero de Control",
    description="Sistema analítico de evaluación de dinosaurios domésticos para Bases de Datos Aplicada (UAI)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

# -------------------------------------------------------------
# 1. AUTENTICACIÓN (LOGIN CON HASH BCRYPT)
# -------------------------------------------------------------
@app.post("/api/auth/login")
def login(credentials: LoginRequest):
    user = query_one(
        "SELECT id, username, password_hash, nombre_completo, rol FROM usuarios WHERE username = ?",
        (credentials.username.strip(),)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    password_bytes = credentials.password.encode("utf-8")
    hash_bytes = user["password_hash"].encode("utf-8")
    
    try:
        is_valid = bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception:
        is_valid = False
        
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
        
    return {
        "status": "success",
        "message": "Autenticación exitosa",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "nombre_completo": user["nombre_completo"],
            "rol": user["rol"]
        },
        "token": f"token_{user['id']}_{user['username']}"
    }

# -------------------------------------------------------------
# 2. INDICADORES GLOBALES (KPIS)
# -------------------------------------------------------------
@app.get("/api/stats/kpis")
def get_kpis():
    general = query_one("""
        SELECT 
            COUNT(*) AS total_dinos,
            ROUND(AVG(peso_kg), 1) AS peso_promedio,
            ROUND(AVG(altura_m), 2) AS altura_promedio,
            ROUND(AVG(indice_mascotabilidad), 1) AS mascotabilidad_promedio,
            MAX(velocidad_kmh) AS max_velocidad
        FROM dinosaurios
    """)
    
    mejor = query_one("""
        SELECT nombre, especie, indice_mascotabilidad, imagen_emoji, peso_kg
        FROM dinosaurios
        ORDER BY indice_mascotabilidad DESC
        LIMIT 1
    """)
    
    peor = query_one("""
        SELECT nombre, especie, indice_mascotabilidad, agresividad_1_10, imagen_emoji
        FROM dinosaurios
        ORDER BY agresividad_1_10 DESC, indice_mascotabilidad ASC
        LIMIT 1
    """)
    
    semaforo = query_all("""
        SELECT 
            CASE 
                WHEN indice_mascotabilidad >= 70 THEN 'VERDE'
                WHEN indice_mascotabilidad >= 40 THEN 'AMARILLO'
                ELSE 'ROJO'
            END AS estado,
            COUNT(*) AS cantidad
        FROM dinosaurios
        GROUP BY estado
    """)
    
    return {
        "general": general,
        "mejor_candidato": mejor,
        "mayor_riesgo": peor,
        "resumen_semaforo": semaforo
    }

# -------------------------------------------------------------
# 3. DRILL-DOWN / DRILL-UP (3 NIVELES DE PROFUNDIDAD)
# -------------------------------------------------------------

# NIVEL 1: Períodos Geológicos
@app.get("/api/stats/drilldown/periodos")
def get_drilldown_periodos():
    query = """
        SELECT 
            p.id_periodo,
            p.nombre AS periodo_nombre,
            p.era,
            p.millones_anios_inicio,
            p.millones_anios_fin,
            p.clima_predominante,
            p.descripcion,
            COUNT(d.id_dinosaurio) AS total_especies,
            ROUND(AVG(d.indice_mascotabilidad), 1) AS promedio_mascotabilidad,
            ROUND(AVG(d.peso_kg), 1) AS peso_promedio_kg,
            ROUND(AVG(d.agresividad_1_10), 1) AS agresividad_promedio
        FROM periodos p
        LEFT JOIN dinosaurios d ON p.id_periodo = d.id_periodo
        GROUP BY p.id_periodo, p.nombre, p.era, p.millones_anios_inicio, p.millones_anios_fin, p.clima_predominante, p.descripcion
        ORDER BY p.millones_anios_inicio DESC
    """
    return query_all(query)

# NIVEL 2: Hábitats del Período
@app.get("/api/stats/drilldown/habitats/{id_periodo}")
def get_drilldown_habitats(id_periodo: int):
    query = """
        SELECT 
            h.id_habitat,
            h.nombre AS habitat_nombre,
            h.tipo_terreno,
            h.superficie_minima_m2,
            h.clima,
            h.dificultad_adaptacion,
            COUNT(d.id_dinosaurio) AS total_especies,
            ROUND(AVG(d.indice_mascotabilidad), 1) AS promedio_mascotabilidad,
            ROUND(AVG(d.espacio_requerido_m2), 1) AS espacio_promedio_m2
        FROM habitats h
        INNER JOIN dinosaurios d ON h.id_habitat = d.id_habitat
        WHERE d.id_periodo = ?
        GROUP BY h.id_habitat, h.nombre, h.tipo_terreno, h.superficie_minima_m2, h.clima, h.dificultad_adaptacion
        ORDER BY total_especies DESC
    """
    periodo = query_one("SELECT id_periodo, nombre, era FROM periodos WHERE id_periodo = ?", (id_periodo,))
    habitats = query_all(query, (id_periodo,))
    return {"periodo": periodo, "habitats": habitats}

# NIVEL 3: Especies con Semaforización
@app.get("/api/stats/drilldown/dinosaurios/{id_periodo}/{id_habitat}")
def get_drilldown_dinosaurios(id_periodo: int, id_habitat: int):
    query = """
        SELECT 
            d.id_dinosaurio,
            d.nombre,
            d.especie,
            d.altura_m,
            d.longitud_m,
            d.peso_kg,
            d.velocidad_kmh,
            d.agresividad_1_10,
            d.inteligencia_1_10,
            d.esperanza_vida_anios,
            d.espacio_requerido_m2,
            d.indice_mascotabilidad,
            d.imagen_emoji,
            d.observaciones,
            dt.tipo AS dieta_tipo,
            dt.consumo_diario_kg,
            dt.costo_mensual_usd,
            dt.nivel_peligro_alimentacion,
            CASE 
                WHEN d.indice_mascotabilidad >= 70 THEN 'VERDE'
                WHEN d.indice_mascotabilidad >= 40 THEN 'AMARILLO'
                ELSE 'ROJO'
            END AS semaforo_color,
            CASE 
                WHEN d.indice_mascotabilidad >= 70 THEN 'Apto para convivencia doméstica / Gran mascota'
                WHEN d.indice_mascotabilidad >= 40 THEN 'Requiere precauciones, adiestramiento y patio amplio'
                ELSE 'Peligro extremo / Riesgo letal para convivientes'
            END AS semaforo_veredicto
        FROM dinosaurios d
        INNER JOIN dietas dt ON d.id_dieta = dt.id_dieta
        WHERE d.id_periodo = ? AND d.id_habitat = ?
        ORDER BY d.indice_mascotabilidad DESC
    """
    periodo = query_one("SELECT id_periodo, nombre FROM periodos WHERE id_periodo = ?", (id_periodo,))
    habitat = query_one("SELECT id_habitat, nombre, tipo_terreno FROM habitats WHERE id_habitat = ?", (id_habitat,))
    dinos = query_all(query, (id_periodo, id_habitat))
    return {"periodo": periodo, "habitat": habitat, "dinosaurios": dinos}

# -------------------------------------------------------------
# 4. FICHA INDIVIDUAL (JOIN DE LAS 4 ENTIDADES)
# -------------------------------------------------------------
@app.get("/api/stats/dinosaurio/{id_dinosaurio}")
def get_dinosaurio_detail(id_dinosaurio: int):
    query = """
        SELECT 
            d.id_dinosaurio,
            d.nombre,
            d.especie,
            d.altura_m,
            d.longitud_m,
            d.peso_kg,
            d.velocidad_kmh,
            d.agresividad_1_10,
            d.inteligencia_1_10,
            d.esperanza_vida_anios,
            d.espacio_requerido_m2,
            d.indice_mascotabilidad,
            d.imagen_emoji,
            d.observaciones,
            p.nombre AS periodo_nombre,
            p.era AS periodo_era,
            h.nombre AS habitat_nombre,
            h.tipo_terreno AS habitat_tipo_terreno,
            h.clima AS habitat_clima,
            dt.tipo AS dieta_tipo,
            dt.consumo_diario_kg,
            dt.costo_mensual_usd,
            dt.nivel_peligro_alimentacion,
            CASE 
                WHEN d.indice_mascotabilidad >= 70 THEN 'VERDE'
                WHEN d.indice_mascotabilidad >= 40 THEN 'AMARILLO'
                ELSE 'ROJO'
            END AS semaforo_color,
            CASE 
                WHEN d.indice_mascotabilidad >= 70 THEN 'Excelente mascota: adaptable, dócil y de fácil convivencia.'
                WHEN d.indice_mascotabilidad >= 40 THEN 'Mascota moderada: requiere espacio y supervisión constante.'
                ELSE 'Peligro inminente: riesgo letal para los propietarios y vecinos.'
            END AS semaforo_justificacion
        FROM dinosaurios d
        INNER JOIN periodos p ON d.id_periodo = p.id_periodo
        INNER JOIN habitats h ON d.id_habitat = h.id_habitat
        INNER JOIN dietas dt ON d.id_dieta = dt.id_dieta
        WHERE d.id_dinosaurio = ?
    """
    dino = query_one(query, (id_dinosaurio,))
    if not dino:
        raise HTTPException(status_code=404, detail="Dinosaurio no encontrado")
    return dino

# -------------------------------------------------------------
# 5. GRÁFICOS ANALÍTICOS (CHART.JS)
# -------------------------------------------------------------
@app.get("/api/stats/charts/dietas")
def get_chart_dietas():
    return query_all("""
        SELECT 
            dt.tipo,
            COUNT(d.id_dinosaurio) AS cantidad,
            ROUND(AVG(dt.costo_mensual_usd), 2) AS costo_promedio,
            ROUND(AVG(d.indice_mascotabilidad), 1) AS mascotabilidad_promedio
        FROM dietas dt
        LEFT JOIN dinosaurios d ON dt.id_dieta = d.id_dieta
        GROUP BY dt.id_dieta, dt.tipo
        ORDER BY cantidad DESC
    """)

@app.get("/api/stats/charts/periodos")
def get_chart_periodos():
    return query_all("""
        SELECT 
            p.nombre AS periodo,
            COUNT(d.id_dinosaurio) AS cantidad,
            ROUND(AVG(d.peso_kg), 1) AS peso_promedio,
            ROUND(AVG(d.indice_mascotabilidad), 1) AS mascotabilidad_promedio
        FROM periodos p
        LEFT JOIN dinosaurios d ON p.id_periodo = d.id_periodo
        GROUP BY p.id_periodo, p.nombre
        ORDER BY p.id_periodo ASC
    """)

@app.get("/api/stats/charts/top-mascotas")
def get_chart_top_mascotas():
    mejores = query_all("""
        SELECT nombre, especie, indice_mascotabilidad, peso_kg, imagen_emoji
        FROM dinosaurios
        ORDER BY indice_mascotabilidad DESC
        LIMIT 5
    """)
    peores = query_all("""
        SELECT nombre, especie, indice_mascotabilidad, peso_kg, imagen_emoji
        FROM dinosaurios
        ORDER BY indice_mascotabilidad ASC
        LIMIT 5
    """)
    return {"mejores": mejores, "peores": peores}

# -------------------------------------------------------------
# 6. SERVIDO DE FRONTEND SPA
# -------------------------------------------------------------
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
INDEX_FILE = os.path.join(STATIC_DIR, "index.html")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return {"message": "DinoMascota Backend API activo. Visite /docs para Swagger UI."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
