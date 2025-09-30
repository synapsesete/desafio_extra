import os
import logging

from typing import Type

from typing import Any

from langchain_core.runnables.base import Runnable
from langchain_core.chat_history import BaseChatMessageHistory,InMemoryChatMessageHistory
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd

import ferramentas
import schemas

logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

class AgenteAnaliseDadosDataFrame:

    def __init__(self,df: Type[pd.DataFrame], chat_memory: Type[BaseChatMessageHistory] = InMemoryChatMessageHistory()) -> None:
        """
        Inicializar o Agente de análise de dados especializado em análise de dataframes Pandas passando para ele o texto de prompt do que deve ser feito.
        """

        self.__agent_executor = create_pandas_dataframe_agent(llm=self._load_llm(),
                                                              df = df,
                                                              verbose=True,
                                                              allow_dangerous_code=True,
                                                              prefix=self._load_prefix_prompt(),
                                                              suffix=self._load_suffix_prompt(),
                                                              extra_tools=[ferramentas.FetchTemporaryFilenameTool()],
                                                              include_df_in_prompt=None,
                                                              handle_parsing_errors=True
                                                              )
                                                              
        self.__memory: Type[BaseChatMessageHistory] = chat_memory


    def _load_llm(self) -> Runnable:
        """
        Carrega e retorna a LLM do Agente.
        """
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_ollama import ChatOllama

        if os.environ.get("GOOGLE_API_KEY"):
            llm = ChatGoogleGenerativeAI(model=os.environ["LLM_MODEL"], temperature=0)
        else:
            llm = ChatOllama(
                temperature=0,
                model=os.environ["OLLAMA_LLM_MODEL"],
                base_url=os.environ["OLLAMA_URL"],
            )

        return llm


    def _load_prefix_prompt(self) -> str:
        """
        Customiza o prompt do Agente informando para quando usar o matplotlib, salvar as imagens em diretório temporário.
        """
        from langchain_experimental.agents.agent_toolkits.pandas.prompt import PREFIX
        return PREFIX +"""
                **Important**: 
                  Whenever before generating any kind of image with matplotlib, please retrieve the temporary directory path with appropriate filename in PNG format that the image will be saved.
                  If you generate more than 1 (one) graphic, please merge them in the same file.
                """
    
    
    def _load_suffix_prompt(self) -> str:
        """
        Customiza o prompt do Agente informando com o o formato de saída desejado.
        """
        from langchain_experimental.agents.agent_toolkits.pandas.prompt import SUFFIX_WITH_DF
        return """
                Conversation history:
                {history}
                **Only** Final Answer JSON schema: 
                {{
                  "answer": "string", // the final answer to the original input question in markdown,
                  "image": "string"  // the optional path of generated image if generated.
                }}
               """  + SUFFIX_WITH_DF


    def invoke(self, question: str) -> Any:
        """
        Invoca a pergunta ao agente, fazendo o parsing da string JSON retornada em seguida.
        """
        from stringutils import get_string_between_chars
        output: str = self.__agent_executor.invoke({"input": question, "history": self.__memory.messages })['output']
        if output:
            json_content = get_string_between_chars(output,'{','}')
            if json_content:
                answer: str = "{"+json_content+"}"
                return schemas.RespostaFinal.model_validate_json(answer)    
            else:
                return schemas.RespostaFinal(answer=output)
        
    