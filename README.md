# Web Scraper Produtos com BeautifulSoup + Bootstrap

## 🎯 Objetivo
Extrair dados de produtos (esteiras ergométricas) de páginas HTML e exportar em formato JSON estruturado.

## 📋 Estrutura de Dados

Formato esperado do JSON:
```json
[
  {
    "Cód.ID": "192397",
    "Artigo": "ESTEIRA ERGOMETRICA",
    "Descrição Resumida": "ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ACO CARBONO..."
  }
]
```

## 🚀 Como Usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Usar o scraper básico
```bash
python scraper_basico.py
```

### 3. Usar o scraper avançado (com tratamento de erros)
```bash
python scraper_avancado.py
```

## 📁 Arquivos

- `scraper_basico.py` - Exemplo simples de web scraping
- `scraper_avancado.py` - Versão robusta com tratamento de erros
- `scraper_bootstrap_html.py` - Exemplo específico para HTML do Bootstrap
- `requirements.txt` - Dependências Python
- `exemplo_dados.json` - Dados de exemplo

## 🛠️ Tecnologias

- **BeautifulSoup4** - Parsing HTML
- **Requests** - Requisições HTTP
- **JSON** - Estrutura de dados
- **Lxml** - Parser XML/HTML

## 💡 Exemplos Práticos

### Extrair de tabela HTML
```python
from scraper_basico import extrair_tabela_html

html = "<table>...</table>"
dados = extrair_tabela_html(html)
print(dados)
```

### Extrair de página Bootstrap
```python
from scraper_bootstrap_html import extrair_produtos_bootstrap

url = "https://www.compras.rj.gov.br/..."
dados = extrair_produtos_bootstrap(url)
print(dados)
```

## 📝 Notas

- Use responsavelmente e respeite o `robots.txt`
- Adicione delays entre requisições
- Sempre verifique os termos de serviço do site
