from exceptions import OpcaoInvalidaException, CpfInvalidoException
from datetime import datetime
import PySimpleGUI as sg


class DoadorView:
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
            [
                sg.Text(
                    "Doadores",
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
                                "Buscar por CPF",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="buscar_por_cpf",
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

    def pegar_dados_doador(self):
        print("\n-------- DADOS DOADOR ----------")
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

        print("DADOS ENDERECO:")
        logradouro = input("\tLogradouro: ")
        numero = input("\tNumero: ")

        return {
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento_convertida,
            "logradouro": logradouro,
            "numero": numero,
        }

    def mostrar_doador(self, dados_doador: dict):
        print("\t- CPF:", dados_doador["cpf"])
        print("\t- NOME:", dados_doador["nome"])
        print(
            "\t- DATA DE NASCIMENTO:",
            dados_doador["data_nascimento"].strftime("%d/%m/%Y"),
        )
        print(f"\t- ENDERECO: {dados_doador['endereco']}\n")

    def validar_cpf(self, cpf: str):
        return len(cpf) == 11

    def selecionar_doador(self):
        cpf = input("CPF do doador que deseja selecionar: ")
        if self.validar_cpf(cpf):
            return cpf
        raise CpfInvalidoException(cpf)

    def mostrar_mensagem(self, msg: str):
        sg.popup("", msg)
