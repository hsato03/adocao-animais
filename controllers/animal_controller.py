from views import AnimalView
from model import Cachorro, TamanhoCachorro, Gato, TIPO_CACHORRO, TIPO_GATO
from exceptions import (
    EntidadeNaoEncontradaException,
    OpcaoInvalidaException,
    IdentificadorJaExistenteException,
)


class AnimalController:
    def __init__(self, controlador_sistema):
        self.__gatos = []
        self.__cachorros = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_animal = AnimalView()

    def buscar_gato_por_numero_chip(self, numero_chip: int):
        for gato in self.__gatos:
            if gato.numero_chip == numero_chip:
                return gato
        raise EntidadeNaoEncontradaException("ERRO: Gato nao existente")

    def buscar_cachorro_por_numero_chip(self, numero_chip: int):
        for cachorro in self.__cachorros:
            if cachorro.numero_chip == numero_chip:
                return cachorro
        raise EntidadeNaoEncontradaException("ERRO: Cachorro nao existente")

    def incluir_animal(self):
        dados_animal = self.__tela_animal.pegar_dados_animal()
        self.verificar_numero_chip_ja_existente(dados_animal["numero_chip"])

        if dados_animal["tipo_animal"] == TIPO_CACHORRO:
            cachorro = Cachorro(
                dados_animal["numero_chip"],
                dados_animal["nome"],
                dados_animal["raca"],
                TamanhoCachorro(dados_animal["tamanho_cachorro"]),
            )
            self.__cachorros.append(cachorro)
        else:
            gato = Gato(
                dados_animal["numero_chip"],
                dados_animal["nome"],
                dados_animal["raca"],
            )
            self.__gatos.append(gato)

    def listar_animais(self):
        tipo_animal = self.__tela_animal.telar_opcoes_tipo_animal()

        if tipo_animal == TIPO_CACHORRO:
            self.listar_cachorros()

        else:
            self.listar_gatos()

    def listar_cachorros(self):
        if self.verificar_nenhum_cachorro_cadastrado():
            return

        for i in range(len(self.__cachorros)):
            cachorro = self.__cachorros[i]
            self.__tela_animal.mostrar_mensagem(f"\nCACHORRO #{i + 1:02d}")
            self.__tela_animal.mostrar_animal(
                {
                    "numero_chip": cachorro.numero_chip,
                    "nome": cachorro.nome,
                    "raca": cachorro.raca,
                    "tamanho_cachorro": cachorro.tamanho,
                    "tipo_animal": TIPO_CACHORRO,
                    "historico_vacinacao": cachorro.historico_vacinacao,
                }
            )

    def listar_gatos(self):
        if self.verificar_nenhum_gato_cadastrado():
            return

        for i in range(len(self.__gatos)):
            gato = self.__gatos[i]
            self.__tela_animal.mostrar_mensagem(f"\nGATO #{i + 1:02d}")
            self.__tela_animal.mostrar_animal(
                {
                    "numero_chip": gato.numero_chip,
                    "nome": gato.nome,
                    "raca": gato.raca,
                    "tipo_animal": TIPO_GATO,
                    "historico_vacinacao": gato.historico_vacinacao,
                }
            )

    def alterar_animal(self):
        tipo_animal = self.__tela_animal.telar_opcoes_tipo_animal()
        self.listar_cachorros() if tipo_animal == TIPO_CACHORRO else self.listar_gatos()
        numero_chip = self.__tela_animal.selecionar_animal()

        if tipo_animal == TIPO_CACHORRO:
            if self.verificar_nenhum_cachorro_cadastrado():
                return

            self.alterar_cachorro(numero_chip)
        else:
            if self.verificar_nenhum_gato_cadastrado():
                return

            self.alterar_gato(numero_chip)

    def alterar_cachorro(self, numero_chip: int):
        cachorro = self.buscar_cachorro_por_numero_chip(numero_chip)
        dados_novos_cachorro = self.__tela_animal.pegar_dados_animal_alterar(
            TIPO_CACHORRO
        )
        self.verificar_numero_chip_ja_existente(dados_novos_cachorro["numero_chip"])
        cachorro.numero_chip = dados_novos_cachorro["numero_chip"]
        cachorro.nome = dados_novos_cachorro["nome"]
        cachorro.raca = dados_novos_cachorro["raca"]
        cachorro.tamanho = TamanhoCachorro(dados_novos_cachorro["tamanho_cachorro"])

    def alterar_gato(self, numero_chip: int):
        gato = self.buscar_gato_por_numero_chip(numero_chip)
        dados_novos_gato = self.__tela_animal.pegar_dados_animal_alterar(TIPO_GATO)
        self.verificar_numero_chip_ja_existente(dados_novos_gato["numero_chip"])
        gato.numero_chip = dados_novos_gato["numero_chip"]
        gato.nome = dados_novos_gato["nome"]
        gato.raca = dados_novos_gato["raca"]

    def excluir_animal(self):
        tipo_animal = self.__tela_animal.telar_opcoes_tipo_animal()
        numero_chip = self.__tela_animal.selecionar_animal()

        if tipo_animal == TIPO_CACHORRO:
            if self.verificar_nenhum_cachorro_cadastrado():
                return

            self.listar_cachorros()
            cachorro = self.buscar_cachorro_por_numero_chip(numero_chip)
            self.__cachorros.remove(cachorro)
            self.__tela_animal.mostrar_mensagem("Cachorro removido com sucesso.")
        else:
            if self.verificar_nenhum_gato_cadastrado():
                return True

            self.listar_gatos()
            gato = self.buscar_gato_por_numero_chip(numero_chip)
            self.__gatos.remove(gato)
            self.__tela_animal.mostrar_mensagem("Gato removido com sucesso.")

    def verificar_nenhum_cachorro_cadastrado(self):
        if len(self.__cachorros) <= 0:
            self.__tela_animal.mostrar_mensagem("Nenhum cachorro cadastrado.")
            return True

    def verificar_nenhum_gato_cadastrado(self):
        if len(self.__gatos) <= 0:
            self.__tela_animal.mostrar_mensagem("Nenhum gato cadastrado.")
            return True

    def listar_animal_por_numero_chip(self):
        tipo_animal = self.__tela_animal.telar_opcoes_tipo_animal()
        numero_chip = self.__tela_animal.selecionar_animal()

        if tipo_animal == TIPO_CACHORRO:
            cachorro = self.buscar_cachorro_por_numero_chip(numero_chip)

            dados_animal = {
                "numero_chip": cachorro.numero_chip,
                "nome": cachorro.nome,
                "raca": cachorro.raca,
                "tamanho_cachorro": cachorro.tamanho,
                "tipo_animal": TIPO_CACHORRO,
                "historico_vacinacao": cachorro.historico_vacinacao,
            }
        else:
            gato = self.buscar_gato_por_numero_chip(numero_chip)
            dados_animal = {
                "numero_chip": gato.numero_chip,
                "nome": gato.nome,
                "raca": gato.raca,
                "tipo_animal": TIPO_GATO,
                "historico_vacinacao": gato.historico_vacinacao,
            }

        self.__tela_animal.mostrar_animal(dados_animal)

    def aplicar_vacina_animal(self):
        tipo_animal = self.__tela_animal.telar_opcoes_tipo_animal()

        if tipo_animal == TIPO_CACHORRO:
            self.listar_cachorros()
            numero_chip = self.__tela_animal.selecionar_animal()
            animal = self.buscar_cachorro_por_numero_chip(numero_chip)
        else:
            self.listar_gatos()
            numero_chip = self.__tela_animal.selecionar_animal()
            animal = self.buscar_gato_por_numero_chip(numero_chip)

        self.__controlador_sistema.controlador_vacinas.listar_vacinas()
        identificador = (
            self.__controlador_sistema.controlador_vacinas.tela_vacina.selecionar_vacina()
        )
        vacina = self.__controlador_sistema.controlador_vacinas.buscar_vacina_por_identificador(
            identificador
        )

        data_aplicacao_vacina = self.__tela_animal.pegar_data_aplicacao_vacina()

        animal.historico_vacinacao.add_vacina(vacina, data_aplicacao_vacina)

    def listar_animais_disponiveis_para_adocao(self):
        contador = 1
        for gato in self.__gatos:
            if self.possui_todas_vacinas_para_adocao(gato):
                self.__tela_animal.mostrar_mensagem(f"ANIMAL #{contador:02d}")
                self.__tela_animal.mostrar_animal(
                    {
                        "numero_chip": gato.numero_chip,
                        "nome": gato.nome,
                        "raca": gato.raca,
                        "tipo_animal": TIPO_GATO,
                        "historico_vacinacao": gato.historico_vacinacao,
                    }
                )
                contador += 1

        for cachorro in self.__cachorros:
            if self.possui_todas_vacinas_para_adocao(cachorro):
                self.__tela_animal.mostrar_mensagem(f"ANIMAL #{contador:02d}")
                self.__tela_animal.mostrar_animal(
                    {
                        "numero_chip": cachorro.numero_chip,
                        "nome": cachorro.nome,
                        "raca": cachorro.raca,
                        "tamanho_cachorro": cachorro.tamanho,
                        "tipo_animal": TIPO_CACHORRO,
                        "historico_vacinacao": cachorro.historico_vacinacao,
                    }
                )
                contador += 1
        if contador == 1:
            self.__tela_animal.mostrar_mensagem("Nenhum animal disponivel para adocao.")

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
        for gato in self.__gatos:
            if gato.numero_chip == numero_chip:
                raise IdentificadorJaExistenteException(numero_chip)
        for cachorro in self.__cachorros:
            if cachorro.numero_chip == numero_chip:
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
