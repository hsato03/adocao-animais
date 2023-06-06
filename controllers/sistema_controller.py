from views import SistemaView
from controllers import (
    AdotanteController,
    AdocaoController,
    AnimalController,
    DoadorController,
    DoacaoController,
    VacinaController,
)
from exceptions import OpcaoInvalidaException


class SistemaController:
    def __init__(self):
        self.__controlador_adotantes = AdotanteController(self)
        self.__controlador_adocoes = AdocaoController(self)
        self.__controlador_animais = AnimalController(self)
        self.__controlador_doadores = DoadorController(self)
        self.__controlador_doacoes = DoacaoController(self)
        self.__controlador_vacinas = VacinaController(self)
        self.__tela_sistema = SistemaView()

    @property
    def controlador_adotantes(self):
        return self.__controlador_adotantes

    @property
    def controlador_adocoes(self):
        return self.__controlador_adocoes

    @property
    def controlador_animais(self):
        return self.__controlador_animais

    @property
    def controlador_doadores(self):
        return self.__controlador_doadores

    @property
    def controlador_vacinas(self):
        return self.__controlador_vacinas

    def inicializar_sistema(self):
        self.abrir_tela()

    def cadastrar_adotantes(self):
        self.__controlador_adotantes.abrir_tela()

    def cadastrar_adocoes(self):
        self.__controlador_adocoes.abrir_tela()

    def cadastrar_animais(self):
        self.__controlador_animais.abrir_tela()

    def cadastrar_doadores(self):
        self.__controlador_doadores.abrir_tela()

    def cadastrar_doacoes(self):
        self.__controlador_doacoes.abrir_tela()

    def cadastrar_vacinas(self):
        self.__controlador_vacinas.abrir_tela()

    def encerrar_sistema(self):
        exit(0)

    def abrir_tela(self):
        lista_opcoes = {
            6: self.cadastrar_vacinas,
            5: self.cadastrar_doacoes,
            4: self.cadastrar_doadores,
            3: self.cadastrar_animais,
            2: self.cadastrar_adocoes,
            1: self.cadastrar_adotantes,
            0: self.encerrar_sistema,
        }

        while True:
            try:
                opcao_escolhida = self.__tela_sistema.telar_opcoes()
                funcao_escolhida = lista_opcoes[opcao_escolhida]
                funcao_escolhida()
            except OpcaoInvalidaException as e:
                print(e)
            except ValueError:
                print("Somente numeros. Tente novamente.")
