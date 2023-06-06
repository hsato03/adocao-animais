class Vacina:
    def __init__(self, identificador: int, nome: str):
        self.__nome = nome
        self.__identificador = identificador

    @property
    def identificador(self):
        return self.__identificador

    @identificador.setter
    def identificador(self, identificador: int):
        self.__identificador = identificador

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome
