from typing import List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)



def suffix(filename: str) -> str:
    return Path(filename).suffix.lower().strip()

def descompactar_arquivo(filename,diretorio_destino=None) -> List[str]:
    import zipfile
    import os

    if not diretorio_destino:
        diretorio_destino = os.path.dirname(filename)

    logging.info("Descompactando o arquivo %s no diretório %s...",filename,diretorio_destino)

    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(diretorio_destino)

    directory_destino_path = Path(diretorio_destino)

    paths_arquivos_descompactados = [
        os.path.join(diretorio_destino, entry.name)
        for entry in directory_destino_path.iterdir()
        if entry.is_file()
    ]

    logging.info(f"Os arquivos descompactados são: {paths_arquivos_descompactados}")

    return paths_arquivos_descompactados
