# -*- coding: utf-8 -*-
import os
import bcrypt
import sqlite3

BASE_DIR = r'C:\Users\Navegador\.gemini\antigravity\scratch\dinomascota'
DB_PATH = os.path.join(BASE_DIR, 'backend', 'database', 'dinomascota.db')
SEEDS_PATH = os.path.join(BASE_DIR, 'backend', 'database', 'seeds.sql')

def hash_pw(pw: str) -> str:
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

admin_hash = hash_pw('admin123')
prof_hash = hash_pw('uai2026')
alum_hash = hash_pw('dino123')

print('Admin hash generated:', admin_hash)
print('Prof hash generated:', prof_hash)
print('Alum hash generated:', alum_hash)

seeds_sql = f"""-- ====================================================================
-- PROYECTO: DinoMascota Dashboard
-- MATERIA: Bases de Datos Aplicada - UAI
-- SCRIPT: DML - Inserción de Datos Iniciales (Seeds)
-- ====================================================================

-- 1. Usuarios con contraseña hasheada en bcrypt
INSERT INTO usuarios (username, password_hash, nombre_completo, rol) VALUES
('admin', '{admin_hash}', 'Administrador General', 'administrador'),
('profesor', '{prof_hash}', 'Prof. Titular BD Aplicada', 'docente'),
('alumno', '{alum_hash}', 'Estudiante de Sistemas', 'alumno');

-- 2. Períodos Geológicos
INSERT INTO periodos (id_periodo, nombre, era, millones_anios_inicio, millones_anios_fin, clima_predominante, descripcion) VALUES
(1, 'Triásico', 'Mesozoico', 251.9, 201.3, 'Cálido y árido, con vastos desiertos y veranos intensos', 'Aparición de los primeros dinosaurios pequeños y ágiles.'),
(2, 'Jurásico', 'Mesozoico', 201.3, 145.0, 'Cálido y húmedo, con densos bosques de coníferas y helechos', 'Época dorada de los grandes saurópodos y depredadores emblemáticos.'),
(3, 'Cretácico', 'Mesozoico', 145.0, 66.0, 'Templado a cálido, diversificación de plantas con flor', 'Mayor diversidad morfológica y desarrollo de dinosaurios emplumados.');

-- 3. Hábitats
INSERT INTO habitats (id_habitat, nombre, tipo_terreno, superficie_minima_m2, clima, dificultad_adaptacion) VALUES
(1, 'Bosque Templado', 'Arbolado denso con abundante follaje', 150, 'Templado', 'Baja'),
(2, 'Llanura Abierta', 'Praderas y pastizales extensos', 1200, 'Templado-Cálido', 'Baja'),
(3, 'Pantano Húmedo', 'Tierras anegadas, ciénagas y aguas poco profundas', 600, 'Húmedo Tropical', 'Media'),
(4, 'Litoral Costero', 'Playas, acantilados y estuarios marítimos', 400, 'Marítimo Húmedo', 'Media'),
(5, 'Cañón Árido', 'Terreno rocoso con vegetación xerófila', 250, 'Árido y Seco', 'Alta'),
(6, 'Valle Fluvial', 'Riberas de ríos caudalosos y deltas fértiles', 800, 'Subtropical', 'Baja');

-- 4. Dietas
INSERT INTO dietas (id_dieta, tipo, consumo_diario_kg, costo_mensual_usd, nivel_peligro_alimentacion) VALUES
(1, 'Herbívoro Estricto', 45.0, 350.00, 'Bajo'),
(2, 'Carnívoro Depredador', 25.0, 1800.00, 'Mortal'),
(3, 'Piscívoro Especializado', 12.0, 600.00, 'Medio'),
(4, 'Insectívoro / Frugívoro', 1.5, 90.00, 'Bajo'),
(5, 'Omnívoro Adaptable', 8.0, 280.00, 'Medio');

-- 5. Dinosaurios (24 especies con atributos analíticos detallados)
INSERT INTO dinosaurios (
    nombre, especie, altura_m, longitud_m, peso_kg, velocidad_kmh, agresividad_1_10, 
    inteligencia_1_10, esperanza_vida_anios, espacio_requerido_m2, indice_mascotabilidad, 
    id_periodo, id_habitat, id_dieta, imagen_emoji, observaciones
) VALUES
-- Triásico (id_periodo = 1)
('Herrerasaurus', 'Herrerasaurus ischigualastensis', 1.5, 3.0, 250.0, 40.0, 8, 5, 20, 300, 22, 1, 5, 2, '🦖', 'Uno de los primeros carnívoros; temperamento impredecible y mordida fuerte.'),
('Eoraptor', 'Eoraptor lunensis', 0.4, 1.0, 10.0, 35.0, 3, 6, 12, 40, 82, 1, 1, 5, '🦎', 'Tamaño de un gato grande; adaptable, come semillas e insectos, excelente mascota de jardín.'),
('Plateosaurus', 'Plateosaurus trossingensis', 3.2, 8.0, 4000.0, 20.0, 4, 3, 45, 1500, 35, 1, 2, 1, '🦕', 'Herbívoro dócil pero su inmenso peso puede aplastar la cochera familiar.'),
('Coelophysis', 'Coelophysis bauri', 0.9, 2.5, 25.0, 50.0, 6, 7, 15, 120, 58, 1, 5, 5, '🦖', 'Muy veloz y curioso; requiere adiestramiento estricto pero es leal.'),
('Marasuchus', 'Marasuchus lilloensis', 0.2, 0.4, 1.2, 28.0, 2, 4, 8, 15, 91, 1, 1, 4, '🦎', 'Minúsculo reptil ágil; se alimenta de grillos, ideal para departamentos amplios.'),
('Staurikosaurus', 'Staurikosaurus pricei', 0.8, 2.0, 30.0, 45.0, 7, 5, 14, 150, 42, 1, 5, 2, '🦖', 'Depredador ágil del Triásico superior; no apto para convivir con niños ni perros.'),

-- Jurásico (id_periodo = 2)
('Brachiosaurus', 'Brachiosaurus altithorax', 13.0, 26.0, 35000.0, 15.0, 1, 2, 80, 5000, 18, 2, 2, 1, '🦕', 'Sumamente pacífico, pero comerá toda la arboleda vecinal y bloqueará el tráfico.'),
('Dilophosaurus', 'Dilophosaurus wetherilli', 2.0, 7.0, 400.0, 38.0, 8, 7, 25, 450, 20, 2, 1, 2, '🦖', 'Territorial y cazador veloz; no escupe veneno real pero muerde severamente.'),
('Stegosaurus', 'Stegosaurus stenops', 4.0, 9.0, 5000.0, 12.0, 3, 2, 50, 1800, 48, 2, 2, 1, '🦕', 'Tranquilo y herbívoro, pero su cola con púas (thagomizer) requiere señalización vial.'),
('Allosaurus', 'Allosaurus fragilis', 3.5, 9.5, 2000.0, 42.0, 9, 8, 30, 1200, 8, 2, 1, 2, '🦖', 'Súper depredador jurásico; riesgo extremo de comerse a sus propios dueños.'),
('Compsognathus', 'Compsognathus longipes', 0.3, 0.8, 2.5, 40.0, 4, 6, 10, 25, 88, 2, 1, 4, '🦎', 'Del tamaño de una gallina; juguetón, caza roedores e insectos domésticos.'),
('Archaeopteryx', 'Archaeopteryx lithographica', 0.3, 0.5, 0.9, 30.0, 1, 7, 12, 20, 94, 2, 1, 4, '🦜', 'Fascinante criatura emplumada; dócil, puede posarse en el hombro como un loro exótico.'),
('Camarasaurus', 'Camarasaurus supremus', 7.5, 15.0, 18000.0, 14.0, 2, 2, 60, 3000, 26, 2, 6, 1, '🦕', 'Saurópodo mediano muy dócil; mantenimiento prohibitivo en forraje.'),
('Ceratosaurus', 'Ceratosaurus nasicornis', 2.2, 6.0, 1000.0, 35.0, 8, 6, 22, 600, 15, 2, 6, 2, '🦖', 'Con cuerno distintivo en el hocico; altamente agresivo cerca del agua.'),

-- Cretácico (id_periodo = 3)
('Tyrannosaurus rex', 'Tyrannosaurus rex', 4.0, 12.5, 8500.0, 27.0, 10, 8, 30, 3500, 6, 3, 2, 2, '🦖', 'El rey indiscutido; fuerza de mordida demoledora, incompatible con la vida urbana.'),
('Triceratops', 'Triceratops horridus', 3.0, 8.5, 7000.0, 32.0, 5, 4, 40, 2000, 45, 3, 2, 1, '🦏', 'Fiel y robusto como un rinoceronte leal; requiere gran patio y cuidado con las embestidas.'),
('Velociraptor', 'Velociraptor mongoliensis', 0.6, 1.8, 15.0, 55.0, 8, 9, 18, 80, 49, 3, 5, 2, '🦅', 'Muy inteligente y emplumado; abre picaportes pero no debe quedarse solo con niños.'),
('Microraptor', 'Microraptor gui', 0.25, 0.77, 1.0, 30.0, 2, 7, 11, 20, 95, 3, 1, 4, '🦜', 'Cuatro alas emplumadas, come bichos, planea por la sala; la mejor mascota voladora.'),
('Ankylosaurus', 'Ankylosaurus magniventris', 1.7, 8.0, 6000.0, 10.0, 2, 2, 45, 1500, 52, 3, 2, 1, '🐢', 'Tanque viviente súper pacífico; excelente podadora de césped si no mueves su mazo.'),
('Spinosaurus', 'Spinosaurus aegyptiacus', 5.0, 15.0, 9000.0, 22.0, 9, 7, 35, 4000, 9, 3, 3, 3, '🐊', 'Colosal amante del agua; vaciará la pileta olímpica y se comerá los peces del acuario.'),
('Pachycephalosaurus', 'Pachycephalosaurus wyomingensis', 1.8, 4.5, 450.0, 24.0, 6, 3, 22, 500, 38, 3, 1, 5, '🐏', 'Propenso a cabezazos contra portones y paredes cuando se frustra.'),
('Parasaurolophus', 'Parasaurolophus walkeri', 2.8, 9.5, 3000.0, 25.0, 2, 4, 35, 1200, 63, 3, 6, 1, '🎺', 'Produce hermosos sonidos de trompeta con su cresta; muy cariñoso y gregario.'),
('Oviraptor', 'Oviraptor philoceratops', 1.0, 1.6, 35.0, 42.0, 4, 8, 16, 100, 71, 3, 5, 5, '🪶', 'Excelente incubador, curioso, come frutas y huevos; requiere juguetes interactivos.'),
('Baryonyx', 'Baryonyx walkeri', 2.5, 7.5, 1700.0, 30.0, 7, 6, 25, 800, 24, 3, 3, 3, '🎣', 'Garra gigante para pescar; si le tienes una laguna privada con truchas se calma.');
"""

with open(SEEDS_PATH, 'w', encoding='utf-8') as f:
    f.write(seeds_sql)

print('[OK] seeds.sql regenerated.')

# Re-inicializar DB
from backend.database.db import init_db
init_db(force_reload=True)
print('[OK] DB reloaded with valid bcrypt hashes.')
