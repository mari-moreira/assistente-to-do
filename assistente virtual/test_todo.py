import unittest
from unittest.mock import patch
import tarefas 

class TesteTarefasCompleto(unittest.TestCase):

    def setUp(self):
     
        self.mock_tarefas = []

    @patch('tarefas.carregar_tarefas')
    @patch('tarefas.salvar_tarefas')
    def test_adicionar_tarefa(self, mock_salvar, mock_carregar):
        mock_carregar.return_value = self.mock_tarefas
        mock_salvar.return_value = True

        resultado = tarefas.adicionar_tarefa("Comprar leite")
        self.assertTrue(resultado)
        self.assertEqual(len(self.mock_tarefas), 1)
        self.assertEqual(self.mock_tarefas[0]["descricao"], "Comprar leite")
        self.assertFalse(self.mock_tarefas[0]["concluida"])

    @patch('tarefas.carregar_tarefas')
    @patch('tarefas.salvar_tarefas')
    def test_remover_tarefa_existente(self, mock_salvar, mock_carregar):
        self.mock_tarefas = [{"id": 1, "descricao": "Estudar Python", "concluida": False}]
        mock_carregar.return_value = self.mock_tarefas
        mock_salvar.return_value = True

        resultado = tarefas.remover_tarefa(1)
        self.assertTrue(resultado)
        self.assertEqual(len(self.mock_tarefas), 0)

    @patch('tarefas.carregar_tarefas')
    @patch('tarefas.salvar_tarefas')
    def test_remover_tarefa_inexistente(self, mock_salvar, mock_carregar):
        self.mock_tarefas = []
        mock_carregar.return_value = self.mock_tarefas
        mock_salvar.return_value = True

        resultado = tarefas.remover_tarefa(1)
        self.assertFalse(resultado)

    @patch('tarefas.carregar_tarefas')
    def test_listar_tarefas(self, mock_carregar):
        self.mock_tarefas = [
            {"id": 1, "descricao": "Lavar roupa", "concluida": False},
            {"id": 2, "descricao": "Comprar leite", "concluida": True}
        ]
        mock_carregar.return_value = self.mock_tarefas

        tarefas_listadas = tarefas.carregar_tarefas()
        self.assertEqual(len(tarefas_listadas), 2)
        self.assertEqual(tarefas_listadas[0]["descricao"], "Lavar roupa")
        self.assertEqual(tarefas_listadas[1]["concluida"], True)

    @patch('tarefas.carregar_tarefas')
    @patch('tarefas.salvar_tarefas')
    def test_marcar_concluida(self, mock_salvar, mock_carregar):
        self.mock_tarefas = [{"id": 1, "descricao": "Estudar Python", "concluida": False}]
        mock_carregar.return_value = self.mock_tarefas
        mock_salvar.return_value = True

        resultado = tarefas.marcar_concluida(1)
        self.assertTrue(resultado)
        self.assertTrue(self.mock_tarefas[0]["concluida"])
        self.assertIn("data_conclusao", self.mock_tarefas[0])

    @patch('tarefas.carregar_tarefas')
    @patch('tarefas.salvar_tarefas')
    def test_atuar_sobre_tarefas_adicionar(self, mock_salvar, mock_carregar):
        mock_carregar.return_value = self.mock_tarefas
        mock_salvar.return_value = True

        tarefas.atuar_sobre_tarefas("adicionar", "Aprender Python")
        self.assertEqual(len(self.mock_tarefas), 1)
        self.assertEqual(self.mock_tarefas[0]["descricao"], "Aprender Python")

    @patch('tarefas.carregar_tarefas')
    @patch('tarefas.salvar_tarefas')
    def test_atuar_sobre_tarefas_remover(self, mock_salvar, mock_carregar):
        self.mock_tarefas = [{"id": 1, "descricao": "Testar função", "concluida": False}]
        mock_carregar.return_value = self.mock_tarefas
        mock_salvar.return_value = True

        tarefas.atuar_sobre_tarefas("remover", "1")
        self.assertEqual(len(self.mock_tarefas), 0)

    @patch('tarefas.carregar_tarefas')
    @patch('tarefas.salvar_tarefas')
    def test_atuar_sobre_tarefas_concluir(self, mock_salvar, mock_carregar):
        self.mock_tarefas = [{"id": 1, "descricao": "Testar função", "concluida": False}]
        mock_carregar.return_value = self.mock_tarefas
        mock_salvar.return_value = True

        tarefas.atuar_sobre_tarefas("concluir", "1")
        self.assertTrue(self.mock_tarefas[0]["concluida"])

    def test_atuar_sobre_tarefas_acao_desconhecida(self):
        
        tarefas.atuar_sobre_tarefas("nao_existe", "parametro")

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
