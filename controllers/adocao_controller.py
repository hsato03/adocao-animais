from views import AdocaoView
from model import (
    Adocao,
    Cachorro,
    TIPO_CACHORRO,
    TIPO_CPF,
    TamanhoCachorro,
    TamanhoHabitacao,
    TipoHabitacao,
)
from exceptions import (
    EntidadeNaoEncontradaException,
    OpcaoInvalidaException,
    AdocaoRegraVioladaException,
)
from datetime import date


class AdocaoController:
    def __init__(self, controlador_sistema):
        self.__adocoes = []
        self.__tela_adocao = AdocaoView()
        self.__controlador_sistema = controlador_sistema

    def buscar_adocao_por_identificador(self, identificador, tipo_id: int):
        for adocao in self.__adocoes:
            if tipo_id == TIPO_CPF:
                if adocao.adotante.cpf == identificador:
                    return adocao
            else:
                if adocao.animal.numero_chip == int(identificador):
                    return adocao
        raise EntidadeNaoEncontradaException("ERRO: Adocao nao existente.")

    def incluir_adocao(self):
        tipo_animal = self.__tela_adocao.telar_opcoes_tipo_animal()
        dados_adocao = self.__tela_adocao.pegar_dados_adocao(criacao=True)

        cpf_adotante = dados_adocao["cpf_adotante"]
        numero_chip = dados_adocao["numero_chip"]

        if tipo_animal == TIPO_CACHORRO:
            animal = self.__controlador_sistema.controlador_animais.buscar_cachorro_por_numero_chip(
                numero_chip
            )
        else:
            animal = self.__controlador_sistema.controlador_animais.buscar_gato_por_numero_chip(
                numero_chip
            )

        adotante = (
            self.__controlador_sistema.controlador_adotantes.buscar_adotante_por_cpf(
                cpf_adotante
            )
        )

        self.verificar_regras_adocao(animal, adotante, verifica_animal=True)

        adocao = Adocao(
            adotante,
            animal,
            dados_adocao["data"],
            True if dados_adocao["termo_assinado"] == 1 else False,
        )
        adotante.possui_animal = True
        self.__adocoes.append(adocao)

    def alterar_adocao(self):
        if self.verificar_nenhuma_adocao_cadastrada():
            return

        self.listar_adocoes()

        tipo_id = self.pegar_tipo_id()
        identificador = self.__tela_adocao.selecionar_adocao(tipo_id)
        adocao = self.buscar_adocao_por_identificador(identificador, tipo_id)
        novos_dados_adocao = self.__tela_adocao.pegar_dados_adocao(criacao=False)

        adocao.data = novos_dados_adocao["data"]
        adocao.termo_assinado = True if novos_dados_adocao["termo_assinado"] == 1 else False

    def listar_adocoes(self):
        if self.verificar_nenhuma_adocao_cadastrada():
            return

        for i in range(len(self.__adocoes)):
            self.__tela_adocao.mostrar_mensagem(f"\nADOCAO #{i + 1:02d}")
            adocao = self.__adocoes[i]
            self.__tela_adocao.mostrar_adocao(
                {
                    "cpf_adotante": adocao.adotante.cpf,
                    "numero_chip": adocao.animal.numero_chip,
                    "data": adocao.data,
                    "termo_assinado": adocao.termo_assinado,
                }
            )

    def excluir_adocao(self):
        if self.verificar_nenhuma_adocao_cadastrada():
            return

        self.listar_adocoes()

        tipo_id = self.pegar_tipo_id()

        identificador = self.__tela_adocao.selecionar_adocao(tipo_id)
        adocao = self.buscar_adocao_por_identificador(identificador, tipo_id)
        self.__adocoes.remove(adocao)
        self.__tela_adocao.mostrar_mensagem("Adocao removida com sucesso.")

    def listar_adocao_por_identificador(self):
        if self.verificar_nenhuma_adocao_cadastrada():
            return

        while True:
            try:
                tipo_id = self.__tela_adocao.telar_opcoes_identificador()
                break
            except OpcaoInvalidaException as e:
                self.__tela_adocao.mostrar_mensagem(e)
            except ValueError:
                self.__tela_adocao.mostrar_mensagem("Somente numeros. Tente novamente.")

        identificador = self.__tela_adocao.selecionar_adocao(tipo_id)

        adocao = self.buscar_adocao_por_identificador(identificador, tipo_id)

        self.__tela_adocao.mostrar_adocao(
            {
                "cpf_adotante": adocao.adotante.cpf,
                "numero_chip": adocao.animal.numero_chip,
                "data": adocao.data,
                "termo_assinado": True if adocao.termo_assinado == 1 else False,
            }
        )

    def listar_animais_disponiveis_para_adocao(self):
        self.__controlador_sistema.controlador_animais.listar_animais_disponiveis_para_adocao()

    def listar_adocoes_por_periodo(self):
        contador = 1
        dados_periodo = self.__tela_adocao.pegar_dados_periodo()
        data_inicio = dados_periodo["data_inicio"]
        data_fim = dados_periodo["data_fim"]

        for adocao in self.__adocoes:
            if data_inicio <= adocao.data <= data_fim:
                self.__tela_adocao.mostrar_mensagem(f"ADOCAO #{contador:02d}")
                self.__tela_adocao.mostrar_adocao(
                    {
                        "cpf_adotante": adocao.adotante.cpf,
                        "numero_chip": adocao.animal.numero_chip,
                        "data": adocao.data,
                        "termo_assinado": adocao.termo_assinado,
                    }
                )
                contador += 1

        if contador == 1:
            self.__tela_adocao.mostrar_mensagem(
                "Nenhuma adocao encontrada neste periodo"
            )

    def verificar_nenhuma_adocao_cadastrada(self):
        if len(self.__adocoes) <= 0:
            self.__tela_adocao.mostrar_mensagem("Nenhuma adocao cadastrada.")
            return True

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

    def verificar_regras_adocao(self, animal, adotante, verifica_animal):
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

        if not verifica_animal:
            return

        for adocao in self.__adocoes:
            if adocao.animal.numero_chip == animal.numero_chip:
                raise AdocaoRegraVioladaException(f"Animal {animal.nome} [{animal.numero_chip}] ja foi adotado")

    def pegar_tipo_id(self):
        while True:
            try:
                tipo_id = self.__tela_adocao.telar_opcoes_identificador()
                return tipo_id
            except OpcaoInvalidaException as e:
                self.__tela_adocao.mostrar_mensagem(e)
            except ValueError:
                self.__tela_adocao.mostrar_mensagem("Somente numeros. Tente novamente.")

    def retornar(self):
        self.__controlador_sistema.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_adocao,
            2: self.alterar_adocao,
            3: self.listar_adocoes,
            4: self.excluir_adocao,
            5: self.listar_adocao_por_identificador,
            6: self.listar_animais_disponiveis_para_adocao,
            7: self.listar_adocoes_por_periodo,
            0: self.retornar,
        }

        while True:
            try:
                lista_opcoes[self.__tela_adocao.telar_opcoes()]()
            except (OpcaoInvalidaException, EntidadeNaoEncontradaException, AdocaoRegraVioladaException) as e:
                self.__tela_adocao.mostrar_mensagem(e)
            except ValueError:
                self.__tela_adocao.mostrar_mensagem("Somente numeros. Tente novamente")
