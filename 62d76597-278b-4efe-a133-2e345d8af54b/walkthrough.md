# 🦖 DinoMascota Dashboard — Guía de Entrega, Arquitectura y Ejecución

Tablero de Control y Análisis Paleontológico desarrollado para **Bases de Datos Aplicada — UAI (Ingeniería en Sistemas Informáticos)**.

---

## 📁 Ubicación del Proyecto

Ruta local del proyecto:
`C:\Users\mdcom\.gemini\antigravity\scratch\dinomascota\Mascoteabilidad-de-dinosaurios`

---

## 🗄️ Modelo de Base de Datos y Entidades (SQLite)

El sistema implementa **5 tablas normalizadas (3FN)**:

1. **`periodos` (Entidad 1):** Períodos históricos (`Triásico`, `Jurásico`, `Cretácico`), eras, rango temporal en millones de años y clima predominante.
2. **`habitats` (Entidad 2):** Tipos de terreno (`Bosque`, `Llanura`, `Pantano`, `Costero`, `Montaña`, `Ribereño`), superficie mínima en $m^2$, clima y dificultad de adaptación.
3. **`dietas` (Entidad 3):** Régimen alimenticio (`Herbívoro`, `Carnívoro`, `Piscívoro`, `Insectívoro`, `Omnívoro`), consumo diario en kg, costo mensual estimado en USD y riesgo de mordida.
4. **`dinosaurios` (Entidad 4):** Más de **50 especies** con atributos biométricos (altura, longitud, peso, velocidad), agresividad (1-10), inteligencia (1-10), espacio requerido y el **Índice de Mascotabilidad (0 a 100)**.
5. **`usuarios` (Seguridad):** Cuentas con contraseñas encriptadas con **Bcrypt**.

---

## 🚦 Cumplimiento de Criterios de Aprobación UAI

| Requisito UAI | Implementación Técnica | Estado |
| :--- | :--- | :---: |
| **Consultas SQL Puras** | Consultas directas con `JOIN`, `GROUP BY`, `AVG()`, `COUNT()`, `ORDER BY` y `CASE WHEN` sin ORM. | ✅ 100% |
| **Drill-Down / Drill-Up (3 Niveles)** | **Nivel 1:** Períodos $\rightarrow$ **Nivel 2:** Hábitats del período $\rightarrow$ **Nivel 3:** Especies con ficha técnica y botón de retorno (*Drill-Up*). | ✅ 100% |
| **Semaforización Visual (3 Estados)** | **Verde ($70-100$ pts):** Mascota viable.<br>**Amarillo ($40-69$ pts):** Requiere patio grande y adiestramiento.<br>**Rojo ($0-39$ pts):** Peligro mortal. | ✅ 100% |
| **Autenticación (Login)** | Validación contra tabla `usuarios` en SQLite con hash seguro `bcrypt`. | ✅ 100% |
| **Carga de Datos** | Scripts DDL (`schema.sql`) y DML (`seeds.sql`) sin requerir pantallas de ABM. | ✅ 100% |
| **Herramientas Analíticas Extra** | Buscador dinámico multifiltro y Comparador cara a cara (*Head-to-Head*). | ✅ 100% |

---

## 🔑 Credenciales de Acceso

| Usuario | Contraseña | Rol en el Sistema |
| :--- | :--- | :--- |
| `admin` | `admin123` | Administrador General |
| `profesor` | `uai2026` | Docente Titular |
| `alumno` | `dino123` | Estudiante Investigador |

---

## 🚀 Cómo Iniciar la Aplicación

Para ejecutar el servidor y abrir el Dashboard:

1. Abrí PowerShell o una terminal en la carpeta del proyecto:
```powershell
cd C:\Users\mdcom\.gemini\antigravity\scratch\dinomascota\Mascoteabilidad-de-dinosaurios
```

2. Inicia el servidor con Python:
```powershell
python -m uvicorn backend.app:app --reload --port 8000
```
*(o si usás el entorno virtual local: `& "C:\Ignacio\UAI\PythonEj\.venv\Scripts\python.exe" -m uvicorn backend.app:app --reload --port 8000`)*

3. Abrí en tu navegador web:
👉 **[http://localhost:8000](http://localhost:8000)** (o **[http://localhost:8000/docs](http://localhost:8000/docs)** para la documentación interactiva Swagger de la API).

---

## 📂 Estructura de Archivos del Repositorio

```
Mascoteabilidad-de-dinosaurios/
├── backend/
│   ├── database/
│   │   ├── schema.sql         # DDL: Definición de tablas, llaves foráneas e índices
│   │   ├── seeds.sql          # DML: Datos iniciales con 50+ dinosaurios y usuarios
│   │   ├── dinomascota.db     # Base de datos SQLite inicializada y operativa
│   │   └── db.py              # Módulo de conexión, SQL puro y sincronización de paleoarte
│   ├── static/
│   │   └── index.html         # Tablero SPA completo en React 18 + Tailwind + Chart.js
│   ├── app.py                 # API REST FastAPI con autenticación y endpoints analíticos
│   └── requirements.txt       # Dependencias de Python (FastAPI, Uvicorn, Bcrypt, Pydantic)
├── frontend/                  # Código fuente modular React
│   ├── src/
│   │   └── services/api.js    # Consumo de endpoints de la API
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── README.md                  # Documentación oficial del repositorio
└── 62d76597-278b-4efe-a133-2e345d8af54b/ # Contexto persistente de conversación Antigravity
    ├── implementation_plan.md
    └── walkthrough.md
```
