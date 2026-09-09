#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Scraper Básico com BeautifulSoup
Extrai dados de tabelas HTML e exporta em JSON
"""

import json
from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Any


def extrair_tabela_html(html_content: str) -> List[Dict[str, str]]:
    """
    Extrai dados de uma tabela HTML padrão
    
    Args:
        html_content: String contendo HTML
    
    Returns:
        Lista de dicionários com os dados
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tabela = soup.find('table')
    
    if not tabela:
        return []
    
    # Extrair headers
    headers = []
    for th in tabela.find_all('th'):
        headers.append(th.text.strip())
    
    # Extrair dados
    dados = []
    tbody = tabela.find('tbody')
    
    if tbody:
        for tr in tbody.find_all('tr'):
            cells = tr.find_all('td')
            if len(cells) == len(headers):
                linha = {headers[i]: cells[i].text.strip() for i in range(len(headers))}
                dados.append(linha)
    
    return dados


def extrair_de_url(url: str) -> List[Dict[str, str]]:
    """
    Extrai dados de uma URL
    
    Args:
        url: URL da página
    
    Returns:
        Lista de dicionários com os dados
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            return extrair_tabela_html(response.text)
        else:
            print(f"Erro: Status code {response.status_code}")
            return []
    
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")
        return []


def salvar_json(dados: List[Dict[str, str]], arquivo: str = 'produtos.json') -> None:
    """
    Salva dados em arquivo JSON
    
    Args:
        dados: Lista de dicionários
        arquivo: Nome do arquivo de saída
    """
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dados salvos em {arquivo}")
    print(f"📊 Total de registros: {len(dados)}")


def exibir_dados(dados: List[Dict[str, str]], limite: int = 5) -> None:
    """
    Exibe dados no console
    
    Args:
        dados: Lista de dicionários
        limite: Número de registros a exibir
    """
    print(f"\n📋 Mostrando {min(limite, len(dados))} de {len(dados)} registros:\n")
    
    for i, item in enumerate(dados[:limite], 1):
        print(f"--- Registro {i} ---")
        for chave, valor in item.items():
            print(f"{chave}: {valor}")
        print()


if __name__ == "__main__":
    # Exemplo 1: HTML inline
    html_exemplo = """
    <table>
        <thead>
            <tr>
                <th>Cód.ID</th>
                <th>Artigo</th>
                <th>Descrição Resumida</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>192397</td>
                <td>ESTEIRA ERGOMETRICA</td>
                <td>ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ACO CARBONO</td>
            </tr>
            <tr>
                <td>187836</td>
                <td>ESTEIRA ERGOMETRICA</td>
                <td>ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ESTEIRA COM CONSOLE EM LED</td>
            </tr>
        </tbody>
    </table>
    """
    
    print("🔍 Extraindo dados da tabela HTML...\n")
    dados = extrair_tabela_html(html_exemplo)
    
    exibir_dados(dados)
    salvar_json(dados, 'produtos_exemplo.json')
