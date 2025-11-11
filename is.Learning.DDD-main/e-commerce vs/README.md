E‑commerce Flask (IFTS9)
=======================

Proyecto demo de e‑commerce con Flask y MySQL. Implementa el flujo del diagrama: login, creación de pedido, selección de productos con verificación y descuento de stock, bucle de agregado, cálculo de total, validación de pedido vacío y confirmación.

Requisitos
- Python 3.11+
- MySQL en localhost (ajusta credenciales en `src/basededatos/config_bd.py`)

Instalación rápida (Windows PowerShell)
1) Crear entorno virtual
   - `python -m venv .venv`
   - Activar: `.venv\Scripts\Activate.ps1` (si bloquea scripts: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`)
2) Instalar dependencias
   - `pip install -r requirements.txt`
3) Ejecutar
   - `python src/app.py`
   - Abrir `http://127.0.0.1:5000`

Notas
- Variables sensibles: mueve `SECRET_KEY` y credenciales de DB a variables de entorno para producción.
- Descuento de stock: ocurre al agregar al pedido (atomicidad vía SQL). Si quieres reservar al confirmar, se puede ajustar.

