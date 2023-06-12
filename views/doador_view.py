from exceptions import CpfInvalidoException, CampoObrigatorioException
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

    def pegar_dados_doador(self, doador):
        if doador:
            layout = [
                [sg.Text("CADASTRO DOADOR", font=("Inter", 25), justification="center")],
                [sg.Text("CPF:", size=(17, 1)), sg.InputText(doador.cpf, key="cpf")],
                [sg.Text("Nome:", size=(17, 1)), sg.InputText(doador.nome, key="nome")],
                [sg.Text("Data de nascimento", size=(17, 1)),
                 sg.Input(doador.data_nascimento.strftime('%d/%m/%Y'), size=(26, 1), key="data_nascimento"),
                 sg.CalendarButton("Abrir calendario", target="data_nascimento", format="%d/%m/%Y")],
                [sg.Text("Logradouro:", size=(17, 1)),
                 sg.InputText(doador.endereco.logradouro, key="logradouro")],
                [sg.Text("Numero:", size=(17, 1)),
                 sg.InputText(doador.endereco.numero, key="numero")],
                [sg.Button("Confirmar", key="confirmar"),
                 sg.Cancel("Cancelar", key="cancelar")]
            ]
        else:
            layout = [
                [sg.Text("CADASTRO DOADOR", font=("Inter", 25), justification="center")],
                [sg.Text("CPF:", size=(17, 1)), sg.InputText("", key="cpf")],
                [sg.Text("Nome:", size=(17, 1)), sg.InputText("", key="nome")],
                [sg.Text("Data de nascimento", size=(17, 1)),
                 sg.Input(size=(26, 1), key="data_nascimento"),
                 sg.CalendarButton("Abrir calendario", target="data_nascimento", format="%d/%m/%Y")],
                [sg.Text("Logradouro:", size=(17, 1)),
                 sg.InputText("", key="logradouro")],
                [sg.Text("Numero:", size=(17, 1)), sg.InputText("", key="numero")],
                [sg.Button("Confirmar", key="confirmar"),
                 sg.Cancel("Cancelar", key="cancelar")],
            ]

        self.__window = sg.Window("Layout", layout)

        while True:
            try:
                button, values = self.__window.read()
                if (button == "confirmar" and self.input_valido()) or button == "cancelar":
                    break
            except (CampoObrigatorioException, CpfInvalidoException) as e:
                sg.popup(e)

        self.__window.close()

        if button == "cancelar":
            return

        cpf = values["cpf"]
        nome = values["nome"]
        data_nascimento_convertida = datetime.strptime(
            values["data_nascimento"], "%d/%m/%Y"
        ).date()

        logradouro = values["logradouro"]
        numero = values["numero"]

        return {
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento_convertida,
            "logradouro": logradouro,
            "numero": numero,
        }

    def mostrar_doador(self, doador):
        nome = doador.nome
        cpf = doador.cpf
        index_endfirstname = nome.find(" ")
        output_doador = "\t - CPF: {}.{}.{}-{}\n".format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
        output_doador += f"\t - Nome: {nome}\n"
        output_doador += f"\t - Data de nascimento: {doador.data_nascimento.strftime('%d/%m/%Y')}\n"
        output_doador += f"\t - Endereco: {doador.endereco}\n"

        sg.Popup(
            f"Dados do doador {nome[0:index_endfirstname if index_endfirstname > -1 else len(nome)]}:",
            output_doador,
        )

    def mostrar_doadores(self, doadores: list):
        layout = self.layout_tabela_mostrar_doadores(doadores)
        layout.append([sg.Button("Fechar", key="fechar", button_color="red")],)

        self.__window = sg.Window("Layout", layout)
        self.__window.read()
        self.__window.close()

    def layout_tabela_mostrar_doadores(self, doadores: list):
        toprow = [
            "CPF",
            "Nome",
            "Data nascimento",
            "Endereco",
        ]
        dados_doadores = [
            [
                "{}.{}.{}-{}".format(doador.cpf[:3], doador.cpf[3:6], doador.cpf[6:9], doador.cpf[9:]),
                doador.nome,
                str(doador.data_nascimento.strftime('%d/%m/%Y')),
                str(doador.endereco),
            ]
            for doador in doadores
        ]
        return [
            [
                sg.Table(
                    headings=toprow,
                    values=dados_doadores,
                    auto_size_columns=True,
                    expand_y=True,
                    expand_x=True,
                    justification="center"
                )
            ],
        ]

    def cpf_invalido(self, cpf: str):
        return len(cpf) != 11

    def selecionar_doador(self, doadores: list, mostrar_opcoes: bool):
        layout = []

        if mostrar_opcoes:
            layout.append(self.layout_tabela_mostrar_doadores(doadores))

        layout.append([
            [sg.Text("CPF do doador que deseja selecionar: ")],
            [sg.Combo(values=[doador.cpf for doador in doadores], default_value=doadores[0].cpf, key="cpf")],
            [sg.Button("Confirmar", key="confirmar"),
             sg.Button("Cancelar", key="cancelar", button_color="red")],
        ])
        self.__window = sg.Window("Layout", layout)
        button, values = self.__window.read()
        self.__window.close()

        if button == "cancelar":
            return

        return values["cpf"]

    def mostrar_mensagem(self, msg: str):
        sg.popup("", msg)

    def input_valido(self):
        data_formato_valido = True
        campos_nao_preenchidos = []

        cpf = self.__window["cpf"].get().strip()
        nome = self.__window["nome"].get().strip()
        logradouro = self.__window["logradouro"].get().strip()
        numero = self.__window["numero"].get().strip()

        try:
            data_nascimento = self.__window["data_nascimento"].get().strip()
            datetime.strptime(data_nascimento, "%d/%m/%Y").date()
        except ValueError:
            sg.popup("Data em formato invalido! Tente novamente.")
            data_formato_valido = False

        if not cpf:
            campos_nao_preenchidos.append("CPF")
        if not nome:
            campos_nao_preenchidos.append("Nome")
        if not logradouro:
            campos_nao_preenchidos.append("Endereco")
        if not numero:
            campos_nao_preenchidos.append("Numero")

        if len(campos_nao_preenchidos) > 0:
            raise CampoObrigatorioException(campos_nao_preenchidos)

        if self.cpf_invalido(cpf):
            raise CpfInvalidoException(cpf)

        return data_formato_valido
