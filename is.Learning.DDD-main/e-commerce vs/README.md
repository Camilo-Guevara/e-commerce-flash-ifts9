# E-commerce Flask + MySQL — Guía del subproyecto

Demostración académica local: autenticación, catálogo, búsqueda, selección de productos, stock y confirmación de pedidos. **No es una tienda lista para producción.**

## Requisitos

- Python 3.11+.
- Servidor MySQL de desarrollo, con una base `ecommerce_db`.
- Esquema disponible en `src/basededatos/My_sql.sql.sql`.

## Ejecutar la versión actual de `main`

Abre PowerShell y entra en `is.Learning.DDD-main/e-commerce vs`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/app.py
```

Después abre `http://127.0.0.1:5000`.

La versión de `main` utiliza configuración MySQL local en `src/basededatos/config_bd.py`, contiene una clave fija de sesión Flask y tiene `debug=True`. **No emplear credenciales reales ni hacer despliegues públicos de esta versión.** Para utilizar la versión corregida, revisar el [PR #1 de seguridad](https://github.com/Camilo-Guevara/e-commerce-flash-ifts9/pull/1) y su configuración mediante variables de entorno; no está fusionado en `main`.

## Qué implementa el ejemplo

- Autenticación académica con consulta de usuarios.
- Búsqueda y catálogo de productos.
- Comprobación y descuento de inventario.
- Gestión de pedido en sesión, resumen y confirmación sin pasarela de pagos.

El descuento de stock sucede al agregar productos; es una simplificación académica que debe revisarse para casos reales de cancelación o concurrencia.

## Calidad y límites

En `main`, el workflow de GitHub Actions verifica únicamente sintaxis. El PR #1 incorpora pruebas de configuración Flask y MySQL con mocks. Aún faltan pruebas end-to-end con base de datos, controles CSRF, autorización y evaluación del algoritmo de almacenamiento de contraseñas.

## Relación con otros proyectos

Este trabajo es parte de mi formación como estudiante de **Análisis de Sistemas en el IFTS N.º 9**.

[Portafolio](https://camilo-guevara.github.io/) · [LinkedIn](https://www.linkedin.com/in/camilo-guevara-778a80385/) · [GitHub](https://github.com/Camilo-Guevara)
