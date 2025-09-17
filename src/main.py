import tkinter as tk
from tkinter import messagebox
from visualization import plot_distribucion, plot_distribucion_acumulada, plot_distribucion_acumulada_interactiva
from data.config import first_season, last_season, min_goles
from control import obtener_datos, export_list_to_csv

# Variables globales
distribuciones = []
jugadores = []

def on_scraping_click():
    global distribuciones, jugadores, first_season, last_season, min_goles
    try:
        first_season = int(entry_first_season.get())
        last_season = int(entry_last_season.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos.")
        return

    distribuciones, jugadores = obtener_datos(first_season, last_season)
    if distribuciones and jugadores:
        btn_exportar_csv.config(state=tk.NORMAL)
        btn_visualizar_distribucion.config(state=tk.NORMAL)
        btn_visualizar_acumulada.config(state=tk.NORMAL)
        btn_visualizar_interactiva.config(state=tk.NORMAL)
        messagebox.showinfo("Scraping", "Scraping completado exitosamente.")
def visualizar_distribucion():
    if distribuciones:
        min_goles = int(entry_min_goles.get())
        plot_distribucion(distribuciones, min_goles, first_season, last_season)
    else:
        messagebox.showerror("Error", "Primero realiza el scraping.")

def visualizar_distribucion_acumulada():
    if distribuciones:
        min_goles = int(entry_min_goles.get())
        plot_distribucion_acumulada(distribuciones, min_goles, first_season, last_season)
    else:
        messagebox.showerror("Error", "Primero realiza el scraping.")

def visualizar_distribucion_acumulada_interactiva():
    if distribuciones and jugadores:
        min_goles = int(entry_min_goles.get())
        plot_distribucion_acumulada_interactiva(distribuciones, jugadores, min_goles, first_season, last_season)
    else:
        messagebox.showerror("Error", "Primero realiza el scraping.")

def exportar_csv():
    if distribuciones and jugadores:
        export_list_to_csv(distribuciones, "distribucion_goles", first_season, last_season)
        export_list_to_csv(jugadores, "goleadores", first_season, last_season)
        messagebox.showinfo("Exportar", "Datos exportados a CSV correctamente.")
    else:
        messagebox.showerror("Error", "Primero realiza el scraping.")

# Crear la ventana principal
root = tk.Tk()
root.title("Goleadores históricos en LaLiga EA Sports")

# Título y fuente
tk.Label(root, text="Goleadores históricos en LaLiga EA Sports", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(root, text="Fuente: Transfermarkt", font=("Arial", 10, "italic")).grid(row=1, column=0, columnspan=2, pady=5)

# Botones de scraping y exportar
btn_scraping = tk.Button(root, text="REALIZAR SCRAPING", command=on_scraping_click, bg="lightblue", font=("Arial", 12))
btn_scraping.grid(row=2, column=0, padx=10, pady=10)

btn_exportar_csv = tk.Button(root, text="EXPORTAR A CSV", command=exportar_csv, bg="lightgreen", font=("Arial", 12), state=tk.DISABLED)
btn_exportar_csv.grid(row=2, column=1, padx=10, pady=10)

# Entradas para configuración
tk.Label(root, text="Primera Temporada:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_first_season = tk.Entry(root, font=("Arial", 12))
entry_first_season.insert(0, str(first_season))
entry_first_season.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Última Temporada:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_last_season = tk.Entry(root, font=("Arial", 12))
entry_last_season.insert(0, str(last_season))
entry_last_season.grid(row=4, column=1, padx=10, pady=5)

# Sección de visualización
tk.Label(root, text="VISUALIZAR CON PYTHON:", font=("Arial", 14, "bold")).grid(row=5, column=0, columnspan=2, pady=10)

btn_visualizar_distribucion = tk.Button(root, text="Distribución de goles", command=visualizar_distribucion, font=("Arial", 12), state=tk.DISABLED)
btn_visualizar_distribucion.grid(row=6, column=0, columnspan=2, pady=5)

btn_visualizar_acumulada = tk.Button(root, text="Distribución acumulada", command=visualizar_distribucion_acumulada, font=("Arial", 12), state=tk.DISABLED)
btn_visualizar_acumulada.grid(row=7, column=0, columnspan=2, pady=5)

btn_visualizar_interactiva = tk.Button(root, text="Distribución interactiva", command=visualizar_distribucion_acumulada_interactiva, font=("Arial", 12), state=tk.DISABLED)
btn_visualizar_interactiva.grid(row=8, column=0, columnspan=2, pady=5)

# Entrada para mínimo de goles
tk.Label(root, text="Mínimo de goles para que aparezcan:", font=("Arial", 12)).grid(row=9, column=0, padx=10, pady=5, sticky="e")
entry_min_goles = tk.Entry(root, font=("Arial", 12))
entry_min_goles.insert(0, str(min_goles))
entry_min_goles.grid(row=9, column=1, padx=10, pady=5)

# Ejecutar la aplicación
root.mainloop()