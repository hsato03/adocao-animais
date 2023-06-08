from controllers.sistema_controller import SistemaController
import PySimpleGUI as sg

if __name__ == "__main__":
    SistemaController.inicializar_sistema(SistemaController())

# layout = [[sg.Text('Date Chooser Test Harness', key='-TXT-')],
#       [sg.Input(key='-IN-', size=(20,1)), sg.CalendarButton('Cal US No Buttons Location (0,0)', close_when_date_chosen=True,  target='-IN-', location=(0,0), no_titlebar=False, )],
#       [sg.Input(key='-IN3-', size=(20,1)), sg.CalendarButton('Cal Monday', title='Pick a date any date', no_titlebar=True, close_when_date_chosen=False,  target='-IN3-', begin_at_sunday_plus=1, month_names=('студзень', 'люты', 'сакавік', 'красавік', 'май', 'чэрвень', 'ліпень', 'жнівень', 'верасень', 'кастрычнік', 'лістапад', 'снежань'), day_abbreviations=('Дш', 'Шш', 'Шр', 'Бш', 'Жм', 'Иш', 'Жш'))],
#       [sg.Input(key='-IN2-', size=(20,1)), sg.CalendarButton('Cal German Feb 2020',  target='-IN2-',  default_date_m_d_y=(2,None,2020), locale='de_DE', begin_at_sunday_plus=1)],
#       [sg.Input(key='data_nascimento', size=(20, 2)), sg.CalendarButton('Cal Format %m-%d-%y Jan 2020',  target='data_nascimento', format='%m-%d-%Y')],
#       [sg.Button('Read'), sg.Button('Date Popup'), sg.Exit()]]
#
# window = sg.Window('window', layout)
#
# while True:
#     event, values = window.read()
#     print(event, values)
#     if event in (sg.WIN_CLOSED, 'Exit'):
#         break
#     elif event == 'Date Popup':
#         sg.popup('You chose:', sg.popup_get_date())
# window.close()