from __future__ import annotations

import random
from typing import List, Optional, Sequence, Tuple

Tablero = List[List[int]]
Mascara = List[List[int]]
Coordenada = Tuple[int, int]


def crear_tablero(filas: int = 16, columnas: int = 16) -> Tablero:
    """
    Crea un tablero vacío inicializado con ceros.
    """
    return [[0 for _ in range(columnas)] for _ in range(filas)]


def validar_coordenada(fila: int, columna: int, filas: int, columnas: int) -> bool:
    """
    Verifica si una coordenada está dentro del tablero.
    """
    return 0 <= fila < filas and 0 <= columna < columnas


def vecinos_de(fila: int, columna: int, filas: int, columnas: int) -> List[Coordenada]:
    """
    Devuelve la lista de coordenadas vecinas válidas alrededor de una celda.
    """
    resultado: List[Coordenada] = []
    for df in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if df == 0 and dc == 0:
                continue
            nf, nc = fila + df, columna + dc
            if validar_coordenada(nf, nc, filas, columnas):
                resultado.append((nf, nc))
    return resultado


def colocar_minas(
        tablero: Tablero,
        minas: int,
        semilla: Optional[int] = None,
        minas_fijas: Optional[Sequence[Coordenada]] = None,
) -> Tablero:
    """
    Coloca minas en el tablero.
    Las minas se representan con -1.

    Puede funcionar de dos maneras:
    - minas_fijas: lista explícita de coordenadas
    - minas aleatorias con semilla opcional
    """
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0

    if minas_fijas is not None:
        usadas = set()
        for fila, columna in minas_fijas:
            if not validar_coordenada(fila, columna, filas, columnas):
                raise ValueError(f"Coordenada de mina fuera de rango: {(fila, columna)}")
            if (fila, columna) in usadas:
                continue
            tablero[fila][columna] = -1
            usadas.add((fila, columna))
        return tablero

    if minas < 0 or minas > filas * columnas:
        raise ValueError("La cantidad de minas es inválida para el tamaño del tablero.")

    rng = random.Random(semilla)
    colocadas = 0
    while colocadas < minas:
        fila = rng.randint(0, filas - 1)
        columna = rng.randint(0, columnas - 1)
        if tablero[fila][columna] != -1:
            tablero[fila][columna] = -1
            colocadas += 1

    return tablero


def calcular_vecinos(tablero: Tablero) -> Tablero:
    """
    Calcula el número de minas vecinas para cada celda no mina.
    Las minas se mantienen en -1.
    """
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0

    for fila in range(filas):
        for columna in range(columnas):
            if tablero[fila][columna] == -1:
                continue

            conteo = 0
            for nf, nc in vecinos_de(fila, columna, filas, columnas):
                if tablero[nf][nc] == -1:
                    conteo += 1

            tablero[fila][columna] = conteo

    return tablero


def contar_minas(tablero: Tablero) -> int:
    return sum(1 for fila in tablero for valor in fila if valor == -1)


def contar_celdas_seguras(tablero: Tablero) -> int:
    return sum(1 for fila in tablero for valor in fila if valor != -1)


def generar_tablero(
        filas: int = 16,
        columnas: int = 16,
        minas: int = 20,
        semilla: Optional[int] = None,
        minas_fijas: Optional[Sequence[Coordenada]] = None,
) -> Tablero:
    """
    Genera un tablero completo de Buscaminas:
    - crea tablero vacío
    - coloca minas
    - calcula vecinos
    """
    tablero = crear_tablero(filas, columnas)
    tablero = colocar_minas(tablero, minas=minas, semilla=semilla, minas_fijas=minas_fijas)
    tablero = calcular_vecinos(tablero)
    return tablero


# ============================================================
# MÁSCARAS DE FORMA
# ============================================================

def crear_mascara_llena(filas: int = 16, columnas: int = 16) -> Mascara:
    """
    Forma completa 16x16.
    1 = celda activa
    0 = celda fuera de la forma
    """
    return [[1 for _ in range(columnas)] for _ in range(filas)]


def crear_mascara_rombo(filas: int = 16, columnas: int = 16) -> Mascara:
    """
    Genera una forma de rombo centrada.
    """
    centro_f = filas // 2
    centro_c = columnas // 2
    radio = min(filas, columnas) // 2

    mascara = [[0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(filas):
        for j in range(columnas):
            if abs(i - centro_f) + abs(j - centro_c) <= radio:
                mascara[i][j] = 1
    return mascara


def crear_mascara_cruz(filas: int = 16, columnas: int = 16, grosor: int = 2) -> Mascara:
    """
    Genera una cruz centrada.
    """
    centro_f = filas // 2
    centro_c = columnas // 2
    mascara = [[0 for _ in range(columnas)] for _ in range(filas)]

    for i in range(filas):
        for j in range(columnas):
            if abs(i - centro_f) <= grosor or abs(j - centro_c) <= grosor:
                mascara[i][j] = 1
    return mascara


def crear_mascara_marco(filas: int = 16, columnas: int = 16, grosor: int = 2) -> Mascara:
    """
    Genera un marco rectangular.
    """
    mascara = [[0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(filas):
        for j in range(columnas):
            if (
                    i < grosor or i >= filas - grosor
                    or j < grosor or j >= columnas - grosor
            ):
                mascara[i][j] = 1
    return mascara


def crear_mascara_personalizada(
        activas: Sequence[Coordenada],
        filas: int = 16,
        columnas: int = 16,
) -> Mascara:
    """
    Genera una máscara manual a partir de coordenadas activas.
    """
    mascara = [[0 for _ in range(columnas)] for _ in range(filas)]
    for fila, columna in activas:
        if not validar_coordenada(fila, columna, filas, columnas):
            raise ValueError(f"Coordenada fuera de rango: {(fila, columna)}")
        mascara[fila][columna] = 1
    return mascara


def generar_mascara(
        forma: str = "llena",
        filas: int = 16,
        columnas: int = 16,
        grosor: int = 2,
        activas: Optional[Sequence[Coordenada]] = None,
) -> Mascara:
    """
    Genera la máscara según el nombre de forma.
    Formas soportadas:
    - llena
    - rombo
    - cruz
    - marco
    - personalizada
    """
    forma = forma.lower().strip()

    if forma == "llena":
        return crear_mascara_llena(filas, columnas)
    if forma == "rombo":
        return crear_mascara_rombo(filas, columnas)
    if forma == "cruz":
        return crear_mascara_cruz(filas, columnas, grosor=grosor)
    if forma == "marco":
        return crear_mascara_marco(filas, columnas, grosor=grosor)
    if forma == "personalizada":
        if activas is None:
            raise ValueError("Para forma 'personalizada' debes enviar 'activas'.")
        return crear_mascara_personalizada(activas, filas, columnas)

    raise ValueError(f"Forma no soportada: {forma}")


def aplicar_mascara_al_tablero(tablero: Tablero, mascara: Mascara) -> Tablero:
    """
    Devuelve una copia lógica del tablero solo para visualización o validación.
    No cambia TABLERO_REAL exportado a MARIE; solo marca como None lógico las
    celdas fuera de forma si se necesita trabajar con ellas externamente.
    Aquí devolvemos -99 en las celdas fuera de forma para ayudar en depuración.
    """
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0

    if len(mascara) != filas or len(mascara[0]) != columnas:
        raise ValueError("La máscara y el tablero deben tener el mismo tamaño.")

    salida = []
    for i in range(filas):
        fila_salida = []
        for j in range(columnas):
            if mascara[i][j] == 1:
                fila_salida.append(tablero[i][j])
            else:
                fila_salida.append(-99)
        salida.append(fila_salida)
    return salida