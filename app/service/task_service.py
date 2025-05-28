#service/task_service.py

import io
import matplotlib.pyplot as plt
import numpy as np

class DataService:
    def __init__(self, storage):
        self.storage = storage
        self.total = 0

    def agregar_datos(self, data):
        self.total = self.calcular_total(data)
        data["total"] = self.total
        self.storage.add_row(data)

    def calcular_total(self, data):
        inversion = self.storage.temp["capital"]
        costo_casa = self.storage.temp["costo_casa"]
        precio_casa = self.storage.temp["precio_casa"]
        porc_maestro = self.storage.temp["porcentaje_maestro"] / 100
        porc_vendedor = self.storage.temp["porcentaje_vendedor"] / 100

        costo_total_casas = data["casas_construidas"] * costo_casa
        ingreso_total_casas = data["casas_vendidas"] * precio_casa
        pago_maestro = data["casas_construidas"] * (porc_maestro * precio_casa)
        pago_vendedor = data["casas_vendidas"] * (porc_vendedor * precio_casa)

        gastos = data["nomina"] + costo_total_casas + pago_maestro + pago_vendedor + data.get("contratistas", 0)
        total = inversion - gastos + ingreso_total_casas
        self.storage.temp["capital"] = total

        data["ganancia_maestro"] = pago_maestro
        data["ganancia_vendedor"] = pago_vendedor
        return total

    def obtener_datos(self):
        return self.storage.get_all()

    def hay_datos(self):
        return not self.storage.is_empty()

    # --- GRAFICAS ---
    def grafica_capital(self):
        df = self.storage.get_all()
        if df.empty:
            return None
        buf = io.BytesIO()
        plt.figure(figsize=(8,5))
        plt.plot(df["semana"], df["total"], marker='o')
        plt.title("Capital restante por semana")
        plt.xlabel("Semana")
        plt.ylabel("Capital restante")
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_dispersion(self):
        df = self.storage.get_all()
        if df.empty:
            return None
        buf = io.BytesIO()
        plt.figure(figsize=(8,5))
        plt.scatter(df["casas_construidas"], df["casas_vendidas"], color="teal")
        plt.title("Dispersión: Casas construidas vs vendidas")
        plt.xlabel("Casas construidas")
        plt.ylabel("Casas vendidas")
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_empleados(self):
        mini_datasets = self.storage.temp.get("mini_datasets")
        if not mini_datasets:
            return None
        buf = io.BytesIO()
        totales = [sum(emp["Total"] for emp in semana) for semana in mini_datasets]
        semanas = list(range(1, len(totales)+1))
        plt.figure(figsize=(8,5))
        plt.bar(semanas, totales, color="mediumseagreen")
        plt.title("Total pagado a empleados por semana")
        plt.xlabel("Semana")
        plt.ylabel("Total pagado")
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_contratistas(self):
        mini_contratistas = self.storage.temp.get("mini_contratistas")
        if not mini_contratistas:
            return None
        personas = {}
        for semana in mini_contratistas:
            for c in semana:
                nombre = c["Nombre"]
                tipo = c["Tipo"]
                key = f"{nombre} ({tipo})"
                if key not in personas:
                    personas[key] = {"Casas":[], "Total":[]}
                personas[key]["Casas"].append(c["Casas"])
                personas[key]["Total"].append(c["Total"])
        nombres = list(personas.keys())
        casas = [sum(personas[n]["Casas"]) for n in nombres]
        promedios = [np.mean(personas[n]["Casas"]) for n in nombres]
        plt.figure(figsize=(12,6))
        plt.bar(nombres, casas, label="Casas", color="deepskyblue")
        plt.plot(nombres, promedios, label="Promedio casas/semana", color="black", marker="o")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Casas")
        plt.title("Casas construidas/vendidas y promedio por contratista")
        plt.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_boxplot_pagos_empleados(self):
        mini_datasets = self.storage.temp.get("mini_datasets")
        if not mini_datasets:
            return None
        datos = []
        for semana in mini_datasets:
            for emp in semana:
                datos.append(emp["Total"])
        plt.figure(figsize=(7, 5))
        plt.boxplot(datos, vert=True, patch_artist=True)
        plt.title("Boxplot: Pagos semanales a empleados")
        plt.ylabel("Pago semana")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return buf

    def grafica_boxplot_casas_contratista(self):
        mini_contratistas = self.storage.temp.get("mini_contratistas")
        if not mini_contratistas:
            return None
        casas = []
        for semana in mini_contratistas:
            for c in semana:
                if c["Tipo"] == "Maestro de obra":
                    casas.append(c["Casas"])
        plt.figure(figsize=(7, 5))
        plt.boxplot(casas, vert=True, patch_artist=True)
        plt.title("Boxplot: Casas construidas por contratista")
        plt.ylabel("Casas")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return buf

    def grafica_boxplot_horas_extra_empleado(self):
        mini_datasets = self.storage.temp.get("mini_datasets")
        if not mini_datasets:
            return None
        horas = []
        for semana in mini_datasets:
            for emp in semana:
                horas.append(emp["Horas extra"])
        plt.figure(figsize=(7, 5))
        plt.boxplot(horas, vert=True, patch_artist=True)
        plt.title("Boxplot: Horas extra por empleado")
        plt.ylabel("Horas extra")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return buf

    def grafica_barra_apilada_casas_semanal(self):
        mini_contratistas = self.storage.temp.get("mini_contratistas")
        if not mini_contratistas:
            return None
        semanas = len(mini_contratistas)
        casas_maestros = []
        casas_vendedores = []
        for semana in mini_contratistas:
            total_maestros = sum(c["Casas"] for c in semana if c["Tipo"] == "Maestro de obra")
            total_vendedores = sum(c["Casas"] for c in semana if c["Tipo"] == "Vendedor")
            casas_maestros.append(total_maestros)
            casas_vendedores.append(total_vendedores)
        x = np.arange(semanas)
        plt.figure(figsize=(9, 6))
        plt.bar(x, casas_maestros, label="Maestros de obra", color="royalblue")
        plt.bar(x, casas_vendedores, bottom=casas_maestros, label="Vendedores", color="orange")
        plt.xlabel("Semana")
        plt.ylabel("Casas")
        plt.title("Casas construidas y vendidas por semana (barra apilada)")
        plt.xticks(x, [f"Semana {i+1}" for i in x])
        plt.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return buf

    def grafica_barra_apilada_gastos_semanales(self):
        df = self.storage.get_all()
        if df.empty:
            return None
        semanas = df["semana"].values
        nomina = df["nomina"].values
        contratistas = df["contratistas"].values
        try:
            costo_casa = self.storage.temp["costo_casa"]
            casas_construidas = df["casas_construidas"].values
            materiales = casas_construidas * costo_casa
        except:
            materiales = np.zeros_like(nomina)
        plt.figure(figsize=(9,6))
        plt.bar(semanas, nomina, label="Nómina", color="skyblue")
        plt.bar(semanas, materiales, bottom=nomina, label="Materiales", color="gray")
        plt.bar(semanas, contratistas, bottom=nomina+materiales, label="Contratistas", color="coral")
        plt.xlabel("Semana")
        plt.ylabel("Gasto")
        plt.title("Gastos semanales (barra apilada)")
        plt.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return buf

    def grafica_histograma_pagos_empleados(self):
        mini_datasets = self.storage.temp.get("mini_datasets")
        if not mini_datasets:
            return None
        totales = []
        for semana_data in mini_datasets:
            for emp in semana_data:
                totales.append(emp["Total"])
        plt.figure(figsize=(8,5))
        plt.hist(totales, bins=10, color="skyblue", edgecolor="black")
        plt.xlabel("Total pagado (empleado semana)")
        plt.ylabel("Frecuencia")
        plt.title("Distribución de pagos a empleados por semana")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_histograma_casas_contratista(self):
        mini_contratistas = self.storage.temp.get("mini_contratistas")
        if not mini_contratistas:
            return None
        casas = []
        for semana in mini_contratistas:
            for c in semana:
                if c["Tipo"] == "Maestro de obra":
                    casas.append(c["Casas"])
        plt.figure(figsize=(8,5))
        plt.hist(casas, bins=10, color="violet", edgecolor="black")
        plt.xlabel("Casas construidas (maestro de obra)")
        plt.ylabel("Frecuencia")
        plt.title("Distribución de casas construidas por contratista")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_pie_maestros(self):
        mini_contratistas = self.storage.temp.get("mini_contratistas")
        if not mini_contratistas:
            return None
        maestros = {}
        for semana in mini_contratistas:
            for c in semana:
                if c["Tipo"] == "Maestro de obra":
                    maestros[c["Nombre"]] = maestros.get(c["Nombre"], 0) + c["Casas"]
        if not maestros:
            return None
        labels = list(maestros.keys())
        sizes = list(maestros.values())
        plt.figure(figsize=(7,7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Proporción de casas construidas por maestro de obra")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_pie_vendedores(self):
        mini_contratistas = self.storage.temp.get("mini_contratistas")
        if not mini_contratistas:
            return None
        vendedores = {}
        for semana in mini_contratistas:
            for c in semana:
                if c["Tipo"] == "Vendedor":
                    vendedores[c["Nombre"]] = vendedores.get(c["Nombre"], 0) + c["Casas"]
        if not vendedores:
            return None
        labels = list(vendedores.keys())
        sizes = list(vendedores.values())
        plt.figure(figsize=(7,7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Proporción de casas vendidas por vendedor")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_pie_gastos(self):
        df = self.storage.get_all()
        if df.empty:
            return None
        total_nomina = df["nomina"].sum()
        total_contratistas = df["contratistas"].sum()
        try:
            total_materiales = (df["casas_construidas"] * self.storage.temp["costo_casa"]).sum()
        except:
            total_materiales = 0
        restantes = max(self.storage.temp["capital"], 0)
        sizes = [total_nomina, total_contratistas, total_materiales, restantes]
        labels = ["Nómina", "Contratistas", "Materiales", "Restante"]
        plt.figure(figsize=(7,7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Proporción de gastos en el capital total")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def grafica_lineplot_multiple(self):
        df = self.storage.get_all()
        if df.empty:
            return None
        semanas = df["semana"].values
        capital = df["total"].values
        nomina = df["nomina"].values
        try:
            costo_casa = self.storage.temp["costo_casa"]
            casas_construidas = df["casas_construidas"].values
            materiales = casas_construidas * costo_casa
        except:
            materiales = np.zeros_like(nomina)
        contratistas = df["contratistas"].values
        ventas = df["casas_vendidas"].values
        plt.figure(figsize=(10,6))
        plt.plot(semanas, capital, marker='o', label="Capital")
        plt.plot(semanas, nomina, marker='o', label="Nómina")
        plt.plot(semanas, materiales, marker='o', label="Materiales")
        plt.plot(semanas, contratistas, marker='o', label="Contratistas")
        plt.plot(semanas, ventas, marker='o', label="Ventas")
        plt.title("Evolución de capital, nómina, gastos y ventas")
        plt.xlabel("Semana")
        plt.ylabel("Valor")
        plt.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf
