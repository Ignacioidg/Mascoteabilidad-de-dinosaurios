# -*- coding: utf-8 -*-
import os
import json
import re
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, status, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr

from backend.database.db import (
    query_all, query_one, execute_query, is_db_initialized,
    fetch_wiki_thumbnail, fetch_jurassic_park_image, fetch_dino_best_image,
    sync_wikipedia_images, get_connection
)
from backend.services.security import hash_password_sha256, verify_password
from backend.services.mailer import send_verification_email, send_password_reset_email

# Verificar si la base de datos fue inicializada de forma independiente
if not is_db_initialized():
    print("[WARN] ALERTA: dinomascota.db no encontrada o no inicializada.")
    print("[WARN] Por favor ejecuta 'python init_database.py' antes de utilizar la aplicacion.")

app = FastAPI(
    title="DinoMascota API - Tablero de Control",
    description="Sistema analítico de evaluación de dinosaurios domésticos para Bases de Datos Aplicada (UAI)",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# MODELOS PYDANTIC
# -------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    nombre_completo: str
    email: str
    password: str
    confirm_password: str

class VerifyEmailRequest(BaseModel):
    email: str
    code: str

class ResendCodeRequest(BaseModel):
    email: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str
    confirm_password: str

class AdminCreateUserRequest(BaseModel):
    username: str
    nombre_completo: str
    email: str
    password: str
    rol: str = "alumno"
    verificado: bool = True

class AdminUpdateRoleRequest(BaseModel):
    rol: str

# Cache en memoria de resoluciones de imágenes
IMAGE_CACHE: Dict[str, Any] = {}

def check_db_ready():
    if not is_db_initialized():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La base de datos no está inicializada. Ejecute 'python init_database.py' en la terminal."
        )

# -------------------------------------------------------------
# 1. AUTENTICACIÓN Y GESTIÓN DE USUARIOS
# -------------------------------------------------------------
@app.post("/api/auth/login")
def login(creds: LoginRequest):
    check_db_ready()
    # Buscar por username o email
    user = query_one(
        "SELECT * FROM usuarios WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)", 
        (creds.username.strip(), creds.username.strip())
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Verificación de contraseña (soporta SHA-256 con salt y legacy Bcrypt)
    is_valid = verify_password(creds.password, user["password_hash"], user.get("salt"))
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
        
    # Verificar si la cuenta fue activada por email
    if user.get("verificado", 1) == 0:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "status": "unverified",
                "message": "Tu cuenta aún no ha sido verificada por correo electrónico.",
                "email": user["email"],
                "username": user["username"]
            }
        )
        
    return {
        "status": "success",
        "message": "Autenticación exitosa",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "nombre_completo": user["nombre_completo"],
            "rol": user["rol"]
        },
        "token": f"token_{user['id']}_{user['username']}"
    }

@app.post("/api/auth/register")
def register(data: RegisterRequest):
    check_db_ready()
    username = data.username.strip()
    email = data.email.strip().lower()
    nombre = data.nombre_completo.strip()
    password = data.password
    
    # Validaciones básicas
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="El nombre de usuario debe tener al menos 3 caracteres.")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise HTTPException(status_code=400, detail="El formato del correo electrónico es inválido.")
    if len(password) < 4:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 4 caracteres.")
    if password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden.")
        
    # Validar duplicados
    existing = query_one("SELECT id FROM usuarios WHERE LOWER(username) = LOWER(?)", (username,))
    if existing:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya se encuentra registrado.")
    existing_mail = query_one("SELECT id FROM usuarios WHERE LOWER(email) = LOWER(?)", (email,))
    if existing_mail:
        raise HTTPException(status_code=400, detail="El correo electrónico ya se encuentra registrado.")

    # Hasheo seguro en SHA-256 con salt criptográfico
    pwd_hash, salt = hash_password_sha256(password)
    
    # Generar código de 6 dígitos con expiración de 15 minutos
    code = str(secrets.randbelow(900000) + 100000)
    exp = (datetime.now() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Insertar en base de datos SQLite (persistencia garantizada)
    execute_query("""
        INSERT INTO usuarios (username, email, password_hash, salt, nombre_completo, rol, verificado, codigo_verificacion, codigo_expiracion)
        VALUES (?, ?, ?, ?, ?, 'alumno', 0, ?, ?)
    """, (username, email, pwd_hash, salt, nombre, code, exp))
    
    # Enviar correo o simular en consola
    mail_res = send_verification_email(email, username, code)
    
    return {
        "status": "success",
        "message": "Usuario registrado exitosamente. Te hemos enviado un código de verificación de 6 dígitos a tu casilla.",
        "email": email,
        "username": username,
        "dev_code": mail_res.get("code")
    }

@app.post("/api/auth/verify-email")
def verify_email(data: VerifyEmailRequest):
    check_db_ready()
    email = data.email.strip().lower()
    code = data.code.strip()
    
    user = query_one("SELECT * FROM usuarios WHERE LOWER(email) = LOWER(?) OR LOWER(username) = LOWER(?)", (email, email))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    if user.get("verificado") == 1:
        return {"status": "info", "message": "La cuenta ya se encuentra activa y verificada."}
        
    if not user.get("codigo_verificacion") or user["codigo_verificacion"] != code:
        raise HTTPException(status_code=400, detail="El código de verificación ingresado es incorrecto.")
        
    if user.get("codigo_expiracion"):
        try:
            exp_date = datetime.strptime(user["codigo_expiracion"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() > exp_date:
                raise HTTPException(status_code=400, detail="El código de verificación ha expirado. Solicita uno nuevo.")
        except ValueError:
            pass
            
    # Marcar cuenta como verificada y limpiar códigos temporales
    execute_query("""
        UPDATE usuarios 
        SET verificado = 1, codigo_verificacion = NULL, codigo_expiracion = NULL 
        WHERE id = ?
    """, (user["id"],))
    
    return {
        "status": "success",
        "message": "¡Cuenta verificada exitosamente! Ya puedes iniciar sesión con tu usuario y contraseña."
    }

@app.post("/api/auth/resend-code")
def resend_code(data: ResendCodeRequest):
    check_db_ready()
    email = data.email.strip().lower()
    user = query_one("SELECT * FROM usuarios WHERE LOWER(email) = LOWER(?) OR LOWER(username) = LOWER(?)", (email, email))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    if user.get("verificado") == 1:
        return {"status": "info", "message": "Esta cuenta ya está verificada."}
        
    new_code = str(secrets.randbelow(900000) + 100000)
    new_exp = (datetime.now() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
    
    execute_query("""
        UPDATE usuarios 
        SET codigo_verificacion = ?, codigo_expiracion = ? 
        WHERE id = ?
    """, (new_code, new_exp, user["id"]))
    
    mail_res = send_verification_email(user["email"], user["username"], new_code)
    
    return {
        "status": "success",
        "message": "Se ha reenviado un nuevo código de 6 dígitos a tu casilla de correo.",
        "email": user["email"],
        "dev_code": mail_res.get("code")
    }

@app.post("/api/auth/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    check_db_ready()
    email = data.email.strip().lower()
    user = query_one("SELECT * FROM usuarios WHERE LOWER(email) = LOWER(?)", (email,))
    if not user:
        # Por seguridad no revelar si el mail existe, pero dar feedback amigable
        return {
            "status": "success",
            "message": "Si el correo está registrado en el sistema, recibirás un código de recuperación en breve."
        }
        
    recovery_code = str(secrets.randbelow(900000) + 100000)
    rec_exp = (datetime.now() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
    
    execute_query("""
        UPDATE usuarios 
        SET token_recuperacion = ?, token_recuperacion_expiracion = ? 
        WHERE id = ?
    """, (recovery_code, rec_exp, user["id"]))
    
    mail_res = send_password_reset_email(user["email"], user["username"], recovery_code)
    
    return {
        "status": "success",
        "message": "Hemos enviado un código de recuperación a tu correo electrónico.",
        "email": user["email"],
        "dev_code": mail_res.get("code")
    }

@app.post("/api/auth/reset-password")
def reset_password(data: ResetPasswordRequest):
    check_db_ready()
    email = data.email.strip().lower()
    code = data.code.strip()
    new_pwd = data.new_password
    
    if len(new_pwd) < 4:
        raise HTTPException(status_code=400, detail="La nueva contraseña debe tener al menos 4 caracteres.")
    if new_pwd != data.confirm_password:
        raise HTTPException(status_code=400, detail="Las nuevas contraseñas no coinciden.")
        
    user = query_one("SELECT * FROM usuarios WHERE LOWER(email) = LOWER(?)", (email,))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    if not user.get("token_recuperacion") or user["token_recuperacion"] != code:
        raise HTTPException(status_code=400, detail="El código de recuperación es incorrecto.")
        
    if user.get("token_recuperacion_expiracion"):
        try:
            exp_date = datetime.strptime(user["token_recuperacion_expiracion"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() > exp_date:
                raise HTTPException(status_code=400, detail="El código de recuperación ha expirado. Solicita uno nuevo.")
        except ValueError:
            pass
            
    # Hashear la nueva contraseña con SHA-256 y un nuevo salt
    new_hash, new_salt = hash_password_sha256(new_pwd)
    
    execute_query("""
        UPDATE usuarios 
        SET password_hash = ?, salt = ?, token_recuperacion = NULL, token_recuperacion_expiracion = NULL, verificado = 1
        WHERE id = ?
    """, (new_hash, new_salt, user["id"]))
    
    return {
        "status": "success",
        "message": "¡Tu contraseña ha sido restablecida exitosamente! Ya puedes iniciar sesión con tu nueva clave."
    }

# -------------------------------------------------------------
# 1.1 GESTOR DE USUARIOS PARA ADMINISTRADOR (/api/admin/*)
# -------------------------------------------------------------
VALID_ROLES = ["administrador", "docente", "investigador", "alumno"]

@app.get("/api/admin/users")
def get_all_users():
    check_db_ready()
    users = query_all("""
        SELECT 
            id, username, email, nombre_completo, rol, verificado, fecha_creacion 
        FROM usuarios 
        ORDER BY id ASC
    """)
    return {"status": "success", "users": users, "total": len(users)}

@app.post("/api/admin/users")
def admin_create_user(data: AdminCreateUserRequest):
    check_db_ready()
    username = data.username.strip()
    email = data.email.strip().lower()
    rol = data.rol.strip().lower()
    
    if rol not in VALID_ROLES:
        raise HTTPException(status_code=400, detail=f"Rol no válido. Permitidos: {', '.join(VALID_ROLES)}")
        
    # Validar duplicados
    if query_one("SELECT id FROM usuarios WHERE LOWER(username) = LOWER(?)", (username,)):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado.")
    if query_one("SELECT id FROM usuarios WHERE LOWER(email) = LOWER(?)", (email,)):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
        
    pwd_hash, salt = hash_password_sha256(data.password)
    verificado_int = 1 if data.verificado else 0
    
    user_id = execute_query("""
        INSERT INTO usuarios (username, email, password_hash, salt, nombre_completo, rol, verificado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, email, pwd_hash, salt, data.nombre_completo.strip(), rol, verificado_int))
    
    return {
        "status": "success",
        "message": f"Usuario '{username}' creado exitosamente por el Administrador.",
        "user": {
            "id": user_id,
            "username": username,
            "email": email,
            "nombre_completo": data.nombre_completo,
            "rol": rol,
            "verificado": verificado_int
        }
    }

@app.put("/api/admin/users/{user_id}/role")
def admin_update_user_role(user_id: int, data: AdminUpdateRoleRequest):
    check_db_ready()
    rol = data.rol.strip().lower()
    if rol not in VALID_ROLES:
        raise HTTPException(status_code=400, detail=f"Rol no válido. Permitidos: {', '.join(VALID_ROLES)}")
        
    user = query_one("SELECT id, username, rol FROM usuarios WHERE id = ?", (user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    # Impedir quitar el rol de administrador si es el único administrador del sistema
    if user["rol"] == "administrador" and rol != "administrador":
        admin_count = query_one("SELECT COUNT(*) as cnt FROM usuarios WHERE rol = 'administrador'")["cnt"]
        if admin_count <= 1:
            raise HTTPException(status_code=400, detail="No es posible degradar al único administrador del sistema.")
            
    execute_query("UPDATE usuarios SET rol = ? WHERE id = ?", (rol, user_id))
    
    return {
        "status": "success",
        "message": f"Rol del usuario '{user['username']}' actualizado a '{rol}'.",
        "user_id": user_id,
        "new_role": rol
    }

@app.delete("/api/admin/users/{user_id}")
def admin_delete_user(user_id: int, current_user_id: Optional[int] = Query(None)):
    check_db_ready()
    user = query_one("SELECT id, username, rol FROM usuarios WHERE id = ?", (user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    # Seguridad: no permitir auto-eliminación
    if current_user_id and user_id == current_user_id:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta de administrador en sesión.")
        
    # No permitir eliminar al último administrador del sistema
    if user["rol"] == "administrador":
        admin_count = query_one("SELECT COUNT(*) as cnt FROM usuarios WHERE rol = 'administrador'")["cnt"]
        if admin_count <= 1:
            raise HTTPException(status_code=400, detail="No es posible eliminar al único administrador del sistema.")
            
    execute_query("DELETE FROM usuarios WHERE id = ?", (user_id,))
    
    return {
        "status": "success",
        "message": f"Usuario '{user['username']}' eliminado definitivamente de la base de datos."
    }


# -------------------------------------------------------------
# 2. RESOLUTOR DE IMÁGENES / API WIKIPEDIA & JURASSIC PARK
# -------------------------------------------------------------
@app.get("/api/dinos/image/{nombre}")
def get_dino_image(nombre: str):
    clean_key = nombre.strip().lower()
    if clean_key in IMAGE_CACHE:
        return IMAGE_CACHE[clean_key]
    
    # 1. Buscar en BD local
    dino = query_one("SELECT id_dinosaurio, imagen_url, imagen_emoji FROM dinosaurios WHERE LOWER(nombre) = LOWER(?) OR LOWER(especie) LIKE LOWER(?)", (nombre, f"%{nombre}%"))
    if dino and dino.get("imagen_url"):
        res_data = {"status": "ok", "url": dino["imagen_url"], "imagen_url": dino["imagen_url"], "source": "database", "emoji": dino.get("imagen_emoji", "🦖")}
        IMAGE_CACHE[clean_key] = res_data
        return res_data
        
    # 2. Consultar API en cascada (Jurassic Park Wiki -> Wikipedia)
    thumb = fetch_dino_best_image(nombre)
    if thumb:
        if dino:
            conn = get_connection()
            conn.execute("UPDATE dinosaurios SET imagen_url = ? WHERE id_dinosaurio = ?", (thumb, dino["id_dinosaurio"]))
            conn.commit()
            conn.close()
        res_data = {"status": "ok", "url": thumb, "imagen_url": thumb, "source": "online_cascade", "emoji": dino.get("imagen_emoji", "🦖") if dino else "🦖"}
        IMAGE_CACHE[clean_key] = res_data
        return res_data
        
    fallback_data = {"status": "not_found", "url": None, "imagen_url": None, "source": "none", "emoji": dino.get("imagen_emoji", "🦖") if dino else "🦖"}
    IMAGE_CACHE[clean_key] = fallback_data
    return fallback_data


# -------------------------------------------------------------
# 3. INDICADORES GLOBALES (KPIS)
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
        SELECT id_dinosaurio, nombre, especie, indice_mascotabilidad, imagen_emoji, imagen_url, peso_kg
        FROM dinosaurios
        ORDER BY indice_mascotabilidad DESC
        LIMIT 1
    """)
    
    peor = query_one("""
        SELECT id_dinosaurio, nombre, especie, indice_mascotabilidad, agresividad_1_10, imagen_emoji, imagen_url
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
            d.imagen_url,
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
            d.imagen_url,
            d.observaciones,
            p.id_periodo,
            p.nombre AS periodo_nombre,
            p.era AS periodo_era,
            h.id_habitat,
            h.nombre AS habitat_nombre,
            h.tipo_terreno AS habitat_tipo_terreno,
            h.clima AS habitat_clima,
            dt.id_dieta,
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
# 5. CATÁLOGO COMPLETO Y BUSCADOR AVANZADO
# -------------------------------------------------------------
@app.get("/api/dinos/all")
def get_all_dinos():
    query = """
        SELECT 
            d.id_dinosaurio,
            d.nombre,
            d.especie,
            d.indice_mascotabilidad,
            d.imagen_emoji,
            d.imagen_url,
            d.peso_kg,
            d.velocidad_kmh,
            d.agresividad_1_10,
            p.nombre AS periodo_nombre,
            h.nombre AS habitat_nombre,
            dt.tipo AS dieta_tipo,
            CASE 
                WHEN d.indice_mascotabilidad >= 70 THEN 'VERDE'
                WHEN d.indice_mascotabilidad >= 40 THEN 'AMARILLO'
                ELSE 'ROJO'
            END AS semaforo_color
        FROM dinosaurios d
        INNER JOIN periodos p ON d.id_periodo = p.id_periodo
        INNER JOIN habitats h ON d.id_habitat = h.id_habitat
        INNER JOIN dietas dt ON d.id_dieta = dt.id_dieta
        ORDER BY d.nombre ASC
    """
    return query_all(query)

@app.get("/api/stats/search")
def search_dinos(
    q: Optional[str] = None,
    periodo_id: Optional[int] = None,
    habitat_id: Optional[int] = None,
    dieta_id: Optional[int] = None,
    semaforo: Optional[str] = None,
    sort_by: Optional[str] = "mascotabilidad_desc"
):
    sql = """
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
            d.imagen_url,
            d.observaciones,
            p.nombre AS periodo_nombre,
            h.nombre AS habitat_nombre,
            dt.tipo AS dieta_tipo,
            dt.costo_mensual_usd,
            dt.nivel_peligro_alimentacion,
            CASE 
                WHEN d.indice_mascotabilidad >= 70 THEN 'VERDE'
                WHEN d.indice_mascotabilidad >= 40 THEN 'AMARILLO'
                ELSE 'ROJO'
            END AS semaforo_color,
            CASE 
                WHEN d.indice_mascotabilidad >= 70 THEN 'Apto para convivencia'
                WHEN d.indice_mascotabilidad >= 40 THEN 'Requiere precauciones'
                ELSE 'Peligro extremo'
            END AS semaforo_veredicto
        FROM dinosaurios d
        INNER JOIN periodos p ON d.id_periodo = p.id_periodo
        INNER JOIN habitats h ON d.id_habitat = h.id_habitat
        INNER JOIN dietas dt ON d.id_dieta = dt.id_dieta
        WHERE 1=1
    """
    params = []
    
    if q and q.strip():
        search_term = f"%{q.strip()}%"
        sql += " AND (d.nombre LIKE ? OR d.especie LIKE ? OR d.observaciones LIKE ?)"
        params.extend([search_term, search_term, search_term])
        
    if periodo_id:
        sql += " AND d.id_periodo = ?"
        params.append(periodo_id)
        
    if habitat_id:
        sql += " AND d.id_habitat = ?"
        params.append(habitat_id)
        
    if dieta_id:
        sql += " AND d.id_dieta = ?"
        params.append(dieta_id)
        
    if semaforo:
        semaforo_upper = semaforo.upper().strip()
        if semaforo_upper == 'VERDE':
            sql += " AND d.indice_mascotabilidad >= 70"
        elif semaforo_upper == 'AMARILLO':
            sql += " AND d.indice_mascotabilidad >= 40 AND d.indice_mascotabilidad < 70"
        elif semaforo_upper == 'ROJO':
            sql += " AND d.indice_mascotabilidad < 40"
            
    # Ordenamiento
    order_map = {
        "mascotabilidad_desc": "d.indice_mascotabilidad DESC, d.nombre ASC",
        "mascotabilidad_asc": "d.indice_mascotabilidad ASC, d.nombre ASC",
        "peso_desc": "d.peso_kg DESC",
        "peso_asc": "d.peso_kg ASC",
        "velocidad_desc": "d.velocidad_kmh DESC",
        "nombre_asc": "d.nombre ASC"
    }
    sql += f" ORDER BY {order_map.get(sort_by, 'd.indice_mascotabilidad DESC')}"
    
    results = query_all(sql, tuple(params))
    return {
        "total_resultados": len(results),
        "filtros_aplicados": {
            "query": q,
            "periodo_id": periodo_id,
            "habitat_id": habitat_id,
            "dieta_id": dieta_id,
            "semaforo": semaforo,
            "sort_by": sort_by
        },
        "dinosaurios": results
    }

# -------------------------------------------------------------
# 6. COMPARADOR CARA A CARA (HEAD-TO-HEAD)
# -------------------------------------------------------------
@app.get("/api/stats/compare/{id1}/{id2}")
def compare_dinos(id1: int, id2: int):
    dino1 = get_dinosaurio_detail(id1)
    dino2 = get_dinosaurio_detail(id2)
    
    diff_mascotabilidad = dino1["indice_mascotabilidad"] - dino2["indice_mascotabilidad"]
    diff_peso = dino1["peso_kg"] - dino2["peso_kg"]
    diff_velocidad = dino1["velocidad_kmh"] - dino2["velocidad_kmh"]
    diff_agresividad = dino1["agresividad_1_10"] - dino2["agresividad_1_10"]
    diff_inteligencia = dino1["inteligencia_1_10"] - dino2["inteligencia_1_10"]
    diff_costo = dino1["costo_mensual_usd"] - dino2["costo_mensual_usd"]
    diff_espacio = dino1["espacio_requerido_m2"] - dino2["espacio_requerido_m2"]
    
    if diff_mascotabilidad > 0:
        ganador = dino1["nombre"]
        ganador_id = dino1["id_dinosaurio"]
        veredicto = f"🏆 {dino1['nombre']} es significativamente más viable como mascota ({dino1['indice_mascotabilidad']}/100 vs {dino2['indice_mascotabilidad']}/100)."
    elif diff_mascotabilidad < 0:
        ganador = dino2["nombre"]
        ganador_id = dino2["id_dinosaurio"]
        veredicto = f"🏆 {dino2['nombre']} es significativamente más viable como mascota ({dino2['indice_mascotabilidad']}/100 vs {dino1['indice_mascotabilidad']}/100)."
    else:
        ganador = "Empate técnico"
        ganador_id = None
        veredicto = f"🤝 Ambos dinosaurios comparten el mismo nivel de mascotabilidad ({dino1['indice_mascotabilidad']}/100)."
        
    return {
        "dino1": dino1,
        "dino2": dino2,
        "ganador": ganador,
        "ganador_id": ganador_id,
        "veredicto": veredicto,
        "diferencias": {
            "mascotabilidad": diff_mascotabilidad,
            "peso_kg": diff_peso,
            "velocidad_kmh": diff_velocidad,
            "agresividad": diff_agresividad,
            "inteligencia": diff_inteligencia,
            "costo_mensual_usd": diff_costo,
            "espacio_m2": diff_espacio
        }
    }

# -------------------------------------------------------------
# 7. GRÁFICOS ANALÍTICOS (CHART.JS)
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
        SELECT id_dinosaurio, nombre, especie, indice_mascotabilidad, peso_kg, imagen_emoji, imagen_url
        FROM dinosaurios
        ORDER BY indice_mascotabilidad DESC
        LIMIT 5
    """)
    peores = query_all("""
        SELECT id_dinosaurio, nombre, especie, indice_mascotabilidad, peso_kg, imagen_emoji, imagen_url
        FROM dinosaurios
        ORDER BY indice_mascotabilidad ASC
        LIMIT 5
    """)
    return {"mejores": mejores, "peores": peores}

# -------------------------------------------------------------
# 8. SERVIDO DE FRONTEND SPA
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
