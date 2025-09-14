# Obtener los datos
from io import StringIO

import pandas as pd
import requests

BASE_URL = (
    "https://www.transfermarkt.es/laliga/torschuetzenliste/wettbewerb/ES1/plus/0/galerie/0?saison_id={season}&page={page}"
)


def scrape_goleadores(season=2024, max_pages=10) -> pd.DataFrame:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36"
    }

    all_data = []
    for page in range(1, max_pages + 1):
        url = BASE_URL.format(season=season, page=page)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Saltando página {page}, status {response.status_code}")
            continue

        tables = pd.read_html(StringIO(response.text))
        if not tables or tables[1].empty:
            break

        df_page = tables[1]
        print(f"Scrapeada página {page}, filas: {len(df_page)//3}")
        all_data.append(df_page)

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

# '''
# tables[0] tiene las columnas: Elegir temporada, Posiciones detalladas, Grupo de edad
# tables[1] tiene las columnas: #, Jugadores, Nac. Edad, Club, PJ, GM

# Si transfermarkt no bloqueara los accesos con pandas, se haría así:
#     tables = pd.read_html(url)
#     df = tables[0]
#     return df
# '''
