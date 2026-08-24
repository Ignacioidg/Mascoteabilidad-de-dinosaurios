# 🦖 DinoMascota - Tablero de Control Paleontológico
### Proyecto Final Cuatrimestral — Bases de Datos Aplicada (UAI)

Sistema web analítico e interactivo desarrollado en **Python (FastAPI) + SQLite + React (Tailwind CSS & Chart.js)** para evaluar la viabilidad de adopción y convivencia doméstica de diversas especies de dinosaurios mediante consultas SQL directas y toma de decisiones multinivel.

---

## 🎯 Cumplimiento de Consignas UAI

1. **Consultas SQL Puras:** Todas las métricas, KPIs, agrupaciones y desgloses se ejecutan mediante consultas SQL sobre la base de datos `dinomascota.db`.
2. **Drill-Down / Drill-Up (3 Niveles):**
   * **Nivel 1:** Períodos Geológicos (Triásico, Jurásico, Cretácico).
   * **Nivel 2:** Hábitats del período seleccionado (Bosque, Llanura, Pantano, etc.).
   * **Nivel 3:** Especies con ficha técnica, biometría y botón de retorno (*Drill-Up*).
3. **Semaforización Visual (3 Estados):**
   * 🟢 **Verde (70-100 pts):** Situación Favorable / Mascota Viable (*Compsognathus*, *Microraptor*).
   * 🟡 **Amarillo (40-69 pts):** Advertencia / Requiere gran patio y adiestramiento (*Triceratops*, *Stegosaurus*).
   * 🔴 **Rojo (0-39 pts):** Peligro Crítico / No recomendable (*Tyrannosaurus Rex*, *Spinosaurus*).
4. **Sistema de Autenticación (Login con Hashing):**
   * Validación contra tabla `usuarios`.
   * Contraseñas hasheadas de forma segura con **Bcrypt**.
5. **4 Entidades Relacionadas:** `periodos`, `habitats`, `dietas` y `dinosaurios` (más tabla `usuarios`).
6. **Carga Inicial:** Realizada mediante scripts DDL (`schema.sql`) y DML (`seeds.sql`).

---

## 🚀 Instrucciones de Ejecución

### 1. Requisitos
* Python 3.10 o superior.

### 2. Instalación de dependencias
```bash
pip install -r backend/requirements.txt
```

### 3. Ejecución del Servidor
```bash
python -m uvicorn backend.app:app --reload --port 8000
```

Abre tu navegador en: **http://localhost:8000**

---

## 🔑 Credenciales de Acceso

| Usuario | Contraseña | Rol |
| :--- | :--- | :--- |
| **admin** | `admin123` | Administrador General |
| **profesor** | `uai2026` | Docente Titular |
| **alumno** | `dino123` | Estudiante Investigador |

---

## 🏛️ Estructura del Proyecto
```
dinomascota/
├── backend/
│   ├── database/
│   │   ├── schema.sql      # DDL de creación de tablas
│   │   ├── seeds.sql       # DML con 24 dinosaurios y usuarios
│   │   └── db.py           # Conexión SQLite y utilidades SQL
│   ├── static/
│   │   └── index.html      # Aplicación React 18 SPA integrada
│   ├── app.py              # Backend FastAPI con endpoints SQL y Auth
│   └── requirements.txt
├── frontend/               # Código fuente React modular
│   ├── src/
│   │   ├── components/
│   │   └── services/api.js
│   ├── package.json
│   └── vite.config.js
└── README.md
```
