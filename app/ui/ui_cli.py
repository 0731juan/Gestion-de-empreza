from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from app.storage.file_storage import MemoryStorage
from app.service.task_service import DataService

router = APIRouter()
storage = MemoryStorage()
service = DataService(storage)

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
        % Maestro por casa construida: <input type="number" name="porcentaje_maestro" step="0.01" required><br>
        % Vendedor por casa vendida: <input type="number" name="porcentaje_vendedor" step="0.01" required><br>
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
    salario: float = Form(...),
    porcentaje_maestro: float = Form(...),
    porcentaje_vendedor: float = Form(...)
):
    storage.temp.update({
        "capital": capital,
        "precio_casa": precio_casa,
        "costo_casa": costo_casa,
        "empleados": empleados,
        "salario": salario,
        "porcentaje_maestro": porcentaje_maestro,
        "porcentaje_vendedor": porcentaje_vendedor
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
    html = "<html><body><h2>Paso 4: Datos por semana</h2><form action='/guardar' method='post'>"
    for i in range(semanas):
        html += f"""
        <h3>Semana {i+1}</h3>
        Casas construidas: <input type="number" name="casas_construidas_{i}" required><br>
        Casas vendidas: <input type="number" name="casas_vendidas_{i}" required><br>
        Horas extra: <input type="number" name="horas_extra_{i}" required><br><br>
        """
    html += "<button type='submit'>Guardar todo</button></form></body></html>"
    return html

@router.post("/guardar", response_class=HTMLResponse)
async def guardar_final(request: Request):
    form = await request.form()
    datos = storage.temp
    semanas = datos["semanas"]

    for i in range(semanas):
        casas_construidas = int(form[f"casas_construidas_{i}"])
        casas_vendidas = int(form[f"casas_vendidas_{i}"])
        horas_extra = int(form[f"horas_extra_{i}"])
        nomina = datos["empleados"] * datos["salario"]

        fila = {
            "empresa": datos["empresa"],
            "proyecto": datos["proyecto"],
            "semana": i + 1,
            "empleados": datos["empleados"],
            "casas_construidas": casas_construidas,
            "casas_vendidas": casas_vendidas,
            "horas_extra": horas_extra,
            "nomina": nomina
        }
        service.agregar_datos(fila)

    return """
    <html><body>
    <h3>Datos guardados correctamente</h3>
    <a href="/">Volver</a> | <a href="/tabla">Ver tabla</a>
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
    <br><a href="/">Volver</a> | <a href="/grafica">Ver gráfica</a>
    </body></html>
    """

@router.get("/grafica")
def ver_grafica():
    if not service.hay_datos():
        return HTMLResponse("<h3>No hay datos para graficar</h3><a href='/'>Volver</a>")
    buf = service.generar_grafica()
    return StreamingResponse(buf, media_type="image/png")
