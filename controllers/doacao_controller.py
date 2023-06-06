from views import DoacaoView
from model import Doacao, Cachorro, TIPO_CACHORRO, TIPO_CPF
from exceptions import EntidadeNaoEncontradaException, OpcaoInvalidaException
from datetime import date


class DoacaoController:
    def __init__(self, controlador_sistema):
        self.__doacoes = []
        self.__tela_doacao = DoacaoView()
        self.__controlador_sistema = controlador_sistema

    def buscar_doacao_por_identificador(self, identificador, tipo_id: int):
        for doacao in self.__doacoes:
            if tipo_id == TIPO_CPF:
                if doacao.doador.cpf == identificador:
                    return doacao
            else:
                if doacao.animal.numero_chip == int(identificador):
                    return doacao
        raise EntidadeNaoEncontradaException("ERRO: Doacao nao existente.")

    def incluir_doacao(self):
        tipo_animal = self.__tela_doacao.telar_opcoes_tipo_animal()
        dados_doacao = self.__tela_doacao.pegar_dados_doacao(criacao=True)

        cpf_doador = dados_doacao["cpf_doador"]

        numero_chip = dados_doacao["numero_chip"]
        if tipo_animal == TIPO_CACHORRO:
            animal = self.__controlador_sistema.controlador_animais.buscar_cachorro_por_numero_chip(
                numero_chip
            )
        else:
            animal = self.__controlador_sistema.controlador_animais.buscar_gato_por_numero_chip(
                numero_chip
            )

        doador = self.__controlador_sistema.controlador_doadores.buscar_doador_por_cpf(
            cpf_doador
        )

        doacao = Doacao(
            doador,
            animal,
            dados_doacao["data"],
            dados_doacao["motivo"],
        )
        self.__doacoes.append(doacao)

    def alterar_doacao(self):
        if self.verificar_nenhuma_doacao_cadastrada():
            return

        self.listar_doacoes()

        tipo_id = self.get_tipo_id()

        identificador = self.__tela_doacao.selecionar_doacao(tipo_id)
        doacao = self.buscar_doacao_por_identificador(identificador, tipo_id)
        novos_dados_doacao = self.__tela_doacao.pegar_dados_doacao(criacao=False)

        doacao.data = novos_dados_doacao["data"]
        doacao.motivo = novos_dados_doacao["motivo"]

    def listar_doacoes(self):
        if self.verificar_nenhuma_doacao_cadastrada():
            return

        for i in range(len(self.__doacoes)):
            self.__tela_doacao.mostrar_mensagem(f"\nDOACAO #{i + 1:02d}")
            doacao = self.__doacoes[i]
            self.__tela_doacao.mostrar_doacao(
                {
                    "cpf_doador": doacao.doador.cpf,
                    "numero_chip": doacao.animal.numero_chip,
                    "data": doacao.data,
                    "motivo": doacao.motivo,
                }
            )

    def excluir_doacao(self):
        if self.verificar_nenhuma_doacao_cadastrada():
            return

        self.listar_doacoes()

        tipo_id = self.get_tipo_id()

        identificador = self.__tela_doacao.selecionar_doacao(tipo_id)
        doacao = self.buscar_doacao_por_identificador(identificador, tipo_id)
        self.__doacoes.remove(doacao)
        self.__tela_doacao.mostrar_mensagem("Doacao removida com sucesso.")

    def listar_doacao_por_identificador(self):
        if self.verificar_nenhuma_doacao_cadastrada():
            return

        while True:
            try:
                tipo_id = self.__tela_doacao.telar_opcoes_identificador()
                break
            except OpcaoInvalidaException as e:
                self.__tela_doacao.mostrar_mensagem(e)

        identificador = self.__tela_doacao.selecionar_doacao(tipo_id)

        doacao = self.buscar_doacao_por_identificador(identificador, tipo_id)

        self.__tela_doacao.mostrar_doacao(
            {
                "cpf_doador": doacao.doador.cpf,
                "numero_chip": doacao.animal.numero_chip,
                "data": doacao.data,
                "motivo": doacao.motivo,
            }
        )

    def listar_doacoes_por_periodo(self):
        contador = 1
        dados_periodo = self.__tela_doacao.pegar_dados_periodo()
        data_inicio = dados_periodo["data_inicio"]
        data_fim = dados_periodo["data_fim"]

        for doacao in self.__doacoes:
            if data_inicio <= doacao.data <= data_fim:
                self.__tela_doacao.mostrar_mensagem(f"DOACAO #{contador:02d}")
                self.__tela_doacao.mostrar_doacao(
                    {
                        "cpf_doador": doacao.doador.cpf,
                        "numero_chip": doacao.animal.numero_chip,
                        "data": doacao.data,
                        "motivo": doacao.motivo,
                    }
                )
                contador += 1

        if contador == 1:
            self.__tela_doacao.mostrar_mensagem(
                "Nenhuma doacao encontrada neste periodo"
            )

    def verificar_nenhuma_doacao_cadastrada(self):
        if len(self.__doacoes) <= 0:
            self.__tela_doacao.mostrar_mensagem("Nenhuma doacao cadastrada.")
            return True

    def get_tipo_id(self):
        while True:
            try:
                tipo_id = self.__tela_doacao.telar_opcoes_identificador()
                return tipo_id
            except OpcaoInvalidaException as e:
                self.__tela_doacao.mostrar_mensagem(e)
            except ValueError:
                self.__tela_doacao.mostrar_mensagem("Somente numeros. Tente novamente.")

    def retornar(self):
        self.__controlador_sistema.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_doacao,
            2: self.alterar_doacao,
            3: self.listar_doacoes,
            4: self.excluir_doacao,
            5: self.listar_doacao_por_identificador,
            6: self.listar_doacoes_por_periodo,
            0: self.retornar,
        }

        while True:
            try:
                lista_opcoes[self.__tela_doacao.telar_opcoes()]()
            except (OpcaoInvalidaException, EntidadeNaoEncontradaException) as e:
                self.__tela_doacao.mostrar_mensagem(e)
            except ValueError:
                self.__tela_doacao.mostrar_mensagem("Somente numeros. Tente novamente")
