from menus import menu, menu_equipo, menu_jugadores, menu_transferencia
from screemControlers import limpiar_pantalla, pausar_pantalla
from equipo import menu_equipo as gestion_equipo

def main():
    while True:
        limpiar_pantalla()
        print(menu)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            while True:
                limpiar_pantalla()
                print(menu_equipo)
                opcion_productos = input("Seleccione una opción: ").strip()

                if opcion_productos == "1":
                    gestion_equipo()
                elif opcion_productos == "2":
                    pass  # Implementar según necesidades
                elif opcion_productos == "3":
                    pass  # Implementar según necesidades
                elif opcion_productos == "4":
                    pass  # Implementar según necesidades
                elif opcion_productos == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                    pausar_pantalla()

        elif opcion == "2":
            while True:
                limpiar_pantalla()
                print(menu_jugadores)
                opcion_pedidos = input("Seleccione una opción: ").strip()

                if opcion_pedidos == "1":
                    pass  # Implementar según necesidades
                elif opcion_pedidos == "2":
                    pass  # Implementar según necesidades
                elif opcion_pedidos == "3":
                    pass  # Implementar según necesidades
                elif opcion_pedidos == "4":
                    pass  # Implementar según necesidades
                elif opcion_pedidos == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                    pausar_pantalla()

        elif opcion == "3":
            while True:
                limpiar_pantalla()
                print(menu_transferencia)
                opcion_pedidos = input("Seleccione una opción: ").strip()

                if opcion_pedidos == "1":
                    pass  # Implementar según necesidades
                elif opcion_pedidos == "2":
                    pass  # Implementar según necesidades
                elif opcion_pedidos == "3":
                    pass  # Implementar según necesidades
                elif opcion_pedidos == "4":
                    pass  # Implementar según necesidades
                elif opcion_pedidos == "5":
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