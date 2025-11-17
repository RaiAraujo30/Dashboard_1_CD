# Dashboard de Controle de Estoque

Dashboard interativo desenvolvido em Python e Streamlit para monitoramento e análise de estoque de produtos. Permite visualizar níveis de estoque, identificar produtos abaixo do estoque mínimo, calcular valores totais e realizar análises por categoria, marca e localização.

## Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework para criação de dashboards interativos
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas

## Estrutura do Projeto

```
Atividade_1/
├── app.py                    # Aplicação principal Streamlit
├── requirements.txt          # Dependências do projeto
├── data/
│   ├── FCD_PRODUTOS.csv      # Dados dos produtos
│   └── FCD_ESTOQUE.csv       # Dados de estoque
└── utils/
    ├── __init__.py
    ├── data_loader.py        # Carregamento e processamento de dados
    └── calculations.py       # Cálculos e métricas
```

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. Clone o repositório ou baixe os arquivos do projeto

2. Navegue até a pasta do projeto:
   ```bash
   cd Atividade_1
   ```

3. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   ```

4. Ative o ambiente virtual:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução

Após a instalação, execute o dashboard:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no navegador padrão na URL `http://localhost:8501`.

## Dados Necessários

O projeto requer dois arquivos CSV na pasta `data/`:

### FCD_PRODUTOS.csv
Contém informações dos produtos:
- `produto_id`: Identificador único do produto
- `sku`: Código SKU
- `produto_nome`: Nome do produto
- `categoria`: Categoria do produto
- `marca`: Marca do produto
- `preco_unitario`: Preço unitário de venda
- `custo_unitario`: Custo unitário
- `estoque_inicial`: Estoque inicial
- `unidade_medida`: Unidade de medida
- `peso_kg`: Peso em quilogramas
- `dimensao_cm`: Dimensões em centímetros

### FCD_ESTOQUE.csv
Contém informações de estoque:
- `estoque_id`: Identificador único do registro
- `data_referencia`: Data de referência do estoque
- `produto_id`: ID do produto (chave para join)
- `quantidade_estoque`: Quantidade atual em estoque
- `estoque_minimo`: Estoque mínimo recomendado
- `localizacao`: Localização do produto

## Funcionalidades

### Filtros Disponíveis

- **Data de Referência**: Seleciona a data específica para análise
- **Categoria**: Filtra produtos por categoria
- **Marca**: Filtra produtos por marca
- **Localização**: Filtra produtos por localização física
- **Status do Estoque**: Mostra apenas produtos abaixo do mínimo, adequados ou todos
- **Faixa de Preço**: Define intervalo de preço unitário
- **Busca por Nome**: Busca parcial por nome do produto

### Visualizações

1. **Métricas Principais**
   - Total de produtos únicos
   - Produtos abaixo do estoque mínimo
   - Valor total do estoque
   - Percentual de produtos em alerta

2. **Visão Geral**
   - Gráfico de barras agrupadas comparando estoque atual vs estoque mínimo
   - Estatísticas rápidas dos produtos exibidos

3. **Alertas**
   - Lista de produtos que precisam de reposição
   - Gráfico de distribuição de alertas por categoria
   - Valor estimado necessário para reposição

4. **Análises**
   - Análise por categoria com gráficos
   - Análise por localização com gráficos

5. **Tabela Completa**
   - Tabela interativa com todos os produtos
   - Ordenação automática (produtos em alerta primeiro)
   - Exportação para CSV

## Módulos do Projeto

### utils/data_loader.py

Responsável pelo carregamento e processamento dos dados:

- `carregar_dados(base_path='data')`: Carrega os CSVs, faz join por `produto_id` e retorna DataFrame unificado
- `obter_categorias(df)`: Retorna lista de categorias únicas
- `obter_marcas(df)`: Retorna lista de marcas únicas
- `obter_localizacoes(df)`: Retorna lista de localizações únicas
- `obter_datas_referencia(df)`: Retorna lista de datas de referência disponíveis
- `filtrar_por_data(df, data_selecionada=None)`: Filtra DataFrame por data (padrão: data mais recente)

### utils/calculations.py

Contém as funções de cálculo:

- `calcular_produtos_abaixo_minimo(df)`: Conta produtos abaixo do estoque mínimo
- `calcular_valor_total_estoque(df)`: Calcula valor total do estoque (agrupa por produto para evitar duplicação)
- `identificar_produtos_abaixo_minimo(df)`: Retorna DataFrame com produtos em alerta

### app.py

Aplicação principal que integra todos os componentes:

- Carrega dados com cache (`@st.cache_data`)
- Implementa interface com filtros na sidebar
- Exibe métricas e visualizações
- Organiza conteúdo em abas para melhor navegação

## Deploy no Streamlit Cloud

### Requisitos

1. Repositório GitHub com o código do projeto
2. Arquivos CSV commitados na pasta `data/`
3. Arquivo `requirements.txt` na raiz do projeto

### Passos

1. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
2. Conecte seu repositório GitHub
3. Configure:
   - **Main file path**: `app.py`
   - **Python version**: 3.8 ou superior
   - **Branch**: Branch principal (geralmente `main` ou `master`)

### Notas Importantes

- Certifique-se de que os arquivos CSV estão commitados no repositório
- Os nomes dos arquivos são case-sensitive no Linux (Streamlit Cloud)
- O código tenta automaticamente diferentes variações de maiúsculas/minúsculas

## Solução de Problemas

### Erro ao carregar arquivos CSV

**Problema**: `FileNotFoundError` ao executar o dashboard

**Soluções**:
1. Verifique se os arquivos `FCD_PRODUTOS.csv` e `FCD_ESTOQUE.csv` estão na pasta `data/`
2. Confirme que os nomes dos arquivos estão corretos
3. No Streamlit Cloud, verifique se os arquivos foram commitados no GitHub

### Erro de módulo não encontrado

**Problema**: `ModuleNotFoundError` ao executar

**Soluções**:
1. Certifique-se de que está na pasta `Atividade_1` ao executar `streamlit run app.py`
2. Verifique se todas as dependências foram instaladas: `pip install -r requirements.txt`
3. Confirme que o arquivo `utils/__init__.py` existe

### Dados não aparecem corretamente

**Problema**: Dashboard carrega mas não mostra dados

**Soluções**:
1. Verifique a estrutura dos CSVs (cabecalhos corretos)
2. Confirme que a coluna `produto_id` existe em ambos os arquivos
3. Verifique se há dados na data de referência selecionada

## Desenvolvimento

### Estrutura de Dados

O join entre produtos e estoque é feito usando `produto_id` como chave. Produtos sem registro de estoque recebem valores padrão (0) para quantidade e estoque mínimo.

### Cache

O projeto utiliza cache do Streamlit (`@st.cache_data`) para otimizar o carregamento dos dados, evitando recarregar os CSVs a cada interação do usuário.

### Processamento de Dados

O cálculo do valor total do estoque agrupa produtos por `produto_id` antes de calcular, evitando duplicação quando o mesmo produto aparece em múltiplas localizações ou datas.

## Licença

Este projeto foi desenvolvido para fins acadêmicos.

## Autor

Desenvolvido para a disciplina de **Fundamentos em Ciência de Dados** - Período 2025.2

Professor: Assuero Ximenes

