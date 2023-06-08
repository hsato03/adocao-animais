from exceptions import OpcaoInvalidaException, CpfInvalidoException
from datetime import datetime
import PySimpleGUI as sg


class AdotanteView:
    def __init__(self):
        self.__window = None
        self.init_components()

    def telar_opcoes(self):
        self.init_components()
        button, values = self.__window.read()
        if button == "incluir":
            opcao = 1
        elif button == "alterar":
            opcao = 2
        elif button == "listar":
            opcao = 3
        elif button == "excluir":
            opcao = 4
        elif button == "buscar_por_cpf":
            opcao = 5
        else:
            opcao = 0
        self.__window.close()
        return opcao

    def init_components(self):
        layout = [
            [sg.Text("Adotantes", font=["Inter", 30, "bold"], size=[20, 2], justification="center",
                     pad=((0, 0), (25, 0)), background_color="#3F3F3F")],
            [sg.Column([
                [sg.Button("Incluir", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="incluir")],
                [sg.Button("Alterar", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="alterar")],
                [sg.Button("Listar", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="listar")],
                [sg.Button("Excluir", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="excluir")],
                [sg.Button("Buscar por CPF", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="buscar_por_cpf")],
                [sg.Button("Retornar", size=(20, 2), button_color=("black", "#FAF000"), font=("Inter", 12), key="retornar", pad=((0, 0), (50, 0)))],
            ], justification="center", background_color="#3F3F3F")]
        ]
        self.__window = sg.Window("Window Layout", layout, size=(500, 650), background_color="#3F3F3F")

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
        sg.popup("", msg)
