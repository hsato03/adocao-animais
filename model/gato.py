from .animal import Animal


class Gato(Animal):
    def __init__(self, numero_chip: int, nome: str, raca: str):
        super().__init__(numero_chip, nome, raca)
