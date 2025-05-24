# storage/file_storage.py
import pandas as pd

class MemoryStorage:
    def __init__(self):
        self.df = pd.DataFrame(columns=[
            "empresa", "proyecto", "semana", "empleados",
            "casas_construidas", "ganancia_maestro",
            "casas_vendidas", "ganancia_vendedor",
            "horas_extra", "nomina", "total"
        ])
        self.temp = {}

    def add_row(self, data: dict):
        self.df = pd.concat([self.df, pd.DataFrame([data])], ignore_index=True)

    def get_all(self):
        return self.df

    def is_empty(self):
        return self.df.empty
