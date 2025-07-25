import json
from datetime import datetime
import os

archivo_json = "equipos.json"

def listar_equipos():
    """Muestra todos los equipos en formato de tabla con opción de exportar"""
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, "r", encoding="utf-8") as file:
                content = file.read()
                if not content.strip():
                    print("No hay equipos registrados.")
                    return
                equipos = json.loads(content)
                if equipos:
                    print("\nListado de Equipos Registrados:\n")
                    print(f"{'ID':<5} {'Nombre':<25} {'Fundación':<12} {'País':<20} {'Liga_ID':<8}")
                    print("-" * 75)
                    for equipo in equipos:
                        print(f"{equipo['id']:<5} {equipo['nombre']:<25} {equipo['fundacion']:<12} {equipo['pais']:<20} {equipo['liga_id']:<8}")
                    print(f"\nTotal de equipos: {len(equipos)}")
                    return equipos
                else:
                    print("No hay equipos registrados.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al leer el archivo: {str(e)}")
    else:
        print("No existe el archivo de equipos. Debes registrar primero.")

def validar_fecha(fundacion):
    """Valida que el año de fundación sea correcto"""
    try:
        year = int(fundacion)
        if 1900 < year <= datetime.now().year:
            return True
        print("Error: El año debe ser >1900 y ≤ año actual")
        return False
    except ValueError:
        print("Error: Debe ser un número entero")
        return False

def obtener_ultimo_id():
    """Obtiene el último ID utilizado"""
    equipos = leer_equipos()
    return max(equipo["id"] for equipo in equipos) if equipos else 0

def crear_equipo():
    """Registra nuevos equipos con validación"""
    equipos = leer_equipos()
    
    while True:
        print("\n--- REGISTRAR NUEVO EQUIPO ---")
        
        # Validación de nombre
        while True:
            nombre = input("Nombre del equipo: ").strip()
            if nombre:
                if not any(equipo['nombre'].lower() == nombre.lower() for equipo in equipos):
                    break
                print("Error: Ya existe un equipo con ese nombre")
            else:
                print("Error: El nombre no puede estar vacío")
        
        # Validación de fundación
        while True:
            fundacion = input("Año de fundación: ").strip()
            if validar_fecha(fundacion):
                break
        
        # Validación de país
        while True:
            pais = input("País: ").strip()
            if pais:
                break
            print("Error: El país no puede estar vacío")
        
        # Generar nuevo ID
        nuevo_id = obtener_ultimo_id() + 1
        
        nuevo_equipo = {
            "id": nuevo_id,
            "nombre": nombre,
            "fundacion": fundacion,
            "pais": pais,
            "liga_id": nuevo_id
        }
        
        equipos.append(nuevo_equipo)
        
        if guardar_equipos(equipos):
            print(f"\n✅ Equipo '{nombre}' registrado con ID {nuevo_id}")
        else:
            equipos.pop()
            print("\n❌ Error al guardar el equipo")
        
        if input("\n¿Agregar otro equipo? (s/n): ").lower() != 's':
            break

def leer_equipos():
    """Carga todos los equipos desde el archivo"""
    if not os.path.exists(archivo_json):
        return []
    
    try:
        with open(archivo_json, "r", encoding="utf-8") as file:
            content = file.read()
            return json.loads(content) if content.strip() else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al leer archivo: {str(e)}")
        return []

def guardar_equipos(equipos):
    """Guarda los equipos en el archivo JSON"""
    try:
        with open(archivo_json, "w", encoding="utf-8") as file:
            json.dump(equipos, file, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error al guardar: {str(e)}")
        return False

def editar_equipo():
    """Edita un equipo existente con confirmación"""
    equipos = leer_equipos()
    if not equipos:
        print("No hay equipos registrados")
        return
    
    listar_equipos()
    
    try:
        equipo_id = int(input("\nID del equipo a editar: "))
    except ValueError:
        print("Error: ID debe ser número entero")
        return
    
    equipo = next((e for e in equipos if e['id'] == equipo_id), None)
    if not equipo:
        print("Error: Equipo no encontrado")
        return
    
    print("\nEditando equipo:")
    print(f"1. Nombre: {equipo['nombre']}")
    print(f"2. Fundación: {equipo['fundacion']}")
    print(f"3. País: {equipo['pais']}")
    print(f"4. ID Liga: {equipo['liga_id']}")
    
    cambios = {}
    campos = ['nombre', 'fundacion', 'pais', 'liga_id']
    
    for i, campo in enumerate(campos, 1):
        nuevo_valor = input(f"\nNuevo {campo} (enter para mantener actual): ").strip()
        if nuevo_valor:
            if campo == 'fundacion' and not validar_fecha(nuevo_valor):
                continue
            if campo == 'liga_id':
                try:
                    nuevo_valor = int(nuevo_valor)
                except ValueError:
                    print("Error: ID Liga debe ser número")
                    continue
            cambios[campo] = nuevo_valor
    
    if cambios:
        confirmar = input("\n¿Confirmar cambios? (s/n): ").lower()
        if confirmar == 's':
            equipo.update(cambios)
            if guardar_equipos(equipos):
                print("✅ Equipo actualizado")
            else:
                print("❌ Error al guardar cambios")
    else:
        print("⚠️ No se realizaron cambios")

def eliminar_equipo():
    """Elimina un equipo con confirmación"""
    equipos = leer_equipos()
    if not equipos:
        print("No hay equipos registrados")
        return
    
    listar_equipos()
    
    try:
        equipo_id = int(input("\nID del equipo a eliminar: "))
    except ValueError:
        print("Error: ID debe ser número entero")
        return
    
    equipo = next((e for e in equipos if e['id'] == equipo_id), None)
    if not equipo:
        print("Error: Equipo no encontrado")
        return
    
    print(f"\nEquipo a eliminar: {equipo['nombre']} (ID: {equipo['id']})")
    confirmar = input("¿Está seguro? (s/n): ").lower()
    
    if confirmar == 's':
        equipos = [e for e in equipos if e['id'] != equipo_id]
        if guardar_equipos(equipos):
            print("✅ Equipo eliminado")
        else:
            print("❌ Error al eliminar equipo")