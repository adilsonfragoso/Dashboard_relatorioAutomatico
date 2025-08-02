#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor FastAPI com webhook para outras aplicações
Recebe solicitações de outras aplicações e processa edições para gerar relatórios
Versão adaptada para Docker/Coolify
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
import subprocess
import asyncio
import logging
from datetime import datetime, time
from dotenv import load_dotenv
import requests
import base64
from pathlib import Path
import mysql.connector

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logs para ambiente local/Docker
import os
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'webhook_server.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurações do Webhook (adaptado para outras aplicações)
WEBHOOK_API_KEY = os.getenv('WEBHOOK_API_KEY', 'webhook_secret')

# Importar configuração do banco
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
    from db_config import DB_CONFIG
except ImportError:
    # Fallback para configuração direta se não conseguir importar
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'pma.linksystems.com.br'),
        'user': os.getenv('DB_USER', 'adseg'),
        'password': os.getenv('DB_PASSWORD', 'Define@4536#8521'),
        'database': os.getenv('DB_NAME', 'litoral'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

# Configurações do servidor
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 8011))
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'webhook_secret')

app = FastAPI(title="Webhook Evolution API", version="1.0.0")

class WebhookHandler:
    """Classe para gerenciar solicitações de outras aplicações"""
    
    def __init__(self):
        self.api_key = WEBHOOK_API_KEY
        
        # Mapeamento de siglas oficiais e seus horários
        self.siglas_horarios = {
            'PPT': time(9, 20),    # 09:20
            'PTM': time(11, 20),   # 11:20
            'PT': time(14, 20),    # 14:20
            'PTV': time(16, 20),   # 16:20
            'PTN': time(18, 20),   # 18:20
            'FEDERAL': time(19, 0), # 19:00
            'CORUJINHA': time(21, 30) # 21:30
        }
        
        # Siglas oficiais válidas
        self.siglas_oficiais = list(self.siglas_horarios.keys())
    
    def extrair_sigla_oficial(self, sigla_completa):
        """
        Extrai a sigla oficial de uma sigla completa
        Ex: 'PT ESPECIAL' -> 'PT', 'PPT EXTRA' -> 'PPT'
        IMPORTANTE: Verifica siglas mais específicas primeiro para evitar confusão
        """
        if not sigla_completa:
            return None
            
        sigla_upper = sigla_completa.upper().strip()
        
        # Lista ordenada por especificidade (mais específicas primeiro)
        # Isso evita que PT seja confundido com PTV, PTN, PTM
        siglas_ordenadas = [
            'CORUJINHA',  # Mais específica
            'FEDERAL',    # Mais específica
            'PPT',        # Mais específica
            'PTV',        # Mais específica que PT
            'PTN',        # Mais específica que PT
            'PTM',        # Mais específica que PT
            'PT'          # Menos específica - deve ser verificada por último
        ]
        
        # Verificar siglas na ordem de especificidade
        for sigla_oficial in siglas_ordenadas:
            if sigla_upper.startswith(sigla_oficial):
                logger.info(f"Sigla extraída: '{sigla_completa}' -> '{sigla_oficial}'")
                return sigla_oficial
        
        logger.warning(f"Nenhuma sigla oficial encontrada em: '{sigla_completa}'")
        return None
    
    def obter_horario_sorteio(self, sigla_oficial):
        """Retorna o horário de sorteio para uma sigla oficial"""
        return self.siglas_horarios.get(sigla_oficial)
    
    def validar_horario_edicao(self, sigla_oficial, data_sorteio):
        """
        Valida se a edição pode ser processada baseada no horário atual
        Retorna: (pode_processar, mensagem_aviso)
        """
        try:
            # Verificar se é data atual ou futura
            hoje = datetime.now().date()
            if data_sorteio < hoje:
                # Edições passadas sempre podem ser processadas
                return True, None
            
            # Para data atual, verificar horário
            if data_sorteio == hoje:
                horario_atual = datetime.now().time()
                horario_sorteio = self.obter_horario_sorteio(sigla_oficial)
                
                if not horario_sorteio:
                    logger.warning(f"Horário não encontrado para sigla: {sigla_oficial}")
                    return True, None  # Processar mesmo sem horário definido
                
                # Calcular diferença em horas
                from datetime import timedelta
                agora = datetime.combine(hoje, horario_atual)
                sorteio = datetime.combine(hoje, horario_sorteio)
                
                if sorteio < agora:
                    # Sorteio já passou, pode processar
                    return True, None
                
                # Sorteio ainda não aconteceu
                diferenca = sorteio - agora
                horas_ate_sorteio = diferenca.total_seconds() / 3600
                
                if horas_ate_sorteio > 2:
                    # Mais de 2 horas até o sorteio - avisar mas processar
                    mensagem = f"⚠️ A edição se refere a {sigla_oficial} de {data_sorteio.strftime('%d/%m/%y')}, que só ocorrerá às {horario_sorteio.strftime('%H:%M')}. Seu relatório está sendo gerado. Aguarde."
                    return True, mensagem
                else:
                    # Menos de 2 horas - pode processar normalmente
                    return True, None
            
            # Data futura - sempre pode processar
            return True, None
            
        except Exception as e:
            logger.error(f"Erro ao validar horário: {e}")
            return True, None  # Em caso de erro, processar
    
    def verificar_proxima_edicao_valida(self, sigla_oficial, data_sorteio):
        """
        Verifica se a edição solicitada não pula a próxima edição válida
        Retorna: (edicao_valida, mensagem_erro)
        """
        try:
            hoje = datetime.now().date()
            logger.info(f"Verificando edição: sigla={sigla_oficial}, data_sorteio={data_sorteio}, hoje={hoje}")
            
            if data_sorteio < hoje:
                # Edições passadas sempre são válidas
                logger.info(f"Edição passada - permitindo processamento")
                return True, None
            
            # Para data atual e futuras, verificar se não pula próxima edição válida
            horario_atual = datetime.now().time()
            
            # Encontrar a próxima edição válida para hoje
            proxima_edicao_hoje = None
            proxima_sigla_hoje = None
            
            for sigla, horario in self.siglas_horarios.items():
                if horario > horario_atual:
                    if proxima_edicao_hoje is None or horario < self.siglas_horarios[proxima_sigla_hoje]:
                        proxima_edicao_hoje = horario
                        proxima_sigla_hoje = sigla
            
            logger.info(f"Próxima edição válida hoje: {proxima_sigla_hoje} às {proxima_edicao_hoje}")
            
            if proxima_edicao_hoje:
                # Se há uma próxima edição válida hoje, verificar se a edição solicitada não a pula
                horario_solicitado = self.obter_horario_sorteio(sigla_oficial)
                logger.info(f"Horário da sigla solicitada: {horario_solicitado}")
                
                if horario_solicitado and horario_solicitado > proxima_edicao_hoje:
                    # A edição solicitada pula a próxima edição válida - RECUSAR
                    if data_sorteio == hoje:
                        mensagem = f"❌ A edição se refere a {sigla_oficial} de hoje, ainda não há relatório disponível. Informe uma edição válida."
                    else:
                        mensagem = f"❌ A edição se refere a {sigla_oficial} de {data_sorteio.strftime('%d/%m/%y')}, ainda não há relatório disponível. Informe uma edição válida."
                    
                    logger.info(f"RECUSANDO: {mensagem}")
                    return False, mensagem
            else:
                logger.info("Não há próxima edição válida hoje - permitindo processamento")
            
            logger.info(f"Edição válida - permitindo processamento")
            return True, None
            
        except Exception as e:
            logger.error(f"Erro ao verificar próxima edição: {e}")
            return True, None  # Em caso de erro, permitir processamento
    
    async def process_request(self, request_data):
        """Processa solicitação recebida de outras aplicações"""
        try:
            # Extrair dados da solicitação
            edition_number = request_data.get('edicao')
            source_app = request_data.get('source_app', 'unknown')
            
            if not edition_number:
                logger.error("Número de edição não fornecido")
                return {"success": False, "error": "Número de edição não fornecido"}
            
            logger.info(f"Solicitação recebida de {source_app} para edição {edition_number}")
            
            # Verificar se é número de edição válido
            if self.is_edition_number(str(edition_number)):
                result = await self.handle_edition_request(edition_number)
                return result
            else:
                logger.error(f"Número de edição inválido: {edition_number}")
                return {"success": False, "error": "Número de edição inválido"}
                
        except Exception as e:
            logger.error(f"Erro ao processar solicitação: {e}")
            return {"success": False, "error": str(e)}
    
    def is_edition_number(self, text):
        """Verifica se o texto é um número de edição válido"""
        try:
            number = int(text)
            # Intervalo válido de edições (ajuste conforme necessário)
            return 5350 <= number <= 20000
        except ValueError:
            return False
    
    async def check_edition_in_database(self, edition_number):
        """Verifica se a edição existe no banco e retorna informações"""
        try:
            # Conectar ao banco
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Consultar a edição na tabela extracoes_cadastro
            sql = """
                SELECT edicao, sigla_oficial, data_sorteio 
                FROM extracoes_cadastro 
                WHERE edicao = %s
            """
            cursor.execute(sql, (edition_number,))
            result = cursor.fetchone()
            
            if result:
                # Formatar a data para o padrão dd/mm/yy
                data_sorteio = result['data_sorteio']
                if data_sorteio:
                    data_formatada = data_sorteio.strftime('%d/%m/%y')
                else:
                    data_formatada = "N/A"
                
                edition_info = {
                    'edicao': result['edicao'],
                    'sigla_oficial': result['sigla_oficial'],
                    'data_formatada': data_formatada,
                    'data_sorteio': data_sorteio
                }
                
                logger.info(f"Edição {edition_number} encontrada: {result['sigla_oficial']} - {data_formatada}")
                return edition_info
            else:
                logger.warning(f"Edição {edition_number} não encontrada no banco")
                return None
                
        except mysql.connector.Error as err:
            logger.error(f"Erro ao consultar banco: {err}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao consultar banco: {e}")
            return None
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
    async def handle_edition_request(self, edition_number):
        """Processa solicitação de edição com validações de horário"""
        try:
            logger.info(f"Processando edição {edition_number}")
            
            # Verificar se a edição existe no banco
            edition_info = await self.check_edition_in_database(edition_number)
            
            if not edition_info:
                logger.error(f"Edição {edition_number} não encontrada no sistema.")
                return {"success": False, "error": f"Edição {edition_number} não encontrada no sistema."}
            
            # Extrair sigla oficial da sigla completa
            sigla_completa = edition_info['sigla_oficial']
            sigla_oficial = self.extrair_sigla_oficial(sigla_completa)
            
            if not sigla_oficial:
                logger.error(f"Sigla não reconhecida: {sigla_completa}")
                return {"success": False, "error": f"Sigla não reconhecida: {sigla_completa}"}
            
            # Validar se não pula próxima edição válida
            edicao_valida, mensagem_erro = self.verificar_proxima_edicao_valida(sigla_oficial, edition_info['data_sorteio'])
            
            if not edicao_valida:
                logger.warning(f"Validação de edição falhou: {mensagem_erro}")
                return {"success": False, "error": mensagem_erro}
            
            # Validar horário da edição
            pode_processar, mensagem_aviso = self.validar_horario_edicao(sigla_oficial, edition_info['data_sorteio'])
            
            if not pode_processar:
                logger.warning("Edição não pode ser processada no momento.")
                return {"success": False, "error": "Edição não pode ser processada no momento."}
            
            # Log de processamento com informações da edição
            data_formatada = edition_info['data_formatada']
            logger.info(f"Gerando relatório edição {edition_number} - {sigla_oficial} - {data_formatada}")
            
            # Se há aviso de horário, incluir no log
            if mensagem_aviso:
                logger.warning(f"Aviso de horário: {mensagem_aviso}")
            
            # Executar script de relatório
            success, pdf_path = await self.execute_report_script(edition_number)
            
            if success and pdf_path:
                # Armazenar PDF localmente (não enviar via WhatsApp)
                logger.info(f"PDF gerado com sucesso: {pdf_path}")
                return {
                    "success": True, 
                    "message": f"Relatório gerado com sucesso para edição {edition_number}",
                    "pdf_path": pdf_path,
                    "edition_info": {
                        "sigla_oficial": edition_info['sigla_oficial'],
                        "data_formatada": edition_info['data_formatada']
                    }
                }
            else:
                logger.error("Erro ao gerar relatório.")
                return {"success": False, "error": "Erro ao gerar relatório. Verifique a edição ou contate o suporte."}
                
        except Exception as e:
            logger.error(f"Erro ao processar edição {edition_number}: {e}")
            return {"success": False, "error": "Erro interno. Tente novamente."}
    
    async def execute_report_script(self, edition_number):
        """Executa o script relatorio_v2_vps.py"""
        try:
            logger.info(f"Executando script para edição {edition_number}")
            
            # Comando para executar o script (funciona tanto local quanto Docker)
            script_path = os.path.join(os.getcwd(), "relatorio_v2_vps.py")
            cmd = [
                "python", 
                script_path, 
                str(edition_number)
            ]
            
            # Executar script usando subprocess.run (síncrono para Windows)
            import subprocess
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                # Procurar caminho do PDF no output
                output_lines = result.stdout.split('\n')
                
                pdf_path = None
                
                for line in output_lines:
                    if 'PDF gerado:' in line:
                        pdf_path = line.replace('PDF gerado:', '').strip()
                        break
                
                if pdf_path and os.path.exists(pdf_path):
                    logger.info(f"PDF gerado: {pdf_path}")
                    return True, pdf_path
                else:
                    logger.error("PDF não encontrado no output")
                    return False, None
            else:
                logger.error(f"Script falhou com código {result.returncode}")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                return False, None
                
        except Exception as e:
            logger.error(f"Erro ao executar script: {e}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            return False, None
    
    def cleanup_pdf(self, pdf_path):
        """Remove arquivo PDF temporário (não usado mais - PDFs ficam armazenados)"""
        try:
            if os.path.exists(pdf_path):
                # Não remover mais - PDFs ficam armazenados localmente
                logger.info(f"PDF mantido localmente: {pdf_path}")
        except Exception as e:
            logger.error(f"Erro ao processar PDF: {e}")

# Instanciar handler
webhook_handler = WebhookHandler()

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {"message": "Webhook Server - Servidor Ativo", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/webhook")
async def webhook_endpoint(request: Request):
    """Endpoint para receber solicitações de outras aplicações"""
    try:
        # Verificar secret (opcional)
        secret = request.headers.get('x-webhook-secret')
        if secret and secret != WEBHOOK_SECRET:
            logger.warning("Webhook secret inválido")
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        # Receber dados da solicitação
        request_data = await request.json()
        logger.info(f"Solicitação recebida: {request_data}")
        
        # Processar solicitação
        result = await webhook_handler.process_request(request_data)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/test")
async def test_endpoint():
    """Endpoint para testes"""
    return {"message": "Test endpoint working", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    logger.info("🚀 Iniciando servidor webhook...")
    logger.info(f"📡 Porta: {WEBHOOK_PORT}")
    logger.info(f"🔗 URL: http://0.0.0.0:{WEBHOOK_PORT}")
    
    uvicorn.run(
        "webhook_server:app",
        host="0.0.0.0",
        port=WEBHOOK_PORT,
        reload=False,
        log_level="info"
    ) 