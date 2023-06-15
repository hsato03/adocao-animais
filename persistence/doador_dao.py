from .generic_dao import GenericDAO
from model import Doador


class DoadorDAO(GenericDAO):
    def __init__(self, datasource=''):
        super().__init__(datasource)

    def add(self, doador: Doador):
        if isinstance(doador, Doador) and doador is not None:
            super().add(doador.cpf, doador)

    def update(self, cpf, doador):
        if isinstance(doador, Doador) and doador is not None:
            super().remove(cpf)
            super().add(doador.cpf, doador)

    def find_by_id(self, cpf):
        return super().find_by_id(cpf)

    def remove(self, cpf):
        return super().remove(cpf)
