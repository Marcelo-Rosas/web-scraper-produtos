#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Scraper Avançado com tratamento robusto de erros
Suporta múltiplas estratégias de extração e validação de dados
"""

import json
import time
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TipoExtracao(Enum):
    """Tipos de estratégias de extração"""
    TABELA = "tabela"
    DIVS = "divs"
    CSS_SELETOR = "css_seletor"
    XPATH_SIMULADO = "xpath_simulado"


@dataclass
class Produto:
    """Classe para representar um produto"""
    cod_id: str
    artigo: str
    descricao: str
    
    def validar(self) -> bool:
        """Valida se o produto tem dados obrigatórios"""
        return bool(self.cod_id and self.artigo and self.descricao)
    
    def to_dict(self) -> Dict[str, str]:
        """Converte para dicionário"""
        return {
            "Cód.ID": self.cod_id,
            "Artigo": self.artigo,
            "Descrição Resumida": self.descricao
        }


class ScraperAvancado:
    """Web Scraper avançado com validação e tratamento de erros"""
    
    def __init__(self, timeout: int = 10, retries: int = 3):
        self.timeout = timeout
        self.retries = retries
        self.produtos = []
    
    def extrair_de_tabela(self, html: str) -> List[Produto]:
        """
        Extrai dados de tabela HTML
        
        Args:
            html: Conteúdo HTML
        
        Returns:
            Lista de produtos extraídos
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tabela = soup.find('table')
            
            if not tabela:
                logger.warning("Nenhuma tabela encontrada no HTML")
                return []
            
            # Extrair headers
            headers = [th.text.strip() for th in tabela.find_all('th')]
            logger.info(f"Headers encontrados: {headers}")
            
            produtos = []
            tbody = tabela.find('tbody') or tabela
            
            for idx, tr in enumerate(tbody.find_all('tr'), 1):
                try:
                    cells = [td.text.strip() for td in tr.find_all('td')]
                    
                    if len(cells) >= 3:
                        produto = Produto(
                            cod_id=cells[0],
                            artigo=cells[1],
                            descricao=cells[2]
                        )
                        
                        if produto.validar():
                            produtos.append(produto)
                        else:
                            logger.warning(f"Produto inválido na linha {idx}")
                    else:
                        logger.debug(f"Linha {idx} com número insuficiente de colunas")
                
                except Exception as e:
                    logger.error(f"Erro ao processar linha {idx}: {e}")
                    continue
            
            logger.info(f"✅ {len(produtos)} produtos extraídos com sucesso")
            return produtos
        
        except Exception as e:
            logger.error(f"Erro ao extrair tabela: {e}")
            return []
    
    def extrair_de_divs(self, html: str, seletor_produto: str = '.produto') -> List[Produto]:
        """
        Extrai dados de estrutura de divs (comum em Bootstrap)
        
        Args:
            html: Conteúdo HTML
            seletor_produto: Seletor CSS para cada produto
        
        Returns:
            Lista de produtos extraídos
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            produtos_html = soup.select(seletor_produto)
            
            logger.info(f"Encontrados {len(produtos_html)} produtos")
            
            produtos = []
            for idx, item in enumerate(produtos_html, 1):
                try:
                    # Ajuste os seletores conforme sua estrutura HTML
                    cod_id = item.select_one('.codigo')
                    artigo = item.select_one('.artigo')
                    descricao = item.select_one('.descricao')
                    
                    if cod_id and artigo and descricao:
                        produto = Produto(
                            cod_id=cod_id.text.strip(),
                            artigo=artigo.text.strip(),
                            descricao=descricao.text.strip()
                        )
                        
                        if produto.validar():
                            produtos.append(produto)
                
                except Exception as e:
                    logger.error(f"Erro ao extrair produto {idx}: {e}")
                    continue
            
            logger.info(f"✅ {len(produtos)} produtos extraídos com sucesso")
            return produtos
        
        except Exception as e:
            logger.error(f"Erro ao extrair divs: {e}")
            return []
    
    def salvar_json(self, produtos: List[Produto], arquivo: str = 'produtos.json') -> bool:
        """
        Salva produtos em arquivo JSON
        
        Args:
            produtos: Lista de produtos
            arquivo: Nome do arquivo
        
        Returns:
            True se salvo com sucesso
        """
        try:
            dados = [p.to_dict() for p in produtos]
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ {len(produtos)} produtos salvos em {arquivo}")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao salvar JSON: {e}")
            return False
    
    def exibir_resumo(self, produtos: List[Produto], limite: int = 3) -> None:
        """
        Exibe resumo dos produtos
        
        Args:
            produtos: Lista de produtos
            limite: Número de produtos a mostrar
        """
        print(f"\n{'='*80}")
        print(f"📊 RESUMO DE DADOS EXTRAÍDOS")
        print(f"{'='*80}")
        print(f"Total de registros: {len(produtos)}")
        print(f"Mostrando: {min(limite, len(produtos))} primeiros\n")
        
        for i, produto in enumerate(produtos[:limite], 1):
            print(f"--- Produto {i} ---")
            print(f"Código ID: {produto.cod_id}")
            print(f"Artigo: {produto.artigo}")
            print(f"Descrição: {produto.descricao[:100]}...\n")
        
        print(f"{'='*80}\n")


if __name__ == "__main__":
    # Exemplo de uso
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
                <td>ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ACO CARBONO, ACABAMENTO ESTRUTURA: PINTURA ELETROSTATICA</td>
            </tr>
            <tr>
                <td>187836</td>
                <td>ESTEIRA ERGOMETRICA</td>
                <td>ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ESTEIRA COM CONSOLE EM LED DE ACO CARBONO</td>
            </tr>
            <tr>
                <td>187599</td>
                <td>ESTEIRA ERGOMETRICA</td>
                <td>ESTEIRA ERGOMETRICA - MATERIAL ESTRUTURA: ACO CARBONO, ACABAMENTO ESTRUTURA: ACO</td>
            </tr>
        </tbody>
    </table>
    """
    
    # Criar scraper
    scraper = ScraperAvancado()
    
    # Extrair dados
    logger.info("🔍 Iniciando extração de dados...")
    produtos = scraper.extrair_de_tabela(html_exemplo)
    
    # Exibir resumo
    scraper.exibir_resumo(produtos)
    
    # Salvar em JSON
    scraper.salvar_json(produtos, 'esteiras_exemplo.json')
    
    # Exibir JSON
    print("\n📄 JSON Gerado:")
    print(json.dumps([p.to_dict() for p in produtos], ensure_ascii=False, indent=2))
