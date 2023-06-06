from exceptions import OpcaoInvalidaException
from datetime import datetime


class VacinaView:
    def telar_opcoes(self):
        print("\n---------------------------------")
        print("|            VACINAS            |")
        print("---------------------------------")
        print("[1] -> Incluir Vacina")
        print("[2] -> Alterar Vacina")
        print("[3] -> Listar Vacinas")
        print("[4] -> Excluir Vacina")
        print("[5] -> Buscar Vacina por ID")
        print("[0] -> Retornar")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(0, 6):
            raise OpcaoInvalidaException()

        return opcao

    def pegar_dados_vacina(self):
        print("\n-------- DADOS VACINA ----------")

        while True:
            try:
                identificador = int(input("ID: "))
                break
            except ValueError:
                print("Somente numeros. Tente novamente")
        nome = input("Nome da vacina: ")

        return {"nome": nome, "identificador": identificador}

    def mostrar_vacina(self, dados_vacina: dict):
        print("\t- ID:", dados_vacina["identificador"])
        print("\t- NOME:", dados_vacina["nome"].lower())

    def selecionar_vacina(self):
        try:
            identificador = int(input("ID da vacina que deseja selecionar: "))
            return identificador
        except ValueError:
            print("Somente numeros. Tente novamente")

    def mostrar_mensagem(self, msg: str):
        print(msg)
