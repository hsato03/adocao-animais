from abc import ABC, abstractmethod
from datetime import date
from .endereco import Endereco


class Pessoa(ABC):
    @abstractmethod
    def __init__(
        self, cpf: str, nome: str, data_nascimento: date, logradouro: str, numero: str
    ):
        self.__cpf = cpf
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__endereco = Endereco(logradouro, numero)

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date):
        self.__data_nascimento = data_nascimento

    @property
    def endereco(self):
        return self.__endereco

    def add_endereco(self, logradouro: str, numero: str):
        self.__endereco = Endereco(logradouro, numero)
