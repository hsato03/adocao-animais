from .animal import Animal
from .tamanho_cachorro import TamanhoCachorro


class Cachorro(Animal):
    def __init__(
        self, numero_chip: int, nome: str, raca: str, tamanho: TamanhoCachorro
    ):
        super(Cachorro, self).__init__(numero_chip, nome, raca)
        self.__tamanho = tamanho

    @property
    def tamanho(self):
        return self.__tamanho

    @tamanho.setter
    def tamanho(self, tamanho: TamanhoCachorro):
        self.__tamanho = tamanho
