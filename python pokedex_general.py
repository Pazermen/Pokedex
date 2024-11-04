import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext

def obtener_pokemon(nombre_o_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre_o_id.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de estado 4xx/5xx
        datos = response.json()
        return datos
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Ocurrió un error: {err}")
    return None

def mostrar_info():
    entrada = entry.get().strip()
    if not entrada:
        messagebox.showwarning("Entrada Vacía", "Por favor, ingresa un nombre o ID de Pokémon.")
        return
    datos = obtener_pokemon(entrada)
    if datos:
        try:
            nombre = datos['name'].capitalize()
            id_pokemon = datos['id']
            tipos = ', '.join([tipo['type']['name'].capitalize() for tipo in datos['types']])
            altura = datos['height'] / 10  # Convertir decímetros a metros
            peso = datos['weight'] / 10    # Convertir hectogramos a kilogramos
            habilidades = ', '.join([habilidad['ability']['name'].capitalize() for habilidad in datos['abilities']])
            
            # Extraer movimientos
            movimientos_lista = [movimiento['move']['name'].capitalize() for movimiento in datos['moves']]
            movimientos = '\n'.join(movimientos_lista)  # Mostrar todos los movimientos en líneas separadas
            
            info = (f"ID: {id_pokemon}\n"
                    f"Nombre: {nombre}\n"
                    f"Tipo(s): {tipos}\n"
                    f"Altura: {altura} m\n"
                    f"Peso: {peso} kg\n"
                    f"Habilidades: {habilidades}\n"
                    f"Movimientos:\n{movimientos}\n")
            
            # Limpiar el widget scrolledtext antes de insertar nueva información
            text_info.config(state='normal')  # Habilitar edición temporalmente
            text_info.delete('1.0', tk.END)
            text_info.insert(tk.END, info)
            text_info.config(state='disabled')  # Deshabilitar edición nuevamente
        except KeyError as e:
            messagebox.showerror("Error", f"Clave no encontrada en los datos: {e}")
    else:
        messagebox.showerror("Error", "Pokémon no encontrado. Verifica el nombre o ID.")

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Pokédex Profesor Eliud")
ventana.geometry("800x600")  # Tamaño ajustado para mejor visualización
ventana.configure(bg="#1E3D59")  # Fondo azul oscuro

# Estilos de colores
color_fondo = "#1E3D59"      # Azul oscuro
color_entrada = "#F0F4F8"    # Blanco humo para entradas
color_boton = "#4B86B4"      # Azul medio para botones
color_texto = "#FFFFFF"      # Blanco para textos
color_label = "#A9DADC"      # Azul claro para etiquetas

# Marco principal para organizar los widgets
marco_principal = tk.Frame(ventana, bg=color_fondo)
marco_principal.pack(pady=20)

# Título de la Pokédex
titulo = tk.Label(marco_principal, text="Pokédex Profesor Eliud", font=("Helvetica", 24, "bold"), bg=color_fondo, fg=color_texto)
titulo.pack(pady=10)

# Entrada de texto
entry = tk.Entry(marco_principal, width=30, font=("Arial", 14), bg=color_entrada, fg="#000000", borderwidth=2, relief="groove")
entry.pack(pady=10)

# Botón para buscar
boton = tk.Button(marco_principal, text="Buscar", command=mostrar_info, font=("Arial", 12, "bold"), bg=color_boton, fg=color_texto, activebackground="#3A5A8C", activeforeground=color_texto, borderwidth=0, padx=10, pady=5)
boton.pack(pady=10)

# Separador
separador = tk.Frame(marco_principal, height=2, width=600, bg=color_label)
separador.pack(pady=10)

# Widget scrolledtext para mostrar la información
text_info = scrolledtext.ScrolledText(marco_principal, width=70, height=20, font=("Arial", 12), bg="#F0F4F8", fg="#000000", borderwidth=2, relief="groove")
text_info.pack(pady=10)
text_info.config(state='disabled')  # Deshabilitar edición

# Ejecutar la ventana
ventana.mainloop()
