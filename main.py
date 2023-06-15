from controllers import SistemaController
from model import *
from datetime import date
from persistence import *


if __name__ == "__main__":
    SistemaController.inicializar_sistema(SistemaController())

    # cachorro = Cachorro(1, "Brisa", "Bulldog ingles", TamanhoCachorro.MEDIO)
    # gato = Gato(2, "Miau", "Persa")
    #
    # animal_dao = AnimalDAO("datasources/animais.pkl")
    #
    # animal_dao.insert(cachorro)
    # animal_dao.insert(gato)
    #
    # animal_dao.remove(cachorro.numero_chip)
    #
    # print(animal_dao.find_by_id(1).nome)
