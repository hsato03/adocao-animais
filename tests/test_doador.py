import io
import sys
import unittest
from unittest.mock import patch
from datetime import datetime
from tests.test_variables import *
from controllers import DoadorController, SistemaController
from exceptions import EntidadeNaoEncontradaException, CpfInvalidoException


class DoadorTest(unittest.TestCase):
    def setUp(self):
        self.controlador_sistema = SistemaController()
        self.controlador_doadores = DoadorController(self.controlador_sistema)

        self.doador_valido = [
            cpf,
            nome,
            data,
            logradouro,
            numero,
        ]

        self.doador_data_nascimento_invalida = [
            cpf,
            nome,
            data_invalida,
            logradouro,
            numero,
        ]

    def incluir_doador_test(self, dados_doador):
        with patch("builtins.input", side_effect=dados_doador):
            try:
                self.controlador_doadores.incluir_doador()
            except StopIteration:
                self.fail("Ocorreu um erro ao incluir uma pessoa")

    def test_incluir_doador_should_work_when_correct_data_(self):
        self.incluir_doador_test(self.doador_valido)

    def test_incluir_doador_should_throw_exception_when_data_nascimento_invalida(
        self,
    ):
        with patch("builtins.input", side_effect=self.doador_data_nascimento_invalida):
            with self.assertRaises(StopIteration):
                self.controlador_doadores.incluir_doador()

    def test_excluir_doador_should_work_when_correct_data(self):
        self.incluir_doador_test(self.doador_valido)

        try:
            sys.stdin = io.StringIO(cpf)
            self.controlador_doadores.excluir_doador()
        except EntidadeNaoEncontradaException:
            self.fail("Ocorreu um erro ao excluir uma pessoa")

        with self.assertRaises(EntidadeNaoEncontradaException):
            self.controlador_doadores.buscar_doador_por_cpf(cpf)

    def test_excluir_doador_should_raise_exception_when_cpf_invalido(
        self,
    ):
        self.incluir_doador_test(self.doador_valido)

        with self.assertRaises(CpfInvalidoException):
            sys.stdin = io.StringIO(cpf_invalido)
            self.controlador_doadores.excluir_doador()

    def test_alterar_doador_should_work_when_correct_data(self):
        self.incluir_doador_test(self.doador_valido)

        dados_alteracao = [
            cpf,
            cpf_atualizado,
            nome_atualizado,
            data_atualizada,
            logradouro_atualizado,
            numero_atualizado,
        ]

        with patch("builtins.input", side_effect=dados_alteracao):
            try:
                self.controlador_doadores.alterar_doador()
            except EntidadeNaoEncontradaException:
                self.fail("Ocorreu um erro ao alterar doador! Entidade nao encontrada.")

        try:
            doador_atualizado = self.controlador_doadores.buscar_doador_por_cpf(
                cpf_atualizado
            )
        except EntidadeNaoEncontradaException:
            self.fail("Doador nao alterado.")

        self.assertEqual(dados_alteracao[1], doador_atualizado.cpf)
        self.assertEqual(dados_alteracao[2], doador_atualizado.nome)
        self.assertEqual(
            datetime.strptime(dados_alteracao[3], "%d/%m/%Y").date(),
            doador_atualizado.data,
        )
        self.assertEqual(dados_alteracao[4], doador_atualizado.endereco.logradouro)
        self.assertEqual(dados_alteracao[5], doador_atualizado.endereco.numero)

    def test_alterar_doador_should_raise_exception_when_cpf_invalido(
        self,
    ):
        self.incluir_doador_test(self.doador_valido)

        with self.assertRaises(CpfInvalidoException):
            sys.stdin = io.StringIO(cpf_invalido)
            self.controlador_doadores.alterar_doador()

    def test_alterar_doador_should_throw_exception_when_data_nascimento_invalida(self):
        self.incluir_doador_test(self.doador_valido)

        with patch(
            "builtins.input", side_effect=[cpf] + self.doador_data_nascimento_invalida
        ):
            with self.assertRaises(StopIteration):
                self.controlador_doadores.alterar_doador()
