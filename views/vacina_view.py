import PySimpleGUI as sg

from exceptions import CampoObrigatorioException


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
            [
                sg.Text(
                    "Vacinas",
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
                                "Buscar por ID",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="buscar_por_id",
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

    def pegar_dados_vacina(self, vacina):
        if vacina:
            layout = [
                [sg.Text("CADASTRO VACINA", font=("Inter", 25), justification="center")],
                [sg.Text("ID:", size=(17, 1)), sg.InputText(vacina.identificador3, key="id")],
                [sg.Text("Nome:", size=(17, 1)), sg.InputText(vacina.nome, key="nome")],
                [sg.Button("Confirmar", key="confirmar"),
                 sg.Cancel("Cancelar", key="cancelar")],
            ]
        else:
            layout = [
                [sg.Text("CADASTRO VACINA", font=("Inter", 25), justification="center")],
                [sg.Text("ID:", size=(17, 1)), sg.InputText("", key="id")],
                [sg.Text("Nome:", size=(17, 1)), sg.InputText("", key="nome")],
                [sg.Button("Confirmar", key="confirmar"),
                 sg.Cancel("Cancelar", key="cancelar")],
            ]

        self.__window = sg.Window("Layout", layout)

        while True:
            try:
                button, values = self.__window.read()
                if (button == "confirmar" and self.input_valido()) or button == "cancelar":
                    break
            except CampoObrigatorioException as e:
                sg.popup(e)

        self.__window.close()

        if button == "cancelar":
            return

        identificador = values["id"]
        nome = values["nome"]

        return {"id": identificador, "nome": nome}

    def mostrar_vacinas(self, vacinas: list):
        layout = self.layout_tabela_mostrar_vacinas(vacinas)
        layout.append([sg.Button("Fechar", key="fechar", button_color="red")],)

        self.__window = sg.Window("Layout", layout)
        self.__window.read()
        self.__window.close()

    def layout_tabela_mostrar_vacinas(self, vacinas):
        toprow = ["ID", "Nome"]
        dados_vacinas = [
            [
                vacina.identificador,
                vacina.nome,
            ]
            for vacina in vacinas
        ]

        return [
            [
                sg.Table(
                    headings=toprow,
                    values=dados_vacinas,
                    auto_size_columns=True,
                    expand_y=True,
                    expand_x=True,
                    justification="center",
                )
            ],
        ]

    def mostrar_vacina(self, dados_vacina: dict):
        output_vacina = f"\t - ID: {dados_vacina['id']}\n"
        output_vacina += f"\t - Nome: {dados_vacina['nome']}\n"

        sg.Popup("", output_vacina)

    def selecionar_vacina(self, ids: list, vacinas: list):
        layout = []
        if vacinas:
            layout.append(self.layout_tabela_mostrar_vacinas(vacinas))
        layout.append([
            [sg.Text("ID da vacina que deseja selecionar: ")],
            [sg.Combo(values=ids, default_value=ids[0], key="id")],
            [sg.Button("Confirmar", key="confirmar"),
             sg.Button("Cancelar", key="cancelar", button_color="red")],
        ])
        self.__window = sg.Window("Layout", layout)
        button, values = self.__window.read()
        self.__window.close()

        if button == "cancelar":
            return

        return values["id"]

    def mostrar_mensagem(self, msg: str):
        sg.popup("", msg)

    def input_valido(self):
        campos_nao_preenchidos = []

        identificador = self.__window["id"].get().strip()
        nome = self.__window["nome"].get().strip()

        if not identificador:
            campos_nao_preenchidos.append("ID")
        if not nome:
            campos_nao_preenchidos.append("Nome")

        if len(campos_nao_preenchidos) > 0:
            raise CampoObrigatorioException(campos_nao_preenchidos)

        return True
