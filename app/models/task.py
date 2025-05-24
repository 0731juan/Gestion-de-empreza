# models/proyecto.py
class Proyecto:
    def __init__(self, empresa, proyecto, capital, presupuesto):
        self.empresa = empresa
        self.proyecto = proyecto
        self.capital = capital
        self.presupuesto = presupuesto

    def to_dict(self):
        return {
            "empresa": self.empresa,
            "proyecto": self.proyecto,
            "capital": self.capital,
            "presupuesto": self.presupuesto,
        }

    @staticmethod
    def from_dict(data: dict) -> "Proyecto":
        return Proyecto(
            empresa=data.get("empresa"),
            proyecto=data.get("proyecto"),
            capital=data.get("capital"),
            presupuesto=data.get("presupuesto"),
        )
