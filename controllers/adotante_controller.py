from views import AdotanteView
from model import Adotante, TipoHabitacao, TamanhoHabitacao
from persistence import AdotanteDAO
from exceptions import (
    EntidadeNaoEncontradaException,
    CpfInvalidoException,
    IdentificadorJaExistenteException,
)


class AdotanteController:
    def __init__(self, controlador_sistema):
        self.__adotante_dao = AdotanteDAO("datasources/adotantes.pkl")
        self.__tela_adotante = AdotanteView()
        self.__controlador_sistema = controlador_sistema

    def buscar_adotante_por_cpf(self, cpf: str):
        adotante = self.__adotante_dao.find_by_id(cpf)
        if adotante is not None:
            return adotante

        raise EntidadeNaoEncontradaException("ERRO: Adotante nao existente.")

    def incluir_adotante(self):
        dados_adotante = self.__tela_adotante.pegar_dados_adotante(adotante=None)

        if not dados_adotante:
            return

        self.validar_digitos_cpf(dados_adotante["cpf"])
        self.verificar_cpf_adotante_ja_cadastrado(dados_adotante["cpf"])
        self.__controlador_sistema.controlador_doadores.verificar_cpf_doador_ja_cadastrado(
            dados_adotante["cpf"]
        )

        adotante = Adotante(
            dados_adotante["cpf"],
            dados_adotante["nome"],
            dados_adotante["data_nascimento"],
            dados_adotante["logradouro"],
            dados_adotante["numero"],
            TipoHabitacao(dados_adotante["tipo_habitacao"]),
            TamanhoHabitacao(dados_adotante["tamanho_habitacao"]),
            True if dados_adotante["possui_animal"] == 1 else False,
        )
        self.__adotante_dao.insert(adotante)

    def alterar_adotante(self):
        self.verificar_nenhum_adotante_cadastrado()

        cpf_adotante = self.__tela_adotante.selecionar_adotante(
            adotantes=self.__adotante_dao.find_all(), mostrar_opcoes=True
        )

        if not cpf_adotante:
            return

        adotante = self.buscar_adotante_por_cpf(cpf_adotante)
        novos_dados_adotante = self.__tela_adotante.pegar_dados_adotante(
            adotante=adotante
        )

        if not novos_dados_adotante:
            return

        self.validar_digitos_cpf(novos_dados_adotante["cpf"])

        if cpf_adotante != novos_dados_adotante["cpf"]:
            self.verificar_cpf_adotante_ja_cadastrado(novos_dados_adotante["cpf"])
            self.__controlador_sistema.controlador_doadores.verificar_cpf_doador_ja_cadastrado(
                novos_dados_adotante["cpf"]
            )

        adotante.nome = novos_dados_adotante["nome"]
        adotante.cpf = novos_dados_adotante["cpf"]
        adotante.data_nascimento = novos_dados_adotante["data_nascimento"]
        adotante.tipo_habitacao = TipoHabitacao(novos_dados_adotante["tipo_habitacao"])
        adotante.tamanho_habitacao = TamanhoHabitacao(
            novos_dados_adotante["tamanho_habitacao"]
        )
        adotante.possui_animal = (
            True if novos_dados_adotante["possui_animal"] == 1 else False
        )
        adotante.add_endereco(
            novos_dados_adotante["logradouro"], novos_dados_adotante["numero"]
        )

        self.__adotante_dao.update(cpf_adotante, adotante)
        self.__tela_adotante.mostrar_mensagem("Adotante alterado com sucesso.")

    def listar_adotantes(self):
        self.verificar_nenhum_adotante_cadastrado()

        self.__tela_adotante.mostrar_adotantes(self.__adotante_dao.find_all())

    def excluir_adotante(self):
        self.verificar_nenhum_adotante_cadastrado()

        cpf_adotante = self.__tela_adotante.selecionar_adotante(adotantes=self.__adotante_dao.find_all(), mostrar_opcoes=True)

        if not cpf_adotante:
            return

        removed = self.__adotante_dao.remove(cpf_adotante)
        if removed:
            self.__tela_adotante.mostrar_mensagem("Adotante removido com sucesso.")
        else:
            self.__tela_adotante.mostrar_mensagem("Adotante não removido.")

    def listar_adotante_por_cpf(self):
        self.verificar_nenhum_adotante_cadastrado()

        cpf_adotante = self.__tela_adotante.selecionar_adotante(
            adotantes=self.__adotante_dao.find_all(), mostrar_opcoes=False
        )

        if not cpf_adotante:
            return

        adotante = self.buscar_adotante_por_cpf(cpf_adotante)
        self.__tela_adotante.mostrar_adotante(adotante)

    def selecionar_adotante(self):
        self.verificar_nenhum_adotante_cadastrado()
        cpf = self.__tela_adotante.selecionar_adotante(adotantes=self.__adotante_dao.find_all(), mostrar_opcoes=True)

        if not cpf:
            return

        return self.buscar_adotante_por_cpf(cpf)

    def verificar_cpf_adotante_ja_cadastrado(self, cpf: str):
        if self.__adotante_dao.find_by_id(cpf):
            raise IdentificadorJaExistenteException(cpf)

    def verificar_nenhum_adotante_cadastrado(self):
        if len(self.__adotante_dao.find_all()) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum adotante cadastrado.")

    def validar_digitos_cpf(self, cpf):
        int(cpf)

    def retornar(self):
        self.__controlador_sistema.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_adotante,
            2: self.alterar_adotante,
            3: self.listar_adotantes,
            4: self.excluir_adotante,
            5: self.listar_adotante_por_cpf,
            0: self.retornar,
        }

        while True:
            try:
                lista_opcoes[self.__tela_adotante.telar_opcoes()]()
            except (
                EntidadeNaoEncontradaException,
                CpfInvalidoException,
                IdentificadorJaExistenteException,
            ) as e:
                self.__tela_adotante.mostrar_mensagem(e)
