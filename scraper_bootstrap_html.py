#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Scraper especializado para HTML com Bootstrap
Extrai dados de páginas Bootstrap e exporta em JSON estruturado
"""

import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScraperBootstrap:
    """Scraper especializado em estruturas Bootstrap"""
    
    @staticmethod
    def extrair_de_tabela_bootstrap(html: str) -> List[Dict[str, str]]:
        """
        Extrai dados de tabela Bootstrap padrão
        
        Bootstrap padrão:
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Coluna 1</th>
                    <th>Coluna 2</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Dado 1</td>
                    <td>Dado 2</td>
                </tr>
            </tbody>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Buscar tabela com classes Bootstrap
        tabela = soup.find('table', class_=['table', 'table-striped'])
        if not tabela:
            tabela = soup.find('table')  # Fallback
        
        if not tabela:
            logger.warning("Nenhuma tabela Bootstrap encontrada")
            return []
        
        # Extrair headers
        headers = []
        thead = tabela.find('thead')
        if thead:
            for th in thead.find_all('th'):
                headers.append(th.text.strip())
        
        if not headers:
            logger.warning("Nenhum header encontrado")
            return []
        
        # Extrair dados
        dados = []
        tbody = tabela.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                cells = [td.text.strip() for td in tr.find_all('td')]
                if len(cells) == len(headers):
                    linha = {headers[i]: cells[i] for i in range(len(headers))}
                    dados.append(linha)
        
        return dados
    
    @staticmethod
    def extrair_de_cards_bootstrap(html: str) -> List[Dict[str, str]]:
        """
        Extrai dados de Cards Bootstrap
        
        Bootstrap padrão:
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Título</h5>
                <p class="card-text">Descrição</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('div', class_='card')
        
        logger.info(f"Encontrados {len(cards)} cards")
        
        dados = []
        for card in cards:
            try:
                body = card.find('div', class_='card-body')
                if body:
                    titulo = body.find('h5', class_='card-title')
                    texto = body.find('p', class_='card-text')
                    
                    item = {
                        'titulo': titulo.text.strip() if titulo else '',
                        'descricao': texto.text.strip() if texto else ''
                    }
                    
                    if item['titulo']:  # Só adiciona se tiver título
                        dados.append(item)
            
            except Exception as e:
                logger.error(f"Erro ao extrair card: {e}")
                continue
        
        return dados
    
    @staticmethod
    def extrair_de_lista_bootstrap(html: str) -> List[Dict[str, str]]:
        """
        Extrai dados de List Groups Bootstrap
        
        Bootstrap padrão:
        <ul class="list-group">
            <li class="list-group-item">Item 1</li>
            <li class="list-group-item">Item 2</li>
        </ul>
        """
        soup = BeautifulSoup(html, 'html.parser')
        list_groups = soup.find_all('ul', class_='list-group')
        
        dados = []
        for grupo in list_groups:
            items = grupo.find_all('li', class_='list-group-item')
            for item in items:
                dados.append({
                    'item': item.text.strip()
                })
        
        return dados
    
    @staticmethod
    def extrair_de_container_bootstrap(html: str) -> List[Dict[str, str]]:
        """
        Extrai dados de containers Bootstrap
        (row, col, etc)
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Buscar containers com padrão Bootstrap (row > col)
        containers = soup.find_all('div', class_='container')
        
        dados = []
        for container in containers:
            rows = container.find_all('div', class_='row')
            for row in rows:
                cols = row.find_all(class_=lambda x: x and 'col' in x)
                
                linha = {}
                for idx, col in enumerate(cols):
                    linha[f'coluna_{idx}'] = col.text.strip()
                
                if linha:
                    dados.append(linha)
        
        return dados


def exemplo_completo():
    """
    Exemplo completo mostrando todas as funcionalidades
    """
    
    # HTML de exemplo com tabela Bootstrap
    html_tabela = """
    <table class="table table-striped">
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
                <td>ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ACO CARBONO, ACABAMENTO ESTRUTURA: PINTURA ELETROSTATICA</td>
            </tr>
            <tr>
                <td>187836</td>
                <td>ESTEIRA ERGOMETRICA</td>
                <td>ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ESTEIRA COM CONSOLE EM LED</td>
            </tr>
            <tr>
                <td>187599</td>
                <td>ESTEIRA ERGOMETRICA</td>
                <td>ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ACO CARBONO</td>
            </tr>
        </tbody>
    </table>
    """
    
    # HTML de exemplo com cards Bootstrap
    html_cards = """
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Esteira 1</h5>
            <p class="card-text">Esteira de alta qualidade com console LED</p>
        </div>
    </div>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Esteira 2</h5>
            <p class="card-text">Esteira com estrutura em aço carbono</p>
        </div>
    </div>
    """
    
    print("\n" + "="*80)
    print("🔍 EXEMPLO 1: Extração de Tabela Bootstrap")
    print("="*80)
    
    scraper = ScraperBootstrap()
    dados_tabela = scraper.extrair_de_tabela_bootstrap(html_tabela)
    print(json.dumps(dados_tabela, ensure_ascii=False, indent=2))
    
    print("\n" + "="*80)
    print("🔍 EXEMPLO 2: Extração de Cards Bootstrap")
    print("="*80)
    
    dados_cards = scraper.extrair_de_cards_bootstrap(html_cards)
    print(json.dumps(dados_cards, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    exemplo_completo()
