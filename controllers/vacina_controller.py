from views import VacinaView
from model import Vacina
from exceptions import EntidadeNaoEncontradaException, IdentificadorJaExistenteException


class VacinaController:
    def __init__(self, controlador_sistema):
        self.__vacinas = []
        self.__tela_vacina = VacinaView()
        self.__controlador_sistema = controlador_sistema

    def buscar_vacina_por_identificador(self, identificador: str):
        for vacina in self.__vacinas:
            if vacina.identificador == identificador:
                return vacina
        raise EntidadeNaoEncontradaException("ERRO: Vacina nao existente.")

    def incluir_vacina(self):
        dados_vacina = self.__tela_vacina.pegar_dados_vacina(vacina=None)

        if not dados_vacina:
            return

        self.verificar_id_ja_cadastrado(dados_vacina["id"])

        vacina = Vacina(
            dados_vacina["id"],
            dados_vacina["nome"],
        )
        self.__vacinas.append(vacina)

    def alterar_vacina(self):
        self.verificar_nenhuma_vacina_cadastrada()

        identificador = self.__tela_vacina.selecionar_vacina(
            [vacina.identificador for vacina in self.__vacinas],
            vacinas=self.__vacinas,
        )

        if not identificador:
            return

        vacina = self.buscar_vacina_por_identificador(identificador)
        novos_dados_vacina = self.__tela_vacina.pegar_dados_vacina(vacina=vacina)

        if not novos_dados_vacina:
            return

        vacina.identificador = novos_dados_vacina["id"]
        vacina.nome = novos_dados_vacina["nome"]

    def listar_vacinas(self):
        self.verificar_nenhuma_vacina_cadastrada()
        self.__tela_vacina.mostrar_vacinas([vacina for vacina in self.__vacinas])

    def excluir_vacina(self):
        self.verificar_nenhuma_vacina_cadastrada()

        identificador = self.__tela_vacina.selecionar_vacina(
            [vacina.identificador for vacina in self.__vacinas],
            vacinas=self.__vacinas,
        )

        if not identificador:
            return

        vacina = self.buscar_vacina_por_identificador(identificador)

        self.__vacinas.remove(vacina)
        self.__tela_vacina.mostrar_mensagem("Vacina removida com sucesso.")

    def listar_vacina_por_identificador(self):
        self.verificar_nenhuma_vacina_cadastrada()

        identificador = self.__tela_vacina.selecionar_vacina(
            ids=[vacina.identificador for vacina in self.__vacinas],
            vacinas=None,
        )

        if not identificador:
            return

        vacina = self.buscar_vacina_por_identificador(identificador)

        self.__tela_vacina.mostrar_vacina(
            {
                "id": vacina.identificador,
                "nome": vacina.nome,
            }
        )

    def selecionar_vacina(self):
        self.verificar_nenhuma_vacina_cadastrada()
        id_vacina = self.__tela_vacina.selecionar_vacina(
            ids=[vacina.identificador for vacina in self.__vacinas],
            vacinas=self.__vacinas,
        )

        if not id_vacina:
            return

        return self.buscar_vacina_por_identificador(id_vacina)

    def verificar_id_ja_cadastrado(self, nova_vacina_id):
        for vacina in self.__vacinas:
            if vacina.identificador == nova_vacina_id:
                raise IdentificadorJaExistenteException(nova_vacina_id)

    def verificar_nenhuma_vacina_cadastrada(self):
        if len(self.__vacinas) <= 0:
            raise EntidadeNaoEncontradaException("Nenhuma vacina cadastrada.")

    def retornar(self):
        self.__controlador_sistema.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_vacina,
            2: self.alterar_vacina,
            3: self.listar_vacinas,
            4: self.excluir_vacina,
            5: self.listar_vacina_por_identificador,
            0: self.retornar,
        }

        while True:
            try:
                lista_opcoes[self.__tela_vacina.telar_opcoes()]()
            except (EntidadeNaoEncontradaException, IdentificadorJaExistenteException) as e:
                self.__tela_vacina.mostrar_mensagem(e)
            except ValueError:
                self.__tela_vacina.mostrar_mensagem("Somente numeros. Tente novamente.")

    @property
    def tela_vacina(self):
        return self.__tela_vacina
