import pandas as pd

class MemoryStorage:
    def __init__(self):
        self.df = pd.DataFrame(columns=[
            "empresa", "proyecto", "semana", "empleados",
            "casas_construidas", "ganancia_maestro",
            "casas_vendidas", "ganancia_vendedor",
            "horas_extra", "nomina", "contratistas", "total"
        ])
        self.temp = {}

    def add_row(self, data: dict):
        # Asegúrate de que data tenga todas las columnas, rellenando con None si falta alguna
        for col in self.df.columns:
            if col not in data:
                data[col] = None
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=self.df.columns)], ignore_index=True)

    def get_all(self):
        return self.df.copy()  # Devuelve una copia para evitar side effects

    def is_empty(self):
        return self.df.empty
