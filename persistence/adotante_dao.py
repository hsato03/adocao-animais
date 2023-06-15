from .generic_dao import GenericDAO
from model.adotante import Adotante


class AdotanteDAO(GenericDAO):
    def __init__(self, datasource=""):
        super().__init__(datasource)

    def insert(self, adotante: Adotante):
        if isinstance(adotante, Adotante) and adotante is not None:
            super().insert(adotante.cpf, adotante)

    def find_by_id(self, cpf: str):
        return super().find_by_id(cpf)

    def update(self, cpf: str, adotante: Adotante):
        if isinstance(adotante, Adotante) and adotante is not None:
            super().update(cpf, adotante.cpf, adotante)
            return adotante

    def remove(self, cpf: str):
        return super().remove(cpf)
