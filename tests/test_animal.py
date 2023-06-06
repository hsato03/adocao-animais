import io
import sys
import unittest
from unittest.mock import patch
from tests.test_variables import *
from controllers import AnimalController
from exceptions import EntidadeNaoEncontradaException, OpcaoInvalidaException


class AnimalTest(unittest.TestCase):
    def setUp(self):
        self.controlador_animais = AnimalController(None)
        self.cachorro_valido = [
            numero_chip,
            nome,
            tipo_cachorro,
            raca,
            tamanho_cachorro_pequeno,
        ]
        self.gato_valido = [numero_chip, nome, tipo_gato, raca]

    def incluir_cachorro_test(self, dados_cachorro):
        with patch("builtins.input", side_effect=dados_cachorro):
            try:
                self.controlador_animais.incluir_animal()
            except StopIteration:
                self.fail("Ocorreu um erro ao incluir o cachorro! Dados invalidos.")

    def incluir_gato_test(self, dados_gato):
        with patch("builtins.input", side_effect=dados_gato):
            try:
                self.controlador_animais.incluir_animal()
            except StopIteration:
                self.fail("Ocorreu um erro ao incluir o gato! Dados inválidos.")

    def test_incluir_cachorro_pequeno_should_work_when_valid_data(self):
        cachorro = [
            numero_chip,
            nome,
            tipo_cachorro,
            raca,
            tamanho_cachorro_pequeno,
        ]
        self.incluir_gato_test(cachorro)

    def test_incluir_cachorro_medio_should_work_when_valid_data(self):
        cachorro = [
            numero_chip,
            nome,
            tipo_cachorro,
            raca,
            tamanho_cachorro_medio,
        ]
        self.incluir_cachorro_test(cachorro)

    def test_incluir_cachorro_grande_should_work_when_valid_data(self):
        cachorro = [
            numero_chip,
            nome,
            tipo_cachorro,
            raca,
            tamanho_cachorro_grande,
        ]
        self.incluir_cachorro_test(cachorro)

    def test_incluir_cachorro_should_raise_exception_when_tamanho_cachorro_invalido(
        self,
    ):
        cachorro = [
            numero_chip,
            nome,
            tipo_cachorro,
            raca,
            tamanho_cachorro_invalido,
        ]
        with patch("builtins.input", side_effect=cachorro):
            with self.assertRaises(StopIteration):
                self.controlador_animais.incluir_animal()

    def test_incluir_gato_should_work_when_valid_data(self):
        gato = [numero_chip, nome, tipo_gato, raca]
        self.incluir_gato_test(gato)

    def test_incluir_animal_should_raise_exception_when_tipo_animal_invalido(self):
        animal = [numero_chip, nome, tipo_animal_invalido]
        with patch("builtins.input", side_effect=animal):
            with self.assertRaises(StopIteration):
                self.controlador_animais.incluir_animal()

    def test_excluir_cachorro_should_work_when_valid_data(self):
        self.incluir_cachorro_test(self.cachorro_valido)

        dados_exclusao = [tipo_cachorro, numero_chip]
        with patch("builtins.input", side_effect=dados_exclusao):
            try:
                self.controlador_animais.excluir_animal()
            except EntidadeNaoEncontradaException:
                self.fail(
                    "Ocorreu um erro ao excluir cachorro! Entidade nao encontrada."
                )

    def test_excluir_cachorro_should_raise_exception_when_numero_chip_invalido(self):
        self.incluir_cachorro_test(self.cachorro_valido)

        dados_exclusao = [tipo_cachorro, numero_chip_invalido]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_animais.excluir_animal()

    def test_excluir_gato_should_work_when_valid_data(self):
        self.incluir_gato_test(self.gato_valido)

        dados_exclusao = [tipo_gato, numero_chip]
        with patch("builtins.input", side_effect=dados_exclusao):
            try:
                self.controlador_animais.excluir_animal()
            except EntidadeNaoEncontradaException:
                self.fail("Ocorreu um erro ao excluir gato! Entidade nao encontrada.")

    def test_excluir_gato_should_raise_exception_when_numero_chip_invalido(self):
        self.incluir_gato_test(self.gato_valido)

        dados_exclusao = [tipo_gato, numero_chip_invalido]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(EntidadeNaoEncontradaException):
                self.controlador_animais.excluir_animal()

    def test_excluir_animal_should_raise_exception_when_tipo_animal_invalido(self):
        self.incluir_gato_test(self.gato_valido)

        dados_exclusao = [tipo_animal_invalido, numero_chip]
        with patch("builtins.input", side_effect=dados_exclusao):
            with self.assertRaises(OpcaoInvalidaException):
                self.controlador_animais.excluir_animal()

    def test_alterar_cachorro_should_work_when_valid_data(self):
        self.incluir_cachorro_test(self.cachorro_valido)

        dados_alteracao = [
            tipo_cachorro,
            numero_chip,
            numero_chip_atualizado,
            nome_atualizado,
            raca_atualizada,
            tamanho_cachorro_medio,
        ]
        with patch("builtins.input", side_effect=dados_alteracao):
            try:
                self.controlador_animais.alterar_animal()
            except EntidadeNaoEncontradaException:
                self.fail(
                    "Ocorreu um erro ao alterar cachorro! Entidade nao encontrada."
                )

        try:
            cachorro_atualizado = (
                self.controlador_animais.buscar_cachorro_por_numero_chip(
                    numero_chip_atualizado
                )
            )
        except EntidadeNaoEncontradaException:
            self.fail("Cachorro nao alterado.")

        self.assertEqual(dados_alteracao[2], cachorro_atualizado.numero_chip)
        self.assertEqual(dados_alteracao[3], cachorro_atualizado.nome)
        self.assertEqual(dados_alteracao[4], cachorro_atualizado.raca)
        self.assertEqual(dados_alteracao[5], cachorro_atualizado.tamanho.value)

    def test_alterar_cachorro_should_raise_exception_when_tamanho_cachorro_invalido(
        self,
    ):
        self.incluir_cachorro_test(self.cachorro_valido)

        dados_alteracao = [
            tipo_cachorro,
            numero_chip,
            numero_chip_atualizado,
            nome_atualizado,
            raca_atualizada,
            tamanho_cachorro_invalido,
        ]
        with patch("builtins.input", side_effect=dados_alteracao):
            with self.assertRaises(StopIteration):
                self.controlador_animais.alterar_animal()

    def test_alterar_gato_should_work_when_valid_data(self):
        self.incluir_gato_test(self.gato_valido)

        dados_alteracao = [
            tipo_gato,
            numero_chip,
            numero_chip_atualizado,
            nome_atualizado,
            raca_atualizada,
        ]

        with patch("builtins.input", side_effect=dados_alteracao):
            try:
                self.controlador_animais.alterar_animal()
            except EntidadeNaoEncontradaException:
                self.fail(
                    "Ocorreu um erro ao alterar cachorro! Entidade nao encontrada."
                )

        try:
            gato_atualizado = self.controlador_animais.buscar_gato_por_numero_chip(
                numero_chip_atualizado
            )
        except EntidadeNaoEncontradaException:
            self.fail("Gato nao alterado.")

        self.assertEqual(dados_alteracao[2], gato_atualizado.numero_chip)
        self.assertEqual(dados_alteracao[3], gato_atualizado.nome)
        self.assertEqual(dados_alteracao[4], gato_atualizado.raca)

    def test_alterar_animal_should_raise_exception_when_tipo_animal_invalido(self):
        self.incluir_gato_test(self.gato_valido)

        with self.assertRaises(OpcaoInvalidaException):
            sys.stdin = io.StringIO(str(tipo_animal_invalido))
            self.controlador_animais.alterar_animal()
