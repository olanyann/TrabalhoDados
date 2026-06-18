import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import re

def clean_text(text):
    """Remove acentos e padroniza."""
    if not isinstance(text, str):
        return text
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = text.strip().lower()
    text = re.sub(r'\s+', '_', text)
    return text

def scrape_real_estate_data():
    """
    NOTA: Este script está desativado pois o scraper_aluguel.py já fornece dados via FipeZAP.
    Se precisar testar, use uma URL real de um índice imobiliário.
    """
    print("⚠️  Este scraper está como exemplo educacional.")
    print("Use 'scraper_aluguel.py' para dados oficiais da FipeZAP.")
    return

if __name__ == "__main__":
    scrape_real_estate_data()
