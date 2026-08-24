# 🦖 DinoMascota Dashboard — Guía de Entrega y Ejecución

Tablero de Control y Análisis Paleontológico desarrollado para **Bases de Datos Aplicada — UAI (Ingeniería en Sistemas Informáticos)**.

---

## 📁 Ubicación del Proyecto

Todo el proyecto ha sido creado y probado en:
`C:\Users\Navegador\.gemini\antigravity\scratch\dinomascota`

---

## 🗄️ Modelo de Base de Datos y Entidades (SQLite)

El sistema implementa **5 tablas normalizadas** (cumpliendo con creces el mínimo de 4 entidades):

1. **`periodos` (Entidad 1):** Períodos históricos (`Triásico`, `Jurásico`, `Cretácico`), eras, rango en millones de años y clima global.
2. **`habitats` (Entidad 2):** Tipos de terreno, requerimiento de espacio en $m^2$, clima y dificultad de adaptación.
3. **`dietas` (Entidad 3):** Régimen (`Herbívoro`, `Carnívoro`, `Piscívoro`, `Insectívoro`, `Omnívoro`), consumo diario en kg, costo mensual estimado en USD y nivel de peligro.
4. **`dinosaurios` (Entidad 4):** 24 especies con atributos biométricos (altura, longitud, peso, velocidad), agresividad (1-10), inteligencia (1-10), espacio requerido y el **Índice de Mascotabilidad (0 a 100)**.
5. **`usuarios` (Seguridad):** Cuentas de usuario con contraseñas encriptadas con **Bcrypt**.

---

## 🚦 Cumplimiento de Criterios de Aprobación UAI

| Requisito UAI | Implementación Técnica | Estado |
| :--- | :--- | :---: |
| **Consultas SQL Puras** | Consultas directas con `JOIN`, `GROUP BY`, `AVG()`, `COUNT()`, `ORDER BY` y `CASE WHEN`. | ✅ 100% |
| **Drill-Down / Drill-Up (3 Niveles)** | **Nivel 1:** Períodos $\rightarrow$ **Nivel 2:** Hábitats del período $\rightarrow$ **Nivel 3:** Especies con ficha técnica y botón de retorno (*Drill-Up*). | ✅ 100% |
| **Semaforización Visual (3 Estados)** | **Verde ($70-100$ pts):** Mascota viable.<br>**Amarillo ($40-69$ pts):** Requiere patio grande y adiestramiento.<br>**Rojo ($0-39$ pts):** Peligro mortal. | ✅ 100% |
| **Autenticación (Login)** | Validación contra tabla `usuarios` en SQLite con hash seguro `bcrypt`. | ✅ 100% |
| **Carga de Datos** | Scripts DDL (`schema.sql`) y DML (`seeds.sql`) sin requerir pantallas de ABM. | ✅ 100% |

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

1. Abre PowerShell o una terminal en la carpeta del proyecto:
```powershell
cd C:\Users\Navegador\.gemini\antigravity\scratch\dinomascota
```

2. Inicia el servidor con Python:
```powershell
python -m uvicorn backend.app:app --reload --port 8000
```

3. Abre en tu navegador web:
👉 **[http://localhost:8000](http://localhost:8000)** (o **[http://localhost:8000/docs](http://localhost:8000/docs)** para la documentación interactiva Swagger de la API).

---

## 📂 Estructura de Archivos Creada

```
dinomascota/
├── backend/
│   ├── database/
│   │   ├── schema.sql         # DDL: Definición de tablas, llaves foráneas e índices
│   │   ├── seeds.sql          # DML: Datos iniciales con contraseñas bcrypt y 24 dinosaurios
│   │   ├── dinomascota.db     # Base de datos SQLite inicializada y operativa
│   │   └── db.py              # Módulo de conexión y ejecución de SQL puro
│   ├── static/
│   │   └── index.html         # Tablero SPA completo en React 18 + Tailwind + Chart.js
│   ├── app.py                 # API REST FastAPI con autenticación y endpoints analíticos
│   └── requirements.txt       # Dependencias mínimas de Python
├── frontend/                  # Código fuente React modular para entregar en el repositorio
│   ├── src/
│   │   ├── services/api.js    # Consumo de endpoints de la API
│   │   ├── components/        # Componentes reutilizables
│   │   └── App.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md                  # Documentación oficial para el informe y el repositorio
```
