#!/bin/bash

# Script de Setup para Dashboard
echo "🚀 Configurando Dashboard de Gerenciamento de Rifas..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp env.example .env
    echo "✅ Arquivo .env criado. Por favor, edite-o com suas configurações de banco de dados."
else
    echo "✅ Arquivo .env já existe."
fi

# Criar pastas necessárias
echo "📁 Criando pastas necessárias..."
mkdir -p static/img static/css static/js scripts downloads

# Verificar se as imagens necessárias existem
echo "🖼️ Verificando imagens necessárias..."
required_images=("static/img/iconepdf.jpg" "static/img/naodisponivel.png" "static/img/option3.png" "static/img/favicon.ico")

for img in "${required_images[@]}"; do
    if [ ! -f "$img" ]; then
        echo "⚠️ Imagem não encontrada: $img"
        echo "   Por favor, adicione esta imagem antes de executar a aplicação."
    else
        echo "✅ $img encontrada"
    fi
done

# Verificar se os scripts necessários existem
echo "📜 Verificando scripts necessários..."
required_scripts=("scripts/novo_chamadas_group_latest.py" "scripts/relatorio_v1.py")

for script in "${required_scripts[@]}"; do
    if [ ! -f "$script" ]; then
        echo "⚠️ Script não encontrado: $script"
        echo "   Este script é opcional, mas pode ser necessário para funcionalidades completas."
    else
        echo "✅ $script encontrado"
    fi
done

echo ""
echo "🎉 Setup concluído!"
echo ""
echo "📋 Próximos passos:"
echo "1. Edite o arquivo .env com suas configurações de banco de dados"
echo "2. Adicione as imagens necessárias na pasta static/img/"
echo "3. Adicione os scripts necessários na pasta scripts/ (opcional)"
echo "4. Execute: docker-compose up -d"
echo ""
echo "🌐 A aplicação estará disponível em: http://localhost:8001"
echo ""
echo "📚 Para mais informações, consulte o README.md" 