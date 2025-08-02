#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuração do banco de dados MySQL
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'pma.linksystems.com.br'),
    'user': os.getenv('DB_USER', 'adseg'),
    'password': os.getenv('DB_PASSWORD', 'Define@4536#8521'),
    'database': os.getenv('DB_NAME', 'litoral'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
    'autocommit': True,
    'raise_on_warnings': True
} 