class OpcaoInvalidaException(Exception):
    def __init__(self):
        super().__init__("ERRO: Opcao invalida! Tente novamente.")
