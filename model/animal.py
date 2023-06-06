from abc import ABC, abstractmethod
from .historico_vacinacao import HistoricoVacinacao

TIPO_CACHORRO = 1
TIPO_GATO = 2


class Animal(ABC):
    @abstractmethod
    def __init__(self, numero_chip: int, nome: str, raca: str):
        self.__numero_chip = numero_chip
        self.__nome = nome
        self.__raca = raca
        self.__historico_vacinacao = HistoricoVacinacao()

    @property
    def numero_chip(self):
        return self.__numero_chip

    @numero_chip.setter
    def numero_chip(self, numero_chip: int):
        self.__numero_chip = numero_chip

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def raca(self):
        return self.__raca

    @raca.setter
    def raca(self, raca: str):
        self.__raca = raca

    @property
    def historico_vacinacao(self):
        return self.__historico_vacinacao
