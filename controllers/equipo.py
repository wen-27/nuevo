import json
from datetime import datetime
import os

# Nombre del archivo donde guardaremos los datos
archivo_json = "equipos.json"

# Función para validar que la fecha sea un año válido
def validar_fecha(fundacion):
    try:
        year = int(fundacion)
        if year > 1900 and year <= datetime.now().year:
            return True
        else:
            print("Año de fundación no válido. Debe ser mayor que 1900 y menor o igual al año actual.")
            return False
    except ValueError:
        print("Fecha de fundación debe ser un número entero.")
        return False

# Función para obtener el último ID registrado
def obtener_ultimo_id():
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, "r") as file:
                content = file.read()
                if not content.strip():
                    return 0
                equipos = json.loads(content)
                if equipos:
                    return max(equipo["id"] for equipo in equipos)
                else:
                    return 0
        except (json.JSONDecodeError, KeyError):
            return 0
    else:
        return 0

# Función para crear un equipo
def crear_equipo():
    if not os.path.exists(archivo_json):
        with open(archivo_json, "w") as file:
            json.dump([], file)

    while True:
        nombre = input("\nIngrese el nombre del equipo: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío. Intenta nuevamente.")
            continue

        while True:
            fundacion = input("Ingrese la fecha de fundación del equipo (año): ").strip()
            if validar_fecha(fundacion):
                break

        pais = input("Ingrese el país del equipo: ").strip()
        if not pais:
            print("El país no puede estar vacío. Intenta nuevamente.")
            continue

        while True:
            try:
                liga_id = int(input("Ingrese el ID de la liga: "))
                if liga_id > 0:
                    break
                else:
                    print("El ID de la liga debe ser un número positivo.")
            except ValueError:
                print("El ID de la liga debe ser un número entero.")

        nuevo_id = obtener_ultimo_id() + 1

        equipo = {
            "id": nuevo_id,
            "nombre": nombre,
            "fundacion": fundacion,
            "pais": pais,
            "liga_id": liga_id
        }

        # Leer equipos existentes
        equipos = leer_equipos()
        equipos.append(equipo)

        # Sobrescribir el archivo con los nuevos datos
        try:
            with open(archivo_json, "w") as file:
                json.dump(equipos, file, indent=4)
            print(f"\nEquipo {nombre} registrado exitosamente con ID {nuevo_id}.")
        except IOError as e:
            print(f"Error al guardar el archivo: {e}")

        continuar = input("\n¿Desea registrar otro equipo? (sí/no): ").strip().lower()
        if continuar != "sí":
            break

# Función para leer todos los equipos
def leer_equipos():
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, "r") as file:
                content = file.read()
                if not content.strip():
                    return []
                equipos = json.loads(content)
                return equipos
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    else:
        return []

# Función para editar un equipo
def editar_equipo():
    equipos = leer_equipos()
    if not equipos:
        print("No hay equipos registrados para editar.")
        return

    print("\nEquipos registrados:")
    for equipo in equipos:
        print(f"ID: {equipo['id']}, Nombre: {equipo['nombre']}")

    try:
        equipo_id = int(input("\nIngrese el ID del equipo que desea editar: "))
        equipo_encontrado = None
        for equipo in equipos:
            if equipo['id'] == equipo_id:
                equipo_encontrado = equipo
                break

        if not equipo_encontrado:
            print("No se encontró un equipo con ese ID.")
            return

        nuevo_nombre = input(f"Nuevo nombre (actual: {equipo_encontrado['nombre']}): ").strip()
        if nuevo_nombre:
            equipo_encontrado['nombre'] = nuevo_nombre

        nueva_fundacion = input(f"Nueva fecha de fundación (actual: {equipo_encontrado['fundacion']}): ").strip()
        if nueva_fundacion and validar_fecha(nueva_fundacion):
            equipo_encontrado['fundacion'] = nueva_fundacion

        nuevo_pais = input(f"Nuevo país (actual: {equipo_encontrado['pais']}): ").strip()
        if nuevo_pais:
            equipo_encontrado['pais'] = nuevo_pais

        nuevo_liga_id = input(f"Nuevo ID de la liga (actual: {equipo_encontrado['liga_id']}): ").strip()
        if nuevo_liga_id.isdigit() and int(nuevo_liga_id) > 0:
            equipo_encontrado['liga_id'] = int(nuevo_liga_id)

        try:
            with open(archivo_json, "w") as file:
                json.dump(equipos, file, indent=4)
            print(f"\nEquipo con ID {equipo_id} editado exitosamente.")
        except IOError as e:
            print(f"Error al guardar el archivo: {e}")

    except ValueError:
        print("ID no válido. Debe ser un número entero.")

# Función para eliminar un equipo
def eliminar_equipo():
    equipos = leer_equipos()
    if not equipos:
        print("No hay equipos registrados para eliminar.")
        return

    print("\nEquipos registrados:")
    for equipo in equipos:
        print(f"ID: {equipo['id']}, Nombre: {equipo['nombre']}")

    try:
        equipo_id = int(input("\nIngrese el ID del equipo que desea eliminar: "))
        equipo_encontrado = None
        for equipo in equipos:
            if equipo['id'] == equipo_id:
                equipo_encontrado = equipo
                break

        if not equipo_encontrado:
            print("No se encontró un equipo con ese ID.")
            return

        equipos = [equipo for equipo in equipos if equipo['id'] != equipo_id]

        try:
            with open(archivo_json, "w") as file:
                json.dump(equipos, file, indent=4)
            print(f"\nEquipo con ID {equipo_id} eliminado exitosamente.")
        except IOError as e:
            print(f"Error al guardar el archivo: {e}")

    except ValueError:
        print("ID no válido. Debe ser un número entero.")