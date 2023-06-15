from .generic_dao import GenericDAO
from model import Doador


class DoadorDAO(GenericDAO):
    def __init__(self, datasource=''):
        super().__init__(datasource)

    def insert(self, doador: Doador):
        if isinstance(doador, Doador) and doador is not None:
            super().insert(doador.cpf, doador)

    def update(self, cpf: str, doador: Doador):
        if isinstance(doador, Doador) and doador is not None:
            super().update(cpf, doador.cpf, doador)
            return doador
