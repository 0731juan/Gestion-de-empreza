# OBRAGEST

Este proyecto consiste en el desarrollo de un software integral para una empresa del sector construcción y venta de viviendas. Su objetivo principal es centralizar y optimizar la gestión de los distintos procesos operativos, financieros y comerciales de la constructora.

### OBJETIVOS
- Registrar la información de la constructora y sus proyectos activos.

- Gestionar la construcción de viviendas, incluyendo el control detallado de materiales y gastos asociados.

- Registrar ventas, calcular comisiones para maestros de obra y vendedores, y administrar el capital disponible para reinversión.

- Controlar el inventario de materiales, actualizándolo dinámicamente con base en el avance de los proyectos.

- Administrar la nómina semanal del personal, considerando horas extras y ausencias.

- Incorporar un módulo de análisis comercial, utilizando datos recolectados de clientes potenciales a través de canales digitales como WhatsApp y formularios online.

##  LENGUAJES Y HERRAMIENTAS UTILIZADAS

- Python 
- FastAPI
- Matplopib
- Uvicorn
- Pandas
- HTML
- CSS

## ESTRUCTURA DEL TRABAJO

├── .venv/
├── __pycache__/
│   ├── aplicacion.cpython-312.pyc
│   └── main.cpython-312.pyc
├── app/
│   ├── models/
│   │   ├── __pycache__/
│   │   └── task.py
│   ├── service/
│   │   ├── __pycache__/
│   │   └── task_service.py
│   ├── storage/
│   │   ├── __pycache__/
│   │   └── file_storage.py
│   └── ui/
│       ├── __pycache__/
│       └── ui_cli.py
├── data/
│   └── task.json
├── README.md
├── commands.txt
├── ejercicio_gestion_emp.ipynb
├── main.py
└── requirements.txt

# EXPLICACIÓN DETALLADA DEL PROYECTO

## CODIGO
#### PASO 1
- En esta sección, se definen listas con nombres y apellidos generados de manera aleatoria, que serán utilizados para generar nombres de empleados en la base de datos y también los nombres asignados para representar personal del área comercial o de ventas. Útiles para simular operaciones relacionadas con comisiones y cierre de negocios.
- Se define una ruta raíz ("/") en un router de FastAPI. Devuelve una respuesta en HTML. Normalmente, esta ruta sirve para mostrar una interfaz básica o una página de bienvenida de la API.
```python
nombres_empleados = [
    "Ana", "Luis", "Carlos", "María", "Jose", "Lucía", "Jorge", "Sofía", "Miguel", "Laura",
    "Andrés", "Valentina", "Diego", "Camila", "Fernando", "Isabela", "Ricardo", "Daniela", "Tomás", "Paula",
    "Santiago", "Juliana", "Juan", "Sara", "Emilio", "Gabriela", "Esteban", "Antonia", "Mateo", "Manuela"
]
apellidos = [
    "Gómez", "Rodríguez", "Martínez", "Pérez", "López", "García", "Hernández", "Sánchez", "Ramírez", "Torres",
    "Flores", "Rivera", "Castro", "Ortiz", "Moreno", "Jiménez", "Vargas", "Mendoza", "Ríos", "Guerrero",
    "Cortés", "Cruz", "Delgado", "Romero", "Silva", "Reyes", "Ruiz", "Navarro", "Medina", "Campos"
]
nombres_maestros = ["Ana", "Carlos", "Lucía", "Jose", "Valentina"]
nombres_vendedores = ["Mateo", "Isabella", "Sebastián", "Daniela", "Tomás"]

@router.get("/", response_class=HTMLResponse)
```

