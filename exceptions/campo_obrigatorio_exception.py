class CampoObrigatorioException(Exception):
    def __init__(self, campos: list):
        msg = "Campo(s) obrigatorio(s): \n"
        for campo in campos:
            msg += f"\t - {campo}\n"
        super().__init__(msg)
