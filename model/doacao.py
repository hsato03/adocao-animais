from .doador import Doador
from .animal import Animal
from datetime import date


class Doacao:
    def __init__(self, doador: Doador, animal: Animal, data: date, motivo: str):
        self.__doador = doador
        self.__animal = animal
        self.__data = data
        self.__motivo = motivo

    @property
    def doador(self):
        return self.__doador

    @doador.setter
    def doador(self, doador: Doador):
        self.__doador = doador

    @property
    def animal(self):
        return self.__animal

    @animal.setter
    def animal(self, animal: Animal):
        self.__animal = animal

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def motivo(self):
        return self.__motivo

    @motivo.setter
    def motivo(self, motivo: str):
        self.__motivo = motivo
