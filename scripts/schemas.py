from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class FetchTempDirInput(BaseModel):
    filename: str = Field(description="O arquivo destino que o plot será salvo.")
    

class RespostaFinal(BaseModel):
    answer: str
    image: Optional[str] = None
