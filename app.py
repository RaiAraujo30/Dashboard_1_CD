"""
Dashboard de Controle de Estoque
Desenvolvido para disciplina de Fundamentos em Ciência de Dados
Versão 2.0 - Interface Melhorada
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.data_loader import (
    carregar_dados, 
    obter_categorias, 
    obter_marcas, 
    obter_localizacoes,
    obter_datas_referencia,
    filtrar_por_data
)
from utils.calculations import (
    calcular_produtos_abaixo_minimo,
    calcular_valor_total_estoque,
    identificar_produtos_abaixo_minimo
)

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Controle de Estoque",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Melhorar contraste das métricas */
    [data-testid="stMetricValue"] {
        color: #1f1f1f !important;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #1f1f1f !important;
        font-weight: 500;
    }
    [data-testid="stMetricDelta"] {
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">📦 Dashboard de Controle de Estoque</h1>', unsafe_allow_html=True)
st.markdown("---")

# Carregar dados com cache
@st.cache_data
def load_data():
    """Carrega os dados dos CSVs com cache"""
    df = carregar_dados('data')
    # Converter data_referencia para datetime se existir
    if 'data_referencia' in df.columns:
        df['data_referencia'] = pd.to_datetime(df['data_referencia'], errors='coerce')
    return df

df_original = load_data()

if df_original.empty:
    st.error("❌ Não foi possível carregar os dados. Verifique se os arquivos CSV estão na pasta 'data'.")
    st.stop()

# ============================================
# SIDEBAR - FILTROS AVANÇADOS
# ============================================
st.sidebar.header("🔍 Filtros Avançados")

# Filtro por Data de Referência
datas_disponiveis = obter_datas_referencia(df_original)
if datas_disponiveis:
    # Converter datas para formato string para exibição
    datas_formatadas = [d.strftime('%d/%m/%Y') if isinstance(d, pd.Timestamp) else str(d) for d in datas_disponiveis]
    
    indice_data_mais_recente = len(datas_formatadas) - 1
    
    data_selecionada_str = st.sidebar.selectbox(
        "📅 Data de Referência:",
        options=datas_formatadas,
        index=indice_data_mais_recente,
        help="Selecione a data de referência para visualizar os dados"
    )
    
    # Converter string selecionada de volta para datetime
    data_selecionada = pd.to_datetime(data_selecionada_str, format='%d/%m/%Y', errors='coerce')
    df_filtrado_data = filtrar_por_data(df_original, data_selecionada)
else:
    df_filtrado_data = df_original.copy()
    st.sidebar.info("⚠️ Nenhuma data de referência encontrada nos dados")

st.sidebar.markdown("---")

# Filtro por Categoria
categorias = obter_categorias(df_filtrado_data)
categoria_selecionada = st.sidebar.selectbox(
    "📂 Categoria:",
    options=["Todas"] + categorias,
    index=0,
    help="Filtre produtos por categoria"
)

# Filtro por Marca
marcas = obter_marcas(df_filtrado_data)
marca_selecionada = st.sidebar.selectbox(
    "🏷️ Marca:",
    options=["Todas"] + marcas,
    index=0,
    help="Filtre produtos por marca"
)

# Filtro por Localização
localizacoes = obter_localizacoes(df_filtrado_data)
localizacao_selecionada = st.sidebar.selectbox(
    "📍 Localização:",
    options=["Todas"] + localizacoes,
    index=0,
    help="Filtre produtos por localização"
)

# Filtro por Status do Estoque
status_selecionado = st.sidebar.selectbox(
    "⚠️ Status do Estoque:",
    options=["Todos", "Abaixo do Mínimo", "Adequado"],
    index=0,
    help="Filtre produtos por status do estoque"
)

# Filtro por Faixa de Preço
st.sidebar.markdown("---")
st.sidebar.subheader("💰 Faixa de Preço (R$)")

preco_min = float(df_filtrado_data['preco_unitario'].min()) if 'preco_unitario' in df_filtrado_data.columns else 0
preco_max = float(df_filtrado_data['preco_unitario'].max()) if 'preco_unitario' in df_filtrado_data.columns else 1000

preco_range = st.sidebar.slider(
    "Selecione a faixa de preço:",
    min_value=preco_min,
    max_value=preco_max,
    value=(preco_min, preco_max),
    step=10.0,
    help="Filtre produtos por faixa de preço unitário"
)

# Busca por Nome do Produto
st.sidebar.markdown("---")
busca_nome = st.sidebar.text_input(
    "🔍 Buscar por Nome:",
    placeholder="Digite o nome do produto...",
    help="Busque produtos pelo nome (busca parcial)"
)

# Botão para limpar filtros
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Limpar Todos os Filtros"):
    st.rerun()

# ============================================
# APLICAÇÃO DOS FILTROS
# ============================================
df_filtrado = df_filtrado_data.copy()

# Aplicar filtro de categoria
if categoria_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_selecionada]

# Aplicar filtro de marca
if marca_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['marca'] == marca_selecionada]

# Aplicar filtro de localização
if localizacao_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['localizacao'] == localizacao_selecionada]

# Aplicar filtro de status
if status_selecionado == "Abaixo do Mínimo":
    df_filtrado = df_filtrado[df_filtrado['quantidade_estoque'] < df_filtrado['estoque_minimo']]
elif status_selecionado == "Adequado":
    df_filtrado = df_filtrado[df_filtrado['quantidade_estoque'] >= df_filtrado['estoque_minimo']]

# Aplicar filtro de faixa de preço
df_filtrado = df_filtrado[
    (df_filtrado['preco_unitario'] >= preco_range[0]) & 
    (df_filtrado['preco_unitario'] <= preco_range[1])
]

# Aplicar busca por nome
if busca_nome:
    df_filtrado = df_filtrado[
        df_filtrado['produto_nome'].str.contains(busca_nome, case=False, na=False)
    ]

# ============================================
# MÉTRICAS PRINCIPAIS
# ============================================
st.header("📊 Métricas Principais")

# Calcular métricas
produtos_abaixo_minimo = calcular_produtos_abaixo_minimo(df_filtrado)
valor_total = calcular_valor_total_estoque(df_filtrado)
total_produtos = len(df_filtrado)
total_produtos_unicos = df_filtrado['produto_id'].nunique() if 'produto_id' in df_filtrado.columns else total_produtos
percentual_alerta = (produtos_abaixo_minimo / total_produtos * 100) if total_produtos > 0 else 0

# Exibir métricas em colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📦 Total de Produtos",
        value=total_produtos_unicos,
        help="Número total de produtos únicos exibidos"
    )

with col2:
    delta_text = f"⚠️ {produtos_abaixo_minimo} em alerta" if produtos_abaixo_minimo > 0 else "✅ OK"
    st.metric(
        label="⚠️ Produtos Abaixo do Mínimo",
        value=produtos_abaixo_minimo,
        delta=delta_text,
        delta_color="inverse" if produtos_abaixo_minimo > 0 else "normal",
        help="Quantidade de produtos que precisam de reposição"
    )

with col3:
    st.metric(
        label="💰 Valor Total do Estoque",
        value=f"R$ {valor_total:,.2f}".replace(",", "."),
        help="Valor total do estoque (quantidade × preço unitário)"
    )

with col4:
    st.metric(
        label="📈 % Produtos em Alerta",
        value=f"{percentual_alerta:.1f}%",
        delta=f"{percentual_alerta:.1f}% do total",
        delta_color="inverse" if percentual_alerta > 10 else "normal",
        help="Percentual de produtos abaixo do estoque mínimo"
    )

st.markdown("---")

# ============================================
# VISUALIZAÇÕES E GRÁFICOS
# ============================================

# Criar abas para organizar melhor as visualizações
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🚨 Alertas", "📈 Análises", "📋 Tabela de Produtos"])

with tab1:
    st.subheader("📊 Visão Geral do Estoque")
    
    # Gráfico de Barras: Estoque Atual vs Estoque Mínimo
    if not df_filtrado.empty:
        # Limitar a 30 produtos para melhor visualização
        df_plot = df_filtrado.copy()
        
        # Primeiro, criar coluna de status e calcular diferença
        df_plot['Status'] = df_plot.apply(
            lambda row: 'Abaixo do Mínimo' if row['quantidade_estoque'] < row['estoque_minimo'] else 'Adequado',
            axis=1
        )
        df_plot['Diferenca'] = df_plot['quantidade_estoque'] - df_plot['estoque_minimo']
        
        # Ordenar: produtos abaixo do mínimo primeiro, depois por diferença (mais críticos primeiro)
        df_plot = df_plot.sort_values(['Status', 'Diferenca'], ascending=[True, True])
        
        # Limitar a 30 produtos para melhor visualização
        if len(df_plot) > 30:
            # Priorizar produtos em alerta
            produtos_abaixo = df_plot[df_plot['Status'] == 'Abaixo do Mínimo']
            produtos_ok = df_plot[df_plot['Status'] == 'Adequado']
            
            if len(produtos_abaixo) >= 30:
                df_plot = produtos_abaixo.head(30)
            else:
                df_plot = pd.concat([
                    produtos_abaixo,
                    produtos_ok.head(30 - len(produtos_abaixo))
                ])
            
            st.info(f"⚠️ Exibindo os 30 produtos mais críticos de {len(df_filtrado)} produtos totais.")
        
        # Resetar índice para melhor visualização
        df_plot = df_plot.reset_index(drop=True)
        
        # Criar gráfico de barras
        fig_barras = go.Figure()
        
        # Adicionar barras de estoque atual
        cores_atual = ['#DC143C' if status == 'Abaixo do Mínimo' else '#28A745' 
                      for status in df_plot['Status']]
        
        # Adicionar barras de estoque atual
        fig_barras.add_trace(go.Bar(
            x=df_plot['produto_nome'],
            y=df_plot['quantidade_estoque'],
            name='Estoque Atual',
            marker_color=cores_atual,
            text=df_plot['quantidade_estoque'],
            textposition='outside',
            textfont=dict(size=9, color='#1f1f1f'),
            hovertemplate='<b>%{x}</b><br>Estoque Atual: %{y}<br>Estoque Mínimo: %{customdata}<extra></extra>',
            customdata=df_plot['estoque_minimo'],
            width=0.4
        ))
        
        # Adicionar barras de estoque mínimo (agrupadas)
        fig_barras.add_trace(go.Bar(
            x=df_plot['produto_nome'],
            y=df_plot['estoque_minimo'],
            name='Estoque Mínimo',
            marker_color='#FF8C00',
            marker_pattern_shape="x",
            opacity=0.7,
            text=df_plot['estoque_minimo'],
            textposition='outside',
            textfont=dict(size=9, color='#1f1f1f'),
            hovertemplate='<b>%{x}</b><br>Estoque Mínimo: %{y}<extra></extra>',
            width=0.4
        ))
        
        fig_barras.update_layout(
            title={
                'text': "Comparação: Estoque Atual vs Estoque Mínimo",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#1f1f1f'}
            },
            xaxis_title="Produtos",
            yaxis_title="Quantidade",
            height=600,
            barmode='group',
            hovermode='x unified',
            xaxis=dict(
                tickangle=-45,
                showticklabels=True,
                tickfont=dict(size=9, color='#1f1f1f'),
                title_font=dict(size=14, color='#1f1f1f')
            ),
            yaxis=dict(
                title_font=dict(size=14, color='#1f1f1f'),
                tickfont=dict(size=12, color='#1f1f1f'),
                gridcolor='rgba(128, 128, 128, 0.2)'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12, color='#1f1f1f'),
                bgcolor='rgba(255, 255, 255, 0.8)'
            ),
            template="plotly_white",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#1f1f1f')
        )
        
        st.plotly_chart(fig_barras, use_container_width=True)
        
        # Estatísticas rápidas
        produtos_abaixo_plot = df_plot[df_plot['Status'] == 'Abaixo do Mínimo']
        produtos_ok_plot = df_plot[df_plot['Status'] == 'Adequado']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Produtos em Alerta", len(produtos_abaixo_plot))
        with col2:
            st.metric("Produtos Adequados", len(produtos_ok_plot))
        with col3:
            if not produtos_abaixo_plot.empty:
                deficit_total = (produtos_abaixo_plot['estoque_minimo'] - 
                                produtos_abaixo_plot['quantidade_estoque']).sum()
                st.metric("Déficit Total", f"{int(deficit_total)} unidades")
            else:
                st.metric("Déficit Total", "0 unidades")
    else:
        st.warning("Nenhum dado disponível para exibição com os filtros selecionados.")

with tab2:
    st.subheader("🚨 Produtos que Precisam de Reposição")
    
    produtos_abaixo = identificar_produtos_abaixo_minimo(df_filtrado)
    
    if not produtos_abaixo.empty:
        st.warning(f"⚠️ **{len(produtos_abaixo)} produto(s) abaixo do estoque mínimo:**")
        
        # Criar gráfico de pizza para distribuição de alertas por categoria
        if 'categoria' in produtos_abaixo.columns:
            alertas_por_categoria = produtos_abaixo['categoria'].value_counts()
            
            fig_pizza = px.pie(
                values=alertas_por_categoria.values,
                names=alertas_por_categoria.index,
                title="Distribuição de Alertas por Categoria",
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pizza, use_container_width=True)
        
        # Tabela de produtos em alerta
        colunas_alerta = ['produto_id', 'produto_nome', 'categoria', 'marca', 'quantidade_estoque', 
                         'estoque_minimo', 'preco_unitario', 'localizacao']
        colunas_alerta = [col for col in colunas_alerta if col in produtos_abaixo.columns]
        
        df_alerta = produtos_abaixo[colunas_alerta].copy()
        df_alerta['Déficit'] = df_alerta['estoque_minimo'] - df_alerta['quantidade_estoque']
        df_alerta['Preço Unitário (R$)'] = df_alerta['preco_unitario'].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", ".")
        )
        
        # Renomear colunas
        df_alerta = df_alerta.rename(columns={
            'produto_id': 'ID',
            'produto_nome': 'Nome do Produto',
            'categoria': 'Categoria',
            'marca': 'Marca',
            'quantidade_estoque': 'Qtd. Atual',
            'estoque_minimo': 'Qtd. Mínima',
            'localizacao': 'Localização'
        })
        
        # Reordenar colunas
        ordem_colunas = ['ID', 'Nome do Produto', 'Categoria', 'Marca', 'Qtd. Atual', 
                        'Qtd. Mínima', 'Déficit', 'Preço Unitário (R$)', 'Localização']
        ordem_colunas = [col for col in ordem_colunas if col in df_alerta.columns]
        df_alerta = df_alerta[ordem_colunas]
        
        st.dataframe(
            df_alerta,
            use_container_width=True,
            hide_index=True
        )
        
        # Calcular valor necessário para reposição
        # Usar os dados originais antes do rename
        valor_reposicao = ((produtos_abaixo['estoque_minimo'] - produtos_abaixo['quantidade_estoque']) * produtos_abaixo['preco_unitario']).sum()
        st.info(f"💰 **Valor estimado para reposição:** R$ {valor_reposicao:,.2f}".replace(",", "."))
    else:
        st.success("✅ Todos os produtos estão com estoque adequado!")

with tab3:
    st.subheader("📈 Análises Detalhadas")
    
    # Análise por Categoria
    if 'categoria' in df_filtrado.columns and not df_filtrado.empty:
        st.markdown("#### 📂 Análise por Categoria")
        
        # Calcular valor total por categoria
        df_filtrado['valor_total'] = df_filtrado['quantidade_estoque'] * df_filtrado['preco_unitario']
        
        analise_categoria = df_filtrado.groupby('categoria').agg({
            'produto_id': 'count',
            'quantidade_estoque': 'sum',
            'estoque_minimo': 'sum',
            'valor_total': 'sum'
        }).rename(columns={
            'produto_id': 'Total Produtos',
            'quantidade_estoque': 'Estoque Total',
            'estoque_minimo': 'Mínimo Total',
            'valor_total': 'Valor Total (R$)'
        })
        analise_categoria['Valor Total (R$)'] = analise_categoria['Valor Total (R$)'].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", ".")
        )
        
        st.dataframe(analise_categoria, use_container_width=True)
        
        # Gráfico de barras por categoria
        fig_categoria = px.bar(
            analise_categoria.reset_index(),
            x='categoria',
            y='Estoque Total',
            title="Estoque Total por Categoria",
            labels={'Estoque Total': 'Quantidade em Estoque', 'categoria': 'Categoria'},
            color='categoria',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_categoria.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig_categoria, use_container_width=True)
    
    # Análise por Localização
    if 'localizacao' in df_filtrado.columns and not df_filtrado.empty:
        st.markdown("#### 📍 Análise por Localização")
        
        analise_localizacao = df_filtrado.groupby('localizacao').agg({
            'produto_id': 'count',
            'quantidade_estoque': 'sum',
            'estoque_minimo': 'sum'
        }).rename(columns={
            'produto_id': 'Total Produtos',
            'quantidade_estoque': 'Estoque Total',
            'estoque_minimo': 'Mínimo Total'
        })
        
        st.dataframe(analise_localizacao, use_container_width=True)
        
        # Gráfico de barras por localização
        fig_localizacao = px.bar(
            analise_localizacao.reset_index(),
            x='localizacao',
            y='Estoque Total',
            title="Estoque Total por Localização",
            labels={'Estoque Total': 'Quantidade em Estoque', 'localizacao': 'Localização'},
            color='localizacao',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_localizacao.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig_localizacao, use_container_width=True)

with tab4:
    st.subheader("📋 Tabela Completa de Produtos")
    
    # Selecionar colunas para exibição
    colunas_tabela = ['produto_id', 'produto_nome', 'categoria', 'marca', 'quantidade_estoque', 
                      'estoque_minimo', 'preco_unitario', 'localizacao']
    colunas_tabela = [col for col in colunas_tabela if col in df_filtrado.columns]
    
    # Criar DataFrame para tabela
    df_tabela = df_filtrado[colunas_tabela].copy()
    
    # Adicionar coluna de status
    df_tabela['Status'] = df_tabela.apply(
        lambda row: '⚠️ Abaixo do Mínimo' if row['quantidade_estoque'] < row['estoque_minimo'] else '✅ OK',
        axis=1
    )
    
    # Calcular diferença
    df_tabela['Diferença'] = df_tabela['quantidade_estoque'] - df_tabela['estoque_minimo']
    
    # Formatação de valores monetários
    df_tabela['Preço Unitário (R$)'] = df_tabela['preco_unitario'].apply(
        lambda x: f"R$ {x:,.2f}".replace(",", ".")
    )
    
    # Renomear colunas
    df_tabela = df_tabela.rename(columns={
        'produto_id': 'ID',
        'produto_nome': 'Nome do Produto',
        'categoria': 'Categoria',
        'marca': 'Marca',
        'quantidade_estoque': 'Qtd. Atual',
        'estoque_minimo': 'Qtd. Mínima',
        'localizacao': 'Localização'
    })
    
    # Reordenar colunas
    ordem_colunas = ['ID', 'Nome do Produto', 'Categoria', 'Marca', 'Qtd. Atual', 
                     'Qtd. Mínima', 'Diferença', 'Status', 'Preço Unitário (R$)', 'Localização']
    ordem_colunas = [col for col in ordem_colunas if col in df_tabela.columns]
    df_tabela = df_tabela[ordem_colunas]
    
    # Ordenar por status (abaixo do mínimo primeiro)
    df_tabela['Status_Order'] = df_tabela['Status'].apply(lambda x: 0 if '⚠️' in str(x) else 1)
    df_tabela = df_tabela.sort_values(['Status_Order', 'Diferença'], ascending=[True, True])
    df_tabela = df_tabela.drop('Status_Order', axis=1)
    
    # Exibir tabela
    st.dataframe(
        df_tabela,
        use_container_width=True,
        hide_index=True
    )
    
    # Botão para exportar dados
    st.markdown("---")
    csv = df_tabela.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"estoque_filtrado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Baixe os dados filtrados em formato CSV"
    )

# ============================================
# RESUMO DOS FILTROS ATIVOS
# ============================================
st.markdown("---")
with st.expander("ℹ️ Informações sobre os Filtros Ativos"):
    filtros_ativos = []
    if categoria_selecionada != "Todas":
        filtros_ativos.append(f"**Categoria:** {categoria_selecionada}")
    if marca_selecionada != "Todas":
        filtros_ativos.append(f"**Marca:** {marca_selecionada}")
    if localizacao_selecionada != "Todas":
        filtros_ativos.append(f"**Localização:** {localizacao_selecionada}")
    if status_selecionado != "Todos":
        filtros_ativos.append(f"**Status:** {status_selecionado}")
    if preco_range[0] > preco_min or preco_range[1] < preco_max:
        filtros_ativos.append(f"**Preço:** R$ {preco_range[0]:,.2f} - R$ {preco_range[1]:,.2f}".replace(",", "."))
    if busca_nome:
        filtros_ativos.append(f"**Busca:** {busca_nome}")
    
    if filtros_ativos:
        st.write("**Filtros aplicados:**")
        for filtro in filtros_ativos:
            st.write(f"- {filtro}")
    else:
        st.write("Nenhum filtro específico aplicado (exibindo todos os dados).")
    
    st.write(f"**Total de registros exibidos:** {len(df_filtrado)} de {len(df_original)}")

# Rodapé
st.markdown("---")
st.caption("📊 Dashboard desenvolvido para disciplina de Fundamentos em Ciência de Dados - 2025.2 | Versão 2.0")
