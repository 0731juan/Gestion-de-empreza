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
#### PASO 1: Formulario de Empresa
- Muestra un formulario donde el usuario ingresa el nombre de la empresa y el nombre del proyecto. Al hacer clic en "Siguiente", los datos se envían por método POST 
```python
def paso_1():
    return """
    <html><body>
    <h2>Paso 1: Datos de la empresa</h2>
    <form action="/paso2" method="post">
        Empresa: <input type="text" name="empresa" required><br>
        Proyecto: <input type="text" name="proyecto" required><br>
        <button type="submit">Siguiente</button>
    </form>
    </body></html>
    """
@router.post("/paso2", response_class=HTMLResponse)
```
#### PASO 2: Guardar datos de empresa y solicitar detalles del proyecto
- Esta función almacena los datos capturados en el paso anterior y presenta un segundo formulario para recopilar más detalles sobre el proyecto de construcción.
```python
def paso_2(empresa: str = Form(...), proyecto: str = Form(...)):
    storage.temp = {"empresa": empresa, "proyecto": proyecto}
    return """
    <html><body>
    <h2>Paso 2: Detalles del proyecto</h2>
    <form action="/paso3" method="post">
        Inversión inicial: <input type="number" name="capital" step="0.01" required><br>
        Precio de cada casa: <input type="number" name="precio_casa" step="0.01" required><br>
        Costo construir casa: <input type="number" name="costo_casa" step="0.01" required><br>
        Empleados asalariados: <input type="number" name="empleados" required><br>
        Salario semanal por empleado: <input type="number" name="salario" step="0.01" required><br>
        <button type="submit">Siguiente</button>
    </form>
    </body></html>
    """
@router.post("/paso3", response_class=HTMLResponse)
```
#### PASO 3: Detalles del proyecto
- guarda los detalles financieros y operativos del proyecto, y solicita al usuario cuántas semanas desea simular o registrar.
```python
def paso_3(
    capital: float = Form(...),
    precio_casa: float = Form(...),
    costo_casa: float = Form(...),
    empleados: int = Form(...),
    salario: float = Form(...)
):
    storage.temp.update({
        "capital": capital,
        "precio_casa": precio_casa,
        "costo_casa": costo_casa,
        "empleados": empleados,
        "salario": salario
    })
    return """
    <html><body>
    <h2>Paso 3: ¿Cuántas semanas deseas registrar?</h2>
    <form action="/paso4" method="post">
        Número de semanas: <input type="number" name="semanas" min="1" required><br>
        <button type="submit">Siguiente</button>
    </form>
    </body></html>
    """
@router.post("/paso4", response_class=HTMLResponse)
```
#### PASO 4: Registro semanal de casas construidas y vendidas, Y Formulario de control de empleados
- recoge los datos semanales del proyecto sobre cuántas casas fueron construidas y vendidas, y prepara un nuevo formulario para ingresar la actividad semanal de cada empleado asalariado (horas extra y faltas).
```python
async def paso_5(request: Request):
    form = await request.form()
    datos = storage.temp
    semanas = datos["semanas"]
    empleados = datos["empleados"]

    # Guardar los datos semanales en una lista
    datos["semanal"] = []
    for i in range(semanas):
        casas_construidas = int(form[f"casas_construidas_{i}"])
        casas_vendidas = int(form[f"casas_vendidas_{i}"])
        datos["semanal"].append({
            "casas_construidas": casas_construidas,
            "casas_vendidas": casas_vendidas
        })

    # Preparar formulario para siguiente paso (horas extra y faltas por semana y empleado)
    html = "<html><body><h2>Paso 5: Horas extra y faltas por empleado por semana</h2>"
    html += "<form action='/paso6' method='post'>"
    for semana in range(semanas):
        html += f"<h3>Semana {semana+1}</h3>"
        html += f"Empleados asalariados esta semana: {empleados}<br>"
        for e in range(empleados):
            html += (
                f"Empleado {e+1} horas extra: <input type='number' name='horas_extra_{semana}_{e}' min='0' max='9' required> "
                f"Faltas: <input type='number' name='faltas_{semana}_{e}' min='0' max='2' required><br>"
            )
        html += "<br>"
    html += "<button type='submit'>Siguiente</button></form></body></html>"
    return html
@router.post("/paso6", response_class=HTMLResponse)
```
#### PASO 5: Registro de horas extra y faltas, Definición de contratistas y comisiones
- Se toma la información ingresada en el formulario anterior y la estructura para cada semana y cada empleado asalariado. Luego, se presenta un nuevo formulario para definir el modelo de comisiones y la cantidad de contratistas (maestros de obra y vendedores).

1. horas extra y faltas
```python
async def paso_6(request: Request):
    form = await request.form()
    datos = storage.temp
    semanas = datos["semanas"]
    empleados = datos["empleados"]

    # Guardar datos de horas extra y faltas
    datos["horas_extra_faltas"] = []
    for semana in range(semanas):
        semana_data = []
        for e in range(empleados):
            horas_extra = int(form.get(f"horas_extra_{semana}_{e}", 0))
            faltas = int(form.get(f"faltas_{semana}_{e}", 0))
            semana_data.append({"horas_extra": horas_extra, "faltas": faltas})
        datos["horas_extra_faltas"].append(semana_data)
```
2. Formulario: Contratistas y comisiones
```python
    # Preguntar por comisiones y número de contratistas
    return """
    <html><body>
    <h2>Paso 6: Contratistas y comisiones</h2>
    <form action="/paso7" method="post">
        % Maestro por casa construida: <input type="number" name="porcentaje_maestro" step="0.01" required><br>
        % Vendedor por casa vendida: <input type="number" name="porcentaje_vendedor" step="0.01" required><br>
        Cantidad de maestros de obra: <input type="number" name="maestros" min="1" required><br>
        Cantidad de vendedores: <input type="number" name="vendedores" min="1" required><br>
        <button type="submit">Siguiente</button>
    </form>
    </body></html>
    """
@router.post("/paso7", response_class=HTMLResponse)
```
#### PASO 7: Registro de casas construidas y vendidas por contratistas
- Finaliza la recopilación de datos solicitando cuántas casas construyó cada maestro de obra y cuántas casas vendió cada vendedor por semana. Se guarda en la variable temporal (storage.temp) los porcentajes de comisión y la cantidad de contratistas.

1. Proceso de comisiones y contratistas
```python
def paso_7(
    porcentaje_maestro: float = Form(...),
    porcentaje_vendedor: float = Form(...),
    maestros: int = Form(...),
    vendedores: int = Form(...)
):
    storage.temp["porcentaje_maestro"] = porcentaje_maestro
    storage.temp["porcentaje_vendedor"] = porcentaje_vendedor
    storage.temp["maestros"] = maestros
    storage.temp["vendedores"] = vendedores
```
2. Casas construidas y vendidas por contratista
```python
    semanas = storage.temp["semanas"]
    html = "<html><body><h2>Paso 7: Casas construidas/vendidas por contratista</h2>"
    html += "<form action='/guardar' method='post'>"
    for semana in range(semanas):
        html += f"<h3>Semana {semana+1}</h3>"
        html += "<b>Maestros de obra:</b><br>"
        for m in range(maestros):
            nombre = nombres_maestros[m % len(nombres_maestros)]
            html += f"{nombre} - Casas construidas: <input type='number' name='casas_maestro_{semana}_{m}' min='0' required><br>"
        html += "<b>Vendedores:</b><br>"
        for v in range(vendedores):
            nombre = nombres_vendedores[v % len(nombres_vendedores)]
            html += f"{nombre} - Casas vendidas: <input type='number' name='casas_vendedor_{semana}_{v}' min='0' required><br>"
        html += "<br>"
    html += "<button type='submit'>Guardar todo</button></form></body></html>"
    return html
@router.post("/guardar", response_class=HTMLResponse)
```
- Genera un formulario dinámico con campos para cada semana y contratista:

  - Lista a los maestros de obra con un campo para el número de casas construidas.

  - Lista a los vendedores con un campo para el número de casas vendidas.

#### PASO 8: Consolidación y Cálculo de Resultados
- Este paso toma toda la información recolectada durante los formularios anteriores y calcula:

     - Costos de salarios de empleados asalariados.

     - Bonificaciones por horas extra.

     - Descuentos por faltas.

     - Comisiones a maestros de obra y vendedores.

     - Rentabilidad del proyecto por semana y total
```python
async def guardar_final(request: Request):
    form = await request.form()
    datos = storage.temp
    semanas = datos["semanas"]
    empleados = datos["empleados"]
    salario = datos["salario"]
    maestros = datos["maestros"]
    vendedores = datos["vendedores"]
    porcentaje_maestro = datos["porcentaje_maestro"]
    porcentaje_vendedor = datos["porcentaje_vendedor"]
    precio_casa = datos["precio_casa"]
    costo_casa = datos["costo_casa"]
```
- Carga desde storage.temp todos los datos necesarios para los cálculos:

     - Parámetros del proyecto.

     - Datos recolectados en los pasos anteriores.

     - Información ingresada sobre contratistas.

#### PASO 9: nómina para empleados

- resumen detallado de los salarios semanales para cada empleado asalariado, considerando:
  
  -  Sueldo base.
  
  - Bonificación por horas extra.
    
  - Descuento por faltas.
```python
# MiniDataset empleados
mini_datasets = []
nominas_semanales = []

for semana in range(semanas):
    mini_data = []
    nomina_total = 0
    for e in range(empleados):
        nombre = nombres_empleados[e % len(nombres_empleados)]
        apellido = apellidos[e % len(apellidos)]

        horas_extra = datos["horas_extra_faltas"][semana][e]["horas_extra"]
        faltas = datos["horas_extra_faltas"][semana][e]["faltas"]
        total_empleado = salario
        pago_hora_extra = salario / 40 * 2
        total_empleado += horas_extra * pago_hora_extra
        descuento_falta = salario / 5
        total_empleado -= faltas * descuento_falta

        mini_data.append({
            "Nombre": nombre,
            "Apellido": apellido,
            "Horas extra": horas_extra,
            "Faltas": faltas,
            "Total": round(total_empleado, 2)
        })
        nomina_total += total_empleado

    mini_datasets.append(mini_data)
    nominas_semanales.append(round(nomina_total, 2))
```
- FUNCIÓN: 
    - Itera por cada semana registrada.

    - Para cada empleado:

       1. Genera nombre y apellido de forma cíclica desde listas predefinidas.

       2. Calcula su salario con:

            - Horas extra bonificadas al doble de la tarifa normal por hora.

            - Faltas con descuento equivalente a 1 día laboral.

            - Guarda el detalle por empleado.

            - Suma el total semanal de la nómina y lo guarda en nominas_semanales
         
#### PASO 10: Comisiones para contratistas - MiniDataset para contratistas (parte Maestros de obra)
- Generar un resumen semanal del pago a contratistas (maestros de obra y vendedores), considerando:

     - Comisión por casas construidas o vendidas.

     - Descuento del costo de construcción para los maestros de obra.
```python
# MiniDataset contratistas
mini_contratistas = []
contratista_totales_semanales = []

for semana in range(semanas):
    semana_contratistas = []
    total_contratistas = 0

    # Maestros de obra
    for m in range(maestros):
        nombre = nombres_maestros[m % len(nombres_maestros)]
        casas_construidas = int(form.get(f"casas_maestro_{semana}_{m}", 0))
        tipo = "Maestro de obra"
        porcentaje = porcentaje_maestro
        casas = casas_construidas
        total = casas_construidas * ((porcentaje / 100) * precio_casa)
        total -= casas_construidas * costo_casa  # descontar el costo de construir casa
        semana_contratistas.append({
            "Nombre": nombre,
            "Tipo": tipo,
            "Porcentaje comisión": f"{porcentaje}%",
            "Casas": casas,
            "Total": round(total, 2)
        })
        total_contratistas += total
```
- FUNCIÓN:
  
1. Itera por cada semana registrada.

2. Para cada maestro de obra:

    - Asigna nombre cíclico desde nombres_maestros.

    - Toma las casas construidas que se ingresaron en formularios anteriores.

    - Calcula la comisión:

       - Gana un porcentaje del precio de venta por cada casa construida.

       - Se descuenta el costo de construcción por cada casa (no es ganancia neta).

3. Guarda los datos individuales y suma el total de pagos a maestros de obra por semana.

##### Resultado parcial:
```JSON
{
  "Nombre": "Ana",
  "Tipo": "Maestro de obra",
  "Porcentaje comisión": "10%",
  "Casas": 4,
  "Total": 8000.0
}
```
#### PASO 11: MiniDataset para contratistas (parte Vendedores)
```python
# Vendedores
for v in range(vendedores):
    nombre = nombres_vendedores[v % len(nombres_vendedores)]
    casas_vendidas = int(form.get(f"casas_vendedor_{semana}_{v}", 0))
    tipo = "Vendedor"
    porcentaje = porcentaje_vendedor
    casas = casas_vendidas
    total = casas_vendidas * (precio_casa - (porcentaje / 100) * precio_casa - (porcentaje_maestro / 100) * precio_casa)
    semana_contratistas.append({
        "Nombre": nombre,
        "Tipo": tipo,
        "Porcentaje comisión": f"{porcentaje}%",
        "Casas": casas,
        "Total": round(total, 2)
    })
    total_contratistas += total

mini_contratistas.append(semana_contratistas)
contratista_totales_semanales.append(round(total_contratistas, 2))
```
- FUNCIÓN:

1. Itera por cada vendedor en cada semana.

2. Asigna un nombre cíclico desde nombres_vendedores.

3. Recupera cuántas casas vendió el vendedor esa semana.

4. Calcula el total generado:

    - Se parte del precio de cada casa vendida.

    - Se descuenta el porcentaje de comisión del vendedor.

    - También se descuenta el porcentaje del maestro, porque ese valor ya se pagó por construcción y no se cuenta como ganancia para el proyecto.

5. Se agrega un resumen con el nombre, tipo, porcentaje, casas y total.

6. El monto se suma al total de contratistas de la semana.

##### RESULTADO FINAL POR SEMANA
```JSON
[
  {
    "Nombre": "Mateo",
    "Tipo": "Vendedor",
    "Porcentaje comisión": "5%",
    "Casas": 3,
    "Total": 25500.0
  },
  ...
]
```

#### PASO 12: Datos Semanales en el Dataset
```python
for semana in range(semanas):
    casas_construidas = datos["semanal"][semana]["casas_construidas"]
    casas_vendidas = datos["semanal"][semana]["casas_vendidas"]
    fila = {
        "empresa": datos["empresa"],
        "proyecto": datos["proyecto"],
        "semana": semana + 1,
        "empleados": empleados,
        "casas_construidas": casas_construidas,
        "casas_vendidas": casas_vendidas,
        "horas_extra": sum([emp["Horas extra"] for emp in mini_datasets[semana]]),
        "nomina": nominas_semanales[semana],
        "contratistas": contratista_totales_semanales[semana]
    }
    service.agregar_datos(fila)
```
- FUNCIÓN:
1. Recorre cada semana del proyecto.

2. Crea una fila resumida con toda la información clave de esa semana:

    - Nombre de la empresa y del proyecto.

    - Número de semana.

    - Total de empleados asalariados.

    - Casas construidas y vendidas.

    - Suma de todas las horas extra de empleados.

    - Total de la nómina semanal (sueldos y horas extra).

    - Total pagado a contratistas (maestros + vendedores).

3. Finalmente, guarda esta fila usando service.agregar_datos.

#### PASO 13: Almacenamiento de MiniDatasets
```python
# Guardar los mini datasets por semana para visualización
storage.temp["mini_datasets"] = mini_datasets
storage.temp["mini_contratistas"] = mini_contratistas

return """
<html><body>
<h3>Datos guardados correctamente</h3>
<a href="/">Volver</a> | <a href="/tabla">Ver dataset principal</a> |
<a href="/mini_tabla">Ver miniDataset empleados</a> |
<a href="/mini_contratistas">Ver miniDataset contratistas</a>
</body></html>
"""

@router.get("/tabla", response_class=HTMLResponse)
```
- FUNCIÓN:
1. Guarda los dos MiniDatasets en la memoria temporal (storage.temp) para permitir su visualización:

     - mini_datasets: detalle de sueldos, horas extra y faltas por empleado, semana a semana.

     - mini_contratistas: detalle de casas construidas/vendidas y comisiones para contratistas.

2. Devuelve una página HTML que confirma que los datos han sido almacenados correctamente.

3. Ofrece enlaces rápidos para:

    - Volver al inicio.

    - Ver el dataset principal (resumen semanal general).

    - Ver el miniDataset de empleados.

    - Ver el miniDataset de contratistas.

#### PASO 14: Visualización del Dataset Principal
```python
def ver_tabla():
    if not service.hay_datos():
        return "<h3>No hay datos guardados</h3><a href='/'>Volver</a>"
    df_html = service.obtener_datos().to_html(index=False)
    return f"""
    <html><body>
    <h2>Datos guardados</h2>
    {df_html}
    <br><a href="/">Volver</a> | <a href="/grafica">Ver gráfica</a> |
    <a href="/mini_tabla">Ver miniDataset empleados</a> |
    <a href="/mini_contratistas">Ver miniDataset contratistas</a>
    </body></html>
    """

@router.get("/mini_tabla", response_class=HTMLResponse)
```
- FUNCIÓN:

1. Verifica si hay datos guardados en el sistema usando service.hay_datos().

2. Si no hay datos, informa al usuario con un mensaje.

3. Si hay datos:

   - Obtiene el DataFrame con la información consolidada.

   - Lo convierte a una tabla HTML (to_html()).

   - Muestra dicha tabla en el navegador.

4. Incluye enlaces para:

   - Volver a la pantalla inicial.

   - Ver una gráfica resumen.

   - Acceder a los miniDatasets de empleados y contratistas.

#### PASO 15: Visualización del MiniDataset de Empleados
```python
def ver_mini_tabla():
    mini_datasets = storage.temp.get("mini_datasets")
    if not mini_datasets:
        return "<h3>No hay miniDataset guardado</h3><a href='/'>Volver</a>"
    html = "<html><body><h2>Mini Dataset por semana (Empleados)</h2>"
    for semana, mini_data in enumerate(mini_datasets):
        html += f"<h3>Semana {semana+1}</h3>"
        df = pd.DataFrame(mini_data)
        html += df.to_html(index=False)
        html += "<br>"
    html += "<a href='/'>Volver</a> | <a href='/tabla'>Ver dataset principal</a> | <a href='/mini_contratistas'>Ver miniDataset contratistas</a></body></html>"
    return html

@router.get("/mini_contratistas", response_class=HTMLResponse)
```
- FUNCIÓN:

1. Recupera el mini dataset semanal de empleados almacenado en storage.temp["mini_datasets"].

2. Si no hay datos, muestra un mensaje informando que no hay registros.

3. Si existen:

   - Recorre cada semana del proyecto.

   - Convierte los datos semanales a un DataFrame (pandas).

   - Muestra una tabla HTML por cada semana.
  
#### PASO 16: Visualización del MiniDataset de Contratistas
```python
def ver_mini_contratistas():
    mini_contratistas = storage.temp.get("mini_contratistas")
    if not mini_contratistas:
        return "<h3>No hay miniDataset de contratistas guardado</h3><a href='/'>Volver</a>"
    html = "<html><body><h2>Mini Dataset por semana (Contratistas)</h2>"
    for semana, mini_data in enumerate(mini_contratistas):
        html += f"<h3>Semana {semana+1}</h3>"
        df = pd.DataFrame(mini_data)
        html += df.to_html(index=False)
        html += "<br>"
    html += "<a href='/'>Volver</a> | <a href='/tabla'>Ver dataset principal</a> | <a href='/mini_tabla'>Ver miniDataset empleados</a></body></html>"
    return html

@router.get("/grafica")
```
- FUNCIÓN:

1. Recupera el dataset temporal mini_contratistas desde la memoria (storage.temp).

2. Si no hay datos, informa que no se ha guardado nada aún.

3. Si existen datos:

   - Recorre cada semana registrada.

   - Convierte los datos de contratistas a tablas con pandas.

   - Renderiza cada semana como una tabla HTML separada.

#### PASO 17: 
```python
def ver_grafica():
    if not service.hay_datos():
        return HTMLResponse("<h3>No hay datos para graficar</h3><a href='/'>Volver</a>")
    buf = service.generar_grafica()
    return StreamingResponse(buf, media_type="image/png")
```
- FUNCIÓN:
1. Verifica si hay datos registrados en el sistema mediante service.hay_datos().

2. Si no hay información, muestra un mensaje de advertencia al usuario.

3. Si sí hay datos, llama a service.generar_grafica(), que devuelve una imagen de la gráfica en formato binario (un BytesIO).

4. Devuelve la gráfica como una imagen PNG directamente en el navegador usando StreamingResponse.







