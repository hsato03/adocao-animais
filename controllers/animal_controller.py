from views import AnimalView
from model import Cachorro, TamanhoCachorro, Gato, TIPO_CACHORRO, TIPO_GATO
from exceptions import (
    EntidadeNaoEncontradaException,
    OpcaoInvalidaException,
    IdentificadorJaExistenteException,
)


class AnimalController:
    def __init__(self, controlador_sistema):
        self.__animais = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_animal = AnimalView()

    @property
    def gatos(self):
        return list(filter(lambda animal: not hasattr(animal, "tamanho"), self.__animais))

    @property
    def cachorros(self):
        return list(filter(lambda animal: hasattr(animal, "tamanho"), self.__animais))

    def buscar_animal_por_numero_chip(self, numero_chip: int):
        for animal in self.__animais:
            if animal.numero_chip == numero_chip:
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
            self.__animais.append(cachorro)
        else:
            gato = Gato(
                dados_animal["numero_chip"],
                dados_animal["nome"],
                dados_animal["raca"],
            )
            self.__animais.append(gato)

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
            self.__tela_animal.mostrar_animais(animais=self.__animais)

    def alterar_animal(self):
        self.verificar_nenhum_animal_cadastrado()

        numero_chip = self.__tela_animal.selecionar_animal(
            nchips=[animal.numero_chip for animal in self.__animais],
            animais=self.__animais,
        )

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

        self.__tela_animal.mostrar_mensagem("Animal alterado com sucesso.")

    def excluir_animal(self):
        self.verificar_nenhum_animal_cadastrado()

        numero_chip = self.__tela_animal.selecionar_animal(
            nchips=[animal.numero_chip for animal in self.__animais],
            animais=self.__animais,
        )

        if not numero_chip:
            return

        animal = self.buscar_animal_por_numero_chip(numero_chip)
        self.__animais.remove(animal)
        self.__tela_animal.mostrar_mensagem("Animal removido com sucesso.")

    def verificar_nenhum_cachorro_cadastrado(self):
        if len(self.cachorros) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum cachorro cadastrado.")

    def verificar_nenhum_gato_cadastrado(self):
        if len(self.gatos) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum gato cadastrado.")

    def verificar_nenhum_animal_cadastrado(self):
        if len(self.__animais) <= 0:
            raise EntidadeNaoEncontradaException("Nenhum animal cadastrado.")

    def listar_animal_por_numero_chip(self):
        self.verificar_nenhum_animal_cadastrado()
        numero_chip = self.__tela_animal.selecionar_animal(
            nchips=[animal.numero_chip for animal in self.__animais],
            animais=None,
        )

        if not numero_chip:
            return

        animal = self.buscar_animal_por_numero_chip(numero_chip)
        self.__tela_animal.mostrar_animal(animal)

    def aplicar_vacina_animal(self):
        self.verificar_nenhum_animal_cadastrado()

        numero_chip = self.__tela_animal.selecionar_animal(
            nchips=[animal.numero_chip for animal in self.__animais],
            animais=self.__animais
        )

        if not numero_chip:
            return

        animal = self.buscar_animal_por_numero_chip(numero_chip)

        vacina = self.__controlador_sistema.controlador_vacinas.selecionar_vacina()

        if not vacina:
            return

        data_aplicacao_vacina = self.__tela_animal.pegar_data_aplicacao_vacina()

        animal.historico_vacinacao.add_vacina(vacina, data_aplicacao_vacina)

    def listar_animais_disponiveis_para_adocao(self):
        animais_disponiveis_adocao = []

        for animal in self.__animais:
            if self.possui_todas_vacinas_para_adocao(animal):
                animais_disponiveis_adocao.append(animal)

            self.__tela_animal.mostrar_animais(animais_disponiveis_adocao)

    def possui_todas_vacinas_para_adocao(self, animal):
        leptospirose = False
        hepatite = False
        raiva = False
        for vacina in animal.historico_vacinacao.vacinas:
            if vacina["vacina"].nome == "raiva":
                raiva = True
            elif vacina["vacina"].nome == "leptospirose":
                leptospirose = True
            elif vacina["vacina"].nome == "hepatite infecciosa":
                hepatite = True
        if leptospirose and hepatite and raiva:
            return True
        return False

    def verificar_numero_chip_ja_existente(self, numero_chip: int):
        for animal in self.__animais:
            if animal.numero_chip == numero_chip:
                raise IdentificadorJaExistenteException(numero_chip)

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
                OpcaoInvalidaException,
                EntidadeNaoEncontradaException,
                IdentificadorJaExistenteException,
            ) as e:
                self.__tela_animal.mostrar_mensagem(e)
