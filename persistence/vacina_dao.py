from .generic_dao import GenericDAO
from model import Vacina


class VacinaDAO(GenericDAO):
    def __init__(self, datasource=""):
        super().__init__(datasource)

    def insert(self, vacina: Vacina):
        if isinstance(vacina, Vacina) and vacina is not None:
            super().insert(vacina.identificador, vacina)

    def find_by_id(self, identificador: int):
        return super().find_by_id(identificador)

    def update(self, identificador: int, vacina: Vacina):
        if isinstance(vacina, Vacina) and vacina is not None:
            super().update(identificador, vacina.identificador, vacina)
            return vacina

    def remove(self, identificador: int):
        return super().remove(identificador)
