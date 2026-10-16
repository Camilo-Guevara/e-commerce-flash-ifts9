# E-commerce académico — Flask y MySQL

**Proyecto de aprendizaje | Python · Flask · MySQL · HTML/CSS**

[Perfil profesional](https://github.com/Camilo-Guevara) · [Portafolio](https://camilo-guevara.github.io/) · [LinkedIn](https://www.linkedin.com/in/camilo-guevara-778a80385/)

## Descripción

Proyecto académico del IFTS N.º 9 para practicar desarrollo web y persistencia de datos. Incluye catálogo, búsqueda de productos, autenticación y flujo de pedidos con comprobación y descuento de stock.

**Estado:** demostración académica local, sin pagos reales ni disponibilidad verificada en producción. La seguridad se está revisando en el [PR #1](https://github.com/Camilo-Guevara/e-commerce-flash-ifts9/pull/1).

## Tecnologías y estructura

- **Python + Flask:** rutas y lógica de aplicación.
- **MySQL:** almacenamiento de usuarios, productos y pedidos.
- **HTML/CSS:** interfaz del catálogo.
- **GitHub Actions:** verificación automatizada de sintaxis en `main`.
- **Carpeta del e-commerce:** [`is.Learning.DDD-main/e-commerce vs/`](is.Learning.DDD-main/e-commerce%20vs/).
- **Guía de instalación:** [README del subproyecto](is.Learning.DDD-main/e-commerce%20vs/README.md).

> El repositorio también contiene una estructura de ejemplo .NET/CarRental. No debe confundirse con la aplicación Flask; se recomienda separar ambos trabajos en repositorios distintos después de revisar su procedencia y configuración.

## Funcionalidades académicas

- Listar y buscar productos.
- Registrar e iniciar sesión con credenciales.
- Agregar productos a pedidos tras comprobar stock.
- Calcular totales, mostrar resumen y confirmar pedidos.
- Practicar consultas SQL parametrizadas.

Las funcionalidades descritas están presentes en el código, pero **no se han verificado aquí con pruebas de integración contra MySQL real**.

## Ejecución local

Usa Python 3.11+ y MySQL. Consulta el [README del e-commerce](is.Learning.DDD-main/e-commerce%20vs/README.md) antes de instalar.

**Importante:** la rama `main` mantiene una configuración de desarrollo con secretos codificados en el código. No utilices credenciales reales ni despliegues esta rama públicamente. Las mejoras para externalizar secretos y ejecutar pruebas están preparadas en el PR #1, **todavía sin fusionar**.

## Pruebas y seguridad

- En `main`: GitHub Actions instala dependencias y ejecuta una comprobación de sintaxis Python; esto **no equivale** a aprobar pruebas funcionales.
- En el **PR #1 de seguridad**: hay pruebas automatizadas de configuración Flask y MySQL, sin integración funcional real.
- Pendiente: validación con MySQL de prueba, CSRF, permisos, sesiones, migración de hashes de contraseña y revisión de la configuración del ejemplo .NET.

## Contexto académico

Proyecto vinculado a mi formación en **Análisis de Sistemas (IFTS N.º 9)**. La documentación se presenta como evidencia de aprendizaje, sin atribuir experiencia laboral o funcionalidades no comprobadas.
