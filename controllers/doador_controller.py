from exceptions import (
    OpcaoInvalidaException,
    EntidadeNaoEncontradaException,
    CpfInvalidoException,
    IdentificadorJaExistenteException,
)
from views import DoadorView
from model import Doador


class DoadorController:
    def __init__(self, controlador_sistema):
        self.__doadores = []
        self.__tela_doador = DoadorView()
        self.__controlador_sistema = controlador_sistema

    def buscar_doador_por_cpf(self, cpf: str):
        for doador in self.__doadores:
            if doador.cpf == cpf:
                return doador
        raise EntidadeNaoEncontradaException("ERRO: Doador nao existente.")

    def incluir_doador(self):
        dados_doador = self.__tela_doador.pegar_dados_doador()

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
        self.__doadores.append(doador)

    def alterar_doador(self):
        if len(self.__doadores) <= 0:
            self.__tela_doador.mostrar_mensagem("Nenhum doador cadastrado.")
            return

        self.listar_doadores()
        cpf_doador = self.__tela_doador.selecionar_doador()
        doador = self.buscar_doador_por_cpf(cpf_doador)
        novos_dados_doador = self.__tela_doador.pegar_dados_doador()

        self.validar_digitos_cpf(novos_dados_doador["cpf"])

        if cpf_doador != novos_dados_doador["cpf"]:
            self.verificar_cpf_doador_ja_cadastrado(novos_dados_doador["cpf"])
            self.__controlador_sistema.controlador_adotantes.verificar_cpf_adotante_ja_cadastrado(
                novos_dados_doador["cpf"]
            )

        doador.nome = novos_dados_doador["nome"]
        doador.cpf = novos_dados_doador["cpf"]
        doador.data = novos_dados_doador["data_nascimento"]
        doador.add_endereco(
            novos_dados_doador["logradouro"], novos_dados_doador["numero"]
        )
        self.listar_doadores()

    def listar_doadores(self):
        if len(self.__doadores) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum doador cadastrado.")

        for i in range(len(self.__doadores)):
            doador = self.__doadores[i]
            self.__tela_doador.mostrar_mensagem(f"\nADOTANTE #{i + 1:02d}")
            self.__tela_doador.mostrar_doador(
                {
                    "cpf": doador.cpf,
                    "nome": doador.nome,
                    "data_nascimento": doador.data_nascimento,
                    "endereco": doador.endereco,
                }
            )

    def excluir_doador(self):
        if len(self.__doadores) <= 0:
            self.__tela_doador.mostrar_mensagem("Nenhum doador cadastrado.")
            return

        self.listar_doadores()
        cpf_doador = self.__tela_doador.selecionar_doador()
        doador = self.buscar_doador_por_cpf(cpf_doador)

        self.__doadores.remove(doador)
        self.__tela_doador.mostrar_mensagem("Doador removido com sucesso.")

    def listar_doador_por_cpf(self):
        if len(self.__doadores) <= 0:
            self.__tela_doador.mostrar_mensagem("Nenhum doador cadastrado.")
            return

        cpf_doador = self.__tela_doador.selecionar_doador()
        doador = self.buscar_doador_por_cpf(cpf_doador)

        self.__tela_doador.mostrar_doador(
            {
                "cpf": doador.cpf,
                "nome": doador.nome,
                "data_nascimento": doador.data_nascimento,
                "endereco": doador.endereco,
            }
        )

    def verificar_cpf_doador_ja_cadastrado(self, cpf: str):
        for doador in self.__doadores:
            if doador.cpf == cpf:
                raise IdentificadorJaExistenteException(cpf)

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
                OpcaoInvalidaException,
                EntidadeNaoEncontradaException,
                CpfInvalidoException,
                IdentificadorJaExistenteException,
            ) as e:
                self.__tela_doador.mostrar_mensagem(e)
            except ValueError:
                self.__tela_doador.mostrar_mensagem("Somente numeros. Tente novamente.")
