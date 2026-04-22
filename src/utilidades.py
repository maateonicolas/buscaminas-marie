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
    """Convierte el tablero a índices fijos para el mapa de colores."""
    salida = []
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0

    for i in range(filas):
        nueva_fila = []
        for j in range(columnas):
            if mascara is not None and mascara[i][j] == 0:
                nueva_fila.append(10)  # Índice 10: Fuera de forma
            else:
                valor = tablero[i][j]
                if valor == -1:
                    nueva_fila.append(9)  # Índice 9: Mina
                else:
                    nueva_fila.append(valor)  # Índices 0 al 8: Números normales
        salida.append(nueva_fila)
    return salida

def guardar_visualizacion(
        tablero: Tablero,
        ruta_salida: str | Path,
        mascara: Optional[Mascara] = None,
        titulo: str = "Vista previa del tablero Buscaminas",
) -> Path:
    ruta = Path(ruta_salida)
    matriz = tablero_para_imagen(tablero, mascara=mascara)

    # PALETA DE COLORES EXACTA (Sincronizada con MARIE y el PDF)
    cmap = ListedColormap([
        "#CCCCCC",  # 0: Gris claro
        "#0000FF",  # 1: Azul
        "#00FF00",  # 2: Verde brillante
        "#FF0000",  # 3: Rojo
        "#0000AA",  # 4: Azul oscuro
        "#880000",  # 5: Rojo oscuro
        "#00FFFF",  # 6: Cian
        "#AA00FF",  # 7: Violeta
        "#FFFFFF",  # 8: Blanco
        "#000000",  # 9: Mina (Negro)
        "#222222",  # 10: Fuera de forma (Gris muy oscuro)
    ])

    plt.figure(figsize=(9, 9))
    # Fijar vmin=0 y vmax=10 garantiza que el índice coincida con el color correcto
    plt.imshow(matriz, cmap=cmap, vmin=0, vmax=10)

    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0

    # Dibujar los números/minas sobre las celdas
    for i in range(filas):
        for j in range(columnas):
            if mascara is not None and mascara[i][j] == 0:
                texto = ""
            else:
                valor = tablero[i][j]
                texto = "*" if valor == -1 else str(valor)

                # Ajustar contraste del texto para que se lea bien sobre fondos oscuros
                if valor in [-1, 1, 4, 5]:
                    color_texto = "white"
                else:
                    color_texto = "black"

                plt.text(j, i, texto, ha="center", va="center", fontsize=9, color=color_texto, fontweight='bold')

    plt.title(titulo, fontsize=14, pad=20)

    # Configurar los ejes (escala de números) en los 4 LADOS
    plt.xticks(range(columnas))
    plt.yticks(range(filas))
    plt.tick_params(
        top=True, bottom=True, left=True, right=True,
        labeltop=True, labelbottom=True, labelleft=True, labelright=True
    )

    # Dibujar la cuadrícula para separar las celdas
    plt.grid(True, which="both", color="#555555", linewidth=1)

    plt.tight_layout()
    plt.savefig(ruta, dpi=200, bbox_inches="tight")
    plt.close()

    return ruta