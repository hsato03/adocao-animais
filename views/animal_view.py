from datetime import datetime

import PySimpleGUI as sg

from exceptions import OpcaoInvalidaException, CampoObrigatorioException

TIPO_CACHORRO = 1
TIPO_GATO = 2

class AnimalView:
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
        elif button == "buscar_por_nchip":
            opcao = 5
        elif button == "vacinar":
            opcao = 6
        else:
            opcao = 0
        self.__window.close()
        return opcao

    def init_components(self):
        layout = [
            [
                sg.Text(
                    "Animais",
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
                                "Buscar por N° Chip",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="buscar_por_nchip",
                            )
                        ],
                        [
                            sg.Button(
                                "Aplicar Vacina",
                                size=(20, 2),
                                font=("Inter", 12),
                                button_color=("black", "#FEFEFE"),
                                key="vacinar",
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

    def telar_opcoes_tipo_animal(self, listagem: bool):
        values = ["Cachorro", "Gato"]
        if listagem:
            values += ["Todos"]
        layout = [
            [sg.Text("Tipo do animal que deseja selecionar: ")],
            [sg.Combo(values=values, default_value=values[0], key="tipo_animal")],
            [sg.Button("Confirmar", key="confirmar")],
        ]
        self.__window = sg.Window("Layout", layout)
        button, values = self.__window.read()
        self.__window.close()

        tipo_animal = None

        if values["tipo_animal"] == "Cachorro":
            tipo_animal = TIPO_CACHORRO
        elif values["tipo_animal"] == "Gato":
            tipo_animal = TIPO_GATO

        return tipo_animal

    def pegar_dados_animal(self, animal, tipo_animal):
        if animal:
            layout = [
                [sg.Text("ALTERAR ANIMAL", font=("Inter", 25), justification="center")],
                [sg.Text("N° Chip:", size=(17, 1)), sg.InputText(animal.numero_chip, key="numero_chip")],
                [sg.Text("Nome:", size=(17, 1)), sg.InputText(animal.nome, key="nome")],
                [sg.Text("Raca:", size=(17, 1)), sg.InputText(animal.raca, key="raca")],
            ]

            if tipo_animal == TIPO_CACHORRO:
                layout.append(self.tamanho_cachorro_padrao(animal.tamanho))

        else:
            layout = [
                [sg.Text("ALTERAR ANIMAL", font=("Inter", 25), justification="center")],
                [sg.Text("N° Chip:", size=(17, 1)), sg.InputText("", key="numero_chip")],
                [sg.Text("Nome:", size=(17, 1)), sg.InputText("", key="nome")],
                [sg.Text("Raca:", size=(17, 1)), sg.InputText("", key="raca")],
            ]

            if tipo_animal == TIPO_CACHORRO:
                layout.append([
                    sg.Column(
                        [
                            [sg.Text("Tamanho: ")],
                            [sg.Radio("Pequeno", "RD1", key="pequeno")],
                            [sg.Radio("Medio", "RD1", key="medio")],
                            [sg.Radio("Grande", "RD1", key="grande")],
                        ]
                    )
                ])

        layout.append([sg.Button("Confirmar", key="confirmar"),
                       sg.Cancel("Cancelar", key="cancelar")])

        self.__window = sg.Window("Layout", layout)

        while True:
            try:
                button, values = self.__window.read()
                if (button == "confirmar" and self.input_valido(tipo_animal == TIPO_CACHORRO)) or button == "cancelar":
                    break
            except CampoObrigatorioException as e:
                sg.popup(e)

        self.__window.close()

        if button == "cancelar":
            return

        dados_animal = {
            "numero_chip": values["numero_chip"],
            "nome": values["nome"],
            "raca": values["raca"],
        }

        if tipo_animal == TIPO_CACHORRO:
            if values["pequeno"]:
                dados_animal["tamanho_cachorro"] = 1
            elif values["medio"]:
                dados_animal["tamanho_cachorro"] = 2
            else:
                dados_animal["tamanho_cachorro"] = 3

        return dados_animal

    def tamanho_cachorro_padrao(self, tamanho_cachorro):
        if tamanho_cachorro.name == "PEQUENO":
            return [
                sg.Column(
                    [
                        [sg.Text("Tamanho: ")],
                        [sg.Radio("Pequeno", "RD1", default=True, key="pequeno")],
                        [sg.Radio("Medio", "RD1", key="medio")],
                        [sg.Radio("Grande", "RD1", key="grande")],
                    ]
                )
            ]
        elif tamanho_cachorro.name == "MEDIO":
            return [
                    sg.Column(
                        [
                            [sg.Text("Tamanho: ")],
                            [sg.Radio("Pequeno", "RD1", key="pequeno")],
                            [sg.Radio("Medio", "RD1", default=True, key="medio")],
                            [sg.Radio("Grande", "RD1", key="grande")],
                        ]
                    )
                ]
        return [
                sg.Column(
                    [
                        [sg.Text("Tamanho: ")],
                        [sg.Radio("Pequeno", "RD1", key="pequeno")],
                        [sg.Radio("Medio", "RD1", key="medio")],
                        [sg.Radio("Grande", "RD1", default=True, key="grande")],
                    ]
                )
            ]

    def pegar_data_aplicacao_vacina(self):
        while True:
            try:
                data_aplicacao = input("Data de aplicacao da vacina (dd/mm/yyyy): ")
                data_aplicacao_convertida = datetime.strptime(
                    data_aplicacao, "%d/%m/%Y"
                ).date()
                return data_aplicacao_convertida
            except ValueError:
                print("ERRO: Data em formato invalido! Tente novamente.")

    def mostrar_animal(self, animal):
        nome = animal.nome
        index_endfirstname = nome.find(" ")
        output_animal = f"\t - N° CHIP: {animal.numero_chip}\n"
        output_animal += f"\t - Nome: {nome}\n"
        output_animal += f"\t - Raca: {animal.raca}\n"

        if hasattr(animal, "tamanho"):
            output_animal += f"\t - Tamanho: {animal.tamanho.name}\n"

        historico_vacinacao = animal.historico_vacinacao
        if len(historico_vacinacao.vacinas) > 0:
            output_animal += "\t- VACINA(S):\n"
            for vacina in historico_vacinacao.vacinas:
                output_animal += f"\t\t+ {vacina['vacina'].nome} " \
                                 f"({vacina['data_aplicacao'].strftime('%d/%m/%Y')})"
        else:
            output_animal += "\t - Nenhuma vacina aplicada"

        sg.Popup(
            f"Dados do animal {nome[0:index_endfirstname if index_endfirstname > -1 else len(nome)]}:",
            output_animal,
        )

    def mostrar_animais(self, animais: list):
        layout = self.layout_tabela_mostrar_animais(animais)
        layout.append([sg.Button("Fechar", key="fechar", button_color="red")],)

        self.__window = sg.Window("Layout", layout)
        self.__window.read()
        self.__window.close()

    def layout_tabela_mostrar_animais(self, animais: list):
        toprow = [
            "N° Chip",
            "Nome",
            "Raca",
            "Tipo",
            "Vacinas",
            "Tamanho",
        ]

        dados_animais = []

        for animal in animais:
            if hasattr(animal, "tamanho"):
                dados_animais.append(
                    [
                        animal.numero_chip,
                        animal.nome,
                        animal.raca,
                        "Cachorro",
                        animal.historico_vacinacao.vacinas,
                        animal.tamanho.name,
                    ]
                )
            else:
                dados_animais.append(
                    [
                        animal.numero_chip,
                        animal.nome,
                        animal.raca,
                        "Gato",
                        animal.historico_vacinacao.vacinas,
                        "",
                    ]
                )

        dados_animais.sort(key=lambda attrs: attrs[0])

        return [
            [
                sg.Table(
                    headings=toprow,
                    values=dados_animais,
                    auto_size_columns=True,
                    expand_y=True,
                    expand_x=True,
                    justification="center",
                )
            ],

        ]

    def selecionar_animal(self, nchips: list, animais: list):
        layout = []
        if animais:
            layout.append(self.layout_tabela_mostrar_animais(animais))
        layout.append([
            [sg.Text("N° chip do animal que deseja selecionar: ")],
            [sg.Combo(values=nchips, default_value=nchips[0], key="numero_chip")],
            [sg.Button("Confirmar", key="confirmar")],
        ])
        self.__window = sg.Window("Layout", layout)
        button, values = self.__window.read()
        self.__window.close()

        return values["numero_chip"]

    def mostrar_mensagem(self, msg: str):
        sg.popup("", msg)

    def input_valido(self, cachorro: bool):
        campos_nao_preenchidos = []

        numero_chip = self.__window["numero_chip"].get().strip()
        nome = self.__window["nome"].get().strip()
        raca = self.__window["raca"].get().strip()

        if not numero_chip:
            campos_nao_preenchidos.append("ID")
        if not nome:
            campos_nao_preenchidos.append("Nome")
        if not raca:
            campos_nao_preenchidos.append("Raca")

        if cachorro:
            tamanho = self.__window["pequeno"].get() or self.__window["medio"].get() or self.__window["grande"].get()
            if not tamanho:
                campos_nao_preenchidos.append("Tamanho")

        if len(campos_nao_preenchidos) > 0:
            raise CampoObrigatorioException(campos_nao_preenchidos)

        return True
