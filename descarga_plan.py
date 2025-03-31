import pandas as pd
def generar_organigrama(data, codigo_inicial, estatus_filtro='todos', nivel=0, contador=0):
    # Filtrar empleados según el estatus deseado
    if estatus_filtro == 'si':  # Si eliges "sí", se muestran todos los estatus
        empleados = data[data['JEFE'] == codigo_inicial]  # Todos los empleados, incluyendo los inactivos y vacantes
    else:  # Si eliges "no", se filtran solo los activos y vacantes
        empleados = data[(data['JEFE'] == codigo_inicial) & (data['ESTATUS SAP'] != 'Inactivo')]  # Excluye 'Inactivo'

    if empleados.empty:
        return contador, 0, 0  # No hay más empleados, devolver contador y vacantes, activos

    vacantes = 0
    activos = 0

    for _, empleado in empleados.iterrows():
        # Contar vacantes y activos
        if empleado['NOMBRE EMPLEADO'] == 'Vacante':
            vacantes += 1
        else:
            activos += 1

        print("  " * nivel + f"• {empleado['NOMBRE EMPLEADO']} (CODIGO: {empleado['CODIGO']})")
        # Incrementar contador por cada empleado encontrado
        contador += 1
        # Llamada recursiva para buscar empleados bajo este jefe
        sub_contador, sub_vacantes, sub_activos = generar_organigrama(data, empleado['CODIGO'], estatus_filtro, nivel + 1, contador)

        # Sumar los vacantes y activos de la subconsulta
        vacantes += sub_vacantes
        activos += sub_activos

    return contador, vacantes, activos


# Ruta del archivo Excel
ruta_archivo = r'C:\Users\Juan\Downloads\1.xlsx'

# Leer el archivo Excel
try:
    data = pd.read_excel(ruta_archivo)

    # Verificar que las columnas necesarias existan
    required_columns = {'CODIGO', 'JEFE', 'NOMBRE EMPLEADO', 'ESTATUS SAP'}
    if not required_columns.issubset(data.columns):
        print(f"Error: El archivo debe contener las columnas {', '.join(required_columns)}.")
    else:
        # Solicitar el código inicial
        codigo_inicial = int(input("Ingrese el CODIGO inicial: ").strip())

        # Solicitar el filtro de estatus
        estatus_filtro = input("¿Quieres incluir todos los estatus? (si/no): ").strip().lower()
        if estatus_filtro not in ['si', 'no']:
            print("Opción inválida, por favor ingresa 'si' o 'no'.")
        else:
            print(f"\nOrganigrama a partir de {codigo_inicial}:\n")
            total_registros, vacantes, activos = generar_organigrama(data, codigo_inicial, estatus_filtro)

            # Mostrar resultados
            print(f"\nTotal de registros encontrados (excluyendo 'Inactivo'): {vacantes + activos}")
            print(f"Total de vacantes: {vacantes}")
            print(f"Total de activos: {activos}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta {ruta_archivo}.")
except Exception as e:
    print(f"Error al leer el archivo: {e}")
