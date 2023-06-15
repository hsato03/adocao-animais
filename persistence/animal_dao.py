from .generic_dao import GenericDAO
from model import Animal


class AnimalDAO(GenericDAO):
    def __init__(self, datasource=""):
        super().__init__(datasource)

    def insert(self, animal: Animal):
        if isinstance(animal, Animal) and animal is not None:
            super().insert(animal.numero_chip, animal)

    def update(self, numero_chip: int, animal: Animal):
        if isinstance(animal, Animal) and animal is not None:
            super().update(numero_chip, animal.numero_chip, animal)
