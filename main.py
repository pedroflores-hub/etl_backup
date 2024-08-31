import os
from typing import List
import boto3
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da AWS a partir do .env
AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION: str = os.getenv('AWS_REGION')
BUCKET_NAME: str = os.getenv('BUCKET_NAME')

# Configura o cliente S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def listar_arquivos(pasta):
    
    arquivos = []
    for nome_arquivo in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, nome_arquivo)
        if os.path.isfile(caminho_completo):
            arquivos.append(caminho_completo)
    return arquivos

def upload_arquivos_para_s3(arquivos):
    
    for arquivo in arquivos:
        nome_arquivo: str = os.path.basename(arquivo)
        s3_client.upload_file(arquivo, BUCKET_NAME, nome_arquivo)
        print(f'{nome_arquivo} foi enviado para o S3.')

def deletar_arquivos_locais(arquivos):
    
    for arquivo in arquivos:
        os.remove(arquivo)
        print(f'{arquivo} foi deletado do local.')

def executar_backup(pasta):
    
    arquivos: List[str] = listar_arquivos(pasta)
    if arquivos:
        upload_arquivos_para_s3(arquivos)
        deletar_arquivos_locais(arquivos)
    else:
        print("Nenhum arquivo encontrado para backup.")

if __name__ == "__main__":
    PASTA_LOCAL: str = 'Arquivos'  
    executar_backup(PASTA_LOCAL)