# Plan de Implementación: Gestión de Usuarios, Hashing SHA-256, Verificación por Email y Desacople de Base de Datos 🦖

Este plan aborda los nuevos requerimientos solicitados para el proyecto **DinoMascota Dashboard** (Bases de Datos Aplicada — UAI):
1. **Desacoplar la inicialización de la Base de Datos del Backend** mediante un script ejecutable independiente.
2. **Registro de Usuarios con Persistencia en BD**.
3. **Hasheo de Contraseñas con SHA-256 + Salt** (y compatibilidad con Bcrypt existente).
4. **Flujo completo de Verificación por Email y Recuperación de Contraseña** ("¿Olvidaste tu contraseña?"), con soporte para SMTP real y modo simulado para evaluación docente offline.
5. **Panel de Gestión de Usuarios para el Administrador** (alta, cambio de roles y eliminación de usuarios con control de seguridad).

---

## 📌 Decisiones de Diseño y Propuestas Técnicas

### 1. Inicialización de Base de Datos y Aclaración MySQL vs SQLite
> [!NOTE]
> **Aclaración sobre la Base de Datos:**
> Actualmente el proyecto corre con **SQLite** (`backend/database/dinomascota.db`), lo que permite que funcione en cualquier computadora sin necesidad de instalar servicios externos como MySQL Server o XAMPP. Los archivos `schema.sql` y `seeds.sql` son scripts SQL estándar.
> 
> * **Separación implementada:** Se creará el script `init_database.py` en la raíz del proyecto. El backend en `backend/app.py` **ya no ejecutará `init_db()` automáticamente** al arrancar. Si el backend arranca y no encuentra la base de datos inicializada, mostrará un mensaje amigable indicando que debe ejecutarse `python init_database.py` primero.
> * **Script compatible con MySQL:** Además, dejaremos disponible `backend/database/schema_mysql.sql` por si en la cátedra les solicitan importar las tablas en MySQL Workbench o phpMyAdmin.

### 2. Método de Hasheo: SHA-256 con Salt
> [!IMPORTANT]
> **Propuesta de Hasheo de Contraseñas:**
> El usuario solicitó **SHA-256**. En seguridad informática, el SHA-256 plano (sin salt) es vulnerable a ataques de tablas *rainbow*.
> Por eso implementaremos **SHA-256 con Salt Criptográfico Aleatorio** (`secrets.token_hex(16)`):
> $$\text{hash} = \text{SHA256}(\text{salt} + \text{contraseña})$$
> El formato almacenado en base de datos será `sha256$<salt>$<hash_hex>`.
> Además, mantendremos compatibilidad hacia atrás con los hashes Bcrypt existentes de los usuarios de prueba (`admin`, `profesor`, `alumno`).

### 3. Verificación por Email y Recuperación de Contraseña
> [!TIP]
> **Modo Híbrido: SMTP Real + Modo Simulación Docente:**
> Para que el profesor o evaluador de la UAI pueda probar el sistema en su máquina local sin necesidad de configurar credenciales de correo o tener conexión a internet:
> 1. **Envío Real:** Si se configuran variables de entorno SMTP (Gmail, Outlook, etc.), envía un correo HTML con el código de 6 dígitos.
> 2. **Modo Simulación / Dev:** Siempre imprimirá el código en la consola del backend con un recuadro vistoso (`[CÓDIGO DE VERIFICACIÓN: 849201]`) y lo informará en la respuesta de desarrollo del backend para que se pueda autocompletar o probar al instante en la pantalla.

---

## 📂 Archivos y Cambios Propuestos

### Componente 1: Base de Datos y Scripts de Inicialización
* **[NEW] `init_database.py`**: Script ejecutable de consola en la raíz para inicializar/resetear `dinomascota.db`, ejecutar `schema.sql`, cargar `seeds.sql` y verificar integridad de tablas.
* **[MODIFY] [backend/database/schema.sql](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/database/schema.sql)**:
  * Modificar tabla `usuarios`:
    * `email VARCHAR(100) UNIQUE NOT NULL`
    * `salt VARCHAR(64)`
    * `verificado INTEGER DEFAULT 0` (0: pendiente, 1: activo)
    * `codigo_verificacion VARCHAR(10)`
    * `codigo_expiracion TIMESTAMP`
    * `token_recuperacion VARCHAR(100)`
    * `token_expiracion TIMESTAMP`
* **[MODIFY] [backend/database/seeds.sql](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/database/seeds.sql)**:
  * Actualizar inserción inicial de usuarios con emails (`admin@dinomascota.uai`, `profesor@uai.edu.ar`, `alumno@alumnos.uai.edu.ar`), estado `verificado = 1`, y passwords hasheadas en SHA-256 + salt.
* **[MODIFY] [backend/database/db.py](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/database/db.py)**:
  * Desactivar la sincronización automática o llamadas bloqueantes en importación.

---

### Componente 2: Servicios de Backend (Seguridad y Correo)
* **[NEW] `backend/services/security.py`**:
  * Funciones `hash_password_sha256(password: str) -> (hash_str, salt)`
  * Función `verify_password(plain_password: str, stored_hash: str, salt: Optional[str]) -> bool` (soporta tanto formato `sha256` como `bcrypt`).
* **[NEW] `backend/services/mailer.py`**:
  * Función `send_email_code(to_email: str, subject: str, code: str, purpose: str) -> bool`
  * Detección de configuración SMTP vs Modo Simulación en terminal / log.

---

### Componente 3: Endpoints en FastAPI ([backend/app.py](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/app.py))
* **Remover** `init_db()` automático de la línea 20; validar existencia de la BD al recibir peticiones.
* **Nuevos endpoints de Autenticación (`/api/auth/*`):**
  * `POST /api/auth/register`: Valida usuario, email único, coincidencia de contraseñas, genera salt + SHA-256, crea usuario con `verificado = 0` y despacha código de 6 dígitos.
  * `POST /api/auth/verify-email`: Recibe email y código; si coincide y no expiró, setea `verificado = 1`.
  * `POST /api/auth/resend-code`: Genera y reenvía nuevo código de verificación.
  * `POST /api/auth/forgot-password`: Solicita reseteo para un email, genera código/token temporal.
  * `POST /api/auth/reset-password`: Valida código de recuperación y actualiza la contraseña con nuevo salt y hash SHA-256.
  * `POST /api/auth/login`: Actualizado para verificar `verificado == 1` y validar con `verify_password`.
* **Nuevos endpoints de Administración (`/api/admin/*`):**
  * `GET /api/admin/users`: Listado de usuarios con roles, emails y estado de verificación.
  * `POST /api/admin/users`: Creación directa de usuarios por el administrador (con opción de asignar rol y verificar automáticamente).
  * `PUT /api/admin/users/{user_id}/role`: Modificación del rol (`administrador`, `docente`, `investigador`, `alumno`).
  * `DELETE /api/admin/users/{user_id}`: Eliminación de usuario (con validación para no auto-eliminarse ni borrar al último administrador).

---

### Componente 4: Frontend SPA ([backend/static/index.html](file:///c:/Users/Navegador/Desktop/Tlabajo/Mascoteabilidad-de-dinosaurios/backend/static/index.html))
* **Vistas de Autenticación:**
  * Pestaña/Botón *"Crear Cuenta"* en la pantalla de Login con validación en vivo de contraseñas coincidentes y formato de email.
  * Modal/Pantalla de *"Verificación de Código"* con cuenta regresiva para reenviar código.
  * Enlace *"¿Olvidaste tu contraseña?"* con flujo paso a paso de recuperación.
  * Alerta interactiva que muestra el código simulado en caso de estar en modo local/dev.
* **Módulo de Gestión de Usuarios (`AdminPanel`):**
  * Solo visible en la barra de navegación si el usuario logueado tiene rol `administrador`.
  * Tabla interactiva con búsqueda de usuarios, insignias de rol y estado.
  * Selector de roles dinámico (`Dropdown`).
  * Modal de alta de usuario administrativo.
  * Confirmación de borrado de usuario con salvaguardas de seguridad.

---

## 🧪 Plan de Verificación

### 1. Verificación del Desacople de BD
* Eliminar `dinomascota.db` temporalmente y levantar `uvicorn backend.app:app`. Confirmar que responde con aviso para ejecutar `python init_database.py`.
* Ejecutar `python init_database.py` y verificar que genera la base de datos completa con las 5 tablas y usuarios iniciales.

### 2. Verificación de Seguridad y Hashing
* Crear un nuevo usuario por registro y comprobar en la tabla `usuarios` que la contraseña está almacenada con formato `sha256$<salt>$<hash>`.
* Iniciar sesión con contraseñas originales (`admin123`, `uai2026`) y con la nueva cuenta creada con SHA-256.

### 3. Verificación de Flujo de Email y Recuperación
* Registrar nuevo usuario `testdino@uai.edu.ar`.
* Verificar que no permite iniciar sesión hasta que se valide el código de 6 dígitos.
* Ingresar código y activar cuenta; verificar login exitoso.
* Probar el flujo de "¿Olvidaste tu contraseña?" cambiando la clave y logueando con la nueva.

### 4. Verificación del Panel de Administración
* Iniciar sesión como `admin`.
* Navegar a la pestaña "Gestión de Usuarios".
* Cambiar el rol del usuario de prueba de `alumno` a `investigador` y validar persistencia en base de datos.
* Probar eliminar un usuario de prueba.
* Intentar eliminar el usuario `admin` propio y verificar que el sistema lo rechaza por seguridad.
