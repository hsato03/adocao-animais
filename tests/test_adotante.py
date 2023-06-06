import io
import sys
import unittest
from unittest.mock import patch
from datetime import datetime
from tests.test_variables import *
from controllers import AdotanteController, SistemaController
from exceptions import EntidadeNaoEncontradaException, CpfInvalidoException


class AdotanteTest(unittest.TestCase):
    def setUp(self):
        self.controlador_sistema = SistemaController()
        self.controlador_adotantes = AdotanteController(self.controlador_sistema)

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

        self.adotante_data_nascimento_invalida = [
            cpf,
            nome,
            data_invalida,
            tipo_habitacao_casa,
            tamanho_habitacao_pequeno,
            possui_animal,
            logradouro,
            numero,
        ]

        self.adotante_tipo_habitacao_invalido = [
            cpf,
            nome,
            data,
            tipo_habitacao_invalido,
            tamanho_habitacao_pequeno,
            possui_animal,
            logradouro,
            numero,
        ]

        self.adotante_tamanho_habitacao_invalido = [
            cpf,
            nome,
            data,
            tipo_habitacao_casa,
            tamanho_habitacao_invalido,
            possui_animal,
            logradouro,
            numero,
        ]

        self.adotante_possui_animal_invalido = [
            cpf,
            nome,
            data,
            tipo_habitacao_casa,
            tamanho_habitacao_pequeno,
            possui_animal_invalido,
            logradouro,
            numero,
        ]

    def incluir_adotante_test(self, dados_adotante):
        with patch("builtins.input", side_effect=dados_adotante):
            try:
                self.controlador_adotantes.incluir_adotante()
            except StopIteration:
                self.fail("Ocorreu um erro ao incluir uma pessoa")

    # Os testes test_incluir_adotante_should_work_when_correct_data (1,2,3)
    # percorrem todos os valores validos para incluir um adotante
    def test_incluir_adotante_should_work_when_correct_data_1(self):
        adotante = [
            cpf,
            nome,
            data,
            tipo_habitacao_casa,
            tamanho_habitacao_pequeno,
            possui_animal,
            logradouro,
            numero,
        ]
        self.incluir_adotante_test(adotante)

    def test_incluir_adotante_should_work_when_correct_data_2(self):
        adotante = [
            cpf,
            nome,
            data,
            tipo_habitacao_apartamento,
            tamanho_habitacao_medio,
            nao_possui_animal,
            logradouro,
            numero,
        ]
        self.incluir_adotante_test(adotante)

    def test_incluir_adotante_should_work_when_correct_data_3(self):
        adotante = [
            cpf,
            nome,
            data,
            tipo_habitacao_apartamento,
            tamanho_habitacao_grande,
            nao_possui_animal,
            logradouro,
            numero,
        ]
        self.incluir_adotante_test(adotante)

    def test_incluir_adotante_should_throw_exception_when_data_nascimento_invalida(
        self,
    ):
        with patch(
            "builtins.input", side_effect=self.adotante_data_nascimento_invalida
        ):
            with self.assertRaises(TypeError):
                self.controlador_adotantes.incluir_adotante()

    def test_incluir_adotante_should_raise_exception_when_tipo_habitacao_invalido(
        self,
    ):
        with patch("builtins.input", side_effect=self.adotante_tipo_habitacao_invalido):
            with self.assertRaises(StopIteration):
                self.controlador_adotantes.incluir_adotante()

    def test_incluir_adotante_should_raise_exception_when_tamanho_habitacao_invalido(
        self,
    ):
        with patch(
            "builtins.input", side_effect=self.adotante_tamanho_habitacao_invalido
        ):
            with self.assertRaises(StopIteration):
                self.controlador_adotantes.incluir_adotante()

    def test_incluir_adotante_should_raise_exception_when_possui_animal_invalido(
        self,
    ):
        with patch("builtins.input", side_effect=self.adotante_possui_animal_invalido):
            with self.assertRaises(StopIteration):
                self.controlador_adotantes.incluir_adotante()

    def test_excluir_adotante_should_work_when_correct_data(self):
        self.incluir_adotante_test(self.adotante_valido)

        try:
            sys.stdin = io.StringIO(cpf)
            self.controlador_adotantes.excluir_adotante()
        except EntidadeNaoEncontradaException:
            self.fail("Ocorreu um erro ao excluir uma pessoa")

        with self.assertRaises(EntidadeNaoEncontradaException):
            self.controlador_adotantes.buscar_adotante_por_cpf(cpf)

    def test_excluir_adotante_should_raise_exception_when_cpf_invalido(
        self,
    ):
        self.incluir_adotante_test(self.adotante_valido)

        with self.assertRaises(CpfInvalidoException):
            sys.stdin = io.StringIO(cpf_invalido)
            self.controlador_adotantes.excluir_adotante()

    def test_alterar_adotante_should_work_when_correct_data(self):
        self.incluir_adotante_test(self.adotante_valido)

        dados_alteracao = [
            cpf,
            cpf_atualizado,
            nome_atualizado,
            data_atualizada,
            tipo_habitacao_apartamento,
            tamanho_habitacao_grande,
            nao_possui_animal,
            logradouro_atualizado,
            numero_atualizado,
        ]

        with patch("builtins.input", side_effect=dados_alteracao):
            try:
                self.controlador_adotantes.alterar_adotante()
            except EntidadeNaoEncontradaException:
                self.fail(
                    "Ocorreu um erro ao alterar adotante! Entidade nao encontrada."
                )

        try:
            adotante_atualizado = self.controlador_adotantes.buscar_adotante_por_cpf(
                cpf_atualizado
            )
        except EntidadeNaoEncontradaException:
            self.fail("Adotante nao alterado.")

        self.assertEqual(dados_alteracao[1], adotante_atualizado.cpf)
        self.assertEqual(dados_alteracao[2], adotante_atualizado.nome)
        self.assertEqual(
            datetime.strptime(dados_alteracao[3], "%d/%m/%Y").date(),
            adotante_atualizado.data,
        )
        self.assertEqual(dados_alteracao[4], adotante_atualizado.tipo_habitacao.value)
        self.assertEqual(
            dados_alteracao[5], adotante_atualizado.tamanho_habitacao.value
        )
        self.assertEqual(
            True if dados_alteracao[6] == 1 else False,
            adotante_atualizado.possui_animal,
        )
        self.assertEqual(dados_alteracao[7], adotante_atualizado.endereco.logradouro)
        self.assertEqual(dados_alteracao[8], adotante_atualizado.endereco.numero)

    def test_alterar_adotante_should_raise_exception_when_cpf_invalido(
        self,
    ):
        self.incluir_adotante_test(self.adotante_valido)

        with self.assertRaises(CpfInvalidoException):
            sys.stdin = io.StringIO(cpf_invalido)
            self.controlador_adotantes.alterar_adotante()

    def test_alterar_adotante_should_throw_exception_when_data_nascimento_invalida(
        self,
    ):
        self.incluir_adotante_test(self.adotante_valido)

        with patch(
            "builtins.input", side_effect=[cpf] + self.adotante_data_nascimento_invalida
        ):
            with self.assertRaises(TypeError):
                self.controlador_adotantes.alterar_adotante()

    def test_alterar_adotante_should_throw_exception_when_tipo_habitacao_invalido(self):
        self.incluir_adotante_test(self.adotante_valido)

        with patch(
            "builtins.input",
            side_effect=[cpf] + self.adotante_tipo_habitacao_invalido,
        ):
            with self.assertRaises(StopIteration):
                self.controlador_adotantes.alterar_adotante()

    def test_alterar_adotante_should_throw_exception_when_tamanho_habitacao_invalido(
        self,
    ):
        self.incluir_adotante_test(self.adotante_valido)

        with patch(
            "builtins.input",
            side_effect=[cpf] + self.adotante_tamanho_habitacao_invalido,
        ):
            with self.assertRaises(StopIteration):
                self.controlador_adotantes.alterar_adotante()

    def test_alterar_adotante_should_throw_exception_when_possui_animal_invalido(self):
        self.incluir_adotante_test(self.adotante_valido)

        with patch(
            "builtins.input",
            side_effect=[cpf] + self.adotante_possui_animal_invalido,
        ):
            with self.assertRaises(StopIteration):
                self.controlador_adotantes.alterar_adotante()
