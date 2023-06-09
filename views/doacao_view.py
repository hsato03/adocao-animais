from datetime import datetime
from model import TIPO_CPF
from exceptions import OpcaoInvalidaException
import PySimpleGUI as sg


class DoacaoView:
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
        elif button == "doacoes_periodo":
            opcao = 5
        else:
            opcao = 0
        self.__window.close()
        return opcao

    def init_components(self):
        layout = [
            [
                sg.Text(
                    "Doacoes",
                    font=["Inter", 30, "bold"],
                    size=[20, 2],
                    justification="center",
                    pad=((0, 0), (25, 0)),
                    background_color="#3F3F3F",
                )
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Button(
                                "Incluir",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="incluir",
                            )
                        ],
                        [
                            sg.Button(
                                "Alterar",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="alterar",
                            )
                        ],
                        [
                            sg.Button(
                                "Listar",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="listar",
                            )
                        ],
                        [
                            sg.Button(
                                "Excluir",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="excluir",
                            )
                        ],
                        [
                            sg.Button(
                                "Doacoes por periodo",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="doacoes_periodo",
                            )
                        ],
                        [
                            sg.Button(
                                "Retornar",
                                size=(20, 2),
                                button_color=("black", "#FAF000"),
                                font=("Inter", 12),
                                key="retornar",
                                pad=((0, 0), (50, 0)),
                            )
                        ],
                    ],
                    justification="center",
                    background_color="#3F3F3F",
                )
            ],
        ]
        self.__window = sg.Window(
            "Window Layout", layout, size=(500, 650), background_color="#3F3F3F"
        )

    def telar_opcoes_identificador(self):
        print("BUSCAR POR:")
        print("\t[1] -> CPF")
        print("\t[2] -> N° chip")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 3):
            raise OpcaoInvalidaException()

        return opcao

    def telar_opcoes_tipo_animal(self):
        print("TIPO DO ANIMAL QUE DESEJA DOAR:")
        print("\t[1] -> Cachorro")
        print("\t[2] -> Gato")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 3):
            raise OpcaoInvalidaException()

        return opcao

    def pegar_dados_doacao(self, criacao):
        print("\n-------- DADOS DOACAO ----------")

        if criacao:
            cpf_doador = input("CPF (doador): ")
            numero_chip = self.pegar_numero_chip()

        while True:
            try:
                data_doacao = input("Data de adocao (dd/mm/yyyy): ")
                data_doacao_convertida = datetime.strptime(
                    data_doacao, "%d/%m/%Y"
                ).date()
                break
            except ValueError:
                print("ERRO: Data em formato invalido! Tente novamente.")

        motivo = input("Motivo: ")

        if criacao:
            return {
                "cpf_doador": cpf_doador,
                "numero_chip": numero_chip,
                "data": data_doacao_convertida,
                "motivo": motivo,
            }
        return {
            "data": data_doacao_convertida,
            "motivo": motivo,
        }

    def pegar_dados_periodo(self):
        while True:
            try:
                data_inicio = input("Data de inicio (dd/mm/yyyy): ")
                data_inicio_convertida = datetime.strptime(
                    data_inicio, "%d/%m/%Y"
                ).date()
                break
            except ValueError:
                print("ERRO: Data em formato invalido! Tente novamente.")
        while True:
            try:
                data_fim = input("Data de fim (dd/mm/yyyy): ")
                data_fim_convertida = datetime.strptime(data_fim, "%d/%m/%Y").date()
                break
            except ValueError:
                print("ERRO: Data em formato invalido! Tente novamente.")

        return {"data_inicio": data_inicio_convertida, "data_fim": data_fim_convertida}

    def pegar_numero_chip(self):
        while True:
            try:
                numero_chip = int(input("N° chip: "))
                return numero_chip
            except ValueError:
                print("Somente numeros. Tente novamente")

    def mostrar_doacao(self, dados_doacao: dict):
        print("\t - CPF DOADOR: ", dados_doacao["cpf_doador"])
        print("\t - N° CHIP ANIMAL: ", dados_doacao["numero_chip"])
        print("\t - DATA DE DOACAO: ", dados_doacao["data"].strftime("%d/%m/%Y"))
        print("\t - TERMO ASSINADO: ", dados_doacao["motivo"])

    def selecionar_doacao(self, tipo_id: int):
        if tipo_id == TIPO_CPF:
            identificador = input("CPF da doacao que deseja selecionar: ")
        else:
            while True:
                try:
                    identificador = int(
                        input("N° Chip da doacao que deseja selecionar: ")
                    )
                    break
                except ValueError:
                    print("Somente numeros. Tente novamente")
        return identificador

    def mostrar_mensagem(self, msg: str):
        sg.popup("", msg)
