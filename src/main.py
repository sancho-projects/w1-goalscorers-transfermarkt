from scraping import scrape_goleadores
from processing import clean_goleadores, calcular_distribucion, get_jugadores
from visualization import plot_distribucion, plot_distribucion_acumulada, plot_distribucion_acumulada_interactiva

FIRST_SEASON = 2010
LAST_SEASON = 2024

if __name__ == "__main__":
    distribuciones, jugadores = [], []

    for year in range(FIRST_SEASON, LAST_SEASON + 1):
        print(f"\nProcesando temporada {year}-{year+1}...")
        raw_df = scrape_goleadores(year, max_pages=12)
        clean_df = clean_goleadores(raw_df)

        jugadores_temp = get_jugadores(clean_df)
        jugadores.append(jugadores_temp)
        distribucion = calcular_distribucion(clean_df)
        distribuciones.append(distribucion)

    plot_distribucion_acumulada_interactiva(distribuciones, jugadores, FIRST_SEASON, LAST_SEASON)
    # plot_distribucion(distribuciones, FIRST_SEASON, LAST_SEASON)
    # plot_distribucion_acumulada(distribuciones, FIRST_SEASON, LAST_SEASON)
