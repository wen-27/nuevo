from utils.screemControlers import limpiar_pantalla, pausar_pantalla
from controllers.equipo import *
from utils.menus import *
from controllers.jugadores import*

def main():
    while True:
        limpiar_pantalla()
        print(menu)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            while True:
                limpiar_pantalla()
                print(menu_equipo)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    listar_equipos()
                elif opcion == "2":
                    crear_equipo()
                elif opcion == "3":
                    editar_equipo()
                elif opcion == "4":
                    eliminar_equipo()
                elif opcion == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                    pausar_pantalla()

        elif opcion == "2":
            while True:
                limpiar_pantalla()
                print(menu_jugadores)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    listar_jugadores()
                elif opcion == "2":
                    crear_jugador()
                elif opcion == "3":
                    editar_jugador()
                elif opcion == "4":
                    eliminar_jugador()
                elif opcion == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                    pausar_pantalla()

        elif opcion == "3":
            while True:
                limpiar_pantalla()
                print(menu_transferencia)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    pass  # Implementar según necesidades
                elif opcion == "2":
                    pass  # Implementar según necesidades
                elif opcion == "3":
                    pass  # Implementar según necesidades
                elif opcion == "4":
                    pass  # Implementar según necesidades
                elif opcion == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                    pausar_pantalla()

        elif opcion == "4":
            print("Saliendo del programa...........")
            break

        else:
            print("Opción inválida. Intente de nuevo.")
            pausar_pantalla()

if __name__ == "__main__":
    main()