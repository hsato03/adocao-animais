from views import AnimalView
from persistence import GenericDAO
from model import Animal, Cachorro, TamanhoCachorro, Gato, TIPO_CACHORRO, TIPO_GATO
from exceptions import (
    EntidadeNaoEncontradaException,
    IdentificadorJaExistenteException,
)


class AnimalController:
    def __init__(self, controlador_sistema):
        self.__animal_dao = GenericDAO(Animal)
        self.__controlador_sistema = controlador_sistema
        self.__tela_animal = AnimalView()

    @property
    def gatos(self):
        return list(filter(lambda animal: not hasattr(animal, "tamanho"), self.__animal_dao.find_all()))

    @property
    def cachorros(self):
        return list(filter(lambda animal: hasattr(animal, "tamanho"), self.__animal_dao.find_all()))

    def buscar_animal_por_numero_chip(self, numero_chip: int):
        animal = self.__animal_dao.find_by_id(numero_chip)
        if animal:
            return animal

        raise EntidadeNaoEncontradaException("ERRO: Animal nao existente")

    def incluir_animal(self):
        tipo_animal = self.__tela_animal.telar_opcoes_tipo_animal(listagem=False)
        dados_animal = self.__tela_animal.pegar_dados_animal(animal=None, tipo_animal=tipo_animal)

        if not dados_animal:
            return

        self.verificar_numero_chip_ja_existente(dados_animal["numero_chip"])

        if tipo_animal == TIPO_CACHORRO:
            cachorro = Cachorro(
                dados_animal["numero_chip"],
                dados_animal["nome"],
                dados_animal["raca"],
                TamanhoCachorro(dados_animal["tamanho_cachorro"]),
            )
            self.__animal_dao.insert(cachorro)
        else:
            gato = Gato(
                dados_animal["numero_chip"],
                dados_animal["nome"],
                dados_animal["raca"],
            )
            self.__animal_dao.insert(gato)

    def listar_animais(self):
        self.verificar_nenhum_animal_cadastrado()
        tipo_animal = self.__tela_animal.telar_opcoes_tipo_animal(listagem=True)

        if tipo_animal == TIPO_CACHORRO:
            self.verificar_nenhum_cachorro_cadastrado()
            self.__tela_animal.mostrar_animais(animais=self.cachorros)
        elif tipo_animal == TIPO_GATO:
            self.verificar_nenhum_gato_cadastrado()
            self.__tela_animal.mostrar_animais(animais=self.gatos)
        else:
            self.verificar_nenhum_animal_cadastrado()
            self.__tela_animal.mostrar_animais(animais=self.__animal_dao.find_all())

    def alterar_animal(self):
        self.verificar_nenhum_animal_cadastrado()

        numero_chip = self.__tela_animal.selecionar_animal(animais=self.__animal_dao.find_all(), mostrar_opcoes=True)

        if not numero_chip:
            return

        animal = self.buscar_animal_por_numero_chip(numero_chip)
        tipo_animal = TIPO_CACHORRO if isinstance(animal, Cachorro) else TIPO_GATO
        novos_dados_animal = self.__tela_animal.pegar_dados_animal(animal, tipo_animal)

        if not novos_dados_animal:
            return

        if animal.numero_chip != novos_dados_animal["numero_chip"]:
            self.verificar_numero_chip_ja_existente(novos_dados_animal["numero_chip"])

        animal.numero_chip = novos_dados_animal["numero_chip"]
        animal.nome = novos_dados_animal["nome"]
        animal.raca = novos_dados_animal["raca"]

        if tipo_animal == TIPO_CACHORRO:
            animal.tamanho = TamanhoCachorro(novos_dados_animal["tamanho_cachorro"])

        self.__animal_dao.update(numero_chip, animal)
        self.__tela_animal.mostrar_mensagem("Animal alterado com sucesso.")

    def excluir_animal(self):
        self.verificar_nenhum_animal_cadastrado()

        numero_chip = self.__tela_animal.selecionar_animal(animais=self.__animal_dao.find_all(), mostrar_opcoes=True)

        if not numero_chip:
            return

        removed = self.__animal_dao.remove(numero_chip)
        if removed:
            self.__tela_animal.mostrar_mensagem("Animal removido com sucesso.")
        else:
            self.__tela_animal.mostrar_mensagem("Animal não removido.")

    def listar_animal_por_numero_chip(self):
        self.verificar_nenhum_animal_cadastrado()
        numero_chip = self.__tela_animal.selecionar_animal(animais=self.__animal_dao.find_all(), mostrar_opcoes=False)

        if not numero_chip:
            return

        animal = self.buscar_animal_por_numero_chip(numero_chip)
        self.__tela_animal.mostrar_animal(animal)

    def aplicar_vacina_animal(self):
        self.verificar_nenhum_animal_cadastrado()

        numero_chip = self.__tela_animal.selecionar_animal(animais=self.__animal_dao.find_all(), mostrar_opcoes=True)

        if not numero_chip:
            return

        animal = self.buscar_animal_por_numero_chip(numero_chip)

        vacina = self.__controlador_sistema.controlador_vacinas.selecionar_vacina()

        if not vacina:
            return

        data_aplicacao_vacina = self.__tela_animal.pegar_data_aplicacao_vacina()

        animal.historico_vacinacao.add_vacina(vacina, data_aplicacao_vacina)
        self.__animal_dao.update(numero_chip, animal)

    def selecionar_animal(self):
        self.verificar_nenhum_animal_cadastrado()
        numero_chip = self.__tela_animal.selecionar_animal(animais=self.__animal_dao.find_all(), mostrar_opcoes=True)

        if not numero_chip:
            return

        return self.buscar_animal_por_numero_chip(numero_chip)

    def selecionar_animal_adocao(self):
        self.verificar_nenhum_animal_cadastrado()
        numero_chip = self.__tela_animal.selecionar_animal(animais=self.animais_disponiveis_para_adocao(),
                                                           mostrar_opcoes=True)

        if not numero_chip:
            return

        return self.buscar_animal_por_numero_chip(numero_chip)

    def listar_animais_disponiveis_para_adocao(self):
        self.verificar_nenhum_animal_cadastrado()
        animais_disponiveis_adocao = self.animais_disponiveis_para_adocao()
        if animais_disponiveis_adocao:
            self.__tela_animal.mostrar_animais(animais=animais_disponiveis_adocao)

    def animais_disponiveis_para_adocao(self):
        animais_disponiveis_adocao = []

        for animal in self.__animal_dao.find_all():
            if self.possui_todas_vacinas_para_adocao(animal) and self.nao_adotado(animal):
                animais_disponiveis_adocao.append(animal)

        if len(animais_disponiveis_adocao) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum animal disponivel para adocao.")

        return animais_disponiveis_adocao

    def possui_todas_vacinas_para_adocao(self, animal):
        vacinas_aplicadas = [vacina["vacina"].nome for vacina in animal.historico_vacinacao.vacinas]
        if vacinas_aplicadas in ("hepatite infecciosa", "leptospirose", "raiva"):
            return True
        return False

    def nao_adotado(self, animal):
        return not self.__controlador_sistema.controlador_adocoes.verificar_animal_ja_adotado(animal)

    def verificar_numero_chip_ja_existente(self, numero_chip: int):
        if self.__animal_dao.find_by_id(numero_chip):
            raise IdentificadorJaExistenteException(numero_chip)

    def verificar_nenhum_cachorro_cadastrado(self):
        if len(self.cachorros) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum cachorro cadastrado.")

    def verificar_nenhum_gato_cadastrado(self):
        if len(self.gatos) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum gato cadastrado.")

    def verificar_nenhum_animal_cadastrado(self):
        if len(self.__animal_dao.find_all()) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum animal cadastrado.")

    def retornar(self):
        self.__controlador_sistema.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_animal,
            2: self.alterar_animal,
            3: self.listar_animais,
            4: self.excluir_animal,
            5: self.listar_animal_por_numero_chip,
            6: self.aplicar_vacina_animal,
            0: self.retornar,
        }

        while True:
            try:
                lista_opcoes[self.__tela_animal.telar_opcoes()]()
            except (
                EntidadeNaoEncontradaException,
                IdentificadorJaExistenteException,
            ) as e:
                self.__tela_animal.mostrar_mensagem(e)
