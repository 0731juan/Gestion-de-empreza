import io
import matplotlib.pyplot as plt

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

        # Ganancias y costos
        costo_total_casas = data["casas_construidas"] * costo_casa
        ingreso_total_casas = data["casas_vendidas"] * precio_casa
        pago_maestro = data["casas_construidas"] * (porc_maestro * precio_casa)
        pago_vendedor = data["casas_vendidas"] * (porc_vendedor * precio_casa)

        gastos = data["nomina"] + costo_total_casas + pago_maestro + pago_vendedor + data.get("contratistas", 0)
        total = inversion - gastos + ingreso_total_casas
        self.storage.temp["capital"] = total  # Actualiza capital restante

        data["ganancia_maestro"] = pago_maestro
        data["ganancia_vendedor"] = pago_vendedor
        return total

    def obtener_datos(self):
        return self.storage.get_all()

    def hay_datos(self):
        return not self.storage.is_empty()

    def generar_grafica(self):
        df = self.storage.get_all()
        plt.figure(figsize=(8,5))
        plt.plot(df["semana"], df["total"], marker='o')
        plt.title("Capital restante por semana")
        plt.xlabel("Semana")
        plt.ylabel("Capital restante")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf