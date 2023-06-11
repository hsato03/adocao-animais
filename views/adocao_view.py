from datetime import datetime
from exceptions import OpcaoInvalidaException
import PySimpleGUI as sg


class AdocaoView:
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
        elif button == "animais_disponiveis":
            opcao = 5
        elif button == "adocoes_periodo":
            opcao = 6
        else:
            opcao = 0
        self.__window.close()
        return opcao

    def init_components(self):
        layout = [
            [
                sg.Text(
                    "Adocoes",
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
                                "Animais disponiveis para adocao",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="animais_disponiveis",
                            )
                        ],
                        [
                            sg.Button(
                                "Adocoes por periodo",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="adocoes_periodo",
                            )
                        ],
                        [
                            sg.Button(
                                "Retornar",
                                size=(20, 2),
                                button_color=("black", "#FAF000"),
                                font=("Inter", 12),
                                key="retornar",
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

    def telar_opcoes_termo(self):
        print("ASSINAR TERMO?")
        print("\t[1] - Sim")
        print("\t[2] - Nao")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 3):
            raise OpcaoInvalidaException()

        return opcao

    def telar_opcoes_identificador(self):
        print("BUSCAR POR:")
        print("\t[1] -> CPF")
        print("\t[2] -> N° chip")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 3):
            raise OpcaoInvalidaException()

        return opcao

    def telar_opcoes_tipo_animal(self):
        print("TIPO DO ANIMAL:")
        print("\t[1] -> Cachorro")
        print("\t[2] -> Gato")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 3):
            raise OpcaoInvalidaException()

        return opcao

    def pegar_dados_adocao(self, criacao):
        print("\n-------- DADOS ADOCAO ----------")
        if criacao:
            cpf_adotante = input("CPF (adotante): ")
            numero_chip = self.pegar_numero_chip()

        while True:
            try:
                data_adocao = input("Data de adocao (dd/mm/yyyy): ")
                data_adocao_convertida = datetime.strptime(
                    data_adocao, "%d/%m/%Y"
                ).date()
                break
            except ValueError:
                print("ERRO: Data em formato invalido! Tente novamente.")

        while True:
            try:
                termo_assinado = self.telar_opcoes_termo()
                break
            except OpcaoInvalidaException as e:
                print(e)
            except ValueError:
                print("Somente numeros. Tente novamente.")

        if criacao:
            return {
                "cpf_adotante": cpf_adotante,
                "numero_chip": numero_chip,
                "data": data_adocao_convertida,
                "termo_assinado": termo_assinado,
            }
        return {
            "data": data_adocao_convertida,
            "termo_assinado": termo_assinado,
        }

    def pegar_numero_chip(self):
        while True:
            try:
                numero_chip = int(input("N° chip: "))
                return numero_chip
            except ValueError:
                print("Somente numeros. Tente novamente")

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

    def mostrar_adocao(self, adocao):
        output_adotante = f"\t - Adotante: {adocao.adotante.cpf}\n"
        output_adotante += f"\t - Animal: {adocao.animal.numero_chip}\n"
        output_adotante += f"\t - Data de adocao: {adocao.data.strftime('%d/%m/%Y')}\n"
        output_adotante += f"\t - Termo assinado: {'Sim' if adocao.termo_assinado else 'Nao'}\n"

        sg.Popup("", output_adotante)

    def selecionar_adocao(self, tipo_id: int):
        if tipo_id == 1:
            identificador = input("CPF da adocao que deseja selecionar: ")
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
