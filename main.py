from controllers.sistema_controller import SistemaController
import PySimpleGUI as sg

# if __name__ == "__main__":
#     sc = SistemaController()
#     sc.inicializar_sistema()

layout = [
    [sg.Text("Donadoption", font=["Inter", 25, "bold"], size=[20, 2], justification="center", pad=((0, 0), (25, 0)), background_color="#3F3F3F")],
    [sg.Column([
        [sg.Button("Adotantes", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"))],
        [sg.Button("Adocoes", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"))],
        [sg.Button("Animais", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"))],
        [sg.Button("Doadores", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"))],
        [sg.Button("Doacoes", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"))],
        [sg.Button("Vacinas", size=(20, 2), font=("Inter", 12), button_color=("black", "#FEFEFE"))],
        [sg.Button("Finalizar Sistema", size=(20, 2), button_color="red", font=("Inter", 12))]
    ], justification="center", background_color="#3F3F3F")]
]

window = sg.Window("Window Layout", layout, size=(400, 530), background_color="#3F3F3F")
button, values = window.read()

print(button)
print(values)

window.close()
