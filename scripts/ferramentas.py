import logging
from typing import List, Optional, Any

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.tools.base import BaseTool

from schemas import *
import os
from pathlib import Path


logger = logging.getLogger(__name__)


class FetchTemporaryFilenameTool(BaseTool):
    name: str = "FetchTemporaryFilename"
    description: str = (
    """
    Retrieves the filename in a temporary directory path. If the directory does not exist, create it before.
    """
    )
    args_schema: type[BaseModel] = FetchTempDirInput
    return_direct: bool = False

    def _run(
        self,
        filename: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        import tempfile
        tmpdir = tempfile.TemporaryDirectory()
        filedest = os.path.join(Path(tmpdir.name),filename)
        logger.info("Dest dir: %s",filedest)
        return filedest
