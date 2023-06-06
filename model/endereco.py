class Endereco:
    def __init__(self, logradouro: str, numero: str):
        self.__logradouro = logradouro
        self.__numero = numero

    @property
    def logradouro(self):
        return self.__logradouro

    @property
    def numero(self):
        return self.__numero

    def __str__(self):
        return f"{self.__logradouro}, {self.__numero}"
