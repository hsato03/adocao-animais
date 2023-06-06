from .pessoa import Pessoa
from datetime import date


class Doador(Pessoa):
    def __init__(
        self, cpf: str, nome: str, data_nascimento: date, logradouro: str, numero: str
    ):
        super().__init__(cpf, nome, data_nascimento, logradouro, numero)
