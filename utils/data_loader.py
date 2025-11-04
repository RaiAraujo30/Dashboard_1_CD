"""
Módulo para carregar e processar dados dos CSVs
"""
import pandas as pd
import os


def carregar_dados(base_path='data'):
    """
    Carrega os dados dos CSVs e faz o join entre produtos e estoque.
    
    Args:
        base_path (str): Caminho base onde estão os arquivos CSV
        
    Returns:
        pd.DataFrame: DataFrame com dados unificados de produtos e estoque
    """
    # Caminhos dos arquivos
    caminho_produtos = os.path.join(base_path, 'FCD_PRODUTOS.csv')
    caminho_estoque = os.path.join(base_path, 'FCD_ESTOQUE.csv')
    
    # Carregar CSVs
    df_produtos = pd.read_csv(caminho_produtos)
    df_estoque = pd.read_csv(caminho_estoque)
    
    # Fazer join por produto_id
    df_merged = pd.merge(
        df_produtos,
        df_estoque,
        on='produto_id',
        how='left'  # Left join para manter todos os produtos, mesmo sem estoque
    )
    
    # Preencher valores NaN em quantidade_estoque e estoque_minimo com 0
    # para produtos que não têm registro de estoque
    df_merged['quantidade_estoque'] = df_merged['quantidade_estoque'].fillna(0).astype(int)
    df_merged['estoque_minimo'] = df_merged['estoque_minimo'].fillna(0).astype(int)
    
    return df_merged


def obter_categorias(df):
    """
    Retorna lista de categorias únicas ordenadas.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de produtos
        
    Returns:
        list: Lista de categorias únicas
    """
    categorias = df['categoria'].unique().tolist()
    categorias.sort()
    return categorias


def obter_marcas(df):
    """
    Retorna lista de marcas únicas ordenadas.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de produtos
        
    Returns:
        list: Lista de marcas únicas
    """
    marcas = df['marca'].dropna().unique().tolist()
    marcas.sort()
    return marcas


def obter_localizacoes(df):
    """
    Retorna lista de localizações únicas ordenadas.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de produtos
        
    Returns:
        list: Lista de localizações únicas
    """
    localizacoes = df['localizacao'].dropna().unique().tolist()
    localizacoes.sort()
    return localizacoes


def obter_datas_referencia(df):
    """
    Retorna lista de datas de referência únicas ordenadas.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de produtos
        
    Returns:
        list: Lista de datas de referência únicas
    """
    if 'data_referencia' in df.columns:
        df_copy = df.copy()
        df_copy['data_referencia'] = pd.to_datetime(df_copy['data_referencia'], errors='coerce')
        datas = df_copy['data_referencia'].dropna().unique().tolist()
        datas.sort()
        return datas
    return []


def filtrar_por_data(df, data_selecionada=None):
    """
    Filtra o DataFrame por data de referência. Se nenhuma data for selecionada,
    retorna apenas os dados da data mais recente.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de produtos
        data_selecionada: Data a ser filtrada (None para usar a data mais recente)
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    if 'data_referencia' not in df.columns:
        return df.copy()
    
    df_copy = df.copy()
    df_copy['data_referencia'] = pd.to_datetime(df_copy['data_referencia'], errors='coerce')
    
    if data_selecionada is None:
        # Se nenhuma data for selecionada, usar a data mais recente
        data_mais_recente = df_copy['data_referencia'].max()
        return df_copy[df_copy['data_referencia'] == data_mais_recente].copy()
    else:
        data_selecionada_dt = pd.to_datetime(data_selecionada, errors='coerce')
        return df_copy[df_copy['data_referencia'] == data_selecionada_dt].copy()


