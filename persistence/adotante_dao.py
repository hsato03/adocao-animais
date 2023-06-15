from .generic_dao import GenericDAO
from model.adotante import Adotante


class AdotanteDAO(GenericDAO):
    def __init__(self, datasource=""):
        super().__init__(datasource)

    def add(self, adotante: Adotante):
        if isinstance(adotante, Adotante) and adotante is not None:
            super().add(adotante.cpf, adotante)

    def find_by_id(self, key):
        return super().find_by_id(key)

    def update(self, cpf, adotante):
        if isinstance(adotante, Adotante) and adotante is not None:
            super().remove(cpf)
            super().add(adotante.cpf, adotante)

    def remove(self, key):
        return super().remove(key)
