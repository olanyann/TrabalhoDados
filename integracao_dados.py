import pandas as pd
import numpy as np

def prepare_state_of_data(parquet_path: str) -> pd.DataFrame:
    """
    Lê o arquivo Parquet do State of Data, limpa o nome das capitais (para bater
    com o nosso scraper) e calcula o salário médio por capital.
    """
    print(f"Lendo base consolidada State of Data: {parquet_path}")
    try:
        # Requer instalação de pyarrow ou fastparquet: pip install pyarrow
        df_sod = pd.read_parquet(parquet_path)
    except FileNotFoundError:
        print(f"ERRO: Arquivo Parquet não encontrado em {parquet_path}")
        return None
    except Exception as e:
        print(f"Erro ao ler Parquet: {e}")
        return None

    # =========================================================================
    # ATENÇÃO: Nomes das colunas precisam ser ajustados para a sua base real!
    # No exemplo abaixo, assumimos que as colunas originais se chamem:
    # 'cidade_residencia' (ou similar) e 'salario' (ou 'faixa_salarial')
    # =========================================================================
    
    coluna_cidade = 'cidade'  # Substitua pelo nome exato na sua base
    coluna_salario = 'salario_atual' # Substitua pelo nome exato na sua base

    # Verificação de segurança (Remova ou adapte se os nomes forem diferentes)
    if coluna_cidade not in df_sod.columns or coluna_salario not in df_sod.columns:
        print(f"Aviso: Colunas {coluna_cidade} ou {coluna_salario} não encontradas.")
        print(f"Colunas disponíveis: {df_sod.columns.tolist()}")
        
        # --- DADOS MOCKADOS TEMPORÁRIOS PARA O SCRIPT RODAR SEM O PARQUET REAL ---
        print("\n--> Criando dados SOD mockados para demonstração...")
        df_sod = pd.DataFrame({
            'cidade': ['São Paulo', 'São Paulo', 'Rio de Janeiro', 'Brasília', 'Curitiba', 'Curitiba', 'Florianópolis'],
            'salario_atual': [12000, 15000, 11000, 14000, 8000, 9500, 10500]
        })
        coluna_cidade, coluna_salario = 'cidade', 'salario_atual'
        # -------------------------------------------------------------------------

    # 1. Limpeza da string da cidade para bater com o padrão (minúscula, sem acento, underscore)
    import unicodedata
    import re
    
    def clean_text(text):
        if pd.isna(text) or not isinstance(text, str):
            return text
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        return re.sub(r'\s+', '_', text.strip().lower())

    df_sod['capital_residencia'] = df_sod[coluna_cidade].apply(clean_text)

    # 2. Agrupamento (Groupby)
    # Calculamos a média salarial por cidade. 
    # Usamos reset_index() para transformar o resultado de volta em um DataFrame normal.
    df_agrupado = (
        df_sod.groupby('capital_residencia')[coluna_salario]
              .mean()
              .reset_index(name='salario_medio') # Renomeia a coluna agregada
    )
    
    # Arredonda o salário para 2 casas decimais
    df_agrupado['salario_medio'] = df_agrupado['salario_medio'].round(2)

    return df_agrupado


def main():
    arquivo_parquet = "dados_state_of_data_consolidados.parquet" # Caminho do seu arquivo real
    arquivo_scraper = "custo_aluguel_capitais.csv"
    
    # 1. Preparar a base do State of Data (Lê Parquet, Limpa Cidade, Calcula Média)
    df_salarios = prepare_state_of_data(arquivo_parquet)
    if df_salarios is None: return
    
    print("\n--- Salários Agrupados (Amostra) ---")
    print(df_salarios.head())

    # 2. Ler a base de custos raspada da Web
    print(f"\nLendo dados raspados de aluguel: {arquivo_scraper}")
    try:
        df_aluguel = pd.read_csv(arquivo_scraper)
    except FileNotFoundError:
        print(f"ERRO: Arquivo {arquivo_scraper} não encontrado. Rode o scraper_aluguel.py primeiro.")
        return

    print("\n--- Custos de Aluguel (Amostra) ---")
    print(df_aluguel.head())

    # 3. O JOIN (Merge)
    # Unimos as tabelas usando 'capital_residencia' como chave.
    # Usamos how='inner' para manter apenas as cidades que existem nas duas bases.
    print("\nRealizando o Merge (Inner Join)...")
    df_final = pd.merge(
        left=df_salarios,
        right=df_aluguel,
        on='capital_residencia',
        how='inner'
    )

    print("\n=== DATASET FINAL CONSOLIDADO ===")
    print(df_final)

    # 4. Salvar o resultado e opcionalmente chamar o gráfico
    arquivo_final = "dataset_analise_final.csv"
    df_final.to_csv(arquivo_final, index=False, encoding='utf-8')
    print(f"\n[OK] Dataset final salvo como: {arquivo_final}")
    
    # Descomente as linhas abaixo se quiser que este script já chame o gráfico automaticamente
    # print("\nGerando visualização...")
    # from visualizacao_dispersao import plot_scatter
    # plot_scatter(df_final)

if __name__ == "__main__":
    main()
