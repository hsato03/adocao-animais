class IdentificadorJaExistenteException(Exception):
    def __init__(self, identificador):
        super().__init__(f"ID {identificador} ja esta cadastrado. Tente novamente")
