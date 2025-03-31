import pandas as pd


def buscar_palabras_y_jefes(data, palabras_clave):
    coincidencias = data.apply(
        lambda row: row.astype(str).str.contains('|'.join(palabras_clave), case=False, na=False).any(), axis=1)
    filtrados = data[coincidencias]
    posiciones_encontradas = set(filtrados['Posición'].tolist())

    while True:
        jefes = data[data['Posición'].isin(filtrados['Jefe'].tolist())]
        if jefes.empty or set(jefes['Posición']) <= posiciones_encontradas:
            break
        filtrados = pd.concat([filtrados, jefes]).drop_duplicates()
        posiciones_encontradas.update(jefes['Posición'].tolist())

    return filtrados


# Ruta del archivo Excel
ruta_archivo = r'C:\Users\Juan\Downloads\12.xlsx'

try:
    data = pd.read_excel(ruta_archivo)

    palabras_clave = input("Ingrese las palabras clave separadas por comas: ").strip().split(',')
    resultado_final = buscar_palabras_y_jefes(data, palabras_clave)

    print("\nResultados filtrados con sus jefes:")
    print(resultado_final)

    ruta_salida = r'C:\Users\Juan\Downloads\resultado_filtrado.xlsx'
    resultado_final.to_excel(ruta_salida, index=False)
    print(f"Archivo guardado en: {ruta_salida}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta {ruta_archivo}.")
except Exception as e:
    print(f"Error al procesar el archivo: {e}")
