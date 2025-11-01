import soundfile as sf
import torch
import whisper
import numpy as np

modelo_whisper = None

def inicializar_whisper(tamanho="base"):
  
    global modelo_whisper
    print(f"🔄 Carregando modelo Whisper ({tamanho})...")
    modelo_whisper = whisper.load_model(tamanho)
    print("✅ Modelo Whisper carregado!")
    return modelo_whisper


def carregar_fala(caminho_audio):

    try:
       
        audio, _ = sf.read(caminho_audio, dtype='float32')
        print(f"✅ Áudio carregado: {len(audio)} amostras")
        return caminho_audio, True
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho_audio}")
        return None, False
    except Exception as e:
        print(f"❌ Erro ao carregar áudio: {str(e)}")
        return None, False


def transcrever_fala_whisper(caminho_audio):
 
    global modelo_whisper
    
    try:
        
        if modelo_whisper is None:
            inicializar_whisper("base")
        
        resultado = modelo_whisper.transcribe(
            caminho_audio,
            language="pt", 
            fp16=False  
        )
        
        transcricao = resultado["text"].strip()
        
        print(f"📝 Transcrição: {transcricao}")
        
        return transcricao.lower()
        
    except Exception as e:
        print(f"❌ Erro ao transcrever: {str(e)}")
        import traceback
        traceback.print_exc()
        return ""


def transcrever_fala(dispositivo, audio, modelo, processador):
 
    return transcrever_fala_whisper(audio)