import json
import os
from datetime import datetime

ARQUIVO_TAREFAS = "C:/Users/morei/Downloads/IA/assistente virtual/tarefas.json"

def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON"""
    if os.path.exists(ARQUIVO_TAREFAS):
        try:
            with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except:
            return []
    return []

def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON"""
    try:
        with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as arquivo:
            json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar tarefas: {str(e)}")
        return False

def adicionar_tarefa(descricao):
    """Adiciona uma nova tarefa"""
    tarefas = carregar_tarefas()
    
    nova_tarefa = {
        "id": len(tarefas) + 1,
        "descricao": descricao,
        "concluida": False,
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    tarefas.append(nova_tarefa)
    
    if salvar_tarefas(tarefas):
        print(f"✅ Tarefa adicionada: '{descricao}'")
        return True
    return False

def remover_tarefa(numero):
    """Remove uma tarefa pelo número"""
    tarefas = carregar_tarefas()
    
    if 1 <= numero <= len(tarefas):
        tarefa_removida = tarefas.pop(numero - 1)
        
        for i, tarefa in enumerate(tarefas):
            tarefa["id"] = i + 1
        
        if salvar_tarefas(tarefas):
            print(f"✅ Tarefa removida: '{tarefa_removida['descricao']}'")
            return True
    else:
        print(f"❌ Tarefa número {numero} não existe")
    return False

def listar_tarefas():
    """Lista todas as tarefas"""
    tarefas = carregar_tarefas()
    
    if not tarefas:
        print("📝 Você não tem tarefas cadastradas")
        return
    
    print("\n" + "="*50)
    print("📋 LISTA DE TAREFAS")
    print("="*50)
    
    pendentes = [t for t in tarefas if not t["concluida"]]
    concluidas = [t for t in tarefas if t["concluida"]]
    
    if pendentes:
        print("\n⏳ PENDENTES:")
        for tarefa in pendentes:
            print(f"  {tarefa['id']}. [ ] {tarefa['descricao']}")
    
    if concluidas:
        print("\n✅ CONCLUÍDAS:")
        for tarefa in concluidas:
            print(f"  {tarefa['id']}. [✓] {tarefa['descricao']}")
    
    print("="*50 + "\n")

def marcar_concluida(numero):
    """Marca uma tarefa como concluída"""
    tarefas = carregar_tarefas()
    
    if 1 <= numero <= len(tarefas):
        tarefas[numero - 1]["concluida"] = True
        tarefas[numero - 1]["data_conclusao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        if salvar_tarefas(tarefas):
            print(f"✅ Tarefa '{tarefas[numero - 1]['descricao']}' marcada como concluída!")
            return True
    else:
        print(f"❌ Tarefa número {numero} não existe")
    return False

def iniciar_tarefas():
    """Inicializa o sistema de tarefas"""
    print("✅ Sistema de tarefas inicializado")
    return True

def atuar_sobre_tarefas(acao, parametro):
    """
    Executa ações sobre as tarefas
    
    Args:
        acao: 'adicionar', 'remover', 'listar', 'concluir'
        parametro: descrição da tarefa ou número
    """
    try:
        if acao == "adicionar":
            adicionar_tarefa(parametro)
        
        elif acao == "remover":
            try:
                numero = int(parametro)
                remover_tarefa(numero)
            except ValueError:
                print("❌ Para remover, informe o número da tarefa")
        
        elif acao == "listar":
            listar_tarefas()
        
        elif acao == "concluir":
            try:
                numero = int(parametro)
                marcar_concluida(numero)
            except ValueError:
                print("❌ Para concluir, informe o número da tarefa")
        
        else:
            print(f"⚠️  Ação '{acao}' não reconhecida para tarefas")
    
    except Exception as e:
        print(f"❌ Erro ao executar ação: {str(e)}")