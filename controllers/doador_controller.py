from exceptions import (
    EntidadeNaoEncontradaException,
    CpfInvalidoException,
    IdentificadorJaExistenteException,
)
from model import Doador
from views import DoadorView
from persistence import DoadorDAO


class DoadorController:
    def __init__(self, controlador_sistema):
        self.__doador_dao = DoadorDAO("datasources/doadores.pkl")
        self.__tela_doador = DoadorView()
        self.__controlador_sistema = controlador_sistema

    def buscar_doador_por_cpf(self, cpf: str):
        doador = self.__doador_dao.find_by_id(cpf)
        if doador:
            return doador

        raise EntidadeNaoEncontradaException("ERRO: Doador nao existente.")

    def incluir_doador(self):
        dados_doador = self.__tela_doador.pegar_dados_doador(doador=None)

        if not dados_doador:
            return

        self.validar_digitos_cpf(dados_doador["cpf"])
        self.verificar_cpf_doador_ja_cadastrado(dados_doador["cpf"])
        self.__controlador_sistema.controlador_adotantes.verificar_cpf_adotante_ja_cadastrado(
            dados_doador["cpf"]
        )

        doador = Doador(
            dados_doador["cpf"],
            dados_doador["nome"],
            dados_doador["data_nascimento"],
            dados_doador["logradouro"],
            dados_doador["numero"],
        )
        self.__doador_dao.insert(doador)

    def alterar_doador(self):
        self.verificar_nenhum_doador_cadastrado()

        cpf_doador = self.__tela_doador.selecionar_doador(self.__doador_dao.find_all(), mostrar_opcoes=True)

        if not cpf_doador:
            return

        doador = self.buscar_doador_por_cpf(cpf_doador)
        novos_dados_doador = self.__tela_doador.pegar_dados_doador(doador=doador)

        if not novos_dados_doador:
            return

        self.validar_digitos_cpf(novos_dados_doador["cpf"])

        if cpf_doador != novos_dados_doador["cpf"]:
            self.verificar_cpf_doador_ja_cadastrado(novos_dados_doador["cpf"])
            self.__controlador_sistema.controlador_adotantes.verificar_cpf_adotante_ja_cadastrado(
                novos_dados_doador["cpf"]
            )

        doador.nome = novos_dados_doador["nome"]
        doador.cpf = novos_dados_doador["cpf"]
        doador.data_nascimento = novos_dados_doador["data_nascimento"]
        doador.add_endereco(
            novos_dados_doador["logradouro"], novos_dados_doador["numero"]
        )

        self.__doador_dao.update(cpf_doador, doador)
        self.__tela_doador.mostrar_mensagem("Doador alterado com sucesso.")

    def listar_doadores(self):
        self.verificar_nenhum_doador_cadastrado()

        self.__tela_doador.mostrar_doadores(self.__doador_dao.find_all())

    def excluir_doador(self):
        self.verificar_nenhum_doador_cadastrado()

        cpf_doador = self.__tela_doador.selecionar_doador(doadores=self.__doador_dao.find_all(), mostrar_opcoes=True)

        if not cpf_doador:
            return

        self.__doador_dao.remove(cpf_doador)
        self.__tela_doador.mostrar_mensagem("Doador removido com sucesso.")

    def listar_doador_por_cpf(self):
        self.verificar_nenhum_doador_cadastrado()

        cpf_doador = self.__tela_doador.selecionar_doador(doadores=self.__doador_dao.find_all(), mostrar_opcoes=False)

        if not cpf_doador:
            return

        doador = self.buscar_doador_por_cpf(cpf_doador)
        self.__tela_doador.mostrar_doador(doador)

    def selecionar_doador(self):
        self.verificar_nenhum_doador_cadastrado()
        cpf = self.__tela_doador.selecionar_doador(doadores=self.__doador_dao.find_all(), mostrar_opcoes=True)

        if not cpf:
            return

        return self.buscar_doador_por_cpf(cpf)

    def verificar_cpf_doador_ja_cadastrado(self, cpf: str):
        if self.__doador_dao.find_by_id(cpf):
            raise IdentificadorJaExistenteException(cpf)

    def verificar_nenhum_doador_cadastrado(self):
        if len(self.__doador_dao.find_all()) <= 0:
            raise EntidadeNaoEncontradaException("Nennum doador cadastrado.")

    def validar_digitos_cpf(self, cpf):
        int(cpf)

    def retornar(self):
        self.__controlador_sistema.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_doador,
            2: self.alterar_doador,
            3: self.listar_doadores,
            4: self.excluir_doador,
            5: self.listar_doador_por_cpf,
            0: self.retornar,
        }

        while True:
            try:
                lista_opcoes[self.__tela_doador.telar_opcoes()]()
            except (
                EntidadeNaoEncontradaException,
                CpfInvalidoException,
                IdentificadorJaExistenteException,
            ) as e:
                self.__tela_doador.mostrar_mensagem(e)
            except ValueError:
                self.__tela_doador.mostrar_mensagem("Somente numeros. Tente novamente.")
