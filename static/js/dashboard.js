// Variáveis globais
let rifasData = [];
let modalEdicaoAtual = null;
let rifasProcessando = new Set(); // Controla quais rifas estão sendo processadas
let ultimaAtualizacaoDados = null; // Timestamp da última atualização dos dados
let verificandoAtualizacoes = false; // Flag para evitar múltiplas verificações simultâneas

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar rodapé
    atualizarStatusRodape('sincronizando', 'Carregando dados iniciais...');
    
    // Verificar status da Heroku inicialmente
    setTimeout(() => {
        verificarStatusHeroku();
    }, 1000); // Aguardar 1 segundo para garantir que a página carregou

    carregarDados(true); // Primeira carga
    iniciarAtualizacaoAutomatica();
    configurarModal();
});

// Configurar modal
function configurarModal() {
    const modal = document.getElementById('acoes-modal');
    const span = document.getElementsByClassName('close')[0];

    span.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
}

// Atualização automática inteligente
function iniciarAtualizacaoAutomatica() {
    // Verificação inteligente de atualizações a cada 15 segundos
    setInterval(() => {
        verificarSeHouveMudancas();
    }, 15000); // 15 segundos - mais frequente para detectar mudanças

    // Verificação do status da Heroku a cada 30 segundos
    setInterval(() => {
        verificarStatusHeroku();
    }, 30000); // 30 segundos

    // Atualização completa a cada 1 minuto (fallback)
    setInterval(() => {
        console.log('[AUTO] Atualização completa programada...');
        // Não atualizar rodapé nas atualizações automáticas programadas
        // O rodapé só será atualizado se houver mudanças detectadas
        carregarDados(false, false); // Não é primeira carga, sem forçar atualização do rodapé
    }, 60000); // 1 minuto
}

// NOVA FUNÇÃO: Verificar se houve mudanças nos dados
async function verificarSeHouveMudancas() {
    if (verificandoAtualizacoes) {
        return; // Evitar múltiplas verificações simultâneas
    }

    try {
        verificandoAtualizacoes = true;
        
        // Fazer uma verificação rápida apenas dos metadados
        const response = await fetch('/api/dashboard/extracoes-recentes');
        const data = await response.json();
        
        if (!response.ok) {
            return; // Ignorar erros na verificação rápida
        }
        
        // Verificar se algo mudou comparando com os dados atuais
        const mudancaDetectada = detectarMudancasNosDados(data.extracoes);
        
        if (mudancaDetectada) {
            console.log('[SYNC] 🔄 Mudanças detectadas! Atualizando dashboard...');
            atualizarStatusRodape('sincronizando', 'Sincronizando dados...');
            
            // Atualizar dados imediatamente (sem loading overlay)
            await carregarDados(false, true); // Segundo parâmetro indica que houve mudanças
            
            // Destacar que houve atualização
            destacarAtualizacaoGeral();
        } else {
            console.log('[SYNC] ✓ Nenhuma mudança detectada');
        }
        
    } catch (error) {
        console.log('[SYNC] ⚠️ Erro na verificação de mudanças:', error);
    } finally {
        verificandoAtualizacoes = false;
    }
}

// NOVA FUNÇÃO: Verificar status da Heroku baseado na tabela logs_andamento
async function verificarStatusHeroku() {
    try {
        const response = await fetch('/api/dashboard/status-heroku');
        if (!response.ok) {
            console.log('[HEROKU] Erro ao verificar status');
            atualizarIndicadorServidor('offline', 'Erro ao verificar status');
            return;
        }

        const data = await response.json();

        if (data.ativo) {
            console.log(`[HEROKU] Status: Ativo (${data.minutos_desde_ultima} min atrás)`);
            atualizarIndicadorServidor('online', `Última atualização: ${data.ultima_atualizacao_formatada}`);
            atualizarUltimaAtualizacaoHeroku(data.ultima_atualizacao_formatada);
        } else {
            console.log(`[HEROKU] Status: Inativo (${data.minutos_desde_ultima || 'N/A'} min atrás)`);
            atualizarIndicadorServidor('offline', data.motivo || 'Sem atualizações recentes');
            if (data.ultima_atualizacao_formatada) {
                atualizarUltimaAtualizacaoHeroku(data.ultima_atualizacao_formatada);
            }
        }
    } catch (error) {
        console.log('[HEROKU] ⚠️ Erro ao verificar status:', error);
        atualizarIndicadorServidor('offline', 'Erro de conexão');
    }
}

// NOVA FUNÇÃO: Atualizar indicador visual do servidor
function atualizarIndicadorServidor(status, mensagem) {
    const indicator = document.getElementById('status-agendador');
    const dot = indicator.querySelector('.status-dot');
    const text = indicator.querySelector('.status-text');

    // Remover classes anteriores
    dot.classList.remove('status-online', 'status-offline');
    indicator.classList.remove('online', 'offline');

    if (status === 'online') {
        dot.classList.add('status-online');
        indicator.classList.add('online');
        text.textContent = 'Servidor Ativo';
        indicator.title = mensagem;
    } else {
        dot.classList.add('status-offline');
        indicator.classList.add('offline');
        text.textContent = 'Servidor Parado';
        indicator.title = mensagem;
    }
}

// NOVA FUNÇÃO: Atualizar última atualização com dados da Heroku
function atualizarUltimaAtualizacaoHeroku(horaFormatada) {
    const elementoUltimaAtualizacao = document.getElementById('texto-ultima-atualizacao');
    if (elementoUltimaAtualizacao && horaFormatada) {
        elementoUltimaAtualizacao.textContent = `Última atualização: ${horaFormatada}`;
        console.log(`[HEROKU] Horário atualizado: ${horaFormatada}`);
    } else {
        console.log('[HEROKU] ⚠️ Elemento texto-ultima-atualizacao não encontrado');
    }
}

// NOVA FUNÇÃO: Detectar mudanças comparando dados atuais com novos
function detectarMudancasNosDados(novosDados) {
    if (!rifasData || rifasData.length === 0) {
        return true; // Primeira carga
    }
    
    if (novosDados.length !== rifasData.length) {
        return true; // Quantidade de rifas mudou
    }
    
    // Comparar andamentos e status de cada rifa
    for (let i = 0; i < novosDados.length; i++) {
        const novaRifa = novosDados[i];
        const rifaAtual = rifasData.find(r => r.edicao === novaRifa.edicao);
        
        if (!rifaAtual) {
            return true; // Nova rifa
        }
        
        // Verificar mudanças nos campos importantes
        if (novaRifa.andamento_percentual !== rifaAtual.andamento_percentual ||
            novaRifa.andamento_numerico !== rifaAtual.andamento_numerico ||
            novaRifa.status_rifa !== rifaAtual.status_rifa ||
            novaRifa.tem_pdf !== rifaAtual.tem_pdf ||
            novaRifa.tem_erro !== rifaAtual.tem_erro) {
            
            console.log(`[SYNC] Mudança detectada na edição ${novaRifa.edicao}:`);
            console.log(`  Andamento: ${rifaAtual.andamento_percentual} → ${novaRifa.andamento_percentual}`);
            console.log(`  Status: ${rifaAtual.status_rifa} → ${novaRifa.status_rifa}`);
            console.log(`  PDF: ${rifaAtual.tem_pdf} → ${novaRifa.tem_pdf}`);
            
            return true;
        }
    }
    
    return false; // Nenhuma mudança significativa
}

// NOVA FUNÇÃO: Destacar que houve atualização geral
function destacarAtualizacaoGeral() {
    const tabela = document.getElementById('rifas-table');
    if (tabela) {
        // Efeito visual de atualização
        tabela.style.transform = 'scale(0.98)';
        tabela.style.transition = 'transform 0.3s ease';
        
        setTimeout(() => {
            tabela.style.transform = 'scale(1)';
            
            setTimeout(() => {
                tabela.style.transform = '';
                tabela.style.transition = '';
            }, 300);
        }, 100);
    }
}

// Carregar dados da API
async function carregarDados(isFirstLoad = false, houveMudancas = false) {
    try {
        // Mostrar loading apropriado
        if (isFirstLoad || !rifasData || rifasData.length === 0) {
            // Primeira carga - loading overlay completo
            mostrarLoadingOverlay('Carregando dados...');
        } else {
            // Atualização - loading compacto
            mostrarLoadingCompacto('Sincronizando...');
        }

        const response = await fetch('/api/dashboard/extracoes-recentes');
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Erro ao carregar dados');
        }

        // Detectar mudanças reais nos dados
        const dadosAtuaisMudaram = rifasData ? detectarMudancasNosDados(data.extracoes) : true;

        // Atualizar status do sistema
        document.getElementById('status-sistema').textContent = `${data.total_ativas} rifas ativas`;
        rifasData = data.extracoes;
        
        preencherTabela(data.extracoes);
        
        // Verificar se há PDFs disponíveis na pasta (sem gerar automaticamente)
        verificarPDFsDisponiveis(data.extracoes);
        
        // Atualizar rodapé APENAS se:
        // 1. É primeira carga (isFirstLoad)
        // 2. Foi forçado por notificação do agendador (houveMudancas)
        // 3. Houve mudanças reais nos dados (dadosAtuaisMudaram)
        if (isFirstLoad || houveMudancas || dadosAtuaisMudaram) {
            // Atualização da Heroku será feita pelo timer separado
            atualizarStatusRodape('atualizado', 'Dados atualizados');
            console.log('[SYNC] Rodapé atualizado - houve mudanças nos dados');
        } else {
            // Se não houve mudanças, apenas manter o status atual
            console.log('[SYNC] Dados carregados sem mudanças - rodapé mantido');
        }
        
        // Ocultar loading
        ocultarTodosLoadings();
        document.getElementById('rifas-table').style.display = 'table';
        
    } catch (error) {
        console.error('Erro:', error);
        ocultarTodosLoadings();
        mostrarErro(`Erro ao carregar dados: ${error.message}`);
    }
}

// Preencher tabela agrupada por data
function preencherTabela(extracoes) {
    const tableBody = document.getElementById('table-body');
    const dataDisplay = document.getElementById('data-rifas');
    tableBody.innerHTML = '';

    if (extracoes.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="3" style="padding: 30px; color: #666;">
                    Nenhuma extração encontrada para esta data
                </td>
            </tr>
        `;
        dataDisplay.style.display = 'none';
        return;
    }

    // Agrupar extrações por data
    const extracoesPorData = {};
    extracoes.forEach(extracao => {
        const dataKey = extracao.data_sorteio;
        if (!extracoesPorData[dataKey]) {
            extracoesPorData[dataKey] = [];
        }
        extracoesPorData[dataKey].push(extracao);
    });

    // Ordenar as datas
    const datasOrdenadas = Object.keys(extracoesPorData).sort();

    // Função para formatar data
    function formatarData(dataString) {
        const data = new Date(dataString + 'T00:00:00');
        const diasSemana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
        const diaSemana = diasSemana[data.getDay()];
        const dataFormatada = data.toLocaleDateString('pt-BR');
        return `${diaSemana}, ${dataFormatada}`;
    }

    // SEMPRE mostrar a data principal acima da tabela
    if (datasOrdenadas.length === 1) {
        // Uma única data
        dataDisplay.innerHTML = `📅 ${formatarData(datasOrdenadas[0])}`;
    } else {
        // Múltiplas datas - mostrar a primeira data como principal
        dataDisplay.innerHTML = `📅 ${formatarData(datasOrdenadas[0])} `;
    }
    dataDisplay.style.display = 'flex';
    
    // Renderizar todas as extrações com separadores quando há múltiplas datas
    if (datasOrdenadas.length === 1) {
        // Uma única data - renderizar sem separadores
        const todasExtracoes = extracoesPorData[datasOrdenadas[0]];
        todasExtracoes.forEach(extracao => {
            adicionarLinhaExtracao(tableBody, extracao);
        });
    } else {
        // Múltiplas datas - usar separadores dentro da tabela também
        datasOrdenadas.forEach((dataKey, indexData) => {
            const extracoesDaData = extracoesPorData[dataKey];
            
            // Criar linha separadora com a data (exceto para a primeira, que já está acima)
            if (indexData > 0) {
                const separadorRow = document.createElement('tr');
                separadorRow.className = 'data-separator';
                separadorRow.innerHTML = `
                    <td colspan="3" class="data-header">
                        <div class="data-title">
                            📅 ${formatarData(dataKey)}
                        </div>
                    </td>
                `;
                tableBody.appendChild(separadorRow);
            }

            // Renderizar extrações desta data
            extracoesDaData.forEach(extracao => {
                adicionarLinhaExtracao(tableBody, extracao);
            });
        });
    }
}

// Função auxiliar para adicionar linha de extração
function adicionarLinhaExtracao(tableBody, extracao) {
    const row = document.createElement('tr');
    
    // Se tem erro, destacar a linha
    if (extracao.tem_erro) {
        row.style.background = '#fff3cd';
        row.style.borderLeft = '5px solid #ffc107';
    }

    // Determinar classe do status e conteúdo
    let statusClass = 'status-0';
    let statusContent = extracao.andamento_percentual;
    
    if (extracao.andamento_percentual === 'X') {
        // Andamento "X" = erro de link - mostrar em vermelho
        statusClass = 'status-error';
        statusContent = 'X';
    } else if (extracao.tem_erro) {
        statusClass = 'status-error';
        statusContent = `<img src="/static/img/naodisponivel.png" alt="Não encontrado" style="width: 32px; height: 32px; object-fit: contain;">`;
    } else if (extracao.andamento_numerico === 100) {
        statusClass = 'status-100';
    } else if (extracao.andamento_numerico > 0) {
        statusClass = 'status-progresso';
    }

    row.innerHTML = `
        <td class="edicao-cell" onclick="abrirModal('${extracao.edicao}', '${extracao.sigla_oficial}', '${extracao.link || ''}')">
            ${extracao.edicao} - ${extracao.sigla_oficial}
        </td>
        <td class="status-cell">
            <div class="status-badge ${statusClass}">
                ${statusContent}
            </div>
        </td>
        <td class="pdf-cell">
            ${renderizarIconePDF(extracao)}
        </td>
    `;

    tableBody.appendChild(row);
}

// Abrir modal com ações
function abrirModal(edicao, sigla, link) {
    // Validação extra para evitar erro 404
    console.log('abrirModal chamada com:', { edicao, sigla, link });
    
    // Garantir que link não seja undefined como string
    if (link === 'undefined' || link === 'null' || link === undefined || link === null) {
        link = '';
        console.log('Link inválido detectado, definindo como string vazia');
    }
    const rifa = rifasData.find(r => r.edicao == edicao);
    if (!rifa) return;

    modalEdicaoAtual = edicao;
    
    // Atualizar título do modal
    document.getElementById('modal-title').textContent = 
        `${edicao} - ${sigla}`;
    
    // Configurar botão WhatsApp com indicação de status
    const btnWhatsapp = document.getElementById('btn-whatsapp');
    btnWhatsapp.onclick = () => enviarWhatsApp(edicao);
    
    // Verificar status de envio e atualizar visual do botão
    const statusEnvio = rifa.status_envio_link || 'pendente';
    if (statusEnvio === 'enviado') {
        btnWhatsapp.innerHTML = `
            <img src="/static/img/option3.png" alt="WhatsApp" style="width: 24px; height: 24px; filter: brightness(0) invert(1);">
            ✅ Enviado (Reenviar)
        `;
        btnWhatsapp.style.background = 'linear-gradient(135deg, #28a745 0%, #1e7e34 100%)';
        btnWhatsapp.title = 'Link já foi enviado. Clique para reenviar.';
    } else {
        btnWhatsapp.innerHTML = `
            <img src="/static/img/option3.png" alt="WhatsApp" style="width: 24px; height: 24px; filter: brightness(0) invert(1);">
            Enviar WhatsApp
        `;
        btnWhatsapp.style.background = 'linear-gradient(135deg, #25d366 0%, #1ea952 100%)';
        btnWhatsapp.title = 'Enviar link via WhatsApp';
    }
    
    // Configurar botão Link
    if (link && link !== 'undefined' && link !== 'null') {
        document.getElementById('btn-link').href = link;
        document.getElementById('btn-link').style.display = 'inline-block';
    } else {
        document.getElementById('btn-link').href = '#';
        document.getElementById('btn-link').style.display = 'none';
        document.getElementById('btn-link').title = 'Link não disponível';
    }
    
    // Mostrar modal
    document.getElementById('acoes-modal').style.display = 'block';
}

// Enviar WhatsApp
async function enviarWhatsApp(edicao) {
    try {
        const rifa = rifasData.find(r => r.edicao == edicao);
        const statusAnterior = rifa ? rifa.status_envio_link || 'pendente' : 'pendente';
        
        if (statusAnterior === 'enviado') {
            atualizarStatusRodape('sincronizando', `Reenviando link da edição ${edicao}...`);
        } else {
            atualizarStatusRodape('sincronizando', `Enviando link da edição ${edicao}...`);
        }
        
        document.getElementById('acoes-modal').style.display = 'none';
        
        const response = await fetch(`/api/dashboard/enviar-link-edicao/${edicao}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok) {
            if (statusAnterior === 'enviado') {
                atualizarStatusRodape('atualizado', `Link reenviado para edição ${edicao}!`);
            } else {
                atualizarStatusRodape('atualizado', `Link enviado para edição ${edicao}!`);
            }
            
            // Atualizar dados após envio para refletir mudança no status
            setTimeout(() => {
                carregarDados();
            }, 1000);
        } else {
            mostrarErro(`Erro ao enviar link: ${data.detail}`);
        }
        
    } catch (error) {
        mostrarErro('Erro de conexão: ' + error.message);
    }
}

// Baixar PDF (apenas verificar se existe na pasta downloads)
async function baixarPDF(edicao) {
    try {
        console.log(`[PDF] Verificando PDF para edição ${edicao}`);
        
        // Verificar se o PDF existe na pasta downloads
        const verificacao = await fetch(`/api/dashboard/verificar-pdf/${edicao}`);
        const dadosVerificacao = await verificacao.json();
        
        console.log(`[PDF] Verificação para edição ${edicao}:`, dadosVerificacao);
        
        if (dadosVerificacao.existe) {
            // PDF existe, fazer download
            console.log(`[PDF] Iniciando download via window.open para edição ${edicao}`);
            window.open(`/api/dashboard/download-pdf/${edicao}`, '_blank');
            atualizarStatusRodape('atualizado', `📄 Download da edição ${edicao} iniciado!`);
        } else {
            // PDF não existe - informar que será gerado pelo script externo
            mostrarErro(`PDF da edição ${edicao} ainda não foi gerado. Aguarde o processamento automático.`);
        }
        
    } catch (error) {
        mostrarErro('Erro de conexão: ' + error.message);
    }
}

// Função removida: Monitoramento de PDF
// Agora o dashboard apenas verifica se PDFs existem na pasta downloads
// Não monitora mais a geração, pois isso é responsabilidade do script externo

// NOVA FUNÇÃO: Destacar visualmente relatório recém-disponível
function destacarRelatorioNovo(edicao) {
    // Encontrar a linha da edição na tabela
    const linhas = document.querySelectorAll('#table-body tr');
    
    linhas.forEach(linha => {
        const celulaEdicao = linha.querySelector('.edicao-cell');
        if (celulaEdicao && celulaEdicao.textContent.includes(edicao)) {
            // Adicionar destaque visual temporário
            linha.style.background = 'linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)';
            linha.style.border = '2px solid #28a745';
            linha.style.transform = 'scale(1.02)';
            linha.style.transition = 'all 0.3s ease';
            
            // Scroll suave até a linha
            linha.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Remover destaque após 5 segundos
            setTimeout(() => {
                linha.style.background = '';
                linha.style.border = '';
                linha.style.transform = '';
            }, 5000);
            
            // Piscar o ícone PDF brevemente
            const iconePdf = linha.querySelector('.pdf-icon');
            if (iconePdf) {
                iconePdf.style.animation = 'pulse 0.5s ease-in-out 3';
            }
        }
    });
}

// Função removida: Geração automática de relatórios
// Agora o dashboard apenas verifica se PDFs existem na pasta downloads
// A geração é responsabilidade do webhook_server.py que recebe notificações do script externo

// Mostrar mensagem de erro
function mostrarErro(mensagem) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = mensagem;
    errorDiv.style.display = 'block';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Atualizar status no rodapé
function atualizarStatusRodape(tipo, mensagem) {
    const statusDiv = document.getElementById('status-atualizacao');
    const textoStatus = document.getElementById('texto-status-atualizacao');
    
    // Remover classes anteriores
    statusDiv.classList.remove('status-atualizado', 'status-sincronizando', 'status-offline');
    
    if (tipo === 'sincronizando') {
        statusDiv.classList.add('status-sincronizando');
        statusDiv.innerHTML = `<span>⏳</span><span>${mensagem}</span>`;
    } else if (tipo === 'offline') {
        statusDiv.classList.add('status-offline');
        statusDiv.innerHTML = `<span>⚠️</span><span>${mensagem}</span>`;
    } else {
        statusDiv.classList.add('status-atualizado');
        statusDiv.innerHTML = `<span>✅</span><span>${mensagem}</span>`;
        
        // Voltar ao estado normal após 3 segundos
        setTimeout(() => {
            statusDiv.innerHTML = `<span>✅</span><span>Dados atualizados</span>`;
        }, 3000);
    }
}

// Nova função para renderizar o ícone PDF com estado de processamento
function renderizarIconePDF(extracao) {
    const edicao = extracao.edicao;
    
    // Estado 1: PDF já disponível
    if (extracao.tem_pdf) {
        return `<img src="/static/img/pdf-download.svg" 
                     alt="PDF ${edicao}" 
                     class="pdf-icon" 
                     onclick="baixarPDF('${edicao}')"
                     title="Clique para baixar PDF da edição ${edicao}">`;
    }
    
    // Estado 2: Processando (rifa 100% sendo processada)
    if (rifasProcessando.has(edicao)) {
        return `<div class="pdf-loading" 
                     alt="Gerando PDF ${edicao}" 
                     title="Processando relatório...">
                </div>`;
    }
    
    // Estado 3: Não disponível (padrão)
    return `<img src="/static/img/pdf-unavailable.svg" 
                 alt="PDF não disponível" 
                 class="pdf-icon disabled" 
                 title="PDF não disponível para esta edição">`;
}

// Função para marcar rifa como processando
function marcarComoProcessando(edicao) {
    rifasProcessando.add(edicao);
    console.log(`[PROCESSING] Edição ${edicao} marcada como processando`);
    // Atualizar apenas esta linha na tabela
    atualizarIconePDF(edicao);
}

// Função para desmarcar rifa como processando
function desmarcarProcessamento(edicao) {
    rifasProcessando.delete(edicao);
    console.log(`[PROCESSING] Edição ${edicao} processamento finalizado`);
    // Será atualizada quando carregarDados() for chamado
}

// Função para atualizar apenas o ícone PDF de uma edição específica
function atualizarIconePDF(edicao) {
    const linhas = document.querySelectorAll('#table-body tr');
    
    linhas.forEach(linha => {
        const celulaEdicao = linha.querySelector('.edicao-cell');
        if (celulaEdicao && celulaEdicao.textContent.includes(edicao)) {
            const celulaPdf = linha.querySelector('.pdf-cell');
            if (celulaPdf) {
                // Encontrar a rifa nos dados para renderizar corretamente
                const rifa = rifasData.find(r => r.edicao == edicao);
                if (rifa) {
                    celulaPdf.innerHTML = renderizarIconePDF(rifa);
                }
            }
        }
    });
}

// Verificar se há PDFs disponíveis na pasta (sem gerar automaticamente)
function verificarPDFsDisponiveis(extracoes) {
    const rifas100SemPdf = extracoes.filter(e => e.andamento_numerico === 100 && !e.tem_pdf);
    
    if (rifas100SemPdf.length > 0) {
        console.log(`[DASHBOARD] ${rifas100SemPdf.length} rifa(s) 100% - verificando PDFs na pasta...`);
        
        // Verificar cada PDF individualmente (sem gerar)
        rifas100SemPdf.forEach(extracao => {
            verificarPDFExistente(extracao.edicao);
        });
    }
}

// Verificar se PDF existe na pasta downloads
async function verificarPDFExistente(edicao) {
    try {
        const response = await fetch(`/api/dashboard/verificar-pdf/${edicao}`);
        const data = await response.json();
        
        if (data.existe) {
            console.log(`[DASHBOARD] ✅ PDF encontrado para edição ${edicao} na pasta downloads`);
            // Atualizar apenas esta linha na tabela
            atualizarIconePDF(edicao);
        } else {
            console.log(`[DASHBOARD] ⏳ PDF ainda não disponível para edição ${edicao}`);
        }
    } catch (error) {
        console.log(`[DASHBOARD] ⚠️ Erro ao verificar PDF da edição ${edicao}:`, error);
    }
}

// Funções para controlar loading sem afetar layout
function mostrarLoadingOverlay(texto = 'Carregando...') {
    const overlay = document.getElementById('loading-overlay');
    const textElement = overlay.querySelector('.loading-text');
    textElement.textContent = texto;
    overlay.style.display = 'flex';
}

function mostrarLoadingCompacto(texto = 'Sincronizando...') {
    const compact = document.getElementById('loading-compact');
    const textElement = compact.querySelector('.loading-text');
    textElement.textContent = texto;
    compact.style.display = 'flex';
}

function ocultarLoadingOverlay() {
    document.getElementById('loading-overlay').style.display = 'none';
}

function ocultarLoadingCompacto() {
    document.getElementById('loading-compact').style.display = 'none';
}

function ocultarTodosLoadings() {
    ocultarLoadingOverlay();
    ocultarLoadingCompacto();
} 