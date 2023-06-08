from exceptions import OpcaoInvalidaException, CpfInvalidoException, CampoObrigatorioException
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
                [sg.Button("Incluir", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"),
                           key="incluir")],
                [sg.Button("Alterar", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"),
                           key="alterar")],
                [sg.Button("Listar", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"),
                           key="listar")],
                [sg.Button("Excluir", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"),
                           key="excluir")],
                [sg.Button("Buscar por CPF", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"),
                           key="buscar_por_cpf")],
                [sg.Button("Retornar", size=(20, 2), button_color=("black", "#FAF000"), font=("Inter", 12),
                           key="retornar", pad=((0, 0), (50, 0)))],
            ], justification="center", background_color="#3F3F3F")]
        ]
        self.__window = sg.Window("Window Layout", layout, size=(500, 650), background_color="#3F3F3F")

    def pegar_dados_adotante(self):
        layout = [
            [sg.Text("CADASTRO ADOTANTE", font=("Inter", 25), justification="center")],
            [sg.Text("CPF:", size=(15, 1)), sg.InputText("", key="cpf")],
            [sg.Text("Nome:", size=(15, 1)), sg.InputText("", key="nome")],
            [sg.CalendarButton("Data de nascimento:", target="data_nascimento", format="%d/%m/%Y"),
             sg.Input(size=(20, 1), key="data_nascimento")],
            [sg.Text("Logradouro:", size=(15, 1)), sg.InputText('', key='logradouro')],
            [sg.Text("Numero:", size=(15, 1)), sg.InputText('', key='numero')],
            [
                [sg.Column([
                    [sg.Text("Tipo de habitacao: ")],
                    [sg.Radio("Casa", "RD1", key="casa")],
                    [sg.Radio("Apartamento", "RD1", key="apartamento")],
                    [sg.HorizontalSeparator()]
                ])],
                [sg.Column([
                    [sg.Text("Tipo de habitacao: ")],
                    [sg.Radio("Pequeno", "RD2", key="pequeno")],
                    [sg.Radio("Medio", "RD2", key="medio")],
                    [sg.Radio("Grande", "RD2", key="grande")],
                ])],
                [sg.Column(
                    [
                        [sg.Text("Possui animal?")],
                        [sg.Radio("Sim", "RD3", key="possui")],
                        [sg.Radio("Nao", "RD3", key="nao_possui")],
                    ])],
            ],

            [sg.Button("Confirmar", key="confirmar"), sg.Cancel("Cancelar", key="cancelar")]
        ]

        self.__window = sg.Window("Sistema de livros", layout, enable_close_attempted_event=True)

        while True:
            try:
                button, values = self.__window.read()
                if (button == "confirmar" and self.input_valido()) or button == "cancelar":
                    break
            except (CampoObrigatorioException, CpfInvalidoException) as e:
                sg.popup(e)

        self.__window.close()

        if button == "confirmar":
            cpf = values["cpf"]
            nome = values["nome"]
            data_nascimento_convertida = datetime.strptime(
                values["data_nascimento"], "%d/%m/%Y"
            ).date()

            if values["apartamento"]:
                tipo_habitacao = 1
            else:
                tipo_habitacao = 2

            if values["pequeno"]:
                tamanho_habitacao = 1
            elif values["medio"]:
                tamanho_habitacao = 2
            else:
                tamanho_habitacao = 3

            possui_animal = True if values["possui"] else False
            logradouro = values["logradouro"]
            numero = values["numero"]

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

    def cpf_invalido(self, cpf: str):
        return len(cpf) != 11

    def selecionar_adotante(self):
        cpf = input("CPF do adotante que deseja selecionar: ")
        if self.cpf_invalido(cpf):
            raise CpfInvalidoException(cpf)
        return cpf

    def mostrar_mensagem(self, msg):
        sg.popup("", msg)

    def input_valido(self):
        campos_nao_preenchidos = []

        cpf = self.__window["cpf"].get().strip()
        nome = self.__window["nome"].get().strip()
        tipo_habitacao = self.__window["casa"].get() or self.__window["apartamento"].get()
        tamanho_habitacao = self.__window["pequeno"].get() or self.__window["medio"] or self.__window["grande"].get()
        possui_animal = self.__window["possui"].get() or self.__window["nao_possui"].get()

        try:
            data_nascimento = self.__window["data_nascimento"].get().strip()
            datetime.strptime(
                data_nascimento, "%d/%m/%Y"
            ).date()
        except ValueError:
            sg.popup("Data em formato invalido! Tente novamente.")

        if not cpf:
            campos_nao_preenchidos.append("CPF")
        if not nome:
            campos_nao_preenchidos.append("Nome")
        if not tipo_habitacao:
            campos_nao_preenchidos.append("Tipo de habitacao")
        if not tamanho_habitacao:
            campos_nao_preenchidos.append("Tamanho da habitacao")
        if not possui_animal:
            campos_nao_preenchidos.append("Possui animal")

        if len(campos_nao_preenchidos) > 0:
            raise CampoObrigatorioException(campos_nao_preenchidos)

        if self.cpf_invalido(cpf):
            raise CpfInvalidoException(cpf)

        return True
