from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from app.storage.file_storage import MemoryStorage
from app.service.task_service import DataService
import random
import pandas as pd

router = APIRouter()
storage = MemoryStorage()
service = DataService(storage)

# Nombres y apellidos para los empleados
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

# Nombres para maestros de obra y vendedores
nombres_maestros = ["Ana", "Carlos", "Lucía", "Jose", "Valentina"]
nombres_vendedores = ["Mateo", "Isabella", "Sebastián", "Daniela", "Tomás"]

@router.get("/", response_class=HTMLResponse)
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
def paso_4(semanas: int = Form(...)):
    storage.temp["semanas"] = semanas
    html = "<html><body><h2>Paso 4: Datos por semana</h2><form action='/paso5' method='post'>"
    for i in range(semanas):
        html += f"""
        <h3>Semana {i+1}</h3>
        Casas construidas: <input type="number" name="casas_construidas_{i}" required><br>
        Casas vendidas: <input type="number" name="casas_vendidas_{i}" required><br>
        """
    html += "<button type='submit'>Siguiente</button></form></body></html>"
    return html

@router.post("/paso5", response_class=HTMLResponse)
async def paso_5(request: Request):
    form = await request.form()
    datos = storage.temp
    semanas = datos["semanas"]
    empleados = datos["empleados"]

    # Guardar datos de casas construidas y vendidas para cada semana en temp
    datos["semanal"] = []
    for i in range(semanas):
        casas_construidas = int(form[f"casas_construidas_{i}"])
        casas_vendidas = int(form[f"casas_vendidas_{i}"])
        datos["semanal"].append({
            "casas_construidas": casas_construidas,
            "casas_vendidas": casas_vendidas
        })

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

    # Guardar filas en el dataset principal
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

    # Guardar los mini datasets por semana para visualización
    storage.temp["mini_datasets"] = mini_datasets
    storage.temp["mini_contratistas"] = mini_contratistas

    return """
    <html><body>
    <h3>Datos guardados correctamente</h3>
    <a href="/">Volver</a> | <a href="/tabla">Ver dataset principal</a> | <a href="/mini_tabla">Ver miniDataset empleados</a> | <a href="/mini_contratistas">Ver miniDataset contratistas</a>
    </body></html>
    """

@router.get("/tabla", response_class=HTMLResponse)
def ver_tabla():
    if not service.hay_datos():
        return "<h3>No hay datos guardados</h3><a href='/'>Volver</a>"
    df_html = service.obtener_datos().to_html(index=False)
    return f"""
    <html><body>
    <h2>Datos guardados</h2>
    {df_html}
    <br><a href="/">Volver</a> | <a href="/grafica">Ver gráfica</a> | <a href="/mini_tabla">Ver miniDataset empleados</a> | <a href="/mini_contratistas">Ver miniDataset contratistas</a>
    </body></html>
    """

@router.get("/mini_tabla", response_class=HTMLResponse)
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
def ver_grafica():
    if not service.hay_datos():
        return HTMLResponse("<h3>No hay datos para graficar</h3><a href='/'>Volver</a>")
    buf = service.generar_grafica()
    return StreamingResponse(buf, media_type="image/png")
