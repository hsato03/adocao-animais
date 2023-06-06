from views import VacinaView
from model import Vacina
from exceptions import EntidadeNaoEncontradaException, OpcaoInvalidaException


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
        dados_vacina = self.__tela_vacina.pegar_dados_vacina()

        vacina = Vacina(
            dados_vacina["identificador"],
            dados_vacina["nome"],
        )
        self.__vacinas.append(vacina)

    def alterar_vacina(self):
        if len(self.__vacinas) <= 0:
            self.__tela_vacina.mostrar_mensagem("Nenhuma vacina cadastrada.")
            return

        self.listar_vacinas()
        identificador = self.__tela_vacina.selecionar_vacina()
        vacina = self.buscar_vacina_por_identificador(identificador)
        novos_dados_vacina = self.__tela_vacina.pegar_dados_vacina()

        vacina.identificador = novos_dados_vacina["identificador"]
        vacina.nome = novos_dados_vacina["nome"]

        self.listar_vacinas()

    def listar_vacinas(self):
        if len(self.__vacinas) <= 0:
            raise EntidadeNaoEncontradaException("Nenhuma vacina cadastrada.")

        for i in range(len(self.__vacinas)):
            vacina = self.__vacinas[i]
            self.__tela_vacina.mostrar_mensagem(f"\nVACINA #{i + 1:02d}")
            self.__tela_vacina.mostrar_vacina(
                {
                    "identificador": vacina.identificador,
                    "nome": vacina.nome,
                }
            )

    def excluir_vacina(self):
        if len(self.__vacinas) <= 0:
            self.__tela_vacina.mostrar_mensagem("Nenhuma vacina cadastrada.")
            return

        self.listar_vacinas()
        identificador = self.__tela_vacina.selecionar_vacina()
        vacina = self.buscar_vacina_por_identificador(identificador)

        self.__vacinas.remove(vacina)
        self.__tela_vacina.mostrar_mensagem("Vacina removida com sucesso.")

    def listar_vacina_por_identificador(self):
        if len(self.__vacinas) <= 0:
            self.__tela_vacina.mostrar_mensagem("Nenhuma vacina cadastrada.")
            return

        identificador = self.__tela_vacina.selecionar_vacina()
        vacina = self.buscar_vacina_por_identificador(identificador)

        self.__tela_vacina.mostrar_vacina(
            {
                "identificador": vacina.identificador,
                "nome": vacina.nome,
            }
        )

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
            except (OpcaoInvalidaException, EntidadeNaoEncontradaException) as e:
                self.__tela_vacina.mostrar_mensagem(e)
            except ValueError:
                self.__tela_vacina.mostrar_mensagem("Somente numeros. Tente novamente.")

    @property
    def tela_vacina(self):
        return self.__tela_vacina
