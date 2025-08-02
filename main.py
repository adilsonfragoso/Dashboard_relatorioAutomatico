from fastapi import FastAPI, HTTPException, Body, UploadFile, File, Form, Query, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import sys
import subprocess
import logging
from pymysql.cursors import DictCursor
import pymysql
from datetime import datetime, timedelta
from dotenv import load_dotenv
import unidecode

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'connect_timeout': 10,
    'read_timeout': 30,
    'write_timeout': 30
}

app = FastAPI(title="Dashboard API", version="1.0.0")

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_dashboard():
    """Serve a página principal do dashboard"""
    return FileResponse("static/dashboard.html")

@app.get("/api/dashboard/extracoes-recentes")
def obter_extracoes_recentes():
    """
    Retorna apenas as extrações ATIVAS para exibir no dashboard
    - Filtra apenas rifas com status_rifa = 'ativo'
    - Remove rifas que atingiram 100% há mais de 11 horas do horário de fechamento
    - Independente da data
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(DictCursor)
        
        # Buscar todas as extrações ativas (sem filtro de data)
        cursor.execute("""
            SELECT 
                ec.id,
                ec.edicao,
                ec.sigla_oficial,
                ec.extracao,
                ec.link,
                ec.status_cadastro,
                ec.status_link,
                ec.error_msg,
                ec.andamento,
                ec.status_rifa,
                ec.data_sorteio,
                p.horario
            FROM extracoes_cadastro ec
            LEFT JOIN premiacoes p ON ec.extracao = p.sigla
            WHERE ec.status_rifa IN ('ativo', 'concluído', 'error')
            AND ec.link IS NOT NULL 
            AND ec.link != ''
            ORDER BY ec.edicao ASC
        """)
        
        extracoes_raw = cursor.fetchall()
        extracoes_validas = []
        agora = datetime.now()
        
        for extracao in extracoes_raw:
            andamento_raw = extracao['andamento'] if extracao and 'andamento' in extracao else None
            if andamento_raw and isinstance(andamento_raw, str) and andamento_raw.strip():
                extracao['andamento_percentual'] = andamento_raw
            else:
                extracao['andamento_percentual'] = '0%'
                
            tem_erro_x = extracao['andamento_percentual'] == 'X'
            percentual_str = extracao['andamento_percentual'].replace('%', '')
            
            try:
                if tem_erro_x:
                    extracao['andamento_numerico'] = 0
                else:
                    extracao['andamento_numerico'] = int(percentual_str)
            except:
                extracao['andamento_numerico'] = 0
                
            if (extracao.get('status_rifa') == 'error' if extracao else False) or tem_erro_x:
                extracao['deve_exibir'] = True
            elif extracao['andamento_numerico'] < 100 and (extracao.get('status_rifa') != 'concluído' if extracao else True):
                extracao['deve_exibir'] = True
            else:
                data_sorteio = extracao['data_sorteio'] if extracao and 'data_sorteio' in extracao else None
                horario_str = extracao['horario'] if extracao and 'horario' in extracao else None
                
                if horario_str and data_sorteio:
                    try:
                        if isinstance(data_sorteio, str):
                            data_obj = datetime.strptime(data_sorteio, '%Y-%m-%d')
                        else:
                            from datetime import date
                            if isinstance(data_sorteio, date):
                                data_obj = datetime.combine(data_sorteio, datetime.min.time())
                            else:
                                data_obj = data_sorteio
                                
                        horario_clean = horario_str.strip()
                        if 'AM' in horario_clean or 'PM' in horario_clean:
                            time_obj = datetime.strptime(horario_clean, '%I:%M %p')
                            hora = time_obj.hour
                            minuto = time_obj.minute
                        else:
                            horario_parts = horario_clean.split(':')
                            hora = int(horario_parts[0])
                            minuto = int(horario_parts[1]) if len(horario_parts) > 1 else 0
                            
                        fechamento = data_obj.replace(hour=hora, minute=minuto, second=0)
                        limite_exibicao = fechamento + timedelta(minutes=865)
                        extracao['deve_exibir'] = agora <= limite_exibicao
                    except Exception as e:
                        print(f"Erro ao processar horário para edição {extracao['edicao'] if extracao and 'edicao' in extracao else ''}: {e}")
                        extracao['deve_exibir'] = True
                else:
                    extracao['deve_exibir'] = False
                    
            if extracao['deve_exibir']:
                tem_erro_x = extracao['andamento_percentual'] == 'X'
                extracao['tem_erro'] = (extracao['status_cadastro'] == 'error' if extracao and 'status_cadastro' in extracao else False) or (extracao.get('status_rifa') == 'error' if extracao else False) or tem_erro_x
                extracao['status_rifa_atual'] = extracao.get('status_rifa', 'ativo') if extracao else 'ativo'
                
                cursor.execute("""
                    SELECT imagem_path 
                    FROM premiacoes 
                    WHERE sigla = %s 
                    LIMIT 1
                """, (extracao['extracao'] if extracao and 'extracao' in extracao else None,))
                
                premiacao = cursor.fetchone()
                if premiacao and 'imagem_path' in premiacao and premiacao['imagem_path']:
                    extracao['imagem_path'] = premiacao['imagem_path']
                else:
                    extracao['imagem_path'] = None
                    
                if extracao['andamento_numerico'] == 100:
                    titulo_simulado = f"{extracao['sigla_oficial']} RJ Edição {extracao['edicao']}" if extracao and 'sigla_oficial' in extracao and 'edicao' in extracao else ''
                    titulo_modificado = unidecode.unidecode(titulo_simulado.lower().replace(" ", "-"))
                    nome_arquivo = f"relatorio-vendas-{titulo_modificado}.pdf"
                    caminho_pdf = os.path.join(os.getcwd(), "downloads", nome_arquivo)
                    extracao['tem_pdf'] = os.path.exists(caminho_pdf)
                else:
                    extracao['tem_pdf'] = False
                    
                extracoes_validas.append(extracao)
                
        data_atual = datetime.now()
        dias_semana = {
            0: 'Segunda-feira',
            1: 'Terça-feira', 
            2: 'Quarta-feira',
            3: 'Quinta-feira',
            4: 'Sexta-feira',
            5: 'Sábado',
            6: 'Domingo'
        }
        dia_semana = dias_semana[data_atual.weekday()]
        data_formatada = f"{dia_semana}, {data_atual.strftime('%d/%m/%Y')}"
        
        cursor.close()
        connection.close()
        
        return {
            "data_recente": data_formatada,
            "data_sorteio": data_atual.strftime('%Y-%m-%d'),
            "extracoes": extracoes_validas,
            "total_ativas": len(extracoes_validas)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar extrações ativas: {str(e)}")

@app.post("/api/dashboard/enviar-link-edicao/{edicao}")
def enviar_link_edicao(edicao: int):
    """
    Envia o link de uma edição específica via WhatsApp
    """
    try:
        # Buscar informações da edição
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(DictCursor)
        
        cursor.execute("""
            SELECT 
                id,
                edicao,
                sigla_oficial,
                extracao,
                link
            FROM extracoes_cadastro 
            WHERE edicao = %s
            LIMIT 1
        """, (edicao,))
        
        extracao = cursor.fetchone()
        
        if not extracao:
            raise HTTPException(status_code=404, detail=f"Edição {edicao} não encontrada")
        
        # Buscar imagem da premiação
        cursor.execute("""
            SELECT imagem_path 
            FROM premiacoes 
            WHERE sigla = %s 
            LIMIT 1
        """, (extracao['extracao'],))
        premiacao = cursor.fetchone()
        if premiacao and premiacao['imagem_path']:
            extracao['imagem_path'] = premiacao['imagem_path']
        else:
            extracao['imagem_path'] = None
        
        cursor.close()
        connection.close()
        
        # Executar o script de envio para esta edição específica
        script_path = os.path.join("scripts", "novo_chamadas_group_latest.py")
        
        if not os.path.exists(script_path):
            raise HTTPException(status_code=404, detail="Script de envio não encontrado")
        
        # Executar script com a edição específica
        resultado = subprocess.run(
            [sys.executable, script_path, str(edicao)],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60,  # 1 minuto timeout
            env=os.environ.copy()
        )
        
        if resultado.returncode == 0:
            return {
                "success": True,
                "message": f"Link da edição {edicao} enviado com sucesso",
                "edicao": edicao,
                "output": resultado.stdout
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar link: {resultado.stderr}"
            )
            
    except HTTPException:
        raise
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Timeout ao enviar link (1 minuto)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

@app.post("/api/dashboard/gerar-relatorio/{edicao}")
def gerar_relatorio(edicao: int):
    """Endpoint para gerar relatório PDF de uma edição que atingiu 100%"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(DictCursor)
        cursor.execute("""
            SELECT andamento, sigla_oficial 
            FROM extracoes_cadastro 
            WHERE edicao = %s
        """, (edicao,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        andamento = result['andamento'] if result and 'andamento' in result else None
        if not result or not andamento or andamento.strip() != '100%':
            raise HTTPException(status_code=400, detail="Relatório só pode ser gerado para rifas 100% vendidas")
            
        script_path = "relatorio_v2_vps.py"
        if not os.path.exists(script_path):
            raise HTTPException(status_code=404, detail="Script de relatório não encontrado")
            
        logger.info(f"Iniciando geração de relatório para edição {edicao}")
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result_proc = subprocess.run(
            [sys.executable, script_path, str(edicao)],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300,  # 5 minutos timeout
            env=env
        )
        
        if result_proc.returncode == 0:
            logger.info(f"Relatório gerado com sucesso para edição {edicao}")
            return {
                "success": True,
                "message": f"Relatório para edição {edicao} gerado com sucesso",
                "edicao": edicao,
                "output": result_proc.stdout
            }
        else:
            logger.error(f"Erro ao gerar relatório para edição {edicao}: {result_proc.stderr}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao gerar relatório: {result_proc.stderr}"
            )
    except HTTPException:
        raise
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout ao gerar relatório para edição {edicao}")
        raise HTTPException(status_code=500, detail="Timeout ao gerar relatório (5 minutos)")
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar relatório: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

@app.get("/api/dashboard/verificar-pdf/{edicao}")
def verificar_pdf(edicao: int):
    """Verifica se o PDF da edição existe"""
    try:
        # Buscar título da edição no banco para montar nome do arquivo
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(DictCursor)
        
        cursor.execute("""
            SELECT sigla_oficial 
            FROM extracoes_cadastro 
            WHERE edicao = %s
        """, (edicao,))
        
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not result:
            return {"existe": False, "nome_arquivo": None}
        
        sigla = result['sigla_oficial']
        
        # Simular o padrão de nome que o script cria
        # Por exemplo: relatorio-vendas-ppt-rj-edicao-6197.pdf
        titulo_simulado = f"{sigla} RJ Edição {edicao}"
        titulo_modificado = unidecode.unidecode(titulo_simulado.lower().replace(" ", "-"))
        nome_arquivo = f"relatorio-vendas-{titulo_modificado}.pdf"
        
        # Verificar se existe no diretório de downloads
        caminho_pdf = os.path.join(os.getcwd(), "downloads", nome_arquivo)
        existe = os.path.exists(caminho_pdf)
        
        return {
            "existe": existe,
            "nome_arquivo": nome_arquivo if existe else None,
            "caminho": caminho_pdf if existe else None
        }
        
    except Exception as e:
        logger.error(f"Erro ao verificar PDF: {e}")
        return {"existe": False, "nome_arquivo": None}

@app.get("/api/dashboard/download-pdf/{edicao}")
def download_pdf(edicao: int):
    """Download do PDF da edição"""
    try:
        # Verificar se o PDF existe
        verificacao = verificar_pdf(edicao)
        
        if not verificacao["existe"]:
            raise HTTPException(status_code=404, detail="PDF não encontrado")
        
        caminho_pdf = verificacao["caminho"]
        nome_arquivo = verificacao["nome_arquivo"]
        
        # Retornar o arquivo para download
        return FileResponse(
            path=caminho_pdf,
            filename=nome_arquivo,
            media_type='application/pdf'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao fazer download do PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/dashboard/status-monitor-andamento")
def obter_status_monitor_andamento():
    """
    Obtém status do servidor de monitoramento de andamento baseado na tabela logs_andamento
    """
    ativo = False  # Initialize ativo to prevent potential UnboundLocalError
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(DictCursor)

        # Buscar último log de sucesso
        cursor.execute("""
            SELECT data_hora, log_status
            FROM logs_andamento
            WHERE log_status = 'success'
            ORDER BY data_hora DESC
            LIMIT 1
        """)

        resultado = cursor.fetchone()
        cursor.close()
        connection.close()

        if not resultado:
            return {
                "ativo": False,
                "motivo": "Nenhum log de sucesso encontrado",
                "ultima_atualizacao": None,
                "minutos_desde_ultima": None
            }

        # Calcular diferença de tempo
        # Configurar timezone local (America/Sao_Paulo)
        import pytz
        tz_local = pytz.timezone('America/Sao_Paulo')
        
        agora = datetime.now(tz_local)
        ultima_atualizacao = resultado['data_hora']

        # Se data_hora for string, converter para datetime
        if isinstance(ultima_atualizacao, str):
            ultima_atualizacao = datetime.strptime(ultima_atualizacao, '%Y-%m-%d %H:%M:%S')
        
        # Garantir que ambos os datetime tenham timezone info
        # Se ultima_atualizacao não tem timezone, assumir que é local
        if ultima_atualizacao.tzinfo is None:
            ultima_atualizacao = tz_local.localize(ultima_atualizacao)
        
        # Se agora não tem timezone, adicionar timezone local
        if agora.tzinfo is None:
            agora = tz_local.localize(agora)

        diferenca = agora - ultima_atualizacao
        minutos_desde_ultima = diferenca.total_seconds() / 60

        # Servidor ativo se última atualização foi há 5 minutos ou menos
        ativo = minutos_desde_ultima <= 5

        # Log para debug com timezone info
        logger.info(f"Status MonitorAndamento - Agora: {agora} (tz: {agora.tzinfo}), Última: {ultima_atualizacao} (tz: {ultima_atualizacao.tzinfo}), Diferença: {minutos_desde_ultima:.1f} min, Ativo: {ativo}")

        # Log adicional para debug
        logger.info(f"Status final - Ativo: {ativo}, Minutos: {minutos_desde_ultima:.1f}")

        return {
            "ativo": ativo,
            "ultima_atualizacao": ultima_atualizacao.isoformat(),
            "ultima_atualizacao_formatada": ultima_atualizacao.strftime('%H:%M:%S'),
            "minutos_desde_ultima": round(minutos_desde_ultima, 1),
            "log_status": resultado['log_status']
        }

    except Exception as e:
        logger.error(f"Erro ao obter status do MonitorAndamento: {e}")
        return {
            "ativo": False,
            "motivo": f"Erro: {str(e)}",
            "ultima_atualizacao": None,
            "minutos_desde_ultima": None
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010) 