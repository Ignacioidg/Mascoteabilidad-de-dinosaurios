# 🦖 DinoMascota Dashboard — Walkthrough de Nuevas Funcionalidades

Tablero de Control y Análisis Paleontológico desarrollado para **Bases de Datos Aplicada — UAI (Ingeniería en Sistemas Informáticos)**.

---

## 🎯 Resumen de Cambios Implementados

### 1. Inicialización Desacoplada de Base de Datos
* **Script Independiente:** Se creó [`init_database.py`](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/init_database.py) en la raíz del proyecto.
* **Desacople del Backend:** Se removió la ejecución automática de `init_db()` al importar [`backend/app.py`](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/app.py). Ahora el backend valida que la base de datos exista e informa un error claro en caso contrario.
* **Esquema y Seeds Actualizados:** [`schema.sql`](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/database/schema.sql) y [`seeds.sql`](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/database/seeds.sql) incorporan soporte completo para emails únicos, tokens de verificación, tokens de recuperación y salts criptográficos.

### 2. Hashing SHA-256 con Salt Criptográfico
* **Módulo de Seguridad:** Se desarrolló [`backend/services/security.py`](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/services/security.py) implementando:
  $$\text{hash} = \text{SHA-256}(\text{salt} + \text{password})$$
  con `salt = secrets.token_hex(16)` único para cada usuario y almacenamiento en formato `sha256$<salt>$<hash_hex>`.
* **Compatibilidad Retroactiva:** La función `verify_password()` soporta tanto el nuevo estándar SHA-256 como hashes Bcrypt preexistentes.

### 3. Sistema Completo de Verificación por Email y Recuperación de Claves
* **Módulo de Mensajería:** [`backend/services/mailer.py`](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/services/mailer.py) provee soporte híbrido:
  1. **SMTP Real:** Si se configuran variables de entorno (`SMTP_HOST`, `SMTP_USER`, etc.).
  2. **Modo Simulación Académico (Offline):** Imprime una tarjeta formateada en la consola del backend con el código de 6 dígitos y lo retorna en la respuesta de desarrollo para pruebas inmediatas.
* **Flujos Integrados:**
  * **Registro:** `/api/auth/register` crea la cuenta con estado `verificado = 0` y despacha el código con vigencia de 15 minutos.
  * **Verificación:** `/api/auth/verify-email` activa la cuenta con el código recibido.
  * **Reenvío:** `/api/auth/resend-code` genera y reenvía un nuevo código si el anterior expiró.
  * **Recuperación ("¿Olvidaste tu contraseña?"):** `/api/auth/forgot-password` y `/api/auth/reset-password` permiten restaurar el acceso con un código temporal y actualizar el hash en SQLite.

### 4. Panel de Gestión de Usuarios para el Administrador
* **Endpoints Administrativos (`/api/admin/*`):**
  * `GET /api/admin/users`: Listado de todos los usuarios con roles y estados.
  * `POST /api/admin/users`: Creación directa de usuarios por el administrador.
  * `PUT /api/admin/users/{user_id}/role`: Modificación del rol (`administrador`, `docente`, `investigador`, `alumno`).
  * `DELETE /api/admin/users/{user_id}`: Eliminación de cuentas con protección contra auto-eliminación y preservación del último administrador.
* **Interfaz de Usuario:** Nueva pestaña interactiva **"👥 Gestión de Usuarios"** en [`backend/static/index.html`](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/static/index.html) visible exclusivamente para usuarios con rol `administrador`.

---

## 🧪 Pruebas y Resultados de Validación

| Componente | Prueba Realizada | Resultado |
| :--- | :--- | :---: |
| **Inicialización** | Ejecución de `python init_database.py` en consola | ✅ 5 tablas creadas y pobladas (52 dinos, 3 usuarios) |
| **Seguridad** | Hasheo y verificación de SHA-256 + Salt y legacy Bcrypt | ✅ 100% verificado |
| **Registro** | Creación de usuario y bloqueo de login antes de verificar | ✅ HTTP 403 Bloqueado correctamente |
| **Verificación** | Activación con código de 6 dígitos y reintento de login | ✅ Cuenta activada y login exitoso |
| **Recuperación** | Solicitud de código de reseteo y cambio de clave | ✅ Clave actualizada y login con nueva clave verificado |
| **Gestión Admin** | Listado, cambio de rol a `investigador` y borrado de usuario | ✅ Cambios persistidos en SQLite |
| **Servido Web** | Integración HTTP completa (FastAPI + React SPA) en puerto 8001 | ✅ HTTP 200 OK en frontend y endpoints |

---

## 🚀 Guía Rápida de Uso

1. **Inicializar la base de datos:**
```powershell
python init_database.py
```

2. **Iniciar el servidor:**
```powershell
python -m uvicorn backend.app:app --reload --port 8000
```

3. **Ingresar al navegador:**
👉 **[http://localhost:8000](http://localhost:8000)** (con usuario `admin` / `admin123` para ver la pestaña de **Gestión de Usuarios**).
