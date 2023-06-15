from .generic_dao import GenericDAO
from model import Doacao


class DoacaoDAO(GenericDAO):
    def __init__(self, datasource=""):
        super().__init__(datasource)

    def insert(self, doacao: Doacao):
        if isinstance(doacao, Doacao) and doacao is not None:
            super().insert(doacao.animal.numero_chip, doacao)

    def update(self, numero_chip: int, doacao: Doacao):
        if isinstance(doacao, Doacao) and doacao is not None:
            super().update(numero_chip, doacao.animal.numero_chip, doacao)
