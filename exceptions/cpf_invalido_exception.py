class CpfInvalidoException(Exception):
    def __init__(self, cpf: str):
        super().__init__(f"CPF: {cpf} invalido. Tente novamente")
