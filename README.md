# 🦖 DinoMascota - Tablero de Control Paleontológico
### Proyecto Final Cuatrimestral — Bases de Datos Aplicada (UAI)

Sistema web analítico e interactivo desarrollado en **Python (FastAPI) + SQLite + React 18 (Tailwind CSS & Chart.js)** para evaluar la viabilidad de adopción y convivencia doméstica de diversas especies de dinosaurios mediante consultas SQL directas, autenticación segura con **SHA-256 + Salt**, verificación por correo y toma de decisiones multinivel.

---

## 🎯 Cumplimiento de Consignas UAI

1. **Consultas SQL Puras:** Todas las métricas, KPIs, agrupaciones y desgloses se ejecutan mediante consultas SQL nativas sobre la base de datos `dinomascota.db` sin intermediación de ORMs.
2. **Drill-Down / Drill-Up (3 Niveles):**
   * **Nivel 1:** Períodos Geológicos (Triásico, Jurásico, Cretácico).
   * **Nivel 2:** Hábitats del período seleccionado (Bosque, Llanura, Pantano, Costero, Montaña, Ribereño).
   * **Nivel 3:** Especies con ficha técnica, biometría y botón de retorno (*Drill-Up*).
3. **Semaforización Visual (3 Estados):**
   * 🟢 **Verde (70-100 pts):** Situación Favorable / Mascota Viable (*Compsognathus*, *Microraptor*, *Yi qi*, *Dryosaurus*).
   * 🟡 **Amarillo (40-69 pts):** Advertencia / Requiere gran patio y adiestramiento (*Triceratops*, *Stegosaurus*, *Ankylosaurus*).
   * 🔴 **Rojo (0-39 pts):** Peligro Crítico / No recomendable (*Tyrannosaurus Rex*, *Spinosaurus*, *Giganotosaurus*).
4. **Sistema de Seguridad y Autenticación:**
   * Almacenamiento y validación con **Hashing SHA-256 + Salt criptográfico individual** (`secrets.token_hex`), con compatibilidad retroactiva para hashes Bcrypt.
   * **Registro de Usuarios con Persistencia:** Nuevas cuentas persisten directamente en SQLite.
   * **Verificación de Email:** Códigos de activación de 6 dígitos con expiración de 15 minutos (soporta SMTP real y Modo Simulación para evaluación docente offline).
   * **Recuperación de Contraseña:** Flujo completo de "¿Olvidaste tu contraseña?" con token temporal de un solo uso.
5. **Panel de Gestión de Usuarios (Rol Administrador):**
   * Pestaña exclusiva para usuarios con rol `administrador`.
   * Alta de usuarios directos, asignación dinámica de roles (`administrador`, `docente`, `investigador`, `alumno`) y eliminación con protección contra auto-borrado.
6. **5 Entidades Normalizadas (3FN):** `periodos`, `habitats`, `dietas`, `dinosaurios` y `usuarios` (supera el mínimo de 4).
7. **Inicialización Independiente de Base de Datos:** Script ejecutable `init_database.py` que crea el esquema DDL y pobla los datos DML de forma desacoplada del servidor web.
8. **Módulos Analíticos Avanzados:**
   * 🔍 **Buscador Dinámico Multifiltro:** Búsqueda en tiempo real por nombre/especie, período, hábitat, dieta y semáforo.
   * ⚔️ **Comparador Cara a Cara (Head-to-Head):** Comparación biométrica entre dos especies con cálculo diferencial y determinación automática del ganador.
   * 📊 **Gráficos Estadísticos con Chart.js:** Distribución por dieta, mascotabilidad media por era y Top 5 mejores/peores mascotas.

---

## 🚀 Instrucciones de Ejecución

### 1. Requisitos Previos
* Python 3.10 o superior instalado.

### 2. Instalar Dependencias
```powershell
pip install -r backend/requirements.txt
```

### 3. Paso 1: Inicializar la Base de Datos (Independiente del Backend)
Ejecuta el script de inicialización para crear `dinomascota.db` y cargar las 5 tablas maestras:
```powershell
python init_database.py
```
*(Opcional: agrega `--sync-images` si deseas predescargar todas las imágenes online de Jurassic Park Wiki y Wikipedia).*

### 4. Paso 2: Iniciar el Servidor Web (Backend FastAPI + Frontend SPA)
```powershell
python -m uvicorn backend.app:app --reload --port 8000
```

* **Aplicación Web:** Abre en tu navegador 👉 **[http://localhost:8000](http://localhost:8000)**
* **Documentación Interactiva Swagger:** 👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🔑 Credenciales de Acceso Iniciales

| Usuario | Contraseña | Rol | Acceso Especial |
| :--- | :--- | :--- | :--- |
| **admin** | `admin123` | `administrador` | **Gestión de Usuarios**, Tablero, Buscador y Comparador |
| **profesor** | `uai2026` | `docente` | Tablero, Buscador y Comparador |
| **alumno** | `dino123` | `alumno` | Tablero, Buscador y Comparador |

*(También puedes hacer clic en **"Crear Cuenta"** en la pantalla de inicio para registrar tu propio usuario y validarlo con el código que aparecerá en la consola del backend o en la alerta de prueba).*

---

## 🏛️ Estructura del Repositorio

```
Mascoteabilidad-de-dinosaurios/
├── init_database.py           # Script independiente de inicialización de SQLite (DDL + DML)
├── backend/
│   ├── app.py                 # Backend FastAPI con endpoints SQL, Auth y Admin
│   ├── database/
│   │   ├── schema.sql         # DDL: Definición de tablas, índices y llaves foráneas
│   │   ├── seeds.sql          # DML: Datos iniciales con 52 especies y usuarios
│   │   ├── dinomascota.db     # Base de datos SQLite creada y operativa
│   │   └── db.py              # Módulo de conexión SQLite pura y utilitarios
│   ├── services/
│   │   ├── security.py        # Hashing SHA-256 + Salt criptográfico y validación
│   │   └── mailer.py          # Envío de correo SMTP y Simulador de Email docente
│   ├── static/
│   │   └── index.html         # Frontend SPA React 18 integrado (Tailwind CSS + Chart.js)
│   └── requirements.txt       # Dependencias del proyecto
└── README.md
```
