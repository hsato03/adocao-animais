from exceptions import EntidadeNaoEncontradaException
from model import Doacao
from views import DoacaoView
from persistence import DoacaoDAO


class DoacaoController:
    def __init__(self, controlador_sistema):
        self.__doacao_dao = DoacaoDAO("doacoes.pkl")
        self.__tela_doacao = DoacaoView()
        self.__controlador_sistema = controlador_sistema

    def buscar_doacao_por_numero_chip(self, numero_chip: int):
        doacao = self.__doacao_dao.find_by_id(numero_chip)
        if doacao:
            return doacao

        raise EntidadeNaoEncontradaException("ERRO: Doacao nao existente.")

    def incluir_doacao(self):
        animal = self.__controlador_sistema.controlador_animais.selecionar_animal()
        if not animal:
            return

        doador = self.__controlador_sistema.controlador_doadores.selecionar_doador()
        if not doador:
            return

        dados_doacao = self.__tela_doacao.pegar_dados_doacao(doacao=None)
        if not dados_doacao:
            return

        doacao = Doacao(
            doador,
            animal,
            dados_doacao["data"],
            dados_doacao["motivo"],
        )
        self.__doacao_dao.insert(doacao)

    def alterar_doacao(self):
        self.verificar_nenhuma_doacao_cadastrada()

        numero_chip = self.__tela_doacao.selecionar_doacao(doacoes=self.__doacao_dao.find_all())

        if not numero_chip:
            return

        doacao = self.buscar_doacao_por_numero_chip(numero_chip)
        novos_dados_doacao = self.__tela_doacao.pegar_dados_doacao(doacao=doacao)

        if not novos_dados_doacao:
            return

        doacao.data = novos_dados_doacao["data"]
        doacao.motivo = novos_dados_doacao["motivo"]

        self.__doacao_dao.update(numero_chip, doacao)
        self.__tela_doacao.mostrar_mensagem("Doacao alterada com sucesso.")

    def listar_doacoes(self):
        self.verificar_nenhuma_doacao_cadastrada()

        self.__tela_doacao.mostrar_doacoes(self.__doacao_dao.find_all())

    def excluir_doacao(self):
        self.verificar_nenhuma_doacao_cadastrada()

        numero_chip = self.__tela_doacao.selecionar_doacao(doacoes=self.__doacao_dao.find_all())

        if not numero_chip:
            return

        removed = self.__doacao_dao.remove(numero_chip)
        if removed:
            self.__tela_doacao.mostrar_mensagem("Doacao removida com sucesso.")
        else:
            self.__tela_doacao.mostrar_mensagem("Doacao não removida.")

    def listar_doacoes_por_periodo(self):
        self.verificar_nenhuma_doacao_cadastrada()

        dados_periodo = self.__tela_doacao.pegar_dados_periodo()
        if not dados_periodo:
            return

        data_inicio = dados_periodo["data_inicio"]
        data_fim = dados_periodo["data_fim"]
        doacoes_periodo = []

        for doacao in self.__doacao_dao.find_all():
            if data_inicio <= doacao.data <= data_fim:
                doacoes_periodo.append(doacao)

        if len(doacoes_periodo) <= 0:
            raise EntidadeNaoEncontradaException("Nenhuma doacao encontrada neste periodo")

        self.__tela_doacao.mostrar_doacoes(doacoes_periodo)

    def verificar_nenhuma_doacao_cadastrada(self):
        if len(self.__doacao_dao.find_all()) <= 0:
            raise EntidadeNaoEncontradaException("Nenhuma doacao cadastrada.")

    def retornar(self):
        self.__controlador_sistema.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_doacao,
            2: self.alterar_doacao,
            3: self.listar_doacoes,
            4: self.excluir_doacao,
            5: self.listar_doacoes_por_periodo,
            0: self.retornar,
        }

        while True:
            try:
                lista_opcoes[self.__tela_doacao.telar_opcoes()]()
            except EntidadeNaoEncontradaException as e:
                self.__tela_doacao.mostrar_mensagem(e)
            except ValueError:
                self.__tela_doacao.mostrar_mensagem("Somente numeros. Tente novamente")
