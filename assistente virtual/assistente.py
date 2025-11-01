from nltk import word_tokenize, corpus
import secrets
import pyaudio
import wave
import json
import os
from tarefas import *        
from transcritor import *    

LINGUAGEM = "portuguese"
FORMATO = pyaudio.paInt16
CANAIS = 1
AMOSTRAS = 1024
TEMPO_GRAVACAO = 5
TAXA_AMOSTRAGEM = 44100

CAMINHO_AUDIO_FALAS = "C:/Users/morei/Downloads/IA/assistente virtual/temp"
CONFIGURACOES = "C:/Users/morei/Downloads/IA/assistente virtual/config.json"


def iniciar():
    gravador = pyaudio.PyAudio()
    palavras_de_parada = set(corpus.stopwords.words(LINGUAGEM))

    inicializar_whisper("base")

    with open(CONFIGURACOES, "r", encoding="utf-8") as arquivo_config:
        configuracoes = json.load(arquivo_config)
        acoes_permitidas = configuracoes["acoes"]

    return gravador, palavras_de_parada, acoes_permitidas


def capturar_fala(gravador):
    stream = gravador.open(
        format=FORMATO,
        channels=CANAIS,
        rate=TAXA_AMOSTRAGEM,
        input=True,
        frames_per_buffer=AMOSTRAS
    )
    print("🎙️  Fale a tarefa...")
    fala = [stream.read(AMOSTRAS) for _ in range(int(TAXA_AMOSTRAGEM / AMOSTRAS * TEMPO_GRAVACAO))]
    stream.stop_stream()
    stream.close()
    return fala

def gravar_fala(gravador, fala):
    arquivo = f"{CAMINHO_AUDIO_FALAS}/{secrets.token_hex(32).lower()}.wav"
    try:
        wav = wave.open(arquivo, "wb")
        wav.setnchannels(CANAIS)
        wav.setsampwidth(gravador.get_sample_size(FORMATO))
        wav.setframerate(TAXA_AMOSTRAGEM)
        wav.writeframes(b"".join(fala))
        wav.close()
        return True, arquivo
    except Exception as e:
        print(f"❌ Erro gravando fala: {e}")
        return False, None



def processar_comando(transcricao, palavras_de_parada):
    tokens = word_tokenize(transcricao)
    return [t for t in tokens if t not in palavras_de_parada]

def validar_comando(comando, transcricao_completa, acoes_permitidas):
    if len(comando) < 1:
        return False, None, None

    primeiro = comando[0].lower()
    acao, parametro = None, None
    valido = False

  
    for acao_info in acoes_permitidas:
        if primeiro == acao_info["nome"] or primeiro in acao_info.get("variantes", []):
            acao = acao_info["nome"]
            
            if acao == "adicionar":
                partes = transcricao_completa.lower().split("tarefa", 1)
                if len(partes) > 1:
                    parametro = partes[1].strip()
                    valido = True
            elif acao in ["remover", "concluir"]:
                numeros = [t for t in comando if t.isdigit()]
                if numeros:
                    parametro = numeros[0]
                    valido = True
            elif acao == "listar":
                parametro = ""
                valido = True
            break

    return valido, acao, parametro


def ativar_to_do_list():
    gravador, palavras_de_parada, acoes_permitidas = iniciar()

    while True:
        fala = capturar_fala(gravador)
        gravado, arquivo = gravar_fala(gravador, fala)

        if gravado:
            caminho_audio, sucesso = carregar_fala(arquivo)
            if sucesso:
                transcricao = transcrever_fala_whisper(caminho_audio)
                if os.path.exists(arquivo):
                    os.remove(arquivo)

                comando = processar_comando(transcricao, palavras_de_parada)
                valido, acao, parametro = validar_comando(comando, transcricao, acoes_permitidas)

                if valido:
                    print(f"✅ Executando '{acao}' com '{parametro}'")
                    atuar_sobre_tarefas(acao, parametro)
                else:
                    print("⚠️  Comando inválido")
            else:
                print("❌ Não foi possível carregar o áudio")
        else:
            print("❌ Erro ao gravar a fala")
            
            
            

if __name__ == "__main__":
    print("✅ Sistema de to-do list com reconhecimento de voz iniciado")
    ativar_to_do_list()
