from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

Tablero = List[List[int]]
Mascara = List[List[int]]


def tablero_a_texto(tablero: Tablero, mascara: Optional[Mascara] = None) -> str:
    """
    Devuelve una representación legible del tablero.
    - mina -> *
    - fuera de forma -> .
    """
    lineas = []
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0

    for i in range(filas):
        partes = []
        for j in range(columnas):
            if mascara is not None and mascara[i][j] == 0:
                partes.append(".")
            else:
                valor = tablero[i][j]
                if valor == -1:
                    partes.append("*")
                else:
                    partes.append(str(valor))
        lineas.append(" ".join(partes))
    return "\n".join(lineas)


def mascara_a_texto(mascara: Mascara) -> str:
    """
    Representa la máscara en texto.
    1 = activa
    0 = fuera
    """
    return "\n".join(" ".join(str(v) for v in fila) for fila in mascara)


def imprimir_tablero(tablero: Tablero, mascara: Optional[Mascara] = None) -> None:
    print(tablero_a_texto(tablero, mascara=mascara))


def imprimir_mascara(mascara: Mascara) -> None:
    print(mascara_a_texto(mascara))


def tablero_para_imagen(tablero: Tablero, mascara: Optional[Mascara] = None) -> List[List[int]]:
    """
    Convierte el tablero a valores adecuados para visualización.

    Convención visual:
    - fuera de forma -> 10
    - mina (-1) -> 9
    - 0..8 se mantienen
    """
    salida: List[List[int]] = []
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0

    for i in range(filas):
        nueva_fila = []
        for j in range(columnas):
            if mascara is not None and mascara[i][j] == 0:
                nueva_fila.append(10)
            else:
                valor = tablero[i][j]
                if valor == -1:
                    nueva_fila.append(9)
                else:
                    nueva_fila.append(valor)
        salida.append(nueva_fila)
    return salida


def guardar_visualizacion(
        tablero: Tablero,
        ruta_salida: str | Path,
        mascara: Optional[Mascara] = None,
        titulo: str = "Vista previa del tablero Buscaminas",
) -> Path:
    """
    Guarda una imagen del tablero real y opcionalmente de la forma.
    """
    ruta = Path(ruta_salida)
    matriz = tablero_para_imagen(tablero, mascara=mascara)

    # 0..8, 9=mina, 10=fuera de forma
    cmap = ListedColormap([
        "#d9d9d9",  # 0
        "#0000ff",  # 1
        "#008000",  # 2
        "#ff0000",  # 3
        "#00008b",  # 4
        "#8b0000",  # 5
        "#00ced1",  # 6
        "#8a2be2",  # 7
        "#ffffff",  # 8
        "#000000",  # mina
        "#333333",  # fuera de forma
    ])

    plt.figure(figsize=(8, 8))
    plt.imshow(matriz, cmap=cmap, vmin=0, vmax=10)

    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0

    for i in range(filas):
        for j in range(columnas):
            if mascara is not None and mascara[i][j] == 0:
                texto = ""
                color_texto = "white"
            else:
                valor = tablero[i][j]
                texto = "*" if valor == -1 else str(valor)
                color_texto = "white" if valor == -1 else "black"

            plt.text(j, i, texto, ha="center", va="center", fontsize=8, color=color_texto)

    plt.title(titulo)
    plt.xticks(range(columnas))
    plt.yticks(range(filas))
    plt.grid(True, which="both", color="gray", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(ruta, dpi=200)
    plt.close()

    return ruta