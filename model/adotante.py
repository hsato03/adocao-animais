from .pessoa import Pessoa
from datetime import date
from .tamanho_habitacao import TamanhoHabitacao
from .tipo_habitacao import TipoHabitacao


class Adotante(Pessoa):
    def __init__(
        self,
        cpf: str,
        nome: str,
        data_nascimento: date,
        logradouro: str,
        numero: str,
        tipo_habitacao: TipoHabitacao,
        tamanho_habitacao: TamanhoHabitacao,
        possui_animal: bool,
    ):
        super().__init__(cpf, nome, data_nascimento, logradouro, numero)
        self.__tipo_habitacao = tipo_habitacao
        self.__tamanho_habitacao = tamanho_habitacao
        self.__possui_animal = possui_animal

    @property
    def tipo_habitacao(self):
        return self.__tipo_habitacao

    @tipo_habitacao.setter
    def tipo_habitacao(self, tipo_habitacao: str):
        self.__tipo_habitacao = tipo_habitacao

    @property
    def tamanho_habitacao(self):
        return self.__tamanho_habitacao

    @tamanho_habitacao.setter
    def tamanho_habitacao(self, tamanho_habitacao: str):
        self.__tamanho_habitacao = tamanho_habitacao

    @property
    def possui_animal(self):
        return self.__possui_animal

    @possui_animal.setter
    def possui_animal(self, possui_animal: bool):
        self.__possui_animal = possui_animal
