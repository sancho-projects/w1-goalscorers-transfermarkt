from typing import List
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd


def plot_distribucion(distribuciones: List[pd.DataFrame], min_goles=10, first_season=2010, larst_season=2025):
    plt.figure(figsize=(10, 6))
    for i, distribucion in enumerate(distribuciones):
        plt.plot(distribucion["Goles"],
                 distribucion["Num_Jugadores"],
                 marker='o',
                 alpha=0.5,
                 label=f"{first_season + i}-{first_season + i + 1}")
    plt.xlabel("Número de goles")
    plt.ylabel("Cantidad de jugadores")
    plt.title(
        f"Distribución de goleadores en LaLiga desde {first_season} hasta {larst_season}, con {min_goles} o más goles")
    plt.legend(title="Temporadas")
    plt.grid(True)
    plt.xlim(left=min_goles)
    plt.show()


def plot_distribucion_acumulada(distribuciones: List[pd.DataFrame], min_goles=10, first_season=2010, larst_season=2025):
    acumulado = pd.DataFrame()
    for i, distribucion in enumerate(distribuciones):
        temporada = f"{first_season + i}-{first_season + i + 1}"
        if acumulado.empty:
            acumulado = (distribucion
                         .set_index("Goles")[["Num_Jugadores"]]
                         .rename(columns={"Num_Jugadores": temporada}))
        else:
            acumulado = acumulado.join(distribucion
                                       .set_index("Goles")[["Num_Jugadores"]]
                                       .rename(columns={"Num_Jugadores": temporada})
                                       , how="outer")

    acumulado = acumulado.fillna(0).sort_index()
    acumulado.plot.area(alpha=0.7, figsize=(10, 6), colormap="viridis")

    plt.xlabel("Número de goles")
    plt.ylabel("Cantidad de jugadores")
    plt.title(
        f"Distribución acumulada de goleadores en LaLiga desde {first_season} hasta {larst_season}, con {min_goles} o más goles")
    plt.legend(title="Temporadas")
    plt.grid(True)
    plt.xlim(left=min_goles)
    plt.show()



def plot_distribucion_acumulada_interactiva(distribuciones: List[pd.DataFrame],
                                            jugadores: List[pd.DataFrame],
                                            min_goles=10,
                                            first_season=2010,
                                            larst_season=2025):
        acumulado = pd.DataFrame()
        for i, (distribucion, jugador) in enumerate(zip(distribuciones, jugadores)):
            temporada = f"{first_season + i}-{first_season + i + 1}"
            distribucion = distribucion.copy()
            distribucion["Temporada"] = temporada

            distribucion = distribucion.merge(
                jugador
                .groupby("Goles")["Jugadores"]
                .apply(list)
                .reset_index(),
                on="Goles", how="left"
            )

            distribucion["Jugadores"] = distribucion["Jugadores"].apply(
                lambda jugadores: ",\n".join(jugadores) if isinstance(jugadores, list) else ""
            )

            if acumulado.empty:
                acumulado = distribucion
            else:
                acumulado = pd.concat([acumulado, distribucion], ignore_index=True)

        fig = px.area(acumulado,
                      x="Goles",
                      y="Num_Jugadores",
                      color="Temporada",
                      markers='o',
                      hover_data=["Jugadores"],
                      title=f"Distribución acumulada de goleadores en LaLiga desde {first_season} hasta {larst_season}, con {min_goles} o más goles")

        max_goles = int(acumulado["Goles"].max())
        max_jug = int(acumulado[acumulado["Goles"] >= min_goles]["Num_Jugadores"].max())

        fig.update_layout(xaxis_title="Número de goles",
                          yaxis_title="Cantidad de jugadores",
                          xaxis=dict(
                              range=[min_goles, max_goles + 1],
                              tickvals=list(range(min_goles, max_goles + 1, 2))
                          ),
                          yaxis=dict(
                              range=[0, max_jug + 1],
                              tickvals=list(range(0, max_jug + 1, 5))
                          ),
                          legend_title="Temporadas")
        fig.show()