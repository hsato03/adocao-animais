from model.vacina import Vacina
from datetime import date


class HistoricoVacinacao:
    def __init__(self):
        self.__vacinas = []

    @property
    def vacinas(self):
        return self.__vacinas

    def add_vacina(self, vacina: Vacina, data_aplicacao: date):
        self.__vacinas.append({"vacina": vacina, "data_aplicacao": data_aplicacao})
