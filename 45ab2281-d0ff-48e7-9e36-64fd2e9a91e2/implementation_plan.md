# Plan de Implementación: DinoMascota Dashboard 🦖

Sistema integral de análisis y tablero de control para evaluación de aptitud doméstica de dinosaurios, desarrollado para la cátedra de **Bases de Datos Aplicada (UAI)**.

---

## 1. Motores de IA y Estrategia de Desarrollo

Para este proyecto utilizamos **Gemini 3.7 / Modelos de Razonamiento Profundo**:
- **Para Arquitectura, Base de Datos y Backend:** Diseña modelos normalizados (3FN), consultas SQL nativas complejas (agregaciones, `JOIN`s, `CASE WHEN` para semaforización) y manejo seguro de contraseñas con `bcrypt`.
- **Para Frontend e Interfaz Gráfica:** Construye interfaces interactivas con Tailwind CSS y Chart.js sin requerir configuraciones complejas de npm o frameworks pesados.

---

## 2. Decisiones de Diseño y Arquitectura

### 🗄️ Modelo de Base de Datos (SQLite + SQL Nativo)
El modelo cuenta con **5 tablas** (cumpliendo y superando el requisito de 4 entidades):
1. `usuarios`: `id`, `username`, `password_hash`, `nombre_completo`, `rol`, `created_at`.
2. `periodos`: `id_periodo`, `nombre` (Triásico, Jurásico, Cretácico), `era`, `millones_anios_inicio`, `millones_anios_fin`, `clima_predominante`.
3. `habitats`: `id_habitat`, `nombre` (Bosque, Llanura, Pantano, Costero, Montaña), `superficie_minima_m2`, `clima`, `dificultad_adaptacion`.
4. `dietas`: `id_dieta`, `tipo` (Herbívoro, Carnívoro, Piscívoro, Insectívoro), `consumo_diario_kg`, `costo_mensual_usd`, `riesgo_mordida`.
5. `dinosaurios`: `id_dinosaurio`, `nombre`, `altura_m`, `longitud_m`, `peso_kg`, `velocidad_kmh`, `agresividad_1_10`, `inteligencia_1_10`, `esperanza_vida_anios`, `espacio_requerido_m2`, `indice_mascotabilidad`, `id_periodo`, `id_habitat`, `id_dieta`, `imagen_url`, `observaciones`.

---

## 3. Componentes a Desarrollar

### [Componente 1: Base de Datos y Datos Iniciales]
#### [NEW] `database/schema.sql`
- Script DDL para crear las 5 tablas con claves primarias, foráneas, restricciones `CHECK` y tipos correctos.
#### [NEW] `database/seeds.sql`
- Script DML con más de 25 dinosaurios históricos detallados y usuarios de prueba con contraseñas hasheadas (`admin` / `profesor` / `alumno`).
#### [NEW] `database/db.py`
- Módulo Python para inicializar la base de datos `dinomascota.db` y proveer funciones para ejecutar consultas SQL puras.

---

### [Componente 2: Backend API (FastAPI / Python)]
#### [NEW] `app.py`
- Endpoints de autenticación (`/api/login`, `/api/logout`, `/api/me`).
- Endpoints analíticos con consultas SQL directas:
  - `/api/stats/kpis`: Métricas generales (total especies, peso promedio, más rápido, más peligroso, etc.).
  - `/api/stats/drill-down/periodos`: Nivel 1 (Resumen por período histórico).
  - `/api/stats/drill-down/habitats/{periodo_id}`: Nivel 2 (Hábitats del período con cantidad de especies).
  - `/api/stats/drill-down/dinosaurios/{periodo_id}/{habitat_id}`: Nivel 3 (Listado de especies con su semáforo de mascotabilidad).
  - `/api/stats/dinosaurio/{dino_id}`: Ficha técnica detallada con análisis comparativo.
  - `/api/stats/charts`: Datos para gráficos de barras, tortas y semaforización global.

---

### [Componente 3: Frontend Web (UI / UX Dinámico)]
#### [NEW] `templates/login.html`
- Pantalla de inicio de sesión moderna, atractiva, validando credenciales contra la BD.
#### [NEW] `templates/dashboard.html`
- Tablero de control con:
  - Panel superior con KPIs globales.
  - Sección de **Drill-Down / Drill-Up interactivo en 3 niveles** (Período ➔ Hábitat ➔ Especie ➔ Ficha técnica).
  - **Semaforización visual (Verde / Amarillo / Rojo)** con referencias y leyendas explicativas.
  - Gráficos interactivos con **Chart.js** (distribución por dieta, peso por era, top 5 más domesticables).

---

## 4. Plan de Verificación

### Pruebas Automáticas y Manuales:
1. **Inicialización de BD:** Ejecutar `schema.sql` y `seeds.sql` verificando que no existan errores de sintaxis ni de claves foráneas.
2. **Prueba de Login:** Validar login correcto con contraseña hasheada y rechazo ante credenciales inválidas.
3. **Prueba de Consultas SQL:** Verificar que cada nivel del drill-down responde correctamente con datos agrupados desde SQLite.
4. **Prueba de UI:** Validar navegación entre niveles (Drill Down y Drill Up) y representación correcta de los colores de semaforización.
