e-commerce-flash-ifts9
======================

Este repositorio contiene la carpeta del proyecto de ejemplo de e‑commerce con Flask y MySQL:

- Código principal: `is.Learning.DDD-main/e-commerce vs/`

Características
- Catálogo de productos con búsqueda
- Login con verificación de credenciales (hash con salt)
- Flujo de pedido según diagrama: agregar productos con validación/descarga de stock, resumen, validación de pedido vacío y confirmación

Cómo ejecutar rápidamente (Windows PowerShell)
1) Crear entorno: `python -m venv .venv` y activar `.venv\Scripts\Activate.ps1`
2) Instalar deps: `pip install -r "is.Learning.DDD-main/e-commerce vs/requirements.txt"`
3) Configurar MySQL en `is.Learning.DDD-main/e-commerce vs/src/basededatos/config_bd.py`
4) Ejecutar: `python "is.Learning.DDD-main/e-commerce vs/src/app.py"`

CI
- Workflow en `.github/workflows/ci.yml` instala dependencias y compila el código para verificar sintaxis.

