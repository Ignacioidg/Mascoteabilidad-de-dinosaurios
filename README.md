# 🦖 DinoMascota - Tablero de Control Paleontológico
### Proyecto Final Cuatrimestral — Bases de Datos Aplicada (UAI)

Sistema web analítico e interactivo desarrollado en **Python (FastAPI) + SQLite + React (Tailwind CSS & Chart.js)** para evaluar la viabilidad de adopción y convivencia doméstica de diversas especies de dinosaurios mediante consultas SQL directas y toma de decisiones multinivel.

---

## 🎯 Cumplimiento de Consignas UAI

1. **Consultas SQL Puras:** Todas las métricas, KPIs, agrupaciones y desgloses se ejecutan mediante consultas SQL nativas sobre la base de datos dinomascota.db.
2. **Drill-Down / Drill-Up (3 Niveles):**
   * **Nivel 1:** Períodos Geológicos (Triásico, Jurásico, Cretácico).
   * **Nivel 2:** Hábitats del período seleccionado (Bosque, Llanura, Pantano, Costero, Montaña, Ribereño).
   * **Nivel 3:** Especies con ficha técnica, biometría y botón de retorno (*Drill-Up*).
3. **Semaforización Visual (3 Estados):**
   * 🟢 **Verde (70-100 pts):** Situación Favorable / Mascota Viable (*Compsognathus*, *Microraptor*, *Yi qi*, *Dryosaurus*).
   * 🟡 **Amarillo (40-69 pts):** Advertencia / Requiere gran patio y adiestramiento (*Triceratops*, *Stegosaurus*, *Ankylosaurus*).
   * 🔴 **Rojo (0-39 pts):** Peligro Crítico / No recomendable (*Tyrannosaurus Rex*, *Spinosaurus*, *Giganotosaurus*).
4. **Sistema de Autenticación (Login con Hashing):**
   * Validación contra tabla usuarios.
   * Contraseñas hasheadas de forma segura con **Bcrypt**.
5. **5 Entidades Normalizadas:** periodos, habitats, dietas, dinosaurios y usuarios (supera el mínimo de 4).
6. **Carga Inicial Automatizada:** Realizada mediante scripts DDL (schema.sql) y DML (seeds.sql) con más de 50 especies.
7. **Módulos Analíticos Avanzados:**
   * 🔍 **Buscador Dinámico Multifiltro:** Búsqueda en tiempo real por nombre/especie, período, hábitat, dieta y color de semáforo con ordenamiento flexible.
   * ⚔️ **Comparador Cara a Cara (Head-to-Head):** Comparación métrica de dos especies con cálculo diferencial y determinación automática del ganador.
   * 📊 **Gráficos Estadísticos con Chart.js:** Distribución por régimen alimenticio, peso promedio por era y Top 5 mejores/peores mascotas.

---

## 🚀 Instrucciones de Ejecución

### 1. Requisitos
* Python 3.10 o superior.

### 2. Instalación de dependencias
`ash
pip install -r backend/requirements.txt
`

### 3. Ejecución del Servidor
`ash
python -m uvicorn backend.app:app --reload --port 8000
`

Abre tu navegador en: **http://localhost:8000**  
Documentación interactiva Swagger: **http://localhost:8000/docs**

---

## 🔑 Credenciales de Acceso

| Usuario | Contraseña | Rol |
| :--- | :--- | :--- |
| **admin** | dmin123 | Administrador General |
| **profesor** | uai2026 | Docente Titular |
| **alumno** | dino123 | Estudiante Investigador |

---

## 🏛️ Estructura del Proyecto
`
Mascoteabilidad-de-dinosaurios/
├── backend/
│   ├── database/
│   │   ├── schema.sql         # DDL: Definición de tablas, llaves foráneas e índices
│   │   ├── seeds.sql          # DML: Datos iniciales con 50+ especies y usuarios
│   │   ├── dinomascota.db     # Base de datos SQLite inicializada y operativa
│   │   └── db.py              # Conexión SQLite, consultas SQL y sincronización de imágenes
│   ├── static/
│   │   └── index.html         # Aplicación React 18 SPA integrada (Tailwind + Chart.js)
│   ├── app.py                 # Backend FastAPI con endpoints SQL, Auth y Comparador
│   └── requirements.txt       # Dependencias de Python
├── frontend/                  # Código fuente React modular
│   ├── src/
│   │   └── services/api.js
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── README.md
└── 62d76597-278b-4efe-a133-2e345d8af54b/ # Contexto persistente de conversación Antigravity
    ├── implementation_plan.md
    └── walkthrough.md
`
