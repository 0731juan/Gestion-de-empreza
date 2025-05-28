from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from app.storage.file_storage import MemoryStorage
from app.service.task_service import DataService
import pandas as pd
import base64

router = APIRouter()
storage = MemoryStorage()
service = DataService(storage)

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

def img_html(buf, title):
    buf.seek(0)
    img_bytes = buf.read()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return f"""
    <div class="grafica-container">
        <h3>{title}</h3>
        <img src="data:image/png;base64,{img_base64}">
    </div>
    """

@router.get("/", response_class=HTMLResponse)
def paso_1():
    return """
    <html>
    <head>
        <title>Olvídate de los recibos en papel</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="form-step">
            <div class="paso1-title">
                <span>Olvídate de los recibos en papel<div class="underline"></div></span>
            </div>
            <div class="paso1-desc">
                Esta aplicación <span class="paso1-appname">Gastos y finanzas construcciones</span> mantiene tu empresa constructora organizada.
            </div>
            <form action="/paso2" method="post">
                <label>Empresa:</label>
                <input type="text" name="empresa" required>
                <label>Proyecto:</label>
                <input type="text" name="proyecto" required>
                <button type="submit">Siguiente</button>
            </form>
        </div>
    </body>
    </html>
    """

@router.post("/paso2", response_class=HTMLResponse)
def paso_2(empresa: str = Form(...), proyecto: str = Form(...)):
    storage.temp = {"empresa": empresa, "proyecto": proyecto}
    return """
    <html>
    <head><link rel="stylesheet" href="/static/style.css"></head>
    <body>
    <div class="form-step">
    <h2>Paso 2: Detalles del proyecto</h2>
    <form action="/paso3" method="post">
        <label>Inversión inicial:</label>
        <input type="number" name="capital" step="0.01" required>
        <label>Precio de cada casa:</label>
        <input type="number" name="precio_casa" step="0.01" required>
        <label>Costo construir casa:</label>
        <input type="number" name="costo_casa" step="0.01" required>
        <label>Empleados asalariados:</label>
        <input type="number" name="empleados" required>
        <label>Salario semanal por empleado:</label>
        <input type="number" name="salario" step="0.01" required>
        <button type="submit">Siguiente</button>
    </form>
    </div>
    </body>
    </html>
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
    <html>
    <head><link rel="stylesheet" href="/static/style.css"></head>
    <body>
    <div class="form-step">
    <h2>Paso 3: ¿Cuántas semanas deseas registrar?</h2>
    <form action="/paso5" method="post">
        <label>Número de semanas:</label>
        <input type="number" name="semanas" min="1" required>
        <button type="submit">Siguiente</button>
    </form>
    </div>
    </body>
    </html>
    """

@router.post("/paso5", response_class=HTMLResponse)
def paso_5(semanas: int = Form(...)):
    storage.temp["semanas"] = semanas
    empleados = storage.temp["empleados"]
    html = """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
        <title>Paso 5 | Gastos y Finanzas Construcciones</title>
    </head>
    <body>
    <div class="form-step">
    <h2 class="step-title">Paso 5: Horas extra y faltas</h2>
    <div class="subtitle">Ingresa las horas extra y faltas de cada empleado para cada semana.</div>
    <form action='/paso6' method='post'>
    """
    for semana in range(semanas):
        html += f"<h3>Semana {semana+1}</h3>"
        html += f"<div class='extra'>Empleados asalariados esta semana: {empleados}</div>"
        for e in range(empleados):
            html += (
                f"<label>Empleado {e+1} horas extra:</label> <input type='number' name='horas_extra_{semana}_{e}' min='0' max='9' required> "
                f"<label>Faltas:</label> <input type='number' name='faltas_{semana}_{e}' min='0' max='2' required><br>"
            )
        html += "<br>"
    html += "<button type='submit'>Siguiente</button></form></div></body></html>"
    return html

@router.post("/paso6", response_class=HTMLResponse)
async def paso_6(request: Request):
    form = await request.form()
    datos = storage.temp
    semanas = datos["semanas"]
    empleados = datos["empleados"]

    datos["horas_extra_faltas"] = []
    for semana in range(semanas):
        semana_data = []
        for e in range(empleados):
            horas_extra = int(form.get(f"horas_extra_{semana}_{e}", 0))
            faltas = int(form.get(f"faltas_{semana}_{e}", 0))
            semana_data.append({"horas_extra": horas_extra, "faltas": faltas})
        datos["horas_extra_faltas"].append(semana_data)

    return """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
        <title>Paso 6 | Gastos y Finanzas Construcciones</title>
    </head>
    <body>
    <div class="form-step">
    <h2 class="step-title">Paso 6: Contratistas y comisiones</h2>
    <div class="subtitle">Configura los porcentajes y la cantidad de contratistas del proyecto.</div>
    <form action="/paso7" method="post">
        <label>% Maestro por casa construida:</label>
        <input type="number" name="porcentaje_maestro" step="0.01" required>
        <label>% Vendedor por casa vendida:</label>
        <input type="number" name="porcentaje_vendedor" step="0.01" required>
        <label>Cantidad de maestros de obra:</label>
        <input type="number" name="maestros" min="1" required>
        <label>Cantidad de vendedores:</label>
        <input type="number" name="vendedores" min="1" required>
        <button type="submit">Siguiente</button>
    </form>
    </div>
    </body>
    </html>
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
    html = """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
        <title>Paso 7 | Gastos y Finanzas Construcciones</title>
    </head>
    <body>
    <div class="form-step">
    <h2 class="step-title">Paso 7: Casas construidas/vendidas por contratista</h2>
    <div class="subtitle">Ingresa la cantidad de casas construidas y vendidas por cada contratista por semana.</div>
    <form action='/guardar' method='post'>
    """
    for semana in range(semanas):
        html += f"<h3>Semana {semana+1}</h3>"
        html += "<div class='extra'><b>Maestros de obra:</b></div>"
        for m in range(maestros):
            nombre = nombres_maestros[m % len(nombres_maestros)]
            html += f"<label>{nombre} - Casas construidas:</label> <input type='number' name='casas_maestro_{semana}_{m}' min='0' required><br>"
        html += "<div class='extra'><b>Vendedores:</b></div>"
        for v in range(vendedores):
            nombre = nombres_vendedores[v % len(nombres_vendedores)]
            html += f"<label>{nombre} - Casas vendidas:</label> <input type='number' name='casas_vendedor_{semana}_{v}' min='0' required><br>"
        html += "<br>"
    html += "<button type='submit'>Guardar todo</button></form></div></body></html>"
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

    mini_contratistas = []
    contratista_totales_semanales = []
    casas_construidas_semanal = []
    casas_vendidas_semanal = []
    for semana in range(semanas):
        semana_contratistas = []
        total_contratistas = 0
        total_casas_maestros = 0
        total_casas_vendedores = 0
        for m in range(maestros):
            nombre = nombres_maestros[m % len(nombres_maestros)]
            casas_construidas = int(form.get(f"casas_maestro_{semana}_{m}", 0))
            tipo = "Maestro de obra"
            porcentaje = porcentaje_maestro
            casas = casas_construidas
            total = casas_construidas * ((porcentaje / 100) * precio_casa)
            total -= casas_construidas * costo_casa
            semana_contratistas.append({
                "Nombre": nombre,
                "Tipo": tipo,
                "Porcentaje comisión": f"{porcentaje}%",
                "Casas": casas,
                "Total": round(total, 2)
            })
            total_contratistas += total
            total_casas_maestros += casas
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
            total_casas_vendedores += casas
        mini_contratistas.append(semana_contratistas)
        contratista_totales_semanales.append(round(total_contratistas, 2))
        casas_construidas_semanal.append(total_casas_maestros)
        casas_vendidas_semanal.append(total_casas_vendedores)

    for semana in range(semanas):
        fila = {
            "empresa": datos["empresa"],
            "proyecto": datos["proyecto"],
            "semana": semana + 1,
            "empleados": empleados,
            "casas_construidas": casas_construidas_semanal[semana],
            "ganancia_maestro": casas_construidas_semanal[semana] * (porcentaje_maestro / 100 * precio_casa),
            "casas_vendidas": casas_vendidas_semanal[semana],
            "ganancia_vendedor": casas_vendidas_semanal[semana] * (porcentaje_vendedor / 100 * precio_casa),
            "horas_extra": sum([emp["Horas extra"] for emp in mini_datasets[semana]]),
            "nomina": nominas_semanales[semana],
            "contratistas": contratista_totales_semanales[semana]
        }
        service.agregar_datos(fila)
    storage.temp["mini_datasets"] = mini_datasets
    storage.temp["mini_contratistas"] = mini_contratistas
    return """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <div class="form-step">
    <h3 class="message-ok">Datos guardados correctamente</h3>
    <a class="btn" href="/">Volver</a> | <a class="btn-secondary" href="/tabla">Ver dataset principal</a> | <a class="btn-secondary" href="/mini_tabla">Ver miniDataset empleados</a> | <a class="btn-secondary" href="/mini_contratistas">Ver miniDataset contratistas</a>
    </div>
    </body>
    </html>
    """
@router.get("/tabla", response_class=HTMLResponse)
def ver_tabla():
    if not service.hay_datos():
        return "<h3>No hay datos guardados</h3><a href='/'>Volver</a>"
    df = service.obtener_datos()
    if df.empty:
        return "<h3>No hay datos guardados</h3><a href='/'>Volver</a>"
    cols = list(df.columns)
    if 'contratistas' in cols and 'total' in cols:
        cols.remove('contratistas')
        cols.remove('total')
        cols = cols + ['contratistas', 'total']
    html = """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
        <title>Datos guardados</title>
    </head>
    <body>
    <div class="table-container">
    <h2>Datos guardados</h2>
    <table>
        <thead><tr>
    """
    for col in cols:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in cols:
            if col == "total":
                clase = "positivo" if row[col] >= 0 else "negativo"
                html += f"<td class='{clase}'>{row[col]}</td>"
            else:
                html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    html += """
    <div class="botones-dataset">
        <a class="btn" href="/">Volver</a>
        <a class="btn-secondary" href="/graficas">Ver todas las gráficas</a>
        <a class="btn-secondary" href="/mini_tabla">Ver miniDataset empleados</a>
        <a class="btn-secondary" href="/mini_contratistas">Ver miniDataset contratistas</a>
        <a class="btn-finalizar" href="/finalizar">Finalizar programa</a>
    </div>
    </div>
    </body></html>
    """
    return HTMLResponse(html)
@router.get("/mini_tabla", response_class=HTMLResponse)
def ver_mini_tabla():
    mini_datasets = storage.temp.get("mini_datasets")
    if not mini_datasets:
        return "<h3>No hay miniDataset guardado</h3><a href='/'>Volver</a>"
    html = """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
        <title>Mini Dataset empleados</title>
    </head>
    <body>
    <div class="table-container">
    <h2>Mini Dataset por semana (Empleados)</h2>
    """
    for semana, mini_data in enumerate(mini_datasets):
        html += f"<h3>Semana {semana+1}</h3>"
        df = pd.DataFrame(mini_data)
        html += "<table><thead><tr>"
        for col in df.columns:
            html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                if col == "Total":
                    clase = "positivo" if row[col] >= 0 else "negativo"
                    html += f"<td class='{clase}'>{row[col]}</td>"
                else:
                    html += f"<td>{row[col]}</td>"
            html += "</tr>"
        html += "</tbody></table><br>"
    html += """
    <div>
        <a class='btn' href='/'>Volver</a>
        <a class='btn-secondary' href='/tabla'>Ver dataset principal</a>
        <a class='btn-secondary' href='/mini_contratistas'>Ver miniDataset contratistas</a>
    </div>
    <div style="margin-top: 22px;">
        <a class='btn-finalizar' href='/finalizar'>Finalizar programa</a>
    </div>
    </div></body></html>
    """
    return html

@router.get("/mini_contratistas", response_class=HTMLResponse)
def ver_mini_contratistas():
    mini_contratistas = storage.temp.get("mini_contratistas")
    if not mini_contratistas:
        return "<h3>No hay miniDataset de contratistas guardado</h3><a href='/'>Volver</a>"
    html = """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
        <title>Mini Dataset contratistas</title>
    </head>
    <body>
    <div class="table-container">
    <h2>Mini Dataset por semana (Contratistas)</h2>
    """
    for semana, mini_data in enumerate(mini_contratistas):
        html += f"<h3>Semana {semana+1}</h3>"
        df = pd.DataFrame(mini_data)
        html += "<table><thead><tr>"
        for col in df.columns:
            html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                if col == "Total":
                    clase = "positivo" if row[col] >= 0 else "negativo"
                    html += f"<td class='{clase}'>{row[col]}</td>"
                else:
                    html += f"<td>{row[col]}</td>"
            html += "</tr>"
        html += "</tbody></table><br>"
    html += """
    <div>
        <a class='btn' href='/'>Volver</a>
        <a class='btn-secondary' href='/tabla'>Ver dataset principal</a>
        <a class='btn-secondary' href='/mini_tabla'>Ver miniDataset empleados</a>
    </div>
    <div style="margin-top: 22px;">
        <a class='btn-finalizar' href='/finalizar'>Finalizar programa</a>
    </div>
    </div></body></html>
    """
    return html

@router.get("/grafica")
def ver_grafica():
    if not service.hay_datos():
        return HTMLResponse("<h3>No hay datos para graficar</h3><a href='/'>Volver</a>")
    buf = service.generar_grafica()
    return StreamingResponse(buf, media_type="image/png")

@router.get("/finalizar", response_class=HTMLResponse)
def finalizar_programa():
    html = """
    <html>
    <head>
        <title>Finalización</title>
        <link rel="stylesheet" href="/static/style.css">
        <style>
            body {
                /* Usa el fondo general de la app */
                background-image: url('/static/fondo.jpg');
                background-size: cover;
                background-position: center center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                margin: 0;
            }
            .fin-main-container {
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .fin-card1 {
                background: #274472;
                color: #fff;
                padding: 48px 38px 38px 44px;
                border-radius: 30px;
                max-width: 540px;
                box-shadow: 0 8px 32px #bbcbe4;
                position: relative;
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin: 30px;
            }
            .fin-card1 h2 {
                margin: 0 0 26px 0;
                font-size: 2.6em;
                font-family: 'Pacifico', 'Comic Sans MS', cursive, sans-serif;
                font-weight: 600;
                color: #16213E;
                letter-spacing: 0.02em;
                text-shadow: 0 2px 7px #e0eaff;
            }
            .fin-card1 p {
                font-size: 1.17em;
                margin-bottom: 22px;
                color: #e3eaf6;
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, 'Liberation Sans', sans-serif;
                font-weight: 400;
            }
            .fin-card1 .btn-aprende {
                display: inline-block;
                margin-top: 16px;
                padding: 13px 38px;
                background: transparent;
                border: 2.5px solid #e3eaf6;
                color: #e3eaf6;
                border-radius: 30px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.24em;
                letter-spacing: .10em;
                transition: background 0.2s, color 0.2s;
                text-align: center;
            }
            .fin-card1 .btn-aprende:hover {
                background: #e3eaf6;
                color: #274472;
            }
            .fin-card1 a {
                color: #a6d3d8;
                text-decoration: underline;
            }
            @media (max-width: 800px) {
                .fin-main-container {
                    padding: 12vw 0;
                }
                .fin-card1 {
                    max-width: 98vw;
                    width: 95vw;
                    margin: 12px;
                    padding: 28px 5vw 28px 5vw;
                }
            }
        </style>
    </head>
    <body>
        <div class="fin-main-container">
            <div class="fin-card1">
                <h2>¡Gracias por usar la app!</h2>
                <p>
                  Has finalizado el registro y visualización de tus datos de gestión de obra.<br>
                  Recuerda que puedes volver al inicio para comenzar un nuevo proceso o consultar las gráficas y datasets guardados.<br>
                  <br>
                  Imagen de <a href="https://www.freepik.com" target="_blank">Freepik</a>
                </p>
                <a class="btn-aprende" href="/">Volver al inicio</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html)
