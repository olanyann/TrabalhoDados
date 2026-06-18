import os
import subprocess
import sys

def download_state_of_data():
    dataset_name = "datahackers/state-of-data-2023"
    print(f"Iniciando o download do dataset: {dataset_name}")
    print("Certifique-se de que o arquivo kaggle.json com suas credenciais esteja em ~/.kaggle/")
    
    try:
        # Tenta usar a biblioteca kaggle diretamente
        import kaggle
        kaggle.api.authenticate()
        print("Autenticação no Kaggle bem-sucedida.")
        
        print("Baixando os arquivos e extraindo...")
        kaggle.api.dataset_download_files(dataset_name, path='.', unzip=True)
        print("[OK] Download e extração concluídos com sucesso via API do Kaggle!")
        
    except ImportError:
        print("A biblioteca 'kaggle' não foi encontrada no Python. Tentando via linha de comando...")
        try:
            # Tenta executar o kaggle como comando de sistema
            subprocess.run(["kaggle", "datasets", "download", "-d", dataset_name, "--unzip"], check=True)
            print("[OK] Download e extração concluídos com sucesso via CLI do Kaggle!")
        except FileNotFoundError:
            print("ERRO: O executável 'kaggle' não foi encontrado. Instale com 'pip install kaggle'.")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"ERRO: Falha ao executar o comando do Kaggle. Detalhes: {e}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Erro inesperado ao tentar baixar o dataset: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_state_of_data()
