import os
from typing import List

import pandas as pd

from src.processing import clean_goleadores, get_jugadores, calcular_distribucion
from src.scraping import scrape_goleadores


def obtener_datos(first_season: int, last_season: int) -> tuple[list, list]:
    global distribuciones, jugadores
    distribuciones, jugadores = [], []
    for year in range(first_season, last_season + 1):
        print(f"\nProcesando temporada {year}-{year+1}...")
        raw_df = scrape_goleadores(year, max_pages=20)
        clean_df = clean_goleadores(raw_df)
        jugadores_temp = get_jugadores(clean_df)
        jugadores.append(jugadores_temp)
        distribucion = calcular_distribucion(clean_df)
        distribuciones.append(distribucion)
    return distribuciones, jugadores


def export_list_to_csv(distribuciones: List[pd.DataFrame], name_prefix, first_season=2025, last_season=2026):
    os.makedirs("../data/processed", exist_ok=True)
    summary = pd.DataFrame()
    for i, distribucion in enumerate(distribuciones):
        temporada = f"{first_season + i}-{first_season + i + 1}"
        distribucion["Temporada"] = temporada
        summary = pd.concat([summary, distribucion], ignore_index=True)

    summary.to_csv(f"../data/processed/{name_prefix}_{first_season}_{last_season}.csv", index=False)