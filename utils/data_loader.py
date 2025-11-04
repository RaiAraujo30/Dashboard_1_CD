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
    # Obter o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Volta um nível para a raiz do projeto
    
    # Caminhos dos arquivos - tentar diferentes localizações e variações de nomes
    # Streamlit Cloud geralmente roda na raiz do projeto
    # Tentar diferentes variações de nomes (maiúsculas/minúsculas)
    variacoes_produtos = ['FCD_PRODUTOS.csv', 'FCD_produtos.csv', 'fcd_produtos.csv']
    variacoes_estoque = ['FCD_ESTOQUE.csv', 'FCD_estoque.csv', 'fcd_estoque.csv']
    
    caminhos_base = [
        os.path.join(project_root, base_path),  # Raiz do projeto/data/
        os.path.join(base_path),  # Relativo ao diretório atual
        'data',  # Relativo simples
        './data',  # Relativo com ./
        os.path.join(os.getcwd(), base_path),  # Diretório de trabalho atual
    ]
    
    caminho_produtos = None
    caminho_estoque = None
    
    # Encontrar os arquivos tentando diferentes combinações
    for caminho_base in caminhos_base:
        for variacao_produto in variacoes_produtos:
            caminho_produto_teste = os.path.join(caminho_base, variacao_produto)
            if os.path.exists(caminho_produto_teste):
                # Encontrar o arquivo de estoque correspondente
                for variacao_estoque in variacoes_estoque:
                    caminho_estoque_teste = os.path.join(caminho_base, variacao_estoque)
                    if os.path.exists(caminho_estoque_teste):
                        caminho_produtos = caminho_produto_teste
                        caminho_estoque = caminho_estoque_teste
                        break
                if caminho_produtos:
                    break
        if caminho_produtos:
            break
    
    # Verificar se os arquivos foram encontrados
    if not caminho_produtos or not os.path.exists(caminho_produtos):
        # Informações de debug
        debug_info = (
            f"Diretório atual: {os.getcwd()}\n"
            f"Diretório do script: {script_dir}\n"
            f"Raiz do projeto: {project_root}\n"
            f"Listando arquivos em {os.path.join(project_root, base_path)}: "
        )
        
        # Tentar listar arquivos no diretório data para debug
        try:
            if os.path.exists(os.path.join(project_root, base_path)):
                arquivos = os.listdir(os.path.join(project_root, base_path))
                debug_info += f"{arquivos}\n"
            else:
                debug_info += f"Diretório não existe\n"
        except Exception as e:
            debug_info += f"Erro ao listar: {str(e)}\n"
        
        raise FileNotFoundError(
            f"Arquivos CSV não encontrados.\n\n"
            f"Informações de debug:\n{debug_info}\n\n"
            f"Nomes esperados: FCD_PRODUTOS.csv (ou FCD_produtos.csv) e FCD_ESTOQUE.csv (ou FCD_estoque.csv)\n"
            f"Verifique se os arquivos estão na pasta 'data/' e foram commitados no repositório GitHub.\n"
            f"Nota: Os nomes dos arquivos são case-sensitive no Linux (Streamlit Cloud)."
        )
    
    if not os.path.exists(caminho_estoque):
        raise FileNotFoundError(
            f"Arquivo FCD_ESTOQUE.csv não encontrado.\n"
            f"Caminho tentado: {caminho_estoque}\n"
            f"Diretório do arquivo de produtos: {os.path.dirname(caminho_produtos)}\n\n"
            f"Verifique se o arquivo está na pasta 'data/' e foi commitado no repositório GitHub.\n"
            f"Consulte DEPLOY.md para mais informações."
        )
    
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


