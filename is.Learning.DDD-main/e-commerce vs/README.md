# E-commerce académico (IFTS N.º 9): Flask + MySQL

Proyecto de práctica con catálogo, autenticación, carrito y flujo de pedidos. No está preparado para producción. El proyecto se ejecuta localmente.

## Requisitos

- Python 3.11 o superior
- MySQL local y base de datos `ecommerce_db` (esquema SQL en `src/basededatos/My_sql.sql.sql`)
- Variables de entorno configuradas; **no guardar contraseñas en el repositorio**

## Inicio rápido (Windows PowerShell)

Desde el directorio de este subproyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Reemplaza el usuario/contraseña por los de tu servidor local.
# Esta configuración solo dura mientras la terminal esté abierta.
$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "tu_usuario_local"
$env:MYSQL_PASSWORD = "tu_clave_local"
$env:MYSQL_DATABASE = "ecommerce_db"

.\.venv\Scripts\python.exe src/app.py
```

Visitar `http://127.0.0.1:5000`.

> `MYSQL_PASSWORD` puede estar vacío en ciertas instalaciones exclusivamente locales, pero debe definirse explícitamente. Para entornos compartidos o desplegados usa un usuario de permisos mínimos y contraseña fuerte.

> `FLASK_SECRET_KEY` es **obligatoria** y debe tener al menos 32 caracteres. Al modificarla se invalidan las sesiones existentes, lo cual es esperado tras retirar la clave fija publicada.

El archivo `.env.example` sirve solo como **referencia**: la aplicación no lo carga automáticamente. Nunca subas archivos `.env`, secretos reales ni contraseñas. No actives el modo debug en despliegues públicos.

## Pruebas de configuración

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q src
```

Estas pruebas usan mocks para validar la configuración de MySQL; no prueban la aplicación end-to-end ni la conexión a una base de datos real.

## Revisión de seguridad pendiente

- Verificar controles CSRF, permisos y manejo de sesiones antes de desplegar la aplicación.
- Verificar pruebas funcionales del flujo de pedidos con MySQL real.
- Evaluar un algoritmo de contraseñas diseñado para almacenamiento (Argon2id o bcrypt) y su migración.
- El repositorio también contiene un proyecto .NET de ejemplo, cuya configuración y documentación se revisarán por separado.
