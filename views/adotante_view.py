from exceptions import (
    CpfInvalidoException,
    CampoObrigatorioException,
)
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
            [
                sg.Column(
                    [
                        [
                            sg.Text(
                                "Adotantes",
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
                                "Buscar por CPF",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="buscar_por_cpf",
                            )
                        ],
                        [
                            sg.Button(
                                "Retornar",
                                size=(20, 2),
                                button_color=("black", "#FAF000"),
                                font=("Inter", 13),
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
            "Window Layout", layout, size=(500, 650), background_color="#3F3F3F", resizable=True,
        )

    def pegar_dados_adotante(self, adotante):
        if adotante:
            layout = [
                [sg.Text("ALTERAR ADOTANTE", font=("Inter", 25), justification="center",
                         background_color="#3F3F3F", pad=15)],
                [sg.Text("CPF:", size=(17, 1), background_color="#3F3F3F"), sg.InputText(adotante.cpf, key="cpf")],
                [sg.Text("Nome:", size=(17, 1), background_color="#3F3F3F"), sg.InputText(adotante.nome, key="nome")],
                [sg.Text("Data de nascimento", size=(17, 1), background_color="#3F3F3F"),
                 sg.Input(adotante.data_nascimento.strftime('%d/%m/%Y'), size=(30, 1), key="data_nascimento"),
                 sg.CalendarButton("Abrir calendario", target="data_nascimento", format="%d/%m/%Y",
                                   button_color=("white", "#2B2B2B"))],
                [sg.Text("Logradouro:", size=(17, 1), background_color="#3F3F3F"),
                 sg.InputText(adotante.endereco.logradouro, key="logradouro")],
                [sg.Text("Numero:", size=(17, 1), background_color="#3F3F3F"),
                 sg.InputText(adotante.endereco.numero, key="numero")],
                self.tipo_habitacao_padrao(adotante.tipo_habitacao),
                self.tamanho_habitacao_padrao(adotante.tamanho_habitacao),
                self.possui_animal_padrao(adotante.possui_animal),
                [sg.Column(
                    [
                        [
                            sg.Button(
                                "Confirmar",
                                key="confirmar",
                                font=("Inter", 12),
                                button_color=("white", "green"),
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
                [sg.Text("CADASTRO ADOTANTE", font=("Inter", 25), justification="center", background_color="#3F3F3F",
                         pad=15)],
                [sg.Text("CPF:", size=(17, 1), background_color="#3F3F3F"), sg.InputText("", key="cpf")],
                [sg.Text("Nome:", size=(17, 1), background_color="#3F3F3F"), sg.InputText("", key="nome")],
                [sg.Text("Data de nascimento:", size=(17, 1), background_color="#3F3F3F"),
                 sg.Input(size=(30, 1), key="data_nascimento"),
                 sg.CalendarButton("Abrir calendario", target="data_nascimento", format="%d/%m/%Y",
                                   button_color=("white", "#2B2B2B"))],
                [sg.Text("Logradouro:", size=(17, 1), background_color="#3F3F3F"),
                 sg.InputText("", key="logradouro")],
                [sg.Text("Numero:", size=(17, 1), background_color="#3F3F3F"), sg.InputText("", key="numero")],
                [
                    [
                        sg.Column(
                            [
                                [sg.Text("Tipo de habitacao: ", background_color="#3F3F3F")],
                                [sg.Radio("Casa", "RD1", key="casa", background_color="#3F3F3F")],
                                [sg.Radio("Apartamento", "RD1", key="apartamento", background_color="#3F3F3F")],
                                [sg.HorizontalSeparator()],
                            ],
                            background_color="#3F3F3F"
                        )
                    ],
                    [
                        sg.Column(
                            [
                                [sg.Text("Tamanho de habitacao: ", background_color="#3F3F3F")],
                                [sg.Radio("Pequeno", "RD2", key="pequeno", background_color="#3F3F3F")],
                                [sg.Radio("Medio", "RD2", key="medio", background_color="#3F3F3F")],
                                [sg.Radio("Grande", "RD2", key="grande", background_color="#3F3F3F")],
                                [sg.HorizontalSeparator()],
                            ],
                            background_color="#3F3F3F"
                        )
                    ],
                    [
                        sg.Column(
                            [
                                [sg.Text("Possui animal?", background_color="#3F3F3F")],
                                [sg.Radio("Sim", "RD3", key="possui", background_color="#3F3F3F")],
                                [sg.Radio("Nao", "RD3", key="nao_possui", background_color="#3F3F3F")],
                            ],
                            background_color="#3F3F3F"
                        )
                    ],
                ],
                [sg.Column(
                    [
                        [
                            sg.Button(
                                "Confirmar",
                                key="confirmar",
                                font=("Inter", 12),
                                button_color=("white", "green"),
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
            except (CampoObrigatorioException, CpfInvalidoException) as e:
                sg.popup(e, background_color="#3F3F3F", button_color=("white", "green"), font=("Inter", 12))

        self.__window.close()

        if button == "cancelar":
            return

        cpf = values["cpf"]
        nome = values["nome"]
        data_nascimento_convertida = datetime.strptime(values["data_nascimento"], "%d/%m/%Y").date()

        if values["casa"]:
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

    def tipo_habitacao_padrao(self, tipo_habitacao):
        if tipo_habitacao.name == "CASA":
            return [
                sg.Column(
                    [
                        [sg.Text("Tipo de habitacao: ", background_color="#3F3F3F")],
                        [sg.Radio("Casa", "RD1", default=True, key="casa", background_color="#3F3F3F")],
                        [sg.Radio("Apartamento", "RD1", key="apartamento", background_color="#3F3F3F")],
                        [sg.HorizontalSeparator()],
                    ],
                    background_color="#3F3F3F"
                )
            ]

        return [
            sg.Column(
                [
                    [sg.Text("Tipo de habitacao: ", background_color="#3F3F3F")],
                    [sg.Radio("Casa", "RD1", key="casa", background_color="#3F3F3F")],
                    [sg.Radio("Apartamento", "RD1", default=True, key="apartamento", background_color="#3F3F3F")],
                    [sg.HorizontalSeparator()],
                ],
                background_color="#3F3F3F"
            )
        ]

    def tamanho_habitacao_padrao(self, tamanho_habitacao):
        if tamanho_habitacao.name == "PEQUENO":
            return [
               sg.Column(
                   [
                       [sg.Text("Tamanho de habitacao: ", background_color="#3F3F3F")],
                       [sg.Radio("Pequeno", "RD2", default=True, key="pequeno", background_color="#3F3F3F")],
                       [sg.Radio("Medio", "RD2", key="medio", background_color="#3F3F3F")],
                       [sg.Radio("Grande", "RD2", key="grande", background_color="#3F3F3F")],
                       [sg.HorizontalSeparator()],
                   ],
                   background_color="#3F3F3F"
               )
            ],

        elif tamanho_habitacao.name == "MEDIO":
            return [
               sg.Column(
                   [
                       [sg.Text("Tamanho de habitacao: ", background_color="#3F3F3F")],
                       [sg.Radio("Pequeno", "RD2", key="pequeno", background_color="#3F3F3F")],
                       [sg.Radio("Medio", "RD2", default=True, key="medio", background_color="#3F3F3F")],
                       [sg.Radio("Grande", "RD2", key="grande", background_color="#3F3F3F")],
                       [sg.HorizontalSeparator()],
                   ],
                   background_color="#3F3F3F"
               )
            ],

        return [
           sg.Column(
               [
                   [sg.Text("Tamanho de habitacao: ", background_color="#3F3F3F")],
                   [sg.Radio("Pequeno", "RD2", key="pequeno", background_color="#3F3F3F")],
                   [sg.Radio("Medio", "RD2", key="medio", background_color="#3F3F3F")],
                   [sg.Radio("Grande", "RD2", default=True, key="grande", background_color="#3F3F3F")],
                   [sg.HorizontalSeparator()],
               ],
               background_color="#3F3F3F"
           )
        ],

    def possui_animal_padrao(self, possui_animal):
        if possui_animal:
            return [
               sg.Column(
                   [
                       [sg.Text("Possui animal?", background_color="#3F3F3F")],
                       [sg.Radio("Sim", "RD3", default=True, key="possui", background_color="#3F3F3F")],
                       [sg.Radio("Nao", "RD3", key="nao_possui", background_color="#3F3F3F")],
                   ],
                   background_color="#3F3F3F"
               )
            ],
        return [
           sg.Column(
               [
                   [sg.Text("Possui animal?", background_color="#3F3F3F")],
                   [sg.Radio("Sim", "RD3", key="possui", background_color="#3F3F3F")],
                   [sg.Radio("Nao", "RD3", default=True, key="nao_possui", background_color="#3F3F3F")],
               ],
               background_color="#3F3F3F"
           )
        ],

    def mostrar_adotante(self, adotante):
        nome = adotante.nome
        cpf = adotante.cpf
        index_endfirstname = nome.find(" ")
        output_adotante = "\t - CPF: {}.{}.{}-{}\n".format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
        output_adotante += f"\t - Nome: {nome}\n"
        output_adotante += f"\t - Data de nascimento: {adotante.data_nascimento.strftime('%d/%m/%Y')}\n"
        output_adotante += (
            f"\t - Tipo de habitacao: {adotante.tipo_habitacao.name}\n"
        )
        output_adotante += (
            f"\t - Tamanho da habitacao: {adotante.tamanho_habitacao.name}\n"
        )
        output_adotante += f"\t - Possui animal: {'Sim' if adotante.possui_animal else 'Nao'}\n"
        output_adotante += f"\t - Endereco: {adotante.endereco}\n"

        sg.Popup(
            f"Dados do adotante {nome[0:index_endfirstname if index_endfirstname > -1 else len(nome)]}:",
            output_adotante, background_color="#3F3F3F", button_color=("white", "green"), font=("Inter", 12)
        )

    def mostrar_adotantes(self, adotantes: list):
        layout = self.layout_tabela_mostrar_adotantes(adotantes)
        layout.append([sg.Button("Fechar", key="fechar", button_color="red", font=("Inter", 12))],)

        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F")
        self.__window.read()
        self.__window.close()

    def layout_tabela_mostrar_adotantes(self, adotantes: list):
        toprow = [
            "CPF",
            "Nome",
            "Data nascimento",
            "Tipo habitacao",
            "Tamanho habitacao",
            "Possui animal",
            "Endereco",
        ]
        dados_adotantes = [
            [
                "{}.{}.{}-{}".format(adotante.cpf[:3], adotante.cpf[3:6], adotante.cpf[6:9], adotante.cpf[9:]),
                adotante.nome,
                str(adotante.data_nascimento.strftime('%d/%m/%Y')),
                adotante.tipo_habitacao.name,
                adotante.tamanho_habitacao.name,
                "Sim" if adotante.possui_animal else "Nao",
                str(adotante.endereco),
            ]
            for adotante in adotantes
        ]
        return [
            [
                sg.Table(
                    headings=toprow,
                    values=dados_adotantes,
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

    def cpf_invalido(self, cpf: str):
        return len(cpf) != 11

    def selecionar_adotante(self, adotantes: list, mostrar_opcoes: bool):
        layout = []

        if mostrar_opcoes:
            layout.append(self.layout_tabela_mostrar_adotantes(adotantes))

        layout.append([
            [sg.Text("CPF do adotante que deseja selecionar: ", font=("Inter", 12), background_color="#3F3F3F",
                     pad=10)],
            [sg.Combo(values=[adotante.cpf for adotante in adotantes],
                      default_value=adotantes[0].cpf,
                      size=(22, 10),
                      font=("Inter", 14),
                      button_background_color="#2B2B2B",
                      pad=((15, 0), (0, 0)),
                      key="cpf")],
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

        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F")
        button, values = self.__window.read()
        self.__window.close()

        if button == "cancelar":
            return

        return values["cpf"]

    def mostrar_mensagem(self, msg):
        sg.popup("", msg, background_color="#3F3F3F", button_color=("white", "green"), font=("Inter", 12))

    def input_valido(self):
        data_formato_valido = True
        campos_nao_preenchidos = []

        cpf = self.__window["cpf"].get().strip()
        nome = self.__window["nome"].get().strip()
        tipo_habitacao = (self.__window["casa"].get() or self.__window["apartamento"].get())
        tamanho_habitacao = (
                self.__window["pequeno"].get()
                or self.__window["medio"].get()
                or self.__window["grande"].get()
        )
        possui_animal = (self.__window["possui"].get() or self.__window["nao_possui"].get())
        logradouro = self.__window["logradouro"].get().strip()
        numero = self.__window["numero"].get().strip()

        try:
            data_nascimento = self.__window["data_nascimento"].get().strip()
            datetime.strptime(data_nascimento, "%d/%m/%Y").date()
        except ValueError:
            sg.popup("Data em formato invalido! Tente novamente.", background_color="#3F3F3F",
                     button_color=("white", "green"), font=("Inter", 12))
            data_formato_valido = False

        if not cpf:
            campos_nao_preenchidos.append("CPF")
        if not nome:
            campos_nao_preenchidos.append("Nome")
        if not logradouro:
            campos_nao_preenchidos.append("Logradouro")
        if not numero:
            campos_nao_preenchidos.append("Numero")
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

        return data_formato_valido
