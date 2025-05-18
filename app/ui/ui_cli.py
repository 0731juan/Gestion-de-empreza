from app.service.task_service import (
    add_task,
    list_tasks,
    mark_task_completed,
    delete_task,
)


def run_cli():

    while True:
        print(f'{"="*10} ToDo App {"="*10}')
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Marcar tarea como completada")
        print("4. Eliminar tarea")
        print("5. Salir")

        print(f'{"="*10}{"="*10}')

        choice = input("Seleccione una opción: ")

        if choice == "1":
            description = input("Ingrese la descripción de la tarea: ")
            add_task(description)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = int(input("Ingrese el ID de la tarea a marcar como completada: "))
            mark_task_completed(task_id)
        elif choice == "4":
            task_id = int(input("Ingrese el ID de la tarea a eliminar: "))
            delete_task(task_id)
        elif choice == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")