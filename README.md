# Dashboard de Controle de Estoque

## 📋 Descrição do Projeto

Dashboard interativo desenvolvido em Python utilizando Streamlit para controle e monitoramento de estoque. O projeto permite aos gestores visualizar, analisar e tomar decisões estratégicas sobre o estoque de produtos de uma empresa.

## 🎯 Objetivos

- Monitorar o nível de estoque de forma detalhada e dinâmica
- Identificar produtos que estão abaixo do estoque mínimo recomendado
- Fornecer informações que auxiliem na reposição de produtos e prevenção de rupturas
- Garantir a manutenção adequada do estoque

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**: Linguagem de programação principal
- **Streamlit 1.28.0+**: Framework para criação do dashboard interativo
- **Pandas 2.0.0+**: Biblioteca para manipulação e análise de dados
- **Plotly 5.17.0+**: Biblioteca para criação de gráficos interativos

## 📁 Estrutura do Projeto

```
Atividade_1/
├── app.py                      # Arquivo principal do dashboard Streamlit
├── requirements.txt            # Dependências do projeto
├── README.md                   # Documentação do projeto
├── ANALISE_PROJETO.md         # Análise inicial dos requisitos
├── data/
│   ├── FCD_PRODUTOS.csv       # Dados dos produtos
│   └── FCD_ESTOQUE.csv         # Dados de estoque
└── utils/
    ├── __init__.py             # Inicialização do módulo utils
    ├── data_loader.py          # Funções para carregar e processar CSVs
    └── calculations.py         # Funções para cálculos e métricas
```

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou baixe o projeto** para sua máquina local

2. **Navegue até a pasta do projeto:**
   ```bash
   cd Atividade_1
   ```

3. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   ```

4. **Ative o ambiente virtual:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

5. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuração

1. **Certifique-se de que os arquivos CSV estão na pasta `data/`:**
   - `FCD_PRODUTOS.csv`: Contém informações dos produtos (ID, nome, categoria, preço, etc.)
   - `FCD_ESTOQUE.csv`: Contém informações de estoque (quantidade atual, estoque mínimo, localização)

2. **Estrutura esperada dos CSVs:**

   **FCD_PRODUTOS.csv:**
   - `produto_id`: ID único do produto
   - `sku`: Código SKU do produto
   - `produto_nome`: Nome do produto
   - `categoria`: Categoria do produto
   - `marca`: Marca do produto
   - `preco_unitario`: Preço unitário de venda
   - `custo_unitario`: Custo unitário
   - `estoque_inicial`: Estoque inicial
   - `unidade_medida`: Unidade de medida
   - `peso_kg`: Peso em quilogramas
   - `dimensao_cm`: Dimensões em centímetros

   **FCD_ESTOQUE.csv:**
   - `estoque_id`: ID único do registro de estoque
   - `data_referencia`: Data de referência
   - `produto_id`: ID do produto (chave para join)
   - `quantidade_estoque`: Quantidade atual em estoque
   - `estoque_minimo`: Estoque mínimo recomendado
   - `localizacao`: Localização do produto

## 🖥️ Execução

Para executar o dashboard, execute o seguinte comando na pasta do projeto:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no navegador padrão na URL: `http://localhost:8501`

## 📊 Funcionalidades do Dashboard

### 1. Tabela Interativa com Filtro por Categoria

- Exibe todos os produtos cadastrados com informações detalhadas:
  - ID do produto
  - Nome do produto
  - Categoria
  - Quantidade em estoque
  - Estoque mínimo
  - Preço unitário
  - Marca
  - Localização
  - Status (OK ou Abaixo do Mínimo)

- Permite filtrar produtos por categoria através do menu lateral
- A tabela é dinâmica e atualiza automaticamente conforme os filtros aplicados

### 2. Indicador de Produtos com Estoque Abaixo do Mínimo

- Exibe um indicador visual destacando a quantidade de produtos abaixo do estoque mínimo
- Gráfico interativo mostrando produtos em alerta (vermelho) vs produtos OK (verde)
- Lista detalhada dos produtos que precisam de reposição
- Atualização em tempo real conforme os filtros aplicados

### 3. Gráfico de Barras: Estoque Atual vs Estoque Mínimo

- Gráfico de barras comparativo mostrando:
  - Quantidade atual de cada produto (barras coloridas)
  - Linha de estoque mínimo (linha laranja tracejada)
- Produtos em alerta são destacados em vermelho
- Produtos OK são destacados em verde
- Permite identificar rapidamente riscos de ruptura no estoque

### 4. Valor Total do Estoque

- Calcula e exibe o valor total do estoque (quantidade × preço unitário)
- Atualização automática conforme os filtros aplicados
- Fornece uma visão financeira clara do inventário

### 5. Métricas Principais

- **Total de Produtos**: Quantidade total de produtos cadastrados
- **Produtos Abaixo do Mínimo**: Quantidade de produtos em alerta
- **Valor Total do Estoque**: Valor financeiro total do estoque
- **% Produtos em Alerta**: Percentual de produtos abaixo do mínimo

## 📈 Decisões para Gestores

Com base nos dados apresentados no dashboard, os gestores podem:

- **Identificar produtos com risco de ruptura**: Visualizar produtos abaixo do estoque mínimo
- **Avaliar a necessidade de reposição**: Analisar quais produtos precisam ser reabastecidos
- **Tomar decisões estratégicas**: Utilizar o valor total do estoque e métricas para planejamento
- **Monitorar por categoria**: Filtrar e analisar produtos por categoria específica

## 🔧 Desenvolvimento

### Módulos do Projeto

#### `utils/data_loader.py`
- `carregar_dados()`: Carrega os CSVs e faz o join entre produtos e estoque
- `obter_categorias()`: Retorna lista de categorias únicas

#### `utils/calculations.py`
- `calcular_produtos_abaixo_minimo()`: Calcula quantidade de produtos abaixo do mínimo
- `calcular_valor_total_estoque()`: Calcula valor total do estoque
- `identificar_produtos_abaixo_minimo()`: Retorna DataFrame com produtos em alerta

#### `app.py`
- Arquivo principal do Streamlit
- Contém toda a interface do dashboard
- Integra os módulos de dados e cálculos

## 📝 Notas Técnicas

- O projeto utiliza cache do Streamlit (`@st.cache_data`) para otimizar o carregamento dos dados
- O join entre produtos e estoque é feito usando `produto_id` como chave
- Produtos sem registro de estoque têm valores padrão (0) para quantidade e estoque mínimo
- Os gráficos são interativos e permitem zoom, pan e hover para mais detalhes

## 🐛 Solução de Problemas

### Erro ao executar o Streamlit
- Verifique se todas as dependências foram instaladas: `pip install -r requirements.txt`
- Certifique-se de que está usando Python 3.8 ou superior

### Erro ao carregar os CSVs
- Verifique se os arquivos CSV estão na pasta `data/`
- Confirme que os nomes dos arquivos estão corretos: `FCD_PRODUTOS.csv` e `FCD_ESTOQUE.csv`
- Verifique se os arquivos CSV têm o cabeçalho correto

### Erro de módulo não encontrado
- Certifique-se de que está executando o comando na pasta `Atividade_1`
- Verifique se o arquivo `utils/__init__.py` existe

## 👨‍💻 Autor

Desenvolvido para a disciplina de **Fundamentos em Ciência de Dados** - Período 2025.2

Professor: Assuero Ximenes

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.


