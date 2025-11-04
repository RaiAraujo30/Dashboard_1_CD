# Análise do Projeto - Dashboard de Controle de Estoque

## Objetivo Principal
Desenvolver um Dashboard interativo em Python (Streamlit) para controle de estoque que permita:
- Monitorar níveis de estoque detalhadamente
- Identificar produtos abaixo do estoque mínimo
- Auxiliar na reposição e prevenção de rupturas

## Requisitos Funcionais

### 1. Tabela Interativa com Filtro por Categoria
- Exibir todos os produtos com:
  - ID do produto
  - Nome do produto
  - Categoria
  - Quantidade em estoque
  - Estoque mínimo
  - Preço unitário
- Permitir filtro por categoria
- Tabela dinâmica que atualiza visualizações ao filtrar

### 2. Indicador de Produtos com Estoque Abaixo do Mínimo
- Indicador visual (número em destaque ou gráfico de alerta)
- Mostrar quantidade de produtos abaixo do estoque mínimo
- Atualização em tempo real conforme filtros aplicados

### 3. Gráfico de Barras: Estoque Atual vs Estoque Mínimo
- Comparar quantidade atual vs estoque mínimo por produto
- Destacar visualmente produtos em alerta
- Identificar rapidamente riscos de ruptura

### 4. Valor Total do Estoque
- Calcular e exibir valor total do estoque
- Atualização automática conforme filtros aplicados
- Fornecer visão financeira do inventário

## Requisitos Técnicos

### Tecnologias Necessárias
- Python
- Streamlit (framework para dashboard)
- Pandas (manipulação de dados CSV)
- Possivelmente: Plotly ou Matplotlib/Seaborn (gráficos)

### Estrutura do Projeto
- Desenvolvimento modular
- Suporte para múltiplos arquivos CSV
- Código organizado e documentado

### Entregáveis
- Código-fonte completo
- Documentação técnica com:
  - Tecnologias utilizadas
  - Instruções de instalação
  - Instruções de configuração
  - Instruções de uso

## Decisões para Gestores
O dashboard deve permitir:
- Identificar produtos com risco de ruptura
- Avaliar necessidade de reposição
- Tomar decisões estratégicas para manter estoque adequado

## Estratégia de Desenvolvimento

### Estrutura de Arquivos Sugerida
```
Atividade_1/
├── app.py                 # Arquivo principal do Streamlit
├── utils/
│   ├── data_loader.py    # Função para carregar CSVs
│   └── calculations.py   # Funções de cálculos (valor total, etc)
├── data/
│   ├── produtos.csv      # Dados dos produtos
│   └── [outros CSVs]
├── README.md              # Documentação do projeto
└── requirements.txt      # Dependências Python
```

### Fluxo de Desenvolvimento
1. **Análise dos CSVs** - Entender estrutura dos dados
2. **Definição do esquema** - Identificar colunas necessárias
3. **Criação da estrutura modular** - Organizar código em funções
4. **Desenvolvimento dos componentes**:
   - Carregamento de dados
   - Tabela interativa com filtros
   - Indicadores visuais
   - Gráficos
   - Cálculos financeiros
5. **Integração no Streamlit** - Montar o dashboard
6. **Testes e validação**
7. **Documentação**

## Próximos Passos
Aguardar recebimento dos CSVs para:
- Analisar estrutura dos dados
- Identificar colunas disponíveis
- Mapear colunas para requisitos do projeto
- Definir estratégia de processamento


