import json
import os
from datetime import datetime

archivo_jugadores = "jugadores.json"

def cargar_jugadores():
    """Carga todos los jugadores desde el archivo"""
    if not os.path.exists(archivo_jugadores):
        return []
    
    try:
        with open(archivo_jugadores, "r", encoding="utf-8") as file:
            content = file.read()
            return json.loads(content) if content.strip() else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar jugadores: {str(e)}")
        return []

def guardar_jugadores(jugadores):
    """Guarda los jugadores en el archivo JSON"""
    try:
        with open(archivo_jugadores, "w", encoding="utf-8") as file:
            json.dump(jugadores, file, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error al guardar jugadores: {str(e)}")
        return False

def listar_jugadores():
    """Lista todos los jugadores registrados"""
    jugadores = cargar_jugadores()
    
    if not jugadores:
        print("No hay jugadores registrados")
        return []
    
    print("\n--- LISTA DE JUGADORES ---")
    print(f"{'ID':<5} {'Nombre':<25} {'Posición':<15} {'Dorsal':<8} {'Equipo ID':<10}")
    print("-" * 70)
    
    for jugador in jugadores:
        print(f"{jugador['id']:<5} {jugador['nombre']:<25} {jugador['posicion']:<15} {jugador['dorsal']:<8} {jugador['equipo_id']:<10}")
    
    print(f"\nTotal: {len(jugadores)} jugadores")
    return jugadores

def crear_jugador():
    """Registra un nuevo jugador con validaciones"""
    from controllers.equipo import listar_equipos
    
    jugadores = cargar_jugadores()
    equipos = listar_equipos()
    
    if not equipos:
        print("Primero debe registrar equipos")
        return
    
    while True:
        print("\n--- REGISTRAR NUEVO JUGADOR ---")
        
        # Validación de nombre
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("Error: Nombre no puede estar vacío")
            continue
        
        # Validación de posición
        posicion = input("Posición (ej. Delantero, Defensa): ").strip()
        if not posicion:
            print("Error: Posición no puede estar vacía")
            continue
        
        # Validación de dorsal
        while True:
            try:
                dorsal = int(input("Número de dorsal: ").strip())
                if dorsal <= 0:
                    print("Error: Dorsal debe ser positivo")
                    continue
                break
            except ValueError:
                print("Error: Debe ser número entero")
        
        # Selección de equipo
        print("\nEquipos disponibles:")
        for equipo in equipos:
            print(f"{equipo['id']}: {equipo['nombre']}")
        
        while True:
            try:
                equipo_id = int(input("\nID del equipo: ").strip())
                if equipo_id not in [e['id'] for e in equipos]:
                    print("Error: ID de equipo no válido")
                    continue
                
                # Verificar dorsal único en equipo
                if any(j['equipo_id'] == equipo_id and j['dorsal'] == dorsal for j in jugadores):
                    print("Error: Dorsal ya existe en este equipo")
                    break
                
                break
            except ValueError:
                print("Error: Debe ser número entero")
        
        # Generar ID
        nuevo_id = max(j['id'] for j in jugadores) + 1 if jugadores else 1
        
        nuevo_jugador = {
            "id": nuevo_id,
            "nombre": nombre,
            "posicion": posicion,
            "dorsal": dorsal,
            "equipo_id": equipo_id
        }
        
        jugadores.append(nuevo_jugador)
        
        if guardar_jugadores(jugadores):
            print(f"\n✅ Jugador '{nombre}' registrado con ID {nuevo_id}")
        else:
            jugadores.pop()
            print("\n❌ Error al guardar jugador")
        
        if input("\n¿Agregar otro jugador? (s/n): ").lower() != 's':
            break

def editar_jugador():
    """Edita la información de un jugador existente"""
    from controllers.equipo import listar_equipos
    
    jugadores = cargar_jugadores()
    if not jugadores:
        print("No hay jugadores registrados para editar")
        return
    
    # Mostrar lista de jugadores
    print("\n--- EDITAR JUGADOR ---")
    listado = listar_jugadores()
    
    try:
        jugador_id = int(input("\nIngrese el ID del jugador a editar: "))
    except ValueError:
        print("Error: Debe ingresar un número válido")
        return
    
    # Buscar jugador
    jugador = next((j for j in jugadores if j['id'] == jugador_id), None)
    if not jugador:
        print("Error: No se encontró jugador con ese ID")
        return
    
    print("\nDatos actuales del jugador:")
    print(f"1. Nombre: {jugador['nombre']}")
    print(f"2. Posición: {jugador['posicion']}")
    print(f"3. Dorsal: {jugador['dorsal']}")
    print(f"4. Equipo ID: {jugador['equipo_id']}")
    
    # Obtener equipos disponibles
    equipos = listar_equipos()
    if not equipos:
        print("Error: No hay equipos registrados")
        return
    
    # Procesar cambios
    cambios = {}
    
    # Editar nombre
    nuevo_nombre = input("\nNuevo nombre (dejar vacío para mantener actual): ").strip()
    if nuevo_nombre:
        cambios['nombre'] = nuevo_nombre
    
    # Editar posición
    nueva_posicion = input("Nueva posición (dejar vacío para mantener actual): ").strip()
    if nueva_posicion:
        cambios['posicion'] = nueva_posicion
    
    # Editar dorsal
    while True:
        nuevo_dorsal = input("Nuevo dorsal (dejar vacío para mantener actual): ").strip()
        if not nuevo_dorsal:
            break
        try:
            nuevo_dorsal = int(nuevo_dorsal)
            if nuevo_dorsal <= 0:
                print("Error: Dorsal debe ser positivo")
                continue
            
            # Verificar dorsal único en equipo
            equipo_actual = jugador['equipo_id']
            if any(j['equipo_id'] == equipo_actual and j['dorsal'] == nuevo_dorsal and j['id'] != jugador_id for j in jugadores):
                print("Error: Dorsal ya existe en este equipo")
                continue
            
            cambios['dorsal'] = nuevo_dorsal
            break
        except ValueError:
            print("Error: Debe ser número entero")
    
    # Editar equipo
    print("\nEquipos disponibles:")
    for equipo in equipos:
        print(f"{equipo['id']}: {equipo['nombre']}")
    
    while True:
        nuevo_equipo = input("\nNuevo ID de equipo (dejar vacío para mantener actual): ").strip()
        if not nuevo_equipo:
            break
        try:
            nuevo_equipo = int(nuevo_equipo)
            if nuevo_equipo not in [e['id'] for e in equipos]:
                print("Error: ID de equipo no válido")
                continue
            
            # Si cambió el equipo, verificar dorsal en nuevo equipo
            if 'dorsal' in cambios or nuevo_equipo != jugador['equipo_id']:
                dorsal = cambios.get('dorsal', jugador['dorsal'])
                if any(j['equipo_id'] == nuevo_equipo and j['dorsal'] == dorsal and j['id'] != jugador_id for j in jugadores):
                    print("Error: Dorsal ya existe en el nuevo equipo")
                    continue
            
            cambios['equipo_id'] = nuevo_equipo
            break
        except ValueError:
            print("Error: Debe ser número entero")
    
    # Aplicar cambios
    if cambios:
        confirmar = input("\n¿Confirmar cambios? (s/n): ").lower()
        if confirmar == 's':
            jugador.update(cambios)
            if guardar_jugadores(jugadores):
                print("✅ Jugador actualizado correctamente")
            else:
                print("❌ Error al guardar cambios")
        else:
            print("⚠️ Cambios cancelados")
    else:
        print("⚠️ No se realizaron cambios")

def eliminar_jugador():
    """Elimina un jugador del sistema con confirmación"""
    jugadores = cargar_jugadores()
    if not jugadores:
        print("No hay jugadores registrados para eliminar")
        return
    
    # Mostrar lista de jugadores
    print("\n--- ELIMINAR JUGADOR ---")
    listado = listar_jugadores()
    
    try:
        jugador_id = int(input("\nIngrese el ID del jugador a eliminar: "))
    except ValueError:
        print("Error: Debe ingresar un número válido")
        return
    
    # Buscar jugador
    jugador = next((j for j in jugadores if j['id'] == jugador_id), None)
    if not jugador:
        print("Error: No se encontró jugador con ese ID")
        return
    
    # Confirmar eliminación
    print(f"\nDatos del jugador a eliminar:")
    print(f"Nombre: {jugador['nombre']}")
    print(f"Posición: {jugador['posicion']}")
    print(f"Dorsal: {jugador['dorsal']}")
    print(f"Equipo ID: {jugador['equipo_id']}")
    
    confirmar = input("\n¿Está seguro que desea eliminar este jugador? (s/n): ").lower()
    if confirmar == 's':
        jugadores = [j for j in jugadores if j['id'] != jugador_id]
        if guardar_jugadores(jugadores):
            print("✅ Jugador eliminado correctamente")
        else:
            print("❌ Error al eliminar jugador")
    else:
        print("⚠️ Eliminación cancelada")