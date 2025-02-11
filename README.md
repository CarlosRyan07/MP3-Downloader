# 🎵 MP3 Downloader - Baixador de Áudio do YouTube

[![Licença MIT](https://img.shields.io/badge/Licença-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Requisito: FFmpeg](https://img.shields.io/badge/Requisito-FFmpeg-important)](https://ffmpeg.org/)

Uma aplicação web moderna para conversão de vídeos e playlists do YouTube em arquivos MP3 de alta qualidade, com monitoramento em tempo real e interface intuitiva.

## ✨ Funcionalidades Principais

### 🚀 Conversão Avançada
- Download de vídeos individuais ou playlists completas
- Conversão para MP3 com qualidade de 192kbps
- Preservação de metadados (título, artista, capa do álbum)
- Suporte a URLs de vídeos e playlists

### 📊 Progresso em Tempo Real
- Barra de progresso interativa
- Estimativa de tempo restante
- Velocidade de download em tempo real
- Notificações de conclusão com efeitos de confete

### 🎨 Interface Moderna
- Tema escuro com design responsivo
- Animções fluidas de carregamento
- Pré-visualização das informações do vídeo
- Efeitos visuais interativos
- Compatibilidade com múltiplos navegadores

## ⚙️ Pré-requisitos

- Python 3.9 ou superior
- FFmpeg instalado e configurado no PATH
- Conexão com internet
- Navegador moderno (Chrome, Firefox, Edge)

## 🛠 Instalação

1. Clone o repositório:
```bash
git clone <your-repository-url>
cd mp3-downloader
```

2. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

## Uso

1. Inicie o servidor:
```bash
python app.py
```

2. Abra seu navegador e navegue para:
```
http://localhost:5000
```

3. Insira um URL de vídeo ou playlist no campo de entrada
4. Clique no botão Download
5. Aguarde a conclusão do download
6. Encontre seus arquivos MP3 baixados na pasta Downloads do seu sistema

## Estrutura do Projeto

```
mp3-downloader/
├── app.py              # Aplicação principal Flask
├── baixar_audio.py     # Módulo de manipulação de download de áudio
├── requirements.txt    # Dependências do projeto
├── static/
│   └── css/
│       └── style.css   # Estilos da aplicação
└── templates/
    └── index.html      # Template principal da aplicação
```

## Dependências

- Flask: Framework web
- Flask-SocketIO: Comunicação em tempo real
- yt-dlp: Download e processamento de vídeos
- Socket.IO: Atualizações em tempo real no lado do cliente
- Anime.js: Efeitos de animação
- Canvas Confetti: Efeitos de celebração

## Funcionalidades em Detalhe

### Rastreamento de Progresso de Download
- Atualizações de progresso em tempo real usando WebSocket
- Visualização da barra de progresso
- Monitoramento da velocidade de download

### Interface do Usuário
- Design com tema escuro
- Tela de boas-vindas animada
- Efeito de brilho no botão de download
- Animações de carregamento
- Efeito de confete na conclusão do download

### Processamento de Áudio
- Conversão de MP3 de alta qualidade
- Preservação de metadados

## Compatibilidade com Navegadores

A aplicação foi testada e funciona em:
- Google Chrome (recomendado)
- Mozilla Firefox
- Microsoft Edge
- Safari

## Problemas Conhecidos

1. Tem a possibilidade de alguns vídeos podem não estar disponíveis para download devido a restrições
2. A modificação da data de criação só funciona em sistemas Windows
3. Playlists muito longas podem levar um tempo significativo para serem processadas

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

## Agradecimentos

- yt-dlp por fornecer a funcionalidade principal de download
- Anime.js pelas animações suaves
- Socket.IO pelas capacidades de comunicação em tempo real