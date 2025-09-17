# Limpiar y calcular
import pandas as pd


def clean_goleadores(df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={"Unnamed: 6": "Goles"})
        df = df.drop(columns=["Nac.", "Club", "Unnamed: 5"], errors="ignore")
        # Renombrar futbolistas: "1. Karim Benzema Delantero Centro" -> "Karim Benzema"
        df.loc[df["Goles"].notna(), "Jugadores"] = df.loc[df["Goles"].notna()].index.map(
            lambda i: df.at[i + 1, "Jugadores"]
            if i + 1 in df.index
            else None)

        df = df[df["Goles"].notna()]
        df["Goles"] = pd.to_numeric(df["Goles"], errors="coerce").astype("Int64")
        return df

def calcular_distribucion(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("Goles").size().reset_index(name="Num_Jugadores")


def get_jugadores(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by="Goles", ascending=True)[["Jugadores", "Goles"]].copy()

