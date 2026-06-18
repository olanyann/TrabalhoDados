import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_scatter(df_final: pd.DataFrame, save_path: str = 'grafico_dispersao.png'):
    """
    Gera um gráfico de dispersão comparando o custo de aluguel e o salário médio.
    Salva como arquivo PNG ao invés de tentar exibir na tela.
    """
    # Validação básica
    if df_final.empty:
        print("Erro: DataFrame vazio.")
        return
    
    required_cols = ['preco_aluguel_m2', 'salario_medio', 'capital_residencia']
    missing = [col for col in required_cols if col not in df_final.columns]
    if missing:
        print(f"Erro: Colunas faltando: {missing}")
        return

    # Configurando o estilo visual do gráfico
    sns.set_theme(style="whitegrid")

    # Criando a figura com um tamanho adequado
    plt.figure(figsize=(12, 8))

    # Gerando o gráfico de dispersão
    sns.scatterplot(
        data=df_final, 
        x='preco_aluguel_m2',
        y='salario_medio',
        s=150,
        color='steelblue',
        alpha=0.8
    )

    # Adicionando os nomes das capitais ao lado de cada ponto
    for i in range(df_final.shape[0]):
        plt.text(
            x=df_final['preco_aluguel_m2'].iloc[i] + 0.5,
            y=df_final['salario_medio'].iloc[i], 
            s=df_final['capital_residencia'].iloc[i].replace('_', ' ').title(),
            fontdict=dict(size=9)
        )

    # Títulos e rótulos
    plt.title('Relação entre Salário Médio em Dados e Custo do Aluguel por Capital', fontsize=16)
    plt.xlabel('Custo Médio do Aluguel (R$/m²)', fontsize=12)
    plt.ylabel('Salário Médio Declarado (R$)', fontsize=12)

    plt.tight_layout()
    
    # Salvar ao invés de mostrar
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo com sucesso em: {save_path}")
    plt.close()

if __name__ == '__main__':
    # Teste com o arquivo que você já tem
    try:
        df_merged = pd.read_csv('dataset_analise_final.csv')
        print("Dataset carregado com sucesso!")
        print(df_merged)
        plot_scatter(df_merged)
    except FileNotFoundError:
        print("Erro: arquivo 'dataset_analise_final.csv' não encontrado.")
