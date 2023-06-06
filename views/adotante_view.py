from exceptions import OpcaoInvalidaException, CpfInvalidoException
from datetime import datetime


class AdotanteView:
    def telar_opcoes(self):
        print("\n---------------------------------")
        print("|           ADOTANTES           |")
        print("---------------------------------")
        print("[1] -> Incluir Adotante")
        print("[2] -> Alterar Adotante")
        print("[3] -> Listar Adotantes")
        print("[4] -> Excluir Adotante")
        print("[5] -> Buscar Adotante por CPF")
        print("[0] -> Retornar")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(0, 6):
            raise OpcaoInvalidaException()

        return opcao

    def telar_opcoes_tipo_habitacao(self):
        print("TIPO HABITACAO:")
        print("\t[1] -> Casa")
        print("\t[2] -> Apartamento")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 3):
            raise OpcaoInvalidaException()

        return opcao

    def telar_opcoes_tamanho_habitacao(self):
        print("TAMANHO HABITACAO:")
        print("\t[1] -> Pequeno")
        print("\t[2] -> Medio")
        print("\t[3] -> Grande")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 4):
            raise OpcaoInvalidaException()

        return opcao

    def telar_opcoes_possui_animal(self):
        print("POSSUI ANIMAL:")
        print("\t[1] -> Sim")
        print("\t[2] -> Nao")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 3):
            raise OpcaoInvalidaException()

        return opcao

    def pegar_dados_adotante(self):
        tipo_habitacao, tamanho_habitacao, possui_animal = (
            None,
            None,
            None,
        )
        print("\n-------- DADOS ADOTANTE ----------")
        cpf = input("CPF: ")
        if not self.validar_cpf(cpf):
            raise CpfInvalidoException(cpf)
        nome = input("Nome: ")
        while True:
            try:
                data_nascimento = input("Data de nascimento (dd/mm/yyyy): ")
                data_nascimento_convertida = datetime.strptime(
                    data_nascimento, "%d/%m/%Y"
                ).date()
                break
            except ValueError:
                print("ERRO: Data em formato invalido! Tente novamente.")
        while True:
            try:
                tipo_habitacao = (
                    self.telar_opcoes_tipo_habitacao()
                    if tipo_habitacao is None
                    else tipo_habitacao
                )
                tamanho_habitacao = (
                    self.telar_opcoes_tamanho_habitacao()
                    if tamanho_habitacao is None
                    else tamanho_habitacao
                )
                possui_animal = (
                    self.telar_opcoes_possui_animal()
                    if possui_animal is None
                    else possui_animal
                )
                break
            except OpcaoInvalidaException as e:
                print(e)
            except ValueError:
                print("Somente numeros. Tente novamente.")

        print("DADOS ENDERECO:")
        logradouro = input("\tLogradouro: ")
        numero = input("\tNumero: ")

        return {
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento_convertida,
            "tipo_habitacao": tipo_habitacao,
            "tamanho_habitacao": tamanho_habitacao,
            "possui_animal": possui_animal,
            "logradouro": logradouro,
            "numero": numero,
        }

    def mostrar_adotante(self, dados_adotante: dict):
        print("\t- CPF:", dados_adotante["cpf"])
        print("\t- NOME:", dados_adotante["nome"])
        print(
            "\t- DATA DE NASCIMENTO:",
            dados_adotante["data_nascimento"].strftime("%d/%m/%Y"),
        )
        print("\t- TIPO DE HABITACAO:", dados_adotante["tipo_habitacao"].name)
        print(
            "\t- TAMANHO DE HABITACAO:",
            dados_adotante["tamanho_habitacao"].name,
        )
        print("\t- POSSUI ANIMAL:", dados_adotante["possui_animal"])
        print(f"\t- ENDERECO: {dados_adotante['endereco']}\n")

    def validar_cpf(self, cpf: str):
        return len(cpf) == 11

    def selecionar_adotante(self):
        cpf = input("CPF do adotante que deseja selecionar: ")
        if self.validar_cpf(cpf):
            return cpf
        raise CpfInvalidoException(cpf)

    def mostrar_mensagem(self, msg):
        print(msg)
