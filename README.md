# Urban Routes QA Project (Ejercicio 2)

## Descripción del proyecto

Este proyecto es una solución para la gestión y análisis de Urban routes, desarrollado como parte del Sprint 8. El objetivo principal es proporcionar herramientas para facilitar la validación de apps mediante pruebas automatizadas.

## Tecnologías y técnicas utilizadas

- **Python 3.13**: Lenguaje principal de desarrollo.
- **Pytest**: Framework utilizado para la ejecución de pruebas automatizadas.
- **Estructura modular**: Separación de la lógica en archivos como `main.py` y `data.py`.

## Instrucciones para ejecutar las pruebas

1. Instala las dependencias necesarias (si aplica):

   ```bash
   python3 -m pip install pytest
   ```

2. Actualiza la variable url de urban routes
   ```bash
   urban_routes_url = ''
   ```

3. Ejecuta las pruebas desde la terminal en el directorio raíz del proyecto:
   ```bash
   pytest main.py
   ```

Esto ejecutará todas las pruebas definidas en el proyecto y mostrará los resultados en la terminal.
