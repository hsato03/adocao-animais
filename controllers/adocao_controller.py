from datetime import date

from exceptions import (
    EntidadeNaoEncontradaException,
    AdocaoRegraVioladaException,
)
from model import (
    Adocao,
    Cachorro,
    TamanhoCachorro,
    TamanhoHabitacao,
    TipoHabitacao,
)
from views import AdocaoView
from persistence import AdocaoDAO


class AdocaoController:
    def __init__(self, controlador_sistema):
        self.__adocao_dao = AdocaoDAO("datasources/adocoes.pkl")
        self.__tela_adocao = AdocaoView()
        self.__controlador_sistema = controlador_sistema

    def buscar_adocao_por_numero_chip(self, numero_chip: int):
        adocao = self.__adocao_dao.find_by_id(numero_chip)
        if adocao:
            return adocao

        raise EntidadeNaoEncontradaException("ERRO: Adocao nao existente.")

    def incluir_adocao(self):
        animal = self.__controlador_sistema.controlador_animais.selecionar_animal_adocao()
        if not animal:
            return

        adotante = self.__controlador_sistema.controlador_adotantes.selecionar_adotante()
        if not adotante:
            return

        dados_adocao = self.__tela_adocao.pegar_dados_adocao(adocao=None)
        if not dados_adocao:
            return

        self.verificar_regras_adocao(animal, adotante)

        adocao = Adocao(
            adotante,
            animal,
            dados_adocao["data"],
            True if dados_adocao["termo_assinado"] == 1 else False,
        )
        adotante.possui_animal = True
        self.__adocao_dao.insert(adocao)

    def alterar_adocao(self):
        self.verificar_nenhuma_adocao_cadastrada()

        numero_chip = self.__tela_adocao.selecionar_adocao(adocoes=self.__adocao_dao.find_all())

        if not numero_chip:
            return

        adocao = self.buscar_adocao_por_numero_chip(numero_chip)
        novos_dados_adocao = self.__tela_adocao.pegar_dados_adocao(adocao=adocao)

        if not novos_dados_adocao:
            return

        adocao.data = novos_dados_adocao["data"]
        adocao.termo_assinado = (
            True if novos_dados_adocao["termo_assinado"] == 1 else False
        )
        self.__adocao_dao.update(numero_chip, adocao)
        self.__tela_adocao.mostrar_mensagem("Adocao alterada com sucesso.")

    def listar_adocoes(self):
        self.verificar_nenhuma_adocao_cadastrada()

        self.__tela_adocao.mostrar_adocoes(adocoes=self.__adocao_dao.find_all())

    def excluir_adocao(self):
        self.verificar_nenhuma_adocao_cadastrada()

        numero_chip = self.__tela_adocao.selecionar_adocao(adocoes=self.__adocao_dao.find_all())

        if not numero_chip:
            return

        removed = self.__adocao_dao.remove(numero_chip)
        if removed:
            self.__tela_adocao.mostrar_mensagem("Adocao removida com sucesso.")
        else:
            self.__tela_adocao.mostrar_mensagem("Adocao não removida.")

    def listar_animais_disponiveis_para_adocao(self):
        self.__controlador_sistema.controlador_animais.listar_animais_disponiveis_para_adocao()

    def listar_adocoes_por_periodo(self):
        self.verificar_nenhuma_adocao_cadastrada()

        dados_periodo = self.__tela_adocao.pegar_dados_periodo()
        if not dados_periodo:
            return

        data_inicio = dados_periodo["data_inicio"]
        data_fim = dados_periodo["data_fim"]
        adocoes_periodo = []

        for adocao in self.__adocao_dao.find_all():
            if data_inicio <= adocao.data <= data_fim:
                adocoes_periodo.append(adocao)

        if len(adocoes_periodo) <= 0:
            raise EntidadeNaoEncontradaException("Nenhuma adocao encontrada neste periodo")

        self.__tela_adocao.mostrar_adocoes(adocoes_periodo)

    def verificar_nenhuma_adocao_cadastrada(self):
        if len(self.__adocao_dao.find_all()) <= 0:
            raise EntidadeNaoEncontradaException("Nenhuma adocao cadastrada.")

    def atingiu_maioridade(self, data_nascimento):
        data_atual = date.today()
        idade = data_atual.year - data_nascimento.year

        if idade > 18:
            return True

        if idade == 18:
            if (data_atual.month, data_atual.day) >= (
                    data_nascimento.month,
                    data_nascimento.day,
            ):
                return True

        return False

    def verificar_regras_adocao(self, animal, adotante):
        if not self.atingiu_maioridade(adotante.data_nascimento):
            raise AdocaoRegraVioladaException(
                "É preciso ter mais de 18 anos para adotar um animal."
            )

        if not self.__controlador_sistema.controlador_animais.possui_todas_vacinas_para_adocao(
                animal
        ):
            raise AdocaoRegraVioladaException(
                "Animal deve ter as vacinas: raiva, hepatite infecciosa e leptospirose para ser adotado"
            )

        if isinstance(animal, Cachorro):
            if (
                    animal.tamanho == TamanhoCachorro.GRANDE
                    and adotante.tipo_habitacao == TipoHabitacao.APARTAMENTO
                    and adotante.tamanho_habitacao == TamanhoHabitacao.PEQUENO
            ):
                raise AdocaoRegraVioladaException(
                    "Adotantes que moram em apartamento pequeno nao podem adotar caes de porte grande"
                )

        if self.verificar_animal_ja_adotado(animal):
            raise AdocaoRegraVioladaException(f"Animal {animal.nome} [{animal.numero_chip}] ja foi adotado")

    def verificar_animal_ja_adotado(self, animal):
        for adocao in self.__adocao_dao.find_all():
            if adocao.animal.numero_chip == animal.numero_chip:
                return True
        return False


    def retornar(self):
        self.__controlador_sistema.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_adocao,
            2: self.alterar_adocao,
            3: self.listar_adocoes,
            4: self.excluir_adocao,
            5: self.listar_animais_disponiveis_para_adocao,
            6: self.listar_adocoes_por_periodo,
            0: self.retornar,
        }

        while True:
            try:
                lista_opcoes[self.__tela_adocao.telar_opcoes()]()
            except (
                    EntidadeNaoEncontradaException,
                    AdocaoRegraVioladaException,
            ) as e:
                self.__tela_adocao.mostrar_mensagem(e)
