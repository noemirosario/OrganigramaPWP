import pandas as pd


def generar_organigrama(data, codigo_inicial, estatus_filtro='todos', nivel=0):
    # -- Filtramos filas según JEFE INMEDIATO y estatus.
    #    Ojo: la columna JEFE INMEDIATO y el codigo_inicial deben ser del mismo tipo (str).

    if estatus_filtro == 'si':
        # Incluimos todos los estatus
        empleados = data[data['JEFE INMEDIATO'] == codigo_inicial]
    else:
        # Excluimos "Inactivo"
        empleados = data[
            (data['JEFE INMEDIATO'] == codigo_inicial)
            & (data['ESTATUS SAP'] != 'Inactivo')
            ]

    # Si no hay empleados, retornamos ceros y lista vacía
    if empleados.empty:
        return 0, 0, 0, []

    # Inicializamos contadores y la lista
    contador = 0
    vacantes = 0
    activos = 0
    empleados_lista = []

    # Iteramos sobre los empleados filtrados
    for _, empleado in empleados.iterrows():
        # Contamos este empleado
        contador += 1

        # Contar vacante o activo
        if empleado['NOMBRE EMPLEADO'] == 'Vacante':
            vacantes += 1
        else:
            activos += 1

        # Extraer la parte después del guion en 'AREA NOMINA' (si aplica)
        if isinstance(empleado['AREA NOMINA'], str) and ' - ' in empleado['AREA NOMINA']:
            area_nomina = empleado['AREA NOMINA'].split(' - ', 1)[-1]
        else:
            area_nomina = empleado['AREA NOMINA']

        # Buscar el nombre del jefe inmediato, si existe en data
        # (asegurándonos de que CODIGO sea string también)
        nombre_jefe = ''
        jefe_match = data[data['CODIGO'] == empleado['JEFE INMEDIATO']]
        if not jefe_match.empty:
            nombre_jefe = jefe_match.iloc[0]['NOMBRE EMPLEADO']

        # Añadir registro a la lista
        empleados_lista.append({
            'ESTATUS SAP': empleado['ESTATUS SAP'],
            'NUMERO EMPLEADO': empleado.get('NUMERO EMPLEADO', ''),
            'NOMBRE EMPLEADO': empleado['NOMBRE EMPLEADO'],
            'CODIGO': empleado['CODIGO'],
            'NOMBRE POSICION': empleado.get('NOMBRE POSICION', ''),
            'CENTRO COSTE': empleado.get('CENTRO COSTE', ''),
            'AREA NOMINA': area_nomina,
            'JEFE INMEDIATO': empleado['JEFE INMEDIATO'],
            'NOMBRE JEFE INMEDIATO': nombre_jefe
        })

        # Imprimir jerarquía con viñetas
        print("  " * nivel + f"• {empleado['NOMBRE EMPLEADO']} (CODIGO: {empleado['CODIGO']})")

        # Llamada recursiva para encontrar subordinados
        sub_contador, sub_vacantes, sub_activos, sub_empleados_lista = generar_organigrama(
            data,
            codigo_inicial=empleado['CODIGO'],  # Pasa el código como string
            estatus_filtro=estatus_filtro,
            nivel=nivel + 1
        )

        # Acumulamos los resultados
        contador += sub_contador
        vacantes += sub_vacantes
        activos += sub_activos
        empleados_lista.extend(sub_empleados_lista)

    return contador, vacantes, activos, empleados_lista


# ---------------------------------------------------------------------
# Ejecución principal
# ---------------------------------------------------------------------
# Ruta del archivo Excel
ruta_archivo = r'C:\Users\Juan\Downloads\PWP.xlsx'

try:
    data = pd.read_excel(ruta_archivo)

    # Asegurarnos de que CODIGO y JEFE INMEDIATO sean strings para que la comparación funcione
    data['CODIGO'] = data['CODIGO'].astype(str)
    data['JEFE INMEDIATO'] = data['JEFE INMEDIATO'].astype(str)

    # Además, si JEFE INMEDIATO contiene algo como "99999 - Nombre", nos quedamos sólo con la parte antes del "-"
    # para que las búsquedas sean coherentes. Hacemos esto solo una vez.
    data['JEFE INMEDIATO'] = data['JEFE INMEDIATO'].apply(
        lambda x: x.split(" - ")[0] if " - " in x else x
    )

    # Pedimos código inicial en string (no lo convirtamos a int)
    codigo_inicial = input("Ingrese el CODIGO inicial: ").strip()

    # Preguntamos por estatus
    estatus_filtro = input("¿Quieres incluir todos los estatus? (si/no): ").strip().lower()
    if estatus_filtro not in ['si', 'no']:
        print("Opción inválida, por favor ingresa 'si' o 'no'.")
    else:
        print(f"\nOrganigrama a partir de {codigo_inicial}:\n")
        total_registros, vacantes, activos, empleados_lista = generar_organigrama(
            data,
            codigo_inicial=codigo_inicial,
            estatus_filtro=estatus_filtro
        )

        # Mostramos resultados
        # Ojo: total_registros incluye tanto 'Vacante' como empleados activos,
        #      y si estatus_filtro == 'si', incluirá también "Inactivo".
        print(f"\nTotal de registros encontrados: {total_registros}")
        print(f"Total de vacantes: {vacantes}")
        print(f"Total de activos: {activos}")

        # Guardar en Excel
        df_empleados = pd.DataFrame(empleados_lista)
        ruta_salida = r'C:\Users\Juan\Downloads\aldo.xlsx'
        df_empleados.to_excel(ruta_salida, index=False)
        print(f"Archivo Excel con los datos organizados guardado en: {ruta_salida}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta {ruta_archivo}.")
except Exception as e:
    print(f"Error al leer o procesar el archivo: {e}")
