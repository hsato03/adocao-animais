from .generic_dao import GenericDAO
from model import Adocao


class AdocaoDAO(GenericDAO):
    def __init__(self, datasource=""):
        super().__init__(datasource)

    def insert(self, adocao: Adocao):
        if isinstance(adocao, Adocao) and adocao is not None:
            super().insert(adocao.animal.numero_chip, adocao)

    def update(self, numero_chip, adocao: Adocao):
        if isinstance(adocao, Adocao) and adocao is not None:
            super().update(numero_chip, adocao.animal.numero_chip, adocao)
