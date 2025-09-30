from typing import Any, Type
import streamlit as st
import logging
import fileutils
from langchain_core.runnables import Runnable
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
from schemas import RespostaFinal

logger = logging.getLogger(__name__)


def exibir_file_uloader():
    """
    Exibe o widget para subir o arquivo para análise. Pode ser zipado contanto que possua um arquivo em formato CSV.
    """
    return st.file_uploader("Submeta seu arquivo aqui", type=["csv", "zip"])


def carregar_dataframe_arquivo_submetido(arquivo) -> Type[pd.DataFrame]:
    """
    A partir de um caminho de arquivo CSV, retorna o dataframe carregado.
    """
    if arquivo is not None and "filepath" not in st.session_state:
        from tempfile import NamedTemporaryFile
        suffix = fileutils.suffix(arquivo.name)
        with NamedTemporaryFile(suffix=suffix) as temp:
            temp.write(arquivo.getvalue())
            if suffix == ".zip":
               arquivos_csvs_descompactados = [filenamecsv for filenamecsv in fileutils.descompactar_arquivo(temp.name) if fileutils.suffix(filenamecsv)==".csv"]
               assert len(arquivos_csvs_descompactados) == 1
               arquivo_csv = arquivos_csvs_descompactados[0]
            else:
               arquivo_csv = temp.name
            df = pd.read_csv(arquivo_csv)
            __exibir_mensagem_chat("assistant","O dataframe foi carregado com sucesso. Seguem as primeiras linhas...")
            st.dataframe(df.head())
            return df

def exibir_historico_mensagens():
    """
    Exibe o histórico de mensagens no chat entre o assistente e o usuário.
    """
    if "messages" not in st.session_state:
        apagar_historico_mensagens()
    for message in st.session_state.messages:
        __exibir_mensagem_chat(message["role"],message["content"])

def apagar_historico_mensagens():
    st.session_state.messages = []


def exibir_chat_input() -> Any:
    prompt = st.chat_input("Pergunte-me algo.")
    return prompt


def exibir_pergunta_usuario(pergunta: str) -> None:
    __exibir_mensagem_chat("user",pergunta)
    __adicionar_mensagem_chat("user",pergunta)


def exibir_resposta_agente(agente: Runnable, prompt: str) -> None:
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response: RespostaFinal = agente.invoke(prompt)
            if response:
                st.write(response.answer)
                __adicionar_mensagem_chat("assistant",response.answer)
                if response.image:
                    try:
                        st.image(response.image.strip())
                    except FileNotFoundError as fnfe:
                        st.write(fnfe)

def __exibir_mensagem_chat(role:str,msg:str) -> None:
    with st.chat_message(role):
        st.markdown(msg)

def __adicionar_mensagem_chat(role:str,msg:str) -> None:
    if "messages" not in st.session_state:
        apagar_historico_mensagens()
    st.session_state.messages.append({"role": role, "content": msg})
