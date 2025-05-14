# Termoo - Jogo de Palavras

Termoo é um jogo inspirado no Wordle, mas com múltiplas palavras para adivinhar simultaneamente.

## Como Jogar

1. Configure o jogo escolhendo:
   - Número de palavras a adivinhar
   - Nível de dificuldade (1-100%)
   - Número de letras por palavra
   - Número de tentativas
   - Se deseja ativar trapaça (mostra as palavras)

2. Tente adivinhar todas as palavras antes de acabarem suas tentativas!

3. Para cada letra em cada palavra:
   - Verde: letra correta na posição correta
   - Amarelo: letra correta na posição errada
   - Cinza: letra não está na palavra

## Como Testar

### Versão PyGame (Local)

1. **Instalação de dependências:**
   ```
   pip install pygame numpy wordfreq
   ```

2. **Execução local:**
   ```
   python termoo_pygame.py
   ```

3. **O que esperar:**
   - Uma janela PyGame será aberta
   - Você verá telas de configuração onde pode definir os parâmetros do jogo
   - Após a configuração, o jogo mostrará o tabuleiro com múltiplas palavras para adivinhar

### Versão PyBag (Navegador)

1. **Instalação do PyBag:**
   ```
   pip install pygbag
   ```

2. **Construindo e iniciando o servidor:**
   ```
   pygbag .
   ```

3. **Acessando o jogo:**
   - Abra seu navegador
   - Acesse `http://localhost:8000`
   - Aguarde o carregamento (pode demorar na primeira vez)
   - Clique na tela quando solicitado para iniciar o jogo

4. **Solução de problemas:**
   - Se encontrar uma tela em branco, aguarde - o PyBag leva tempo para compilar
   - Para depuração, acesse `http://localhost:8000/#debug`
   - Verifique se seu navegador tem suporte para WebAssembly (a maioria dos navegadores modernos tem)

5. **Publicando online:**
   - Os arquivos para upload ficam na pasta `build`
   - Você pode hospedar esses arquivos em qualquer servidor web estático (GitHub Pages, Netlify, etc.)

## Controles

- Mouse: Clique nas caixas de entrada para ativar
- Teclado: Digite suas respostas
- ENTER: Confirma entradas
- ESC: Sai do jogo
- R: Reinicia (na tela final)

## Requisitos

- Python 3.6 ou superior
- PyGame (para versão local)
- PyBag (para versão web)

## Estrutura do Projeto

- `termoo_pygame.py` - Versão para execução local
- `main.py` - Versão compatível com PyBag (necessário para execução web)
- `README.md` - Este arquivo de instruções

## Dicas de Teste

1. **Teste Completo:**
   - Experimente diferentes configurações (número de palavras, letras)
   - Teste o modo trapaça para verificar se as palavras corretas são mostradas
   - Verifique se o feedback colorido está funcionando corretamente

2. **Cenários de Teste:**
   - Ganhar o jogo (acertar todas as palavras)
   - Perder o jogo (esgotar tentativas)
   - Desistir usando os comandos especiais
   - Digitar palavras inválidas ou que não estão no dicionário
