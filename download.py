import os
import time

# Caminho da pasta de downloads
#download_folder = "/caminho/para/sua/pasta"

def retorna_arquivo_mais_recente(path_downloads):
    """Retorna o arquivo mais recente da pasta especificada."""
    arquivos = [os.path.join(path_downloads, f) for f in os.listdir(path_downloads)]
    arquivos = [f for f in arquivos if os.path.isfile(f)]  # Apenas arquivos
    return max(arquivos, key=os.path.getctime) if arquivos else None

# Aguarda o download ser concluído
def espera_pelo_download(path_downloads, timeout=60):
    """Espera um arquivo aparecer na pasta de downloads."""
    tempo_maximo_download = time.time() + timeout
    while time.time() < tempo_maximo_download:
        ultimo_arquivo = retorna_arquivo_mais_recente(path_downloads)
        if ultimo_arquivo and not ultimo_arquivo.endswith(".crdownload"):  # Verifica se o download foi concluído
            return ultimo_arquivo
        time.sleep(1)
    raise TimeoutError("O arquivo não foi baixado dentro do tempo limite.")


