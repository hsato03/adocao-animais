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
                sg.Column(
                    [
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
                    ],
                    justification="center",
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
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="incluir",
                            )
                        ],
                        [
                            sg.Button(
                                "Alterar",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="alterar",

                            )
                        ],
                        [
                            sg.Button(
                                "Listar",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="listar",
                            )
                        ],
                        [
                            sg.Button(
                                "Excluir",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="excluir",
                            )
                        ],
                        [
                            sg.Button(
                                "Buscar por ID",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="buscar_por_id",
                            )
                        ],
                    ],
                    justification="center",
                    background_color="#3F3F3F",
                )
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Button(
                                "Retornar",
                                size=(20, 2),
                                button_color=("black", "#FAF000"),
                                font=("Inter", 13),
                                key="retornar",
                                pad=((0, 0), (60, 0)),
                            )
                        ],
                    ],
                    justification="center",
                    background_color="#3F3F3F",
                )
            ],
        ]
        self.__window = sg.Window(
            "Window Layout", layout, size=(500, 650), background_color="#3F3F3F",
        )

    def pegar_dados_vacina(self, vacina):
        if vacina:
            layout = [
                [sg.Text("ALTERAR VACINA", font=("Inter", 25), justification="center", background_color="#3F3F3F", pad=15)],
                [sg.Text("ID:", size=(10, 1), background_color="#3F3F3F"), sg.InputText(vacina.identificador, key="id")],
                [sg.Text("Nome:", size=(10, 1), background_color="#3F3F3F"), sg.InputText(vacina.nome, key="nome")],
                [sg.Column(
                    [
                        [
                            sg.Button(
                                "Confirmar",
                                key="confirmar",
                                font=("Inter", 12),
                                button_color=("white", "green")
                            ),
                            sg.Cancel("Cancelar", key="cancelar", button_color="red", font=("Inter", 12)),
                        ],
                    ],
                    justification="right", background_color="#3F3F3F", pad=20
                ),
                ]
            ]
        else:
            layout = [
                [sg.Text("CADASTRO VACINA", font=("Inter", 25), justification="center", background_color="#3F3F3F", pad=15)],
                [sg.Text("ID:", size=(10, 1), background_color="#3F3F3F"), sg.InputText("", key="id")],
                [sg.Text("Nome:", size=(10, 1), background_color="#3F3F3F"), sg.InputText("", key="nome")],
                [sg.Column(
                    [
                        [
                            sg.Button(
                                "Confirmar",
                                key="confirmar",
                                font=("Inter", 12),
                                button_color=("white", "green")
                            ),
                            sg.Cancel("Cancelar", key="cancelar", button_color="red", font=("Inter", 12)),
                        ],
                    ],
                    justification="right", background_color="#3F3F3F", pad=20
                ),
                ]
            ]
        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F", font=("Inter", 12))

        while True:
            try:
                button, values = self.__window.read()
                if (button == "confirmar" and self.input_valido()) or button == "cancelar":
                    break
            except CampoObrigatorioException as e:
                self.mostrar_mensagem(e)

        self.__window.close()

        if button == "cancelar":
            return

        identificador = int(values["id"])
        nome = values["nome"]

        return {"id": identificador, "nome": nome}

    def mostrar_vacinas(self, vacinas: list):
        layout = self.layout_tabela_mostrar_vacinas(vacinas)
        layout.append([sg.Button("Fechar", key="fechar", button_color="red", font=("Inter", 12))], )

        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F", font=("Inter", 12))
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

        dados_vacinas.sort(key=lambda attrs: attrs[0])

        return [
            [
                sg.Table(
                    headings=toprow,
                    values=dados_vacinas,
                    auto_size_columns=True,
                    expand_y=True,
                    expand_x=True,
                    justification="center",
                    background_color="#FEFEFE",
                    text_color="#000",
                    alternating_row_color="#BDBDBD",
                    selected_row_colors=("#FFF", "#2B2B2B"),
                    font=("Inter", 12),
                    sbar_background_color="#2B2B2B",
                    num_rows=10,
                )
            ],
        ]

    def mostrar_vacina(self, vacina):
        output_vacina = f"\t - ID: {vacina.identificador}\n"
        output_vacina += f"\t - Nome: {vacina.nome}\n"

        self.mostrar_mensagem(output_vacina)

    def selecionar_vacina(self, vacinas: list, mostrar_opcoes):
        layout = []

        if mostrar_opcoes:
            layout.append(self.layout_tabela_mostrar_vacinas(vacinas))

        vacinas.sort(key=lambda vacina: vacina.identificador)
        layout.append([
            [sg.Text("ID da vacina que deseja selecionar: ", font=("Inter", 12), background_color="#3F3F3F", pad=10)],
            [sg.Combo(values=[vacina.identificador for vacina in vacinas],
                      default_value=vacinas[0].identificador,
                      size=(22, 10),
                      font=("Inter", 14),
                      button_background_color="#2B2B2B",
                      pad=((15, 0), (0, 0)),
                      key="id")],
            [sg.Column(
                [
                    [
                        sg.Button(
                            "Confirmar",
                            key="confirmar",
                            font=("Inter", 12),
                            button_color=("white", "green")
                        ),
                        sg.Cancel("Cancelar", key="cancelar", button_color="red", font=("Inter", 12)),
                    ],
                ],
                justification="right", background_color="#3F3F3F", pad=15
            ),
            ],
        ])
        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F", font=("Inter", 12))
        button, values = self.__window.read()
        self.__window.close()

        if button == "cancelar":
            return

        return values["id"]

    def mostrar_mensagem(self, msg: str):
        sg.popup("",
                 msg,
                 background_color="#3F3F3F",
                 button_color=("white", "red"),
                 font=("Inter", 13),
                 custom_text="Fechar")

    def input_valido(self):
        campos_nao_preenchidos = []
        id_valido = True

        identificador = self.__window["id"].get().strip()
        nome = self.__window["nome"].get().strip()

        try:
            int(identificador)
        except ValueError:
            self.mostrar_mensagem("ID deve ser um valor inteiro")
            id_valido = False

        if not identificador:
            campos_nao_preenchidos.append("ID")
        if not nome:
            campos_nao_preenchidos.append("Nome")

        if len(campos_nao_preenchidos) > 0:
            raise CampoObrigatorioException(campos_nao_preenchidos)

        return id_valido
