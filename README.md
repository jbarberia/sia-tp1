# Trabajo Práctico 1: Métodos de Búsqueda

Este repositorio contiene el código fuente y la documentación del primer trabajo práctico de la asignatura Sistemas Inteligentes Aplicados. El objetivo principal es implementar y analizar diferentes métodos de búsqueda aplicados al juego Sokoban.

## Descripción del Proyecto

El proyecto se centra en la resolución de tableros del juego Sokoban utilizando diversos algoritmos de búsqueda. Sokoban es un juego de lógica en el que un jugador debe empujar cajas hasta ubicarlas en posiciones específicas dentro de un almacén, enfrentándose a restricciones de movimiento y espacio.

## Estructura del Repositorio

- `config/`: Archivos de configuración utilizados en el proyecto.
- `docs/`: Consignas y respuestros asociadas al TP.
- `src/`: Código fuente principal de las implementaciones.
- `test/`: Pruebas y casos de prueba para las implementaciones.
- `algoritmos_de_busqueda.ipynb`: Cuaderno de Jupyter que contiene ejemplos y análisis de los algoritmos de búsqueda implementados.

## Presentación
> ⚠️ Tienen acceso como editor al [Link a la presentación](https://docs.google.com/presentation/d/1waLDKe33UqgkzqL2cKOTyAEzE2uUm4ZlU1D-ub639Ks/edit?usp=sharing)


## Algoritmos Implementados

Se han implementado los siguientes algoritmos de búsqueda:

- Búsqueda en Anchura (BFS)
- Búsqueda en Profundidad (DFS)
- Búsqueda Greedy
- Búsqueda A*

## Correr demostración
Para correr la demostración del TP usar el script de la interfaz gráfica creada en pygame.

```bash
python src/interfaz.py config.py
```

## Recursos Adicionales

Los tableros del sokoban se pueden descargar de [game-sokoban](http://www.game-sokoban.com/).
