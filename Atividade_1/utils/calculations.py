"""
Módulo para cálculos e métricas do estoque
"""
import pandas as pd


def calcular_produtos_abaixo_minimo(df):
    """
    Calcula a quantidade de produtos abaixo do estoque mínimo.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de produtos e estoque
        
    Returns:
        int: Quantidade de produtos abaixo do estoque mínimo
    """
    produtos_abaixo = df[df['quantidade_estoque'] < df['estoque_minimo']]
    return len(produtos_abaixo)


def calcular_valor_total_estoque(df):
    """
    Calcula o valor total do estoque (quantidade * preço unitário).
    Considera apenas produtos únicos para evitar duplicação.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de produtos e estoque
        
    Returns:
        float: Valor total do estoque
    """
    # Verificar se há duplicatas de produto_id (pode haver múltiplas datas/localizações)
    # Para calcular o valor total, precisamos considerar apenas uma entrada por produto
    # ou somar todas as quantidades por produto
    if 'produto_id' in df.columns:
        # Agrupar por produto_id e somar as quantidades (caso haja múltiplas localizações)
        df_agrupado = df.groupby('produto_id').agg({
            'quantidade_estoque': 'sum',
            'preco_unitario': 'first'  # Usar o primeiro preço (normalmente são iguais)
        }).reset_index()
        valor_total = (df_agrupado['quantidade_estoque'] * df_agrupado['preco_unitario']).sum()
    else:
        # Se não houver produto_id, usar cálculo direto
        valor_total = (df['quantidade_estoque'] * df['preco_unitario']).sum()
    
    return round(valor_total, 2)


def identificar_produtos_abaixo_minimo(df):
    """
    Retorna DataFrame com produtos abaixo do estoque mínimo.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de produtos e estoque
        
    Returns:
        pd.DataFrame: DataFrame filtrado com produtos abaixo do mínimo
    """
    produtos_abaixo = df[df['quantidade_estoque'] < df['estoque_minimo']].copy()
    return produtos_abaixo


