from datetime import datetime

import PySimpleGUI as sg

from exceptions import CampoObrigatorioException


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

    def pegar_dados_doacao(self, doacao):
        if doacao:
            layout = [
                [sg.Text("ALTERAR DOACAO", font=("Inter", 25), justification="center")],
                [sg.Text("Data de doacao:", size=(15, 1)),
                 sg.Input(doacao.data.strftime('%d/%m/%Y'), size=(26, 1), key="data"),
                 sg.CalendarButton("Abrir calendario", target="data", format="%d/%m/%Y")],
                [sg.Text("Motivo:", size=(15, 1)),
                 sg.Input(doacao.motivo, key="motivo")],
                [sg.Button("Confirmar", key="confirmar"),
                 sg.Cancel("Cancelar", key="cancelar")]
            ]
        else:
            layout = [
                [sg.Text("CADASTRO DOACAO", font=("Inter", 25), justification="center")],
                [sg.Text("Data de doacao:", size=(15, 1)),
                 sg.Input("", size=(26, 1), key="data"),
                 sg.CalendarButton("Abrir calendario", target="data", format="%d/%m/%Y")],
                [sg.Text("Motivo:", size=(15, 1)),
                 sg.Input("", key="motivo")],
                [sg.Button("Confirmar", key="confirmar"),
                 sg.Cancel("Cancelar", key="cancelar")]
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

        data_doacao_convertida = datetime.strptime(
            values["data"], "%d/%m/%Y"
        ).date()

        return {
            "data": data_doacao_convertida,
            "motivo": values["motivo"]
        }

    def pegar_dados_periodo(self):
        layout = [
            [sg.Text("Data de inicio:", size=(20, 1)),
             sg.Input("", size=(26, 1), key="data_inicio"),
             sg.CalendarButton("Abrir calendario", target="data_inicio", format="%d/%m/%Y")],
            [sg.Text("Data de fim:", size=(20, 1)),
             sg.Input("", size=(26, 1), key="data_fim"),
             sg.CalendarButton("Abrir calendario", target="data_fim", format="%d/%m/%Y")],
            [sg.Button("Confirmar", key="confirmar"),
             sg.Button("Cancelar", key="cancelar")],
        ]

        self.__window = sg.Window("Layout", layout)
        while True:
            try:
                button, values = self.__window.read()
                if button == "cancelar":
                    self.__window.close()
                    return

                data_inicio_convertida = datetime.strptime(values["data_inicio"], "%d/%m/%Y").date()
                data_fim_convertida = datetime.strptime(values["data_fim"], "%d/%m/%Y").date()
                self.__window.close()
                return {"data_inicio": data_inicio_convertida, "data_fim": data_fim_convertida}
            except ValueError:
                sg.popup("", "ERRO: Data em formato invalido")

    def mostrar_doacao(self, doacao):
        output_adotante = f"\t - Adotante: {doacao.doador.cpf}\n"
        output_adotante += f"\t - Animal: {doacao.animal.numero_chip}\n"
        output_adotante += f"\t - Data de doacao: {doacao.data.strftime('%d/%m/%Y')}\n"
        output_adotante += f"\t - Motivo: {doacao.motivo}\n"

        sg.Popup("", output_adotante)

    def mostrar_doacoes(self, doacoes: list):
        dados_doacoes = [
            [
                "{}.{}.{}-{}".format(
                    doacao.doador.cpf[:3],
                    doacao.doador.cpf[3:6],
                    doacao.doador.cpf[6:9],
                    doacao.doador.cpf[9:]
                ),
                doacao.animal.numero_chip,
                str(doacao.data.strftime('%d/%m/%Y')),
                doacao.motivo,
            ]
            for doacao in doacoes
        ]

        layout = self.layout_tabela_mostrar_doacoes(dados_doacoes)
        layout.append([sg.Button("Fechar", key="fechar", button_color="red")],)

        self.__window = sg.Window("Layout", layout)
        self.__window.read()
        self.__window.close()

    def layout_tabela_mostrar_doacoes(self, dados_doacoes: list):
        toprow = [
            "Doador",
            "Animal",
            "Data doacao",
            "Motivo",
        ]

        return [
            [
                sg.Table(
                    headings=toprow,
                    values=dados_doacoes,
                    auto_size_columns=True,
                    expand_y=True,
                    expand_x=True,
                    justification="center",
                    display_row_numbers=True,
                    key="table",
                )
            ],
        ]

    def selecionar_doacao(self, doacoes: list):
        dados_doacoes = [
            [
                "{}.{}.{}-{}".format(
                    doacao.doador.cpf[:3],
                    doacao.doador.cpf[3:6],
                    doacao.doador.cpf[6:9],
                    doacao.doador.cpf[9:]
                ),
                doacao.animal.numero_chip,
                str(doacao.data.strftime('%d/%m/%Y')),
                doacao.motivo,
            ]
            for doacao in doacoes
        ]
        layout = self.layout_tabela_mostrar_doacoes(dados_doacoes)

        layout.append([
            [sg.Text("Doacao que deseja selecionar: ")],
            [sg.Combo(values=[i for i in range(len(doacoes))], default_value=0, key="row")],
            [sg.Button("Confirmar", key="confirmar"),
             sg.Button("Cancelar", key="cancelar", button_color="red")],
        ])
        self.__window = sg.Window("Layout", layout)
        button, values = self.__window.read()
        print(values["row"])
        doacao = dados_doacoes[int(values["row"])]
        numero_chip = doacao[1]
        self.__window.close()

        if button == "cancelar":
            return

        return int(numero_chip)

    def mostrar_mensagem(self, msg: str):
        sg.popup("", msg)

    def input_valido(self):
        data_formato_valido = True
        campos_nao_preenchidos = []

        motivo = self.__window["motivo"].get()

        try:
            data_doacao = self.__window["data"].get().strip()
            datetime.strptime(data_doacao, "%d/%m/%Y").date()
        except ValueError:
            sg.popup("Data em formato invalido! Tente novamente.")
            data_formato_valido = False

        if not motivo:
            campos_nao_preenchidos.append("Motivo")

        if len(campos_nao_preenchidos) > 0:
            raise CampoObrigatorioException(campos_nao_preenchidos)

        return data_formato_valido
