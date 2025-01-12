# 1 Etapa

pip install yt-dlp

# Baixar Audio e Videos

    Para baixar audio pode utilizar o codigo tranquilamente👍🏻, mas para baixar videos é necessario umas etapas a mais, Pois precisamos instalar o FFmpeg pois ele é essencial para combinar áudio e vídeo baixados separadamente.
    Porque o yt-dlp não faz isso automaticamente, então é necessário instalar o FFmpeg e adicionar ele ao PATH do sistema.

    1. Instale o FFmpeg
    
        Windows:
        Baixe o FFmpeg:

        Acesse o site oficial do FFmpeg.
        Escolha uma versão compatível com o Windows (recomendo usar builds do gyan.dev).
        Extraia os Arquivos:

        Extraia o arquivo baixado para uma pasta, como C:\ffmpeg.
        Adicione ao PATH:

        Copie o caminho da pasta bin dentro da instalação do FFmpeg, por exemplo, C:\ffmpeg\bin.
        Adicione esse caminho ao PATH do sistema:
        
        Clique com o botão direito em Este Computador > Propriedades.
        Vá em Configurações Avançadas do Sistema > Variáveis de Ambiente.
        Edite a variável Path e adicione o caminho copiado.
        Salve e reinicie o terminal.
        
        Teste: Abra um terminal e digite:
        
        ffmpeg -version
        Deve aparecer a versão instalada.

