import unittest
from unittest.mock import patch
from tests.test_variables import *
from model import TIPO_GATO, TIPO_CPF
from exceptions import EntidadeNaoEncontradaException
from controllers import DoacaoController, SistemaController


class DoacaoTest(unittest.TestCase):
    def setUp(self):
        self.controlador_sistema = SistemaController()

        self.controlador_doacoes = DoacaoController(self.controlador_sistema)

        self.doacao_valida = [TIPO_GATO, cpf, numero_chip, data, motivo]

        self.doacao_atualizada = [cpf_atualizado, numero_chip_atualizado, data, motivo]

        self.doacao_doador_invalido = [
            TIPO_GATO,
            cpf_invalido,
            numero_chip,
            data,
            motivo,
        ]

        self.doacao_animal_invalido = [
            TIPO_GATO,
            cpf,
            numero_chip_invalido,
            data,
            motivo,
        ]

        self.doador_valido = [
            cpf,
            nome,
            data,
            logradouro,
            numero,
        ]

        self.doador_atualizado = [
            cpf_atualizado,
            nome,
            data,
            logradouro,
            numero,
        ]

        self.doador_invalido = [
            cpf_invalido,
            nome,
            data,
            logradouro,
            numero,
        ]

        self.animal_valido = [numero_chip, nome, tipo_gato, raca]

        self.animal_invalido = [numero_chip_invalido, nome, tipo_gato, raca]

        self.animal_atualizado = [numero_chip_atualizado, nome, tipo_gato, raca]

        self.incluir_doador_animal_test(self.doador_valido, self.animal_valido)
        self.incluir_doador_animal_test(self.doador_atualizado, self.animal_atualizado)

    def incluir_doador_animal_test(self, dados_doador, dados_animal):
        with patch("builtins.input", side_effect=dados_doador):
            try:
                self.controlador_sistema.controlador_doadores.incluir_doador()
            except EntidadeNaoEncontradaException:
                self.fail("Adotante nao encontrado")

        with patch("builtins.input", side_effect=dados_animal):
            try:
                self.controlador_sistema.controlador_animais.incluir_animal()
            except EntidadeNaoEncontradaException:
                self.fail("Animal nao encontrado")

    def incluir_doacao_test(self, dados_doacao):
        with patch("builtins.input", side_effect=dados_doacao):
            try:
                self.controlador_doacoes.incluir_doacao()
            except StopIteration:
                self.fail("Ocorreu um erro ao incluir Doacao")

    def test_incluir_doacao_should_work_when_valid_data(self):
        self.incluir_doacao_test(self.doacao_valida)

    def test_incluir_doacao_should_raise_exception_when_cpf_invalido(self):
        with patch("builtins.input", side_effect=self.doacao_doador_invalido):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_doacoes.incluir_doacao()

    def test_incluir_doacao_should_raise_exception_when_numero_chip_invalido(self):
        with patch("builtins.input", side_effect=self.doacao_animal_invalido):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_doacoes.incluir_doacao()

    def test_excluir_doacao_should_work_when_valid_data(self):
        self.incluir_doacao_test(self.doacao_valida)
        dados_exclusao = [TIPO_CPF, cpf]
        with patch("builtins.input", side_effect=dados_exclusao):
            try:
                self.controlador_doacoes.excluir_doacao()
            except EntidadeNaoEncontradaException:
                self.fail("Ocorreu um erro excluir Doacao: entidade nao encontrada")

    def test_excluir_doacao_should_raise_exception_when_cpf_invalido(self):
        self.incluir_doacao_test(self.doacao_valida)
        dados_exclusao = [TIPO_CPF, cpf_invalido]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_doacoes.excluir_doacao()

    def test_excluir_doacao_should_raise_exception_when_numero_chip_invalido(self):
        self.incluir_doacao_test(self.doacao_valida)
        dados_exclusao = [TIPO_CPF, cpf_invalido]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_doacoes.excluir_doacao()

    def test_excluir_doacao_should_raise_exception_when_tipo_id_invalido(self):
        self.incluir_doacao_test(self.doacao_valida)
        dados_exclusao = [100, cpf]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(StopIteration):
                self.controlador_doacoes.excluir_doacao()

    def test_alterar_doacao_should_work_when_valid_data(self):
        self.incluir_doacao_test(self.doacao_valida)
        with patch(
            "builtins.input", side_effect=[TIPO_CPF, cpf, data_atualizada, motivo_atualizado]
        ):
            try:
                self.controlador_doacoes.alterar_doacao()
            except EntidadeNaoEncontradaException:
                self.fail("Ocorreu um erro ao alterar Doacao: entidade nao encontrada")

        try:
            adoacao_atualizada = (
                self.controlador_doacoes.buscar_doacao_por_identificador(
                    cpf, TIPO_CPF
                )
            )
        except EntidadeNaoEncontradaException:
            self.fail("Doacao nao alterada.")

        self.assertNotEqual(data, adoacao_atualizada.data)
        self.assertNotEqual(motivo, adoacao_atualizada.motivo)

    def test_alterar_doacao_should_raise_exception_when_tipo_id_invalido(self):
        self.incluir_doacao_test(self.doacao_valida)
        with patch("builtins.input", side_effect=[100, cpf] + self.doacao_atualizada):
            with self.assertRaises(StopIteration):
                self.controlador_doacoes.alterar_doacao()
