from exceptions import OpcaoInvalidaException
from model import TIPO_CACHORRO
from datetime import datetime


class AnimalView:
    def telar_opcoes(self):
        print("\n---------------------------------")
        print("|            ANIMAIS            |")
        print("---------------------------------")
        print("[1] -> Incluir Animal")
        print("[2] -> Alterar Animal")
        print("[3] -> Listar Animais")
        print("[4] -> Excluir Animal")
        print("[5] -> Buscar Animal por N° chip")
        print("[6] -> Aplicar vacina Animal")
        print("[0] -> Retornar")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(0, 7):
            raise OpcaoInvalidaException()

        return opcao

    def telar_opcoes_tipo_animal(self):
        print("TIPO ANIMAL:")
        print("\t[1] -> Cachorro")
        print("\t[2] -> Gato")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 3):
            raise OpcaoInvalidaException()

        return opcao

    def telar_opcoes_tamanho_cachorro(self):
        print("TAMANHO CACHORRO:")
        print("\t[1] - Pequeno")
        print("\t[2] - Medio")
        print("\t[3] - Grande")

        opcao = int(input("Escolha a opcao: "))
        if opcao not in range(1, 4):
            raise OpcaoInvalidaException()

        return opcao

    def pegar_dados_animal(self):
        print("\n-------- DADOS ANIMAL ----------")
        numero_chip = self.pegar_numero_chip()
        nome = input("Nome: ")

        dados_animal = {
            "numero_chip": numero_chip,
            "nome": nome,
        }

        while True:
            try:
                tipo_animal = self.telar_opcoes_tipo_animal()
                dados_animal["tipo_animal"] = tipo_animal
                break
            except OpcaoInvalidaException as e:
                print(e)
            except ValueError:
                print("Somente numeros. Tente novamente.")

        raca = input("Raca: ")
        dados_animal["raca"] = raca

        if tipo_animal == TIPO_CACHORRO:
            while True:
                try:
                    tamanho_cachorro = self.telar_opcoes_tamanho_cachorro()
                    dados_animal["tamanho_cachorro"] = tamanho_cachorro
                    break
                except OpcaoInvalidaException as e:
                    print(e)
                except ValueError:
                    print("Somente numeros. Tente novamente.")

        return dados_animal

    def pegar_dados_animal_alterar(self, tipo_animal: int):
        print("\n-------- DADOS ANIMAL ----------")
        numero_chip = self.pegar_numero_chip()
        nome = input("Nome: ")

        dados_animal = {
            "numero_chip": numero_chip,
            "nome": nome,
        }

        raca = input("Raca: ")
        dados_animal["raca"] = raca

        if tipo_animal == TIPO_CACHORRO:
            while True:
                try:
                    tamanho_cachorro = self.telar_opcoes_tamanho_cachorro()
                    dados_animal["tamanho_cachorro"] = tamanho_cachorro
                    break
                except OpcaoInvalidaException as e:
                    print(e)
                except ValueError:
                    print("Somente numeros. Tente novamente.")

        return dados_animal

    def pegar_data_aplicacao_vacina(self):
        while True:
            try:
                data_aplicacao = input("Data de aplicacao da vacina (dd/mm/yyyy): ")
                data_aplicacao_convertida = datetime.strptime(
                    data_aplicacao, "%d/%m/%Y"
                ).date()
                return data_aplicacao_convertida
            except ValueError:
                print("ERRO: Data em formato invalido! Tente novamente.")

    def pegar_numero_chip(self):
        while True:
            try:
                numero_chip = int(input("N° chip: "))
                return numero_chip
            except ValueError:
                print("Somente numeros. Tente novamente")

    def mostrar_animal(self, dados_animal: dict):
        print(f"\t- N° CHIP: {dados_animal['numero_chip']}")
        print(f"\t- NOME: {dados_animal['nome']}")
        print(f"\t- RACA: {dados_animal['raca']}")

        if dados_animal["tipo_animal"] == TIPO_CACHORRO:
            print(f"\t- TAMANHO CACHORRO: {dados_animal['tamanho_cachorro'].name}")

        historico_vacinacao = dados_animal["historico_vacinacao"]
        if len(historico_vacinacao.vacinas) > 0:
            print("\t- VACINA(S):")
            for vacina in historico_vacinacao.vacinas:
                print(
                    f"\t\t+ {vacina['vacina'].nome} ({vacina['data_aplicacao'].strftime('%d/%m/%Y')})"
                )
        else:
            print("\tNenhuma vacina aplicada")

    def selecionar_animal(self):
        try:
            numero_chip = int(input("N° chip do animal que deseja selecionar: "))
            return numero_chip
        except ValueError:
            print("Somente numeros. Tente novamente")

    def mostrar_mensagem(self, msg: str):
        print(msg)
