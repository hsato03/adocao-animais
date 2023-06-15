from controllers import SistemaController
from model import Doador
from datetime import date
from persistence import DoadorDAO


if __name__ == "__main__":
    SistemaController.inicializar_sistema(SistemaController())

    # doador1 = Doador("02860078002", "Henrique", date.today(), "dasdasdaas", "132312")
    # doador2 = Doador("00011122233", "Joao", date.today(), "aaaaaa", "1111")
    # dao = DoadorDAO("doadores.pkl")
    #
    # dao.add(doador1)
    # print(dao.find_all())
    #
    # dao.remove(doador1.cpf)
    # dao.add(doador2)
    # print(dao.find_all())
