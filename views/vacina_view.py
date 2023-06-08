from exceptions import OpcaoInvalidaException
from datetime import datetime
import PySimpleGUI as sg


class VacinaView:
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
        elif button == "buscar_por_id":
            opcao = 5
        else:
            opcao = 0
        self.__window.close()
        return opcao

    def init_components(self):
        layout = [
            [sg.Text("Vacinas", font=["Inter", 30, "bold"], size=[20, 2], justification="center",
                     pad=((0, 0), (25, 0)), background_color="#3F3F3F")],
            [sg.Column([
                [sg.Button("Incluir", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="incluir")],
                [sg.Button("Alterar", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="alterar")],
                [sg.Button("Listar", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="listar")],
                [sg.Button("Excluir", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="excluir")],
                [sg.Button("Buscar por ID", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"), key="buscar_por_id")],
                [sg.Button("Retornar", size=(20, 2), button_color=("black", "#FAF000"), font=("Inter", 12), key="retornar", pad=((0, 0), (50, 0)))],
            ], justification="center", background_color="#3F3F3F")]
        ]
        self.__window = sg.Window("Window Layout", layout, size=(500, 650), background_color="#3F3F3F")

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
        sg.popup("", msg)
