import logging
import ui
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from agente import AgenteAnaliseDadosDataFrame
import streamlit as st

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

def main():

    arquivo_submetido = ui.exibir_file_uloader()

    if arquivo_submetido:

        try: 

            df = ui.carregar_dataframe_arquivo_submetido(arquivo_submetido)

            agente = AgenteAnaliseDadosDataFrame(df,StreamlitChatMessageHistory(key="messages"))

            ui.exibir_historico_mensagens()

            if input := ui.exibir_chat_input():

                ui.exibir_pergunta_usuario(input)

                ui.exibir_resposta_agente(agente,input)


        except ValueError as e:
            
            ui.exibir_mensagem_erro(str(e))

    

if __name__ == "__main__":
    main()
