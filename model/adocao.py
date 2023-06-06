from .adotante import Adotante
from .animal import Animal
from datetime import date

TIPO_CPF = 1
TIPO_N_CHIP = 2


class Adocao:
    def __init__(
        self, adotante: Adotante, animal: Animal, data: date, termo_assinado: bool
    ):
        self.__adotante = adotante
        self.__animal = animal
        self.__data = data
        self.__termo_assinado = termo_assinado

    @property
    def adotante(self):
        return self.__adotante

    @adotante.setter
    def adotante(self, adotante: Adotante):
        self.__adotante = adotante

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
    def termo_assinado(self):
        return self.__termo_assinado

    @termo_assinado.setter
    def termo_assinado(self, termo_assinado: bool):
        self.__termo_assinado = termo_assinado
