from views import AdotanteView
from model import Adotante, TipoHabitacao, TamanhoHabitacao
from exceptions import (
    EntidadeNaoEncontradaException,
    OpcaoInvalidaException,
    CpfInvalidoException,
    IdentificadorJaExistenteException,
)


class AdotanteController:
    def __init__(self, controlador_sistema):
        self.__adotantes = []
        self.__tela_adotante = AdotanteView()
        self.__controlador_sistema = controlador_sistema

    def buscar_adotante_por_cpf(self, cpf: str):
        for adotante in self.__adotantes:
            if adotante.cpf == cpf:
                return adotante
        raise EntidadeNaoEncontradaException("ERRO: Adotante nao existente.")

    def incluir_adotante(self):
        dados_adotante = self.__tela_adotante.pegar_dados_adotante()

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
        self.__adotantes.append(adotante)

    def alterar_adotante(self):
        if len(self.__adotantes) <= 0:
            self.__tela_adotante.mostrar_mensagem("Nenhum adotante cadastrado.")
            return

        self.listar_adotantes()
        cpf_adotante = self.__tela_adotante.selecionar_adotante()
        adotante = self.buscar_adotante_por_cpf(cpf_adotante)
        novos_dados_adotante = self.__tela_adotante.pegar_dados_adotante()

        self.validar_digitos_cpf(novos_dados_adotante["cpf"])

        if cpf_adotante != novos_dados_adotante["cpf"]:
            self.verificar_cpf_adotante_ja_cadastrado(novos_dados_adotante["cpf"])
            self.__controlador_sistema.controlador_doadores.verificar_cpf_doador_ja_cadastrado(
                novos_dados_adotante["cpf"]
            )

        adotante.nome = novos_dados_adotante["nome"]
        adotante.cpf = novos_dados_adotante["cpf"]
        adotante.data = novos_dados_adotante["data_nascimento"]
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
        self.listar_adotantes()

    def listar_adotantes(self):
        if len(self.__adotantes) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum adotante cadastrado.")

        for i in range(len(self.__adotantes)):
            adotante = self.__adotantes[i]
            self.__tela_adotante.mostrar_mensagem(f"\nADOTANTE #{i + 1:02d}")
            self.__tela_adotante.mostrar_adotante(
                {
                    "cpf": adotante.cpf,
                    "nome": adotante.nome,
                    "data_nascimento": adotante.data_nascimento,
                    "tipo_habitacao": adotante.tipo_habitacao,
                    "tamanho_habitacao": adotante.tamanho_habitacao,
                    "possui_animal": adotante.possui_animal,
                    "endereco": adotante.endereco,
                }
            )

    def excluir_adotante(self):
        if len(self.__adotantes) <= 0:
            self.__tela_adotante.mostrar_mensagem("Nenhum adotante cadastrado.")
            return

        self.listar_adotantes()
        cpf_adotante = self.__tela_adotante.selecionar_adotante()
        adotante = self.buscar_adotante_por_cpf(cpf_adotante)

        self.__adotantes.remove(adotante)
        self.__tela_adotante.mostrar_mensagem("Adotante removido com sucesso.")

    def listar_adotante_por_cpf(self):
        if len(self.__adotantes) <= 0:
            self.__tela_adotante.mostrar_mensagem("Nenhum adotante cadastrado.")
            return

        cpf_adotante = self.__tela_adotante.selecionar_adotante()
        adotante = self.buscar_adotante_por_cpf(cpf_adotante)

        self.__tela_adotante.mostrar_adotante(
            {
                "cpf": adotante.cpf,
                "nome": adotante.nome,
                "data_nascimento": adotante.data_nascimento,
                "tipo_habitacao": adotante.tipo_habitacao,
                "tamanho_habitacao": adotante.tamanho_habitacao,
                "possui_animal": adotante.possui_animal,
                "endereco": adotante.endereco,
            }
        )

    def verificar_cpf_adotante_ja_cadastrado(self, cpf: str):
        for adotante in self.__adotantes:
            if adotante.cpf == cpf:
                raise IdentificadorJaExistenteException(cpf)

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
                OpcaoInvalidaException,
                EntidadeNaoEncontradaException,
                CpfInvalidoException,
                IdentificadorJaExistenteException,
            ) as e:
                self.__tela_adotante.mostrar_mensagem(e)
            except ValueError:
                self.__tela_adotante.mostrar_mensagem(
                    "Somente numeros. Tente novamente."
                )
