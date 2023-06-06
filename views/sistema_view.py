from exceptions import OpcaoInvalidaException


class SistemaView:
    def telar_opcoes(self):
        print("\n--------------------------------")
        print("|        MENU PRINCIPAL        |")
        print("--------------------------------")
        print("[1] -> Adotantes")
        print("[2] -> Adocoes")
        print("[3] -> Animais")
        print("[4] -> Doadores")
        print("[5] -> Doacoes")
        print("[6] -> Vacinas")
        print("[0] -> Finalizar sistema")
        opcao = int(input("Escolha a opcao: "))

        if opcao not in range(0, 7):
            raise OpcaoInvalidaException()

        return opcao
