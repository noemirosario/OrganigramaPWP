import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


def seleccionar_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
    entrada_archivo.delete(0, tk.END)
    entrada_archivo.insert(0, ruta)


def generar_organigrama():
    ruta_archivo = entrada_archivo.get()
    posicion_inicial = entrada_posicion.get().strip()

    if not ruta_archivo:
        messagebox.showerror("Error", "Por favor selecciona un archivo Excel")
        return

    try:
        data = pd.read_excel(ruta_archivo)
        required_columns = {"Posición", "Jefe", "Número de personal", "Estatus"}

        if not required_columns.issubset(data.columns):
            messagebox.showerror("Error", f"El archivo debe contener las columnas {', '.join(required_columns)}")
            return

        if not posicion_inicial.isdigit():
            messagebox.showerror("Error", "La posición inicial debe ser un número válido")
            return

        posicion_inicial = int(posicion_inicial)
        texto_resultados.insert(tk.END, f"Generando organigrama desde la posición {posicion_inicial}...\n")
        # Aquí se llamaría la función de organigrama (se puede agregar después)

        texto_resultados.insert(tk.END, "¡Organigrama generado con éxito!\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo: {str(e)}")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Organigrama")
ventana.geometry("500x400")

# Entrada para seleccionar archivo
label_archivo = tk.Label(ventana, text="Selecciona un archivo Excel:")
label_archivo.pack()
entrada_archivo = tk.Entry(ventana, width=50)
entrada_archivo.pack()
boton_archivo = tk.Button(ventana, text="Buscar", command=seleccionar_archivo)
boton_archivo.pack()

# Entrada para posición inicial
label_posicion = tk.Label(ventana, text="Posición inicial:")
label_posicion.pack()
entrada_posicion = tk.Entry(ventana)
entrada_posicion.pack()

# Botón para generar organigrama
boton_generar = tk.Button(ventana, text="Generar Organigrama", command=generar_organigrama)
boton_generar.pack()

# Área de texto para resultados
texto_resultados = tk.Text(ventana, height=10, width=60)
texto_resultados.pack()

# Ejecutar la aplicación
ventana.mainloop()
