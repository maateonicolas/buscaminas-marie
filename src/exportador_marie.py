from __future__ import annotations

from pathlib import Path
from typing import List

Tablero = List[List[int]]
Mascara = List[List[int]]


def a_lineal(matriz: List[List[int]]) -> List[int]:
    """
    Convierte una matriz en una lista lineal por filas.
    """
    return [valor for fila in matriz for valor in fila]


def bloque_dec_desde_matriz(matriz: List[List[int]]) -> str:
    """
    Genera un bloque MARIE en formato DEC a partir de una matriz.
    """
    valores = a_lineal(matriz)
    lineas = [f"    DEC {valor}" for valor in valores]
    return "\n".join(lineas)


def bloque_tablero_real(tablero: Tablero) -> str:
    """
    Genera el bloque de memoria MARIE para TABLERO_REAL usando DEC.
    """
    return bloque_dec_desde_matriz(tablero)


def bloque_shape_preset(mascara: Mascara) -> str:
    """
    Genera el bloque de memoria MARIE para SHAPE_PRESET usando DEC.
    Los valores deben ser 0 o 1.
    """
    for fila in mascara:
        for valor in fila:
            if valor not in (0, 1):
                raise ValueError("La máscara solo puede contener 0 y 1.")
    return bloque_dec_desde_matriz(mascara)


def exportar_mem(tablero: Tablero, ruta_salida: str | Path) -> Path:
    """
    Exporta solo el mapa lineal del tablero real para revisión.
    """
    ruta = Path(ruta_salida)
    contenido = "TABLERO_REAL,\n" + bloque_tablero_real(tablero) + "\n"
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


def exportar_shape_mem(mascara: Mascara, ruta_salida: str | Path) -> Path:
    """
    Exporta solo la máscara de forma para revisión.
    """
    ruta = Path(ruta_salida)
    contenido = "SHAPE_PRESET,\n" + bloque_shape_preset(mascara) + "\n"
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


def insertar_en_template(
        template_str: str,
        tablero: Tablero,
        mascara: Mascara,
        marcador_real: str = "__TABLERO_REAL__",
        marcador_shape: str = "__SHAPE_PRESET__",
) -> str:
    """
    Inserta TABLERO_REAL y SHAPE_PRESET dentro de la plantilla .mas.
    """
    if marcador_real not in template_str:
        raise ValueError(f"No se encontró el marcador {marcador_real} en la plantilla.")
    if marcador_shape not in template_str:
        raise ValueError(f"No se encontró el marcador {marcador_shape} en la plantilla.")

    contenido = template_str.replace(marcador_real, bloque_tablero_real(tablero))
    contenido = contenido.replace(marcador_shape, bloque_shape_preset(mascara))
    return contenido


def exportar_mas(
        template_str: str,
        tablero: Tablero,
        mascara: Mascara,
        ruta_salida: str | Path,
        marcador_real: str = "__TABLERO_REAL__",
        marcador_shape: str = "__SHAPE_PRESET__",
) -> Path:
    """
    Genera el archivo .mas final listo para abrir en Marie.js.
    """
    ruta = Path(ruta_salida)
    contenido = insertar_en_template(
        template_str=template_str,
        tablero=tablero,
        mascara=mascara,
        marcador_real=marcador_real,
        marcador_shape=marcador_shape,
    )
    ruta.write_text(contenido, encoding="utf-8")
    return ruta