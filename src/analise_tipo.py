import pandas as pd
import matplotlib.pyplot as plt

def tipos_de_chamado(df: pd.DataFrame, n=10):
    """Exibe os tipos de chamados mais frequentes com base no 'Item_do_Catálogo'."""
    coluna_tipo = 'Item_do_Catálogo'
    if coluna_tipo in df.columns:
        print(f"\nTop {n} tipos de chamados mais frequentes:")
        tipos_frequentes = df[coluna_tipo].value_counts().head(n)
        print(tipos_frequentes)

        # Gerar gráfico para os tipos mais frequentes
        plt.figure(figsize=(10, 6))
        tipos_frequentes.plot(kind='bar', color='skyblue')
        for i, v in enumerate(tipos_frequentes.values):  # Mostrar valores exatos no gráfico
            plt.text(i, v + 0.05, str(v), ha='center', va='bottom', fontsize=12)
        plt.title(f'Top {n} Tipos de Chamados mais Frequentes')
        plt.xlabel('Tipo de Chamado')
        plt.ylabel('Quantidade de Chamados')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('graficos/tipos_de_chamado.png')  # Salvar o gráfico
        plt.show()

    else:
        print(f"Coluna '{coluna_tipo}' não encontrada.")

def chamados_sem_tipo(df: pd.DataFrame):
    """Informa quantos chamados estão sem tipo definido (vazios ou NaN) baseado no 'Item_do_Catálogo'."""
    coluna_tipo = 'Item_do_Catálogo'
    if coluna_tipo in df.columns:
        sem_tipo = df[coluna_tipo].isna().sum()
        print(f"\nQuantidade de chamados sem tipo definido: {sem_tipo}")
    else:
        print(f"Coluna '{coluna_tipo}' não encontrada.")
