import PySimpleGUI as sg


class SistemaView:
    def __init__(self):
        self.__window = None
        self.init_components()

    def telar_opcoes(self):
        self.init_components()
        button, values = self.__window.read()
        if button == "adotantes":
            opcao = 1
        elif button == "adocoes":
            opcao = 2
        elif button == "animais":
            opcao = 3
        elif button == "doadores":
            opcao = 4
        elif button == "doacoes":
            opcao = 5
        elif button == "vacinas":
            opcao = 6
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
                                "DONAPTION",
                                font=["Inter", 30, "bold underline"],
                                size=[20, 2],
                                justification="center",
                                pad=((0, 0), (40, 0)),
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
                                "Adotantes",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="adotantes",
                            )
                        ],
                        [
                            sg.Button(
                                "Adocoes",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="adocoes",
                            )
                        ],
                        [
                            sg.Button(
                                "Animais",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="animais",
                            )
                        ],
                        [
                            sg.Button(
                                "Doadores",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="doadores",
                            )
                        ],
                        [
                            sg.Button(
                                "Doacoes",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="doacoes",
                            )
                        ],
                        [
                            sg.Button(
                                "Vacinas",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="vacinas",
                            )
                        ],
                        [
                            sg.Button(
                                "Finalizar Sistema",
                                size=(20, 2),
                                button_color="#FF2929",
                                mouseover_colors="#FF5454",
                                font=("Inter", 13),
                                key="sair",
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
