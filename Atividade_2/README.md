# Dashboard de Vendas — Atividade 2

Este repositório contém a Atividade 2 do curso, um projeto que entrega um Dashboard interativo para análise de vendas, construído em Python com Streamlit. O objetivo é facilitar a tomada de decisão para gestores, mostrando tendências, produtos estratégicos e picos de demanda de forma clara e dinâmica.

## 1. Objetivo do Projeto

O objetivo deste projeto é desenvolver um Dashboard de análise de vendas que permita aos gestores monitorar o desempenho de produtos em diferentes lojas e períodos, identificar tendências de vendas, produtos estratégicos e picos de demanda, apoiando decisões estratégicas de reposição, marketing e planejamento de estoque.

## 2. Descrição do Projeto

O Dashboard foi desenvolvido com foco em usabilidade e rapidez de entendimento. Ele permite explorar vendas por loja, produto e período e apresenta visualizações que ajudam a responder perguntas como "quais produtos mais venderam neste trimestre?" ou "quando tivemos picos de demanda?".

Principais elementos implementados:

- Filtros por Loja, Produto e Período
  - Permite selecionar uma ou mais lojas, produtos específicos e intervalo de datas (mês/ano).
  - Os filtros atualizam todos os gráficos e indicadores do Dashboard em tempo real.

- Gráfico de Série Temporal (Quantidade Vendida por Mês)
  - Mostra a evolução das vendas ao longo do tempo e evidencia picos e vales.

- Top 10 Produtos Mais Vendidos
  - Gráfico de barras (ou tabela) com os 10 produtos com maior quantidade vendida no período filtrado.

- Receita Total no Período
  - Cálculo da receita baseado em quantidade vendida * preço unitário, exibido de forma destacada para comparação entre períodos.

## 3. Estrutura do projeto

Arquivos principais:

- `app.py` — aplicação Streamlit que inicia o Dashboard.
- `FCD_produtos.csv` — base de dados de produtos (códigos, descrições, preço, etc.).
- `FCD_vendas.csv` — base de dados de vendas (transações, quantidade, data, loja, produto).

Observação: se você mantiver os mesmos nomes de arquivo, o app irá carregar os dados automaticamente a partir da pasta do projeto.

## 4. Tecnologias utilizadas

- Python 3.8+ (recomendado)
- Streamlit — interface web interativa
- pandas — manipulação de dados
- plotly / matplotlib / seaborn — visualizações (dependendo da implementação)

Arquivo de dependências sugerido (ex.: `requirements.txt`):

```
streamlit
pandas
plotly
matplotlib
seaborn
```

## 5. Como executar (Windows / PowerShell)

1. Abra o PowerShell e navegue até a pasta do projeto:

```powershell
cd "C:\Users\Raí Araujo\Documents\Faculdade\7_Periodo\CD\Atividade_2"
```

2. (Opcional, mas recomendado) crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale as dependências (se houver `requirements.txt`):

```powershell
pip install -r requirements.txt
```

4. Rode o Dashboard com Streamlit:

```powershell
streamlit run app.py
```

O navegador abrirá uma interface com os filtros e gráficos. Caso não abra automaticamente, acesse o endereço exibido no terminal (geralmente `http://localhost:8501`).

## 6. Observações para entrega e documentação

- Envie o código-fonte completo no Google Classroom, incluindo todos os arquivos de dados usados para validação.
- Na entrega, informe claramente todas as tecnologias utilizadas e descreva os passos de instalação e execução (como neste README).
- Inclua uma pequena seção de documentação técnica (se possível, um `docs/` ou um arquivo `DOCUMENTATION.md`) que explique as transformações realizadas nos dados e possíveis limitações (dados faltantes, formatos de data, etc.).

## 7. Decisões que o Dashboard apoia (para gestores)

Com base nos dados e visualizações apresentadas, os gestores devem ser capazes de:

- Identificar picos de demanda e planejar estoque adequadamente.
- Determinar quais produtos são estratégicos para focar em vendas ou promoções.
- Tomar decisões de marketing, reposição e planejamento de vendas com base nas tendências observadas.

## 8. Contato / Autor

Aluno: (substitua pelo seu nome)

Se quiser, posso ajudar a melhorar o README com capturas de tela do Dashboard, instruções de deploy (Heroku / Streamlit Cloud) ou uma checklist de avaliação para o professor.

---

Boa sorte com a entrega — se quiser, eu já adiciono prints, exemplos de análise ou um roteiro de apresentação em 5 minutos para acompanhar este README.
