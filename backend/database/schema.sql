-- ====================================================================
-- PROYECTO: DinoMascota Dashboard
-- MATERIA: Bases de Datos Aplicada - UAI
-- SCRIPT: DDL - Creación de Esquema de Base de Datos
-- ====================================================================

DROP TABLE IF EXISTS dinosaurios;
DROP TABLE IF EXISTS dietas;
DROP TABLE IF EXISTS habitats;
DROP TABLE IF EXISTS periodos;
DROP TABLE IF EXISTS usuarios;

-- 1. Tabla de Usuarios (Autenticación con Hashing Bcrypt)
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    rol VARCHAR(20) DEFAULT 'investigador' CHECK (rol IN ('administrador', 'docente', 'investigador', 'alumno')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Entidad 1: Períodos Geológicos
CREATE TABLE periodos (
    id_periodo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    era VARCHAR(50) NOT NULL,
    millones_anios_inicio REAL NOT NULL,
    millones_anios_fin REAL NOT NULL,
    clima_predominante VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- 3. Entidad 2: Hábitats
CREATE TABLE habitats (
    id_habitat INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    tipo_terreno VARCHAR(100) NOT NULL,
    superficie_minima_m2 INTEGER NOT NULL,
    clima VARCHAR(50) NOT NULL,
    dificultad_adaptacion VARCHAR(20) CHECK (dificultad_adaptacion IN ('Baja', 'Media', 'Alta', 'Extrema'))
);

-- 4. Entidad 3: Dietas y Alimentación
CREATE TABLE dietas (
    id_dieta INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo VARCHAR(50) UNIQUE NOT NULL,
    consumo_diario_kg REAL NOT NULL,
    costo_mensual_usd REAL NOT NULL,
    nivel_peligro_alimentacion VARCHAR(20) CHECK (nivel_peligro_alimentacion IN ('Bajo', 'Medio', 'Alto', 'Mortal'))
);

-- 5. Entidad 4: Dinosaurios (Especies y Características Biométricas)
CREATE TABLE dinosaurios (
    id_dinosaurio INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    especie VARCHAR(100) NOT NULL,
    altura_m REAL NOT NULL,
    longitud_m REAL NOT NULL,
    peso_kg REAL NOT NULL,
    velocidad_kmh REAL NOT NULL,
    agresividad_1_10 INTEGER NOT NULL CHECK (agresividad_1_10 BETWEEN 1 AND 10),
    inteligencia_1_10 INTEGER NOT NULL CHECK (inteligencia_1_10 BETWEEN 1 AND 10),
    esperanza_vida_anios INTEGER NOT NULL,
    espacio_requerido_m2 INTEGER NOT NULL,
    indice_mascotabilidad INTEGER NOT NULL CHECK (indice_mascotabilidad BETWEEN 0 AND 100),
    id_periodo INTEGER NOT NULL,
    id_habitat INTEGER NOT NULL,
    id_dieta INTEGER NOT NULL,
    imagen_emoji VARCHAR(20) DEFAULT '🦖',
    observaciones TEXT,
    FOREIGN KEY (id_periodo) REFERENCES periodos(id_periodo) ON DELETE RESTRICT,
    FOREIGN KEY (id_habitat) REFERENCES habitats(id_habitat) ON DELETE RESTRICT,
    FOREIGN KEY (id_dieta) REFERENCES dietas(id_dieta) ON DELETE RESTRICT
);

-- Índices para optimizar las consultas analíticas del Dashboard
CREATE INDEX idx_dinos_periodo ON dinosaurios(id_periodo);
CREATE INDEX idx_dinos_habitat ON dinosaurios(id_habitat);
CREATE INDEX idx_dinos_dieta ON dinosaurios(id_dieta);
CREATE INDEX idx_dinos_mascotabilidad ON dinosaurios(indice_mascotabilidad);
