import unittest
from unittest.mock import patch
from tests.test_variables import *
from model import TIPO_GATO, TIPO_CPF
from exceptions import EntidadeNaoEncontradaException
from controllers import AdocaoController, SistemaController


class AdocaoTest(unittest.TestCase):
    def setUp(self):
        self.controlador_sistema = SistemaController()

        self.controlador_adocoes = AdocaoController(self.controlador_sistema)

        self.adocao_valida = [TIPO_GATO, cpf, numero_chip, data, termo_assinado]

        self.adocao_atualizada = [
            cpf_atualizado,
            numero_chip_atualizado,
            data,
            termo_assinado,
        ]

        self.adocao_adotante_invalido = [
            TIPO_GATO,
            cpf_invalido,
            numero_chip,
            data,
            termo_assinado,
        ]

        self.adocao_animal_invalido = [
            TIPO_GATO,
            cpf,
            numero_chip_invalido,
            data,
            termo_assinado,
        ]

        self.adocao_termo_assinado_invalido = [
            TIPO_GATO,
            cpf,
            numero_chip,
            data,
            termo_assinado_invalido,
        ]

        self.adotante_valido = [
            cpf,
            nome,
            data,
            tipo_habitacao_casa,
            tamanho_habitacao_pequeno,
            possui_animal,
            logradouro,
            numero,
        ]

        self.adotante_atualizado = [
            cpf_atualizado,
            nome,
            data,
            tipo_habitacao_casa,
            tamanho_habitacao_pequeno,
            possui_animal,
            logradouro,
            numero,
        ]

        self.adotante_invalido = [
            cpf_invalido,
            nome,
            data,
            tipo_habitacao_casa,
            tamanho_habitacao_pequeno,
            possui_animal,
            logradouro,
            numero,
        ]

        self.animal_valido = [numero_chip, nome, tipo_gato, raca]

        self.animal_invalido = [numero_chip_invalido, nome, tipo_gato, raca]

        self.animal_atualizado = [numero_chip_atualizado, nome, tipo_gato, raca]

        self.incluir_adotante_animal_test(self.adotante_valido, self.animal_valido)
        self.incluir_adotante_animal_test(
            self.adotante_atualizado, self.animal_atualizado
        )
        self.incluir_vacinas_necessarias_test()
        self.aplicar_vacinas_necessarias_test(numero_chip)
        self.aplicar_vacinas_necessarias_test(numero_chip_atualizado)

    def incluir_adotante_animal_test(self, dados_adotante, dados_animal):
        with patch("builtins.input", side_effect=dados_adotante):
            try:
                self.controlador_sistema.controlador_adotantes.incluir_adotante()
            except StopIteration:
                self.fail("Ocorreu um erro ao incluir Adotante")

        with patch("builtins.input", side_effect=dados_animal):
            try:
                self.controlador_sistema.controlador_animais.incluir_animal()
            except StopIteration:
                self.fail("Ocorreu um erro ao incluir Animal")

    def incluir_adocao_test(self, dados_adocao):
        with patch("builtins.input", side_effect=dados_adocao):
            try:
                self.controlador_adocoes.incluir_adocao()
            except StopIteration:
                self.fail("Ocorreu um erro ao incluir Adocao")

    def incluir_vacinas_necessarias_test(self):
        leptospirose = [1, "leptospirose"]
        hepatite = [2, "hepatite infecciosa"]
        raiva = [3, "raiva"]

        try:
            with patch("builtins.input", side_effect=leptospirose):
                self.controlador_sistema.controlador_vacinas.incluir_vacina()
            with patch("builtins.input", side_effect=hepatite):
                self.controlador_sistema.controlador_vacinas.incluir_vacina()
            with patch("builtins.input", side_effect=raiva):
                self.controlador_sistema.controlador_vacinas.incluir_vacina()
        except StopIteration:
            self.fail("Ocorreu um erro ao incluir vacinas")

    def aplicar_vacinas_necessarias_test(self, n_chip):
        leptospirose = [TIPO_GATO, n_chip, 1, data]
        hepatite = [TIPO_GATO, n_chip, 2, data]
        raiva = [TIPO_GATO, n_chip, 3, data]

        try:
            with patch("builtins.input", side_effect=leptospirose):
                self.controlador_sistema.controlador_animais.aplicar_vacina_animal()
            with patch("builtins.input", side_effect=hepatite):
                self.controlador_sistema.controlador_animais.aplicar_vacina_animal()
            with patch("builtins.input", side_effect=raiva):
                self.controlador_sistema.controlador_animais.aplicar_vacina_animal()
        except StopIteration:
            self.fail("Ocorreu um erro ao incluir vacinas")

    def test_incluir_adocao_should_work_when_valid_data_1(self):
        self.incluir_adocao_test(self.adocao_valida)

    def test_incluir_adocao_should_work_when_valid_data_2(self):
        dados_adocao = [
            TIPO_GATO,
            cpf,
            numero_chip,
            data,
            termo_nao_assinado,
        ]
        self.incluir_adocao_test(dados_adocao)

    def test_incluir_adocao_should_raise_exception_when_cpf_invalido(self):
        with patch("builtins.input", side_effect=self.adocao_adotante_invalido):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_adocoes.incluir_adocao()

    def test_incluir_adocao_should_raise_exception_when_numero_chip_invalido(self):
        with patch("builtins.input", side_effect=self.adocao_animal_invalido):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_adocoes.incluir_adocao()

    def test_incluir_adocao_should_raise_exception_when_assinar_termo_invalido(self):
        with patch("builtins.input", side_effect=self.adocao_termo_assinado_invalido):
            with self.assertRaises(StopIteration):
                self.controlador_adocoes.incluir_adocao()

    def test_excluir_adocao_should_work_when_valid_data(self):
        self.incluir_adocao_test(self.adocao_valida)
        dados_exclusao = [TIPO_CPF, cpf]
        with patch("builtins.input", side_effect=dados_exclusao):
            try:
                self.controlador_adocoes.excluir_adocao()
            except EntidadeNaoEncontradaException:
                self.fail("Ocorreu um erro excluir Adocao: entidade nao encontrada")

    def test_excluir_adocao_should_raise_exception_when_cpf_invalido(self):
        self.incluir_adocao_test(self.adocao_valida)
        dados_exclusao = [TIPO_CPF, cpf_invalido]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_adocoes.excluir_adocao()

    def test_excluir_adocao_should_raise_exception_when_numero_chip_invalido(self):
        self.incluir_adocao_test(self.adocao_valida)
        dados_exclusao = [TIPO_CPF, cpf_invalido]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_adocoes.excluir_adocao()

    def test_excluir_adocao_should_raise_exception_when_tipo_id_invalido(self):
        self.incluir_adocao_test(self.adocao_valida)
        dados_exclusao = [100, cpf]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(StopIteration):
                self.controlador_adocoes.excluir_adocao()

    def test_alterar_adocao_should_work_when_valid_data(self):
        self.incluir_adocao_test(self.adocao_valida)
        with patch(
            "builtins.input", side_effect=[TIPO_CPF, cpf, data_atualizada, termo_nao_assinado]
        ):
            try:
                self.controlador_adocoes.alterar_adocao()
            except EntidadeNaoEncontradaException:
                self.fail("Ocorreu um erro ao alterar Adocao: entidade nao encontrada")

        try:
            adoacao_atualizada = (
                self.controlador_adocoes.buscar_adocao_por_identificador(
                    cpf, TIPO_CPF
                )
            )
        except EntidadeNaoEncontradaException:
            self.fail("Adocao nao alterada.")

        self.assertNotEqual(data_atualizada, adoacao_atualizada.data)
        self.assertNotEqual(termo_assinado, adoacao_atualizada.termo_assinado)

    def test_alterar_adocao_should_raise_exception_when_termo_assinado_invalido(self):
        self.incluir_adocao_test(self.adocao_valida)
        with patch(
            "builtins.input",
            side_effect=[TIPO_CPF, cpf, data, termo_assinado_invalido],
        ):
            with self.assertRaises(StopIteration):
                self.controlador_adocoes.alterar_adocao()
