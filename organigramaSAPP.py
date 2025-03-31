import pandas as pd
import streamlit as st

# Configuración de la app
#st.title("📂 Generacion de organigrama")
#st.write("Sube la base ")

def generar_organigrama(data, Posición_inicial, estatus_filtro='todos', nivel=0, contador=0, empleados_lista=None):
    if empleados_lista is None:
        empleados_lista = []

    # Si la posición inicial no está en la lista, agregarla
    if not any(emp['Posición'] == Posición_inicial for emp in empleados_lista):
        posicion_inicial_data = data[data['Posición'] == Posición_inicial]

        if not posicion_inicial_data.empty:
            empleado_inicial = posicion_inicial_data.iloc[0]
            empleados_lista.append({
                'Estatus': empleado_inicial['Estatus'],
                'fecha ing': empleado_inicial.get('fecha ing', ''),
                'Nº pers': empleado_inicial['Nº pers'],
                'Número de personal': empleado_inicial['Número de personal'],
                'Posición': empleado_inicial['Posición'],
                'Nombre Pos': empleado_inicial['Nombre Pos'],
                #'Subdivisión del': empleado_inicial.get('Subdivisión de', ''),
                #'Área de nómina': empleado_inicial.get('Área de nómina', ''),
                'Jefe': empleado_inicial['Jefe']
            })

            print(f"• {empleado_inicial['Número de personal']} (Posición: {empleado_inicial['Posición']})")

    # Filtrar empleados según el jefe asignado
    if estatus_filtro == 'si':
        empleados = data[data['Jefe'] == Posición_inicial]
    else:
        empleados = data[(data['Jefe'] == Posición_inicial) & (data['Estatus'] != 'Vacante')]  # Excluye 'Vacante'

    if empleados.empty:
        return contador, 0, 0, empleados_lista

    vacantes = 0
    activos = 0

    for _, empleado in empleados.iterrows():
        if empleado['Estatus'] == 'Vacante':
            vacantes += 1
        else:
            activos += 1

        # Evitar duplicados antes de agregar
        if not any(emp['Posición'] == empleado['Posición'] for emp in empleados_lista):
            empleados_lista.append({
                'Estatus': empleado['Estatus'],
                'fecha ing': empleado.get('fecha ing', ''),
                'Nº pers': empleado['Nº pers'],
                'Número de personal': empleado['Número de personal'],
                'Posición': empleado['Posición'],
                'Nombre Pos': empleado['Nombre Pos'],
                #'Subdivisión del': empleado.get('Subdivisión de', ''),
                #'Área de nómina': empleado.get('Área de nómina', ''),
                'Jefe': empleado['Jefe']
            })

        print("  " * nivel + f"• {empleado['Número de personal']} (Posición: {empleado['Posición']})")

        # Llamada recursiva para buscar empleados bajo este Jefe
        sub_contador, sub_vacantes, sub_activos, empleados_lista = generar_organigrama(
            data, empleado['Posición'], estatus_filtro, nivel + 1, contador, empleados_lista
        )

        vacantes += sub_vacantes
        activos += sub_activos

    return contador + len(empleados), vacantes, activos, empleados_lista


# Ruta del archivo Excel
ruta_archivo = r'C:\Users\Juan\Downloads\unido2.xlsx'

# Leer el archivo Excel
try:
    data = pd.read_excel(ruta_archivo)

    # Verificar que las columnas necesarias existan
    required_columns = {'Posición', 'Jefe', 'Número de personal', 'Estatus'}
    if not required_columns.issubset(data.columns):
        print(f"Error: El archivo debe contener las columnas {', '.join(required_columns)}.")
    else:
        # Solicitar el código inicial
        Posición_inicial = int(input("Ingrese el Posición inicial: ").strip())

        # Solicitar el filtro de estatus
        estatus_filtro = input("¿Quieres incluir todos los estatus? (si/no): ").strip().lower()
        if estatus_filtro not in ['si', 'no']:
            print("Opción inválida, por favor ingresa 'si' o 'no'.")
        else:
            print(f"\nOrganigrama a partir de {Posición_inicial}:\n")
            total_registros, vacantes, activos, empleados_lista = generar_organigrama(data, Posición_inicial, estatus_filtro)

            # Mostrar resultados
            print(f"\nTotal de registros encontrados (excluyendo 'Vacantes'): {vacantes + activos}")
            print(f"Total de vacantes: {vacantes}")
            print(f"Total de activos: {activos}")

            # Guardar los datos organizados en un archivo Excel
            df_empleados = pd.DataFrame(empleados_lista)
            ruta_salida = rf'C:\Users\Juan\Downloads\{Posición_inicial}2.xlsx'
            df_empleados.to_excel(ruta_salida, index=False)
            print(f"Archivo Excel con los datos organizados guardado en: {ruta_salida}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta {ruta_archivo}.")
except Exception as e:
    print(f"Error al leer el archivo: {e}")