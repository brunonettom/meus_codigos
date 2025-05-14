import pygame
import sys
import random
import unicodedata
import os
import asyncio  # Adicionar importação de asyncio para compatibilidade com Pygbag
from wordfreq import word_frequency, top_n_list
from filtra_palavras import lista_de_palavras
try:
    from lista_unificada_20_04_2025__20_32 import palavras as possiveis_palavras
except ImportError:
    # Fallback para caso o arquivo de palavras não exista
    possiveis_palavras = []

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 180, 0)
AMARELO = (255, 200, 0)
CINZA_CLARO = (230, 230, 230)
CINZA_ESCURO = (80, 80, 80)
VERMELHO = (220, 0, 0)
AZUL = (50, 120, 220)

# Fontes
FONTE_PRINCIPAL = pygame.font.SysFont("Arial", 24)
FONTE_GRANDE = pygame.font.SysFont("Arial", 36, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 18)
FONTE_MUITO_PEQUENA = pygame.font.SysFont("Arial", 14)

# Variáveis globais para tela cheia
TELA_CHEIA = False
TAMANHO_JANELA = (800, 600)

# Função para alternar modo de tela cheia
def alternar_tela_cheia():
    global TELA_CHEIA
    TELA_CHEIA = not TELA_CHEIA
    if TELA_CHEIA:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(TAMANHO_JANELA)

class TelaConfiguracao:
    """Tela de configuração inicial do jogo."""
    
    def __init__(self, tela):
        self.tela = tela
        self.largura_tela, self.altura_tela = tela.get_size()
        
        # Valores padrão
        self.num_palavras = 4
        self.num_letras = 5
        self.num_tentativas = self.num_palavras + self.num_letras
        self.dificuldade = 50
        self.modo_trapaca = False
        
        # Campos de entrada
        self.campos = [
            {"nome": "Número de palavras:", "valor": "4", "ativo": False, "min": 1, "max": 8},
            {"nome": "Número de letras por palavra:", "valor": "5", "ativo": False, "min": 3, "max": 10},
            {"nome": "Número de tentativas:", "valor": str(self.num_palavras + self.num_letras), 
             "ativo": False, "min": 3, "max": 20},
            {"nome": "Dificuldade (1-100%):", "valor": "50", "ativo": False, "min": 1, "max": 100}
        ]
        
        # Botões
        self.botao_iniciar = pygame.Rect(self.largura_tela // 2 - 100, self.altura_tela - 150, 200, 50)
        
        # Checkbox para trapaça
        self.checkbox_rect = pygame.Rect(self.largura_tela // 2 - 160, self.altura_tela - 200, 20, 20)
        
        # Estados
        self.ativo = True
        
        # Adicionar uma variável para rastrear se o número de tentativas foi modificado manualmente
        self.tentativas_modificadas_manualmente = False
    
    def processar_eventos(self):
        """Processa eventos da tela de configuração."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return {"acao": "sair"}
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica clique nos campos de entrada
                y_pos = 100
                for i, campo in enumerate(self.campos):
                    campo_rect = pygame.Rect(self.largura_tela // 2 - 100, y_pos, 200, 40)
                    if campo_rect.collidepoint(evento.pos):
                        for j in range(len(self.campos)):
                            self.campos[j]["ativo"] = (j == i)
                    y_pos += 80
                
                # Verifica clique no checkbox de trapaça
                if self.checkbox_rect.collidepoint(evento.pos):
                    self.modo_trapaca = not self.modo_trapaca
                
                # Verifica clique no botão iniciar
                if self.botao_iniciar.collidepoint(evento.pos):
                    try:
                        self.num_palavras = max(1, min(8, int(self.campos[0]["valor"])))
                        self.num_letras = max(3, min(10, int(self.campos[1]["valor"])))
                        
                        # Recalcular o valor padrão das tentativas baseado nos novos valores
                        tentativas_valor = self.campos[2]["valor"]
                        tentativas_padrao = self.num_palavras + self.num_letras
                        
                        # Se o usuário não modificou o valor das tentativas, atualiza automaticamente
                        tentativas_atual = int(tentativas_valor) if tentativas_valor else 0
                        if tentativas_atual == self.num_tentativas:  # Valor anterior
                            self.campos[2]["valor"] = str(tentativas_padrao)
                            self.num_tentativas = tentativas_padrao
                        else:
                            self.num_tentativas = max(3, min(20, int(self.campos[2]["valor"])))
                        
                        self.dificuldade = max(1, min(100, int(self.campos[3]["valor"])))
                        
                        return {
                            "acao": "iniciar_jogo",
                            "config": {
                                "num_palavras": self.num_palavras,
                                "num_letras": self.num_letras,
                                "num_tentativas": self.num_tentativas,
                                "dificuldade": self.dificuldade / 100,  # Convertido para 0-1
                                "modo_trapaca": self.modo_trapaca
                            }
                        }
                    except ValueError:
                        # Se houver erro na conversão dos valores, não faz nada
                        pass
            
            elif evento.type == pygame.KEYDOWN:
                # Tecla F11 ou Alt+Enter para alternar tela cheia
                if evento.key == pygame.K_F11 or \
                   (evento.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT):
                    self.tela = alternar_tela_cheia()
                    self.largura_tela, self.altura_tela = self.tela.get_size()
                    # Reposiciona elementos da interface após mudança de resolução
                    self.botao_iniciar = pygame.Rect(self.largura_tela // 2 - 100, self.altura_tela - 150, 200, 50)
                    self.checkbox_rect = pygame.Rect(self.largura_tela // 2 - 160, self.altura_tela - 200, 20, 20)
                    return {"acao": "continuar"}
                
                # Processa teclas nos campos ativos
                for i, campo in enumerate(self.campos):
                    if campo["ativo"]:
                        valor_antigo = campo["valor"]
                        
                        if evento.key == pygame.K_BACKSPACE:
                            campo["valor"] = campo["valor"][:-1]
                        elif evento.key == pygame.K_RETURN:
                            campo["ativo"] = False
                        elif evento.unicode.isdigit() and len(campo["valor"]) < 2:
                            campo["valor"] += evento.unicode
                            
                        # Se o valor mudou, atualiza as configurações
                        if valor_antigo != campo["valor"]:
                            # Se modificamos o campo de palavras ou letras, atualiza tentativas automaticamente
                            if i == 0 or i == 1:  # índices dos campos de palavras e letras
                                try:
                                    palavras = int(self.campos[0]["valor"]) if self.campos[0]["valor"] else 0
                                    letras = int(self.campos[1]["valor"]) if self.campos[1]["valor"] else 0
                                    
                                    # Só atualiza se não foi modificado manualmente ou estamos modificando agora
                                    if not self.tentativas_modificadas_manualmente:
                                        # Só calcula se ambos os valores são válidos
                                        if palavras > 0 and letras > 0:
                                            tentativas_padrao = palavras + letras
                                            self.campos[2]["valor"] = str(tentativas_padrao)
                                            self.num_tentativas = tentativas_padrao
                                except ValueError:
                                    pass
                            
                            # Se estamos modificando o campo de tentativas
                            if i == 2:  # índice do campo de tentativas
                                self.tentativas_modificadas_manualmente = True
                
                # Tecla Escape sai do jogo
                if evento.key == pygame.K_ESCAPE:
                    return {"acao": "sair"}
        
        return {"acao": "continuar"}
    
    def renderizar(self):
        """Renderiza a tela de configuração."""
        self.tela.fill(BRANCO)
        
        # Título
        titulo = FONTE_GRANDE.render("Configuração do Jogo", True, PRETO)
        self.tela.blit(titulo, (self.largura_tela // 2 - titulo.get_width() // 2, 30))
        
        # Campos de entrada
        y_pos = 100
        for i, campo in enumerate(self.campos):
            # Nome do campo
            texto = FONTE_PRINCIPAL.render(campo["nome"], True, PRETO)
            self.tela.blit(texto, (self.largura_tela // 2 - 300, y_pos + 10))
            
            # Retângulo do campo
            cor_borda = AZUL if campo["ativo"] else CINZA_ESCURO
            campo_rect = pygame.Rect(self.largura_tela // 2 - 100, y_pos, 200, 40)
            pygame.draw.rect(self.tela, BRANCO, campo_rect)
            pygame.draw.rect(self.tela, cor_borda, campo_rect, 2)
            
            # Valor do campo
            valor_texto = FONTE_PRINCIPAL.render(campo["valor"], True, PRETO)
            self.tela.blit(valor_texto, (campo_rect.x + 10, campo_rect.y + 10))
            
            # Adicionar dica visual para o campo de tentativas
            if i == 2:  # Campo de tentativas
                if self.tentativas_modificadas_manualmente:
                    dica_texto = FONTE_MUITO_PEQUENA.render("(Valor personalizado)", True, AZUL)
                else:
                    dica_texto = FONTE_MUITO_PEQUENA.render("(Auto: palavras + letras)", True, CINZA_ESCURO)
                self.tela.blit(dica_texto, (campo_rect.x + 10, campo_rect.y + campo_rect.height + 5))
            
            y_pos += 80
        
        # Checkbox de trapaça
        pygame.draw.rect(self.tela, BRANCO, self.checkbox_rect)
        pygame.draw.rect(self.tela, CINZA_ESCURO, self.checkbox_rect, 2)
        if self.modo_trapaca:
            pygame.draw.line(self.tela, VERMELHO, 
                            (self.checkbox_rect.left + 3, self.checkbox_rect.top + 3), 
                            (self.checkbox_rect.right - 3, self.checkbox_rect.bottom - 3), 3)
            pygame.draw.line(self.tela, VERMELHO, 
                            (self.checkbox_rect.right - 3, self.checkbox_rect.top + 3), 
                            (self.checkbox_rect.left + 3, self.checkbox_rect.bottom - 3), 3)
        
        texto_trapaca = FONTE_PRINCIPAL.render("Ativar modo trapaça (ver palavras)", True, PRETO)
        self.tela.blit(texto_trapaca, (self.checkbox_rect.right + 10, self.checkbox_rect.y))
        
        # Botão iniciar
        pygame.draw.rect(self.tela, VERDE, self.botao_iniciar)
        pygame.draw.rect(self.tela, PRETO, self.botao_iniciar, 2)
        texto_iniciar = FONTE_PRINCIPAL.render("Iniciar Jogo", True, BRANCO)
        self.tela.blit(texto_iniciar, (self.botao_iniciar.x + (self.botao_iniciar.width - texto_iniciar.get_width()) // 2, 
                                       self.botao_iniciar.y + (self.botao_iniciar.height - texto_iniciar.get_height()) // 2))
        
        pygame.display.flip()


class TermooPygame:
    """Classe principal do jogo Termoo com interface Pygame."""
    
    def __init__(self, config):
        """Inicializa o jogo com as configurações fornecidas."""
        # Configurações do jogo
        self.num_palavras = config["num_palavras"]
        self.num_letras = config["num_letras"]
        self.num_tentativas = config["num_tentativas"]
        self.dificuldade = config["dificuldade"]
        self.modo_trapaca = config["modo_trapaca"]
        
        # Configurações da tela
        self.tela = pygame.display.get_surface()  # Usa a superfície já criada
        self.largura_tela, self.altura_tela = self.tela.get_size()
        pygame.display.set_caption("Termoo")
        
        # Carrega dicionários
        self.dicionario_pt = top_n_list('pt', 300000)
        self.palavras_possiveis = self._carregar_palavras_possiveis()
        
        # Estado do jogo
        self.inicializar_jogo()
        
        # Variáveis de entrada
        self.entrada_atual = ""
        self.entrada_ativa = True
        self.mensagem = ""
        self.contador_mensagem = 0
        self.jogo_terminado = False
        self.resultado_jogo = ""
        
        # Adiciona posição do cursor para navegação na entrada
        self.cursor_pos = 0
        
        # Adiciona uma variável para controlar a disposição dos elementos
        self.altura_tabuleiro = 0

        # Adiciona o botão de home
        self.botao_home_tamanho = 40
        self.botao_home_margem = 20
        self.botao_home_rect = pygame.Rect(
            self.largura_tela - self.botao_home_tamanho - self.botao_home_margem,
            self.botao_home_margem,
            self.botao_home_tamanho,
            self.botao_home_tamanho
        )
    
    def inicializar_jogo(self):
        """Inicializa ou reinicia o estado do jogo."""
        # Palavras do jogo
        self.palavras_chave = self._selecionar_palavras()
        self.palavras_chave_originais = self.palavras_chave.copy()
        
        # Estado do jogo
        self.tentativas = []
        self.palavras_acertadas = []
        self.palavras_erradas = []
        self.letras_usadas = set()
        self.status_letras = {}
        self.tentativa_atual = 0
        self.jogo_terminado = False
    
    def _carregar_palavras_possiveis(self):
        """Carrega e filtra palavras possíveis para o jogo."""
        try:
            palavras = lista_de_palavras(self.dificuldade)
            # Filtra palavras pelo tamanho
            return [p for p in palavras if len(p) == self.num_letras and ' ' not in p and '-' not in p]
        except Exception as e:
            print(f"Erro ao carregar palavras: {e}")
            # Fallback para um conjunto básico de palavras
            return [p for p in possiveis_palavras if len(p) == self.num_letras and ' ' not in p and '-' not in p]
    
    def _selecionar_palavras(self):
        """Seleciona aleatoriamente palavras para o jogo."""
        if len(self.palavras_possiveis) < self.num_palavras:
            # Não há palavras suficientes, usar todas
            return self.palavras_possiveis[:self.num_palavras]
        
        palavras = []
        candidatos = self.palavras_possiveis.copy()
        
        while len(palavras) < self.num_palavras and candidatos:
            palavra = random.choice(candidatos)
            candidatos.remove(palavra)
            # Normaliza a palavra (remove acentos)
            palavra = self._remover_acentos(palavra)
            palavras.append(palavra)
        
        return palavras
    
    def _remover_acentos(self, palavra):
        """Remove acentos e substitui 'ç' por 'c'."""
        nfkd = unicodedata.normalize('NFD', palavra)
        sem_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        sem_acentos = sem_acentos.replace('ç', 'c').replace('Ç', 'C')
        return sem_acentos
    
    def _verificar_tentativa(self, tentativa, palavra):
        """Verifica a tentativa contra uma palavra específica e retorna o resultado."""
        if len(tentativa) != len(palavra):
            return []
        
        resultado = [0] * len(tentativa)  # 0: ausente, 1: posição incorreta, 2: posição correta
        letras_restantes = list(palavra)
        
        # Primeiro, marca as letras em posição correta
        for i in range(len(tentativa)):
            if tentativa[i] == palavra[i]:
                resultado[i] = 2
                letras_restantes[i] = None
        
        # Depois, marca as letras em posição incorreta
        for i in range(len(tentativa)):
            if resultado[i] != 2 and tentativa[i] in letras_restantes:
                resultado[i] = 1
                letras_restantes[letras_restantes.index(tentativa[i])] = None
        
        return resultado
    
    def _atualizar_status_letras(self):
        """Atualiza o status das letras com base nas tentativas atuais."""
        if not self.tentativas:
            return
        
        ultima_tentativa = self.tentativas[-1]
        for letra in ultima_tentativa:
            if letra not in self.letras_usadas:
                self.letras_usadas.add(letra)
                self.status_letras[letra] = {}
        
        # Para cada letra, verifica seu status em cada palavra
        for letra in self.letras_usadas:
            for i, palavra in enumerate(self.palavras_chave_originais):
                if palavra in self.palavras_acertadas:
                    # Se a palavra foi acertada, todas as letras são verdes
                    self.status_letras[letra][i] = 2 if letra in palavra else 0
                else:
                    # Determina o status da letra nesta palavra
                    if letra not in palavra:
                        self.status_letras[letra][i] = 0  # Não está na palavra
                    else:
                        # Verifica se está em posição correta em alguma ocorrência
                        posicao_correta = False
                        for j, char in enumerate(palavra):
                            if letra == char and any(chute[j] == letra for chute in self.tentativas):
                                posicao_correta = True
                                break
                        
                        if posicao_correta:
                            self.status_letras[letra][i] = 2  # Está na posição correta
                        else:
                            self.status_letras[letra][i] = 1  # Está na palavra, mas em posição errada
    
    def processar_eventos(self):
        """Processa eventos do jogo."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se clicou no botão home
                if self.botao_home_rect.collidepoint(evento.pos):
                    return "reiniciar"  # Usa a mesma funcionalidade do "reiniciar" para voltar à tela inicial
                
                # Verifica se clicou na área de entrada para posicionar o cursor
                largura_entrada = min(300, self.largura_tela - 60)
                entrada_y = 0  # Será calculado na função renderizar, mas podemos estimar aqui
                
                # Estimar a posição do campo de entrada
                if hasattr(self, 'altura_tabuleiro'):
                    status_letras_y = 20 + FONTE_GRANDE.get_height() + 10
                    altura_status = 100 if self.num_palavras <= 4 else 120
                    tabuleiro_y = status_letras_y + altura_status + 10
                    entrada_y = tabuleiro_y + self.altura_tabuleiro + 50
                else:
                    entrada_y = self.altura_tela // 2  # Fallback
                
                entrada_rect = pygame.Rect(
                    self.largura_tela // 2 - largura_entrada // 2, 
                    entrada_y, 
                    largura_entrada, 
                    40
                )
                
                if entrada_rect.collidepoint(evento.pos):
                    # Calcula a posição do cursor baseado no clique
                    x_rel = evento.pos[0] - (entrada_rect.x + 10)
                    
                    # Estima a posição do caractere clicado
                    largura_media_char = FONTE_PRINCIPAL.size("A")[0]
                    pos_estimada = int(x_rel / largura_media_char)
                    
                    # Limita à faixa válida
                    self.cursor_pos = max(0, min(len(self.entrada_atual), pos_estimada))
            
            if evento.type == pygame.KEYDOWN:
                # Tecla F11 ou Alt+Enter para alternar tela cheia
                if evento.key == pygame.K_F11 or \
                   (evento.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT):
                    self.tela = alternar_tela_cheia()
                    self.largura_tela, self.altura_tela = self.tela.get_size()
                    return "continuar"
            
            if self.jogo_terminado:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "sair"
                    elif evento.key == pygame.K_RETURN:
                        return "reiniciar"
                continue
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "sair"
                
                elif evento.key == pygame.K_RETURN:
                    if self.entrada_atual:
                        return self._processar_tentativa(self.entrada_atual)
                
                elif evento.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        # Remove o caractere à esquerda do cursor
                        self.entrada_atual = self.entrada_atual[:self.cursor_pos-1] + self.entrada_atual[self.cursor_pos:]
                        self.cursor_pos -= 1
                        self.mensagem = ""
                
                elif evento.key == pygame.K_DELETE:
                    # Remove o caractere à direita do cursor
                    if self.cursor_pos < len(self.entrada_atual):
                        self.entrada_atual = self.entrada_atual[:self.cursor_pos] + self.entrada_atual[self.cursor_pos+1:]
                        self.mensagem = ""
                
                elif evento.key == pygame.K_LEFT:
                    # Move o cursor para a esquerda
                    if self.cursor_pos > 0:
                        self.cursor_pos -= 1
                
                elif evento.key == pygame.K_RIGHT:
                    # Move o cursor para a direita
                    if self.cursor_pos < len(self.entrada_atual):
                        self.cursor_pos += 1
                
                elif evento.key == pygame.K_HOME:
                    # Move o cursor para o início
                    self.cursor_pos = 0
                
                elif evento.key == pygame.K_END:
                    # Move o cursor para o final
                    self.cursor_pos = len(self.entrada_atual)
                
                elif len(self.entrada_atual) < self.num_letras and evento.unicode.isalpha():
                    # Insere o caractere na posição atual do cursor
                    self.entrada_atual = (self.entrada_atual[:self.cursor_pos] + 
                                        evento.unicode.lower() + 
                                        self.entrada_atual[self.cursor_pos:])
                    self.cursor_pos += 1
        
        return "continuar"
    
    def _processar_tentativa(self, tentativa):
        """Processa uma tentativa de palavra."""
        # Verificações básicas
        if len(tentativa) != self.num_letras:
            self.mensagem = f"A palavra deve ter {self.num_letras} letras!"
            self.contador_mensagem = 180  # 3 segundos (60 frames por segundo)
            return "continuar"
        
        if tentativa not in self.dicionario_pt and tentativa not in self.palavras_possiveis:
            self.mensagem = "Palavra não encontrada no dicionário!"
            self.contador_mensagem = 180
            return "continuar"
        
        # Adiciona a tentativa à lista
        self.tentativas.append(tentativa)
        self.tentativa_atual += 1
        
        # Verifica se acertou alguma palavra
        for palavra in list(self.palavras_chave):
            if tentativa == palavra:
                self.palavras_acertadas.append(palavra)
                self.palavras_chave.remove(palavra)
                self.mensagem = f"Parabéns! Você acertou a palavra '{palavra}'!"
                self.contador_mensagem = 180
                break
        else:
            # Não acertou nenhuma palavra
            self.palavras_erradas.append(tentativa)
        
        # Atualiza o status das letras
        self._atualizar_status_letras()
        
        # Limpa a entrada e reseta o cursor
        self.entrada_atual = ""
        self.cursor_pos = 0
        
        # Verifica condições de fim de jogo
        if not self.palavras_chave:
            self.jogo_terminado = True
            self.resultado_jogo = "vitoria"
            return "continuar"
        
        if self.tentativa_atual >= self.num_tentativas:
            self.jogo_terminado = True
            self.resultado_jogo = "derrota"
            return "continuar"
        
        return "continuar"
    
    def renderizar(self):
        """Renderiza o jogo na tela."""
        self.tela.fill(BRANCO)
        
        # Calcula altura disponível para melhor posicionamento dos elementos
        altura_util = self.altura_tela - 100  # Reserve espaço para margens
        
        # Renderizar título
        titulo = FONTE_GRANDE.render("TERMOO", True, PRETO)
        titulo_pos_y = 20
        self.tela.blit(titulo, (self.largura_tela // 2 - titulo.get_width() // 2, titulo_pos_y))
        
        # Renderizar modo trapaça (se ativado)
        if self.modo_trapaca:
            palavras_str = ", ".join(self.palavras_chave_originais)
            trapaca_texto = FONTE_PEQUENA.render(f"Palavras: {palavras_str}", True, CINZA_ESCURO)
            self.tela.blit(trapaca_texto, (20, titulo_pos_y))
        
        # Posição vertical inicial do status de letras
        status_letras_y = titulo_pos_y + titulo.get_height() + 10
        
        # Renderizar status das letras com altura adaptativa
        altura_status = 100 if self.num_palavras <= 4 else 120
        self._renderizar_status_letras(status_letras_y)
        
        # Calculando altura disponível para tabuleiro e estatísticas
        altura_disponivel = altura_util - status_letras_y - altura_status - 20  # -20 para margem
        
        # Altura do tabuleiro não deve exceder 60% da altura disponível em tela cheia
        if TELA_CHEIA:
            max_altura_tabuleiro = int(altura_disponivel * 0.6)
        else:
            max_altura_tabuleiro = int(altura_disponivel * 0.7)
        
        # Posição vertical inicial do tabuleiro
        tabuleiro_y = status_letras_y + altura_status + 10
        
        # Renderizar tabuleiro
        self.altura_tabuleiro = self._renderizar_tabuleiro(tabuleiro_y, max_altura_tabuleiro)
        
        # Posição vertical inicial da entrada
        entrada_y = tabuleiro_y + self.altura_tabuleiro + 20
        
        # Renderizar entrada atual
        self._renderizar_entrada(entrada_y)
        
        # Posição vertical inicial das estatísticas
        estatisticas_y = entrada_y + 80
        
        # Renderizar estatísticas
        self._renderizar_estatisticas(estatisticas_y)
        
        # Renderizar mensagem temporária
        if self.mensagem and self.contador_mensagem > 0:
            self._renderizar_mensagem()
            self.contador_mensagem -= 1
        
        # Renderizar tela de fim de jogo
        if self.jogo_terminado:
            self._renderizar_fim_jogo()
        
        # Renderizar o botão home (ícone de casa)
        self._renderizar_botao_home()
        
        pygame.display.flip()
    
    def _renderizar_status_letras(self, pos_y=80):
        """Renderiza a tabela de status das letras usadas."""
        # Fundo da área de status - Aumentar altura para acomodar mais letras
        altura_status = 100 if self.num_palavras <= 4 else 120  # Altura adaptativa
        
        pygame.draw.rect(self.tela, CINZA_CLARO, 
                        pygame.Rect(20, pos_y, self.largura_tela - 40, altura_status))
        pygame.draw.rect(self.tela, CINZA_ESCURO, 
                        pygame.Rect(20, pos_y, self.largura_tela - 40, altura_status), 2)
        
        # Título da área
        titulo = FONTE_PEQUENA.render("Status das Letras:", True, PRETO)
        self.tela.blit(titulo, (30, pos_y + 5))
        
        # Criar uma grade com todas as letras
        alfabeto = 'abcdefghijklmnopqrstuvwxyz'
        
        # Calcular o layout conforme o espaço disponível
        area_largura = self.largura_tela - 60
        
        # Determinar quantas letras por linha para distribuir melhor o espaço
        num_colunas = min(26, max(13, area_largura // 30))  # Pelo menos 13 letras por linha
        num_linhas = (26 + num_colunas - 1) // num_colunas  # Arredonda para cima
        
        espacamento_x = area_largura // num_colunas
        espacamento_y = (altura_status - 30) // num_linhas  # 30 pixels para título e margem
        
        # Calcular posição inicial
        pos_x_inicial = 30
        pos_y_inicial = pos_y + 25
        
        # Para cada letra do alfabeto
        for i, letra in enumerate(alfabeto):
            # Calcular posição da letra
            linha = i // num_colunas
            coluna = i % num_colunas
            
            pos_x = pos_x_inicial + coluna * espacamento_x
            pos_y_letra = pos_y_inicial + linha * espacamento_y
            
            # Cor da letra
            cor_letra = CINZA_ESCURO
            if letra in self.letras_usadas:
                cor_letra = PRETO
            
            # Renderizar a letra
            letra_surf = FONTE_PEQUENA.render(letra.upper(), True, cor_letra)
            self.tela.blit(letra_surf, (pos_x, pos_y_letra))
            
            # Se a letra foi usada, mostrar indicadores coloridos
            if letra in self.status_letras:
                # Configura tamanho dos indicadores baseado no número de palavras
                tamanho_indicador = max(4, min(8, 20 // self.num_palavras))
                espaco_indicador = tamanho_indicador + 2
                
                # Posição inicial dos indicadores
                ix = pos_x
                iy = pos_y_letra + 18
                
                # Desenha os indicadores para cada palavra
                for i in range(self.num_palavras):
                    status = self.status_letras.get(letra, {}).get(i, 0)
                    
                    cor = CINZA_ESCURO
                    if status == 1:
                        cor = AMARELO
                    elif status == 2:
                        cor = VERDE
                    
                    # Desenha o quadrado indicador
                    pygame.draw.rect(self.tela, cor, (ix, iy, tamanho_indicador, tamanho_indicador))
                    
                    # Avança a posição horizontal
                    ix += espaco_indicador
    
    def _renderizar_tabuleiro(self, pos_y=180, max_altura=None):
        """Renderiza o tabuleiro do jogo com todas as tentativas."""
        # Calcula a altura máxima disponível para o tabuleiro
        if max_altura is None:
            max_altura = self.altura_tela - pos_y - 200  # Valor padrão
        
        # Calcula dimensões do tabuleiro
        if TELA_CHEIA:
            largura_celula_max = 60  # Células maiores em tela cheia
            espaco_entre_palavras = 30  # Maior espaçamento em tela cheia
        else:
            largura_celula_max = 50
            espaco_entre_palavras = 20
        
        # Determina tamanho das células baseado no espaço disponível, garantindo uniformidade
        largura_max_disponivel = self.largura_tela - 60  # Margens laterais
        largura_total_ideal = self.num_palavras * self.num_letras * largura_celula_max + (self.num_palavras - 1) * espaco_entre_palavras
        
        if largura_total_ideal > largura_max_disponivel:
            # Calculamos o tamanho para caber tudo na tela
            espaco_total_para_celulas = largura_max_disponivel - (self.num_palavras - 1) * espaco_entre_palavras
            largura_celula = espaco_total_para_celulas // (self.num_palavras * self.num_letras)
            # Ajuste para garantir um tamanho mínimo
            largura_celula = max(30, largura_celula)
        else:
            largura_celula = largura_celula_max
        
        # Calculando a altura das células
        altura_celula = largura_celula  # Mantém aspecto quadrado
        altura_total_ideal = self.num_tentativas * (altura_celula + 5)
        
        # Redimensiona se necessário para caber verticalmente
        if max_altura and altura_total_ideal > max_altura:
            altura_celula = max(30, (max_altura - self.num_tentativas * 5) // self.num_tentativas)
            largura_celula = altura_celula  # Mantém células quadradas
        
        # Calcula a altura total ocupada pelo tabuleiro
        altura_tabuleiro = self.num_tentativas * (altura_celula + 5) - 5
        
        # Centralização horizontal precisa: calcule a largura total exata
        largura_total = self.num_palavras * (self.num_letras * largura_celula) + (self.num_palavras - 1) * espaco_entre_palavras
        pos_x_inicial = (self.largura_tela - largura_total) // 2
        
        # Para cada palavra-chave
        for i_palavra in range(self.num_palavras):
            palavra = self.palavras_chave_originais[i_palavra]
            pos_x = pos_x_inicial + i_palavra * (self.num_letras * largura_celula + espaco_entre_palavras)
            acertou = palavra in self.palavras_acertadas
            
            # Para cada linha (tentativa)
            for i_linha in range(self.num_tentativas):
                celula_y = pos_y + i_linha * (altura_celula + 5)
                
                # Se esta palavra já foi acertada e estamos em uma linha após o acerto
                if acertou and i_linha >= self.tentativas.index(palavra) + 1:
                    # Desenha underscores para linhas após o acerto
                    for j in range(self.num_letras):
                        pos_x_celula = pos_x + j * largura_celula
                        pygame.draw.rect(self.tela, CINZA_CLARO, 
                                        (pos_x_celula, celula_y, largura_celula, altura_celula))
                        pygame.draw.rect(self.tela, CINZA_ESCURO, 
                                        (pos_x_celula, celula_y, largura_celula, altura_celula), 1)
                        texto = FONTE_PRINCIPAL.render("_", True, CINZA_ESCURO)
                        self.tela.blit(texto, (pos_x_celula + largura_celula//2 - texto.get_width()//2, 
                                            celula_y + altura_celula//2 - texto.get_height()//2))
                
                # Se já temos uma tentativa para esta linha
                elif i_linha < len(self.tentativas):
                    tentativa = self.tentativas[i_linha]
                    
                    # Se esta palavra já foi acertada e estamos na linha do acerto
                    if acertou and tentativa == palavra:
                        # Palavras acertadas ficam todas verdes
                        for j in range(self.num_letras):
                            pos_x_celula = pos_x + j * largura_celula
                            pygame.draw.rect(self.tela, VERDE, 
                                            (pos_x_celula, celula_y, largura_celula, altura_celula))
                            pygame.draw.rect(self.tela, CINZA_ESCURO, 
                                            (pos_x_celula, celula_y, largura_celula, altura_celula), 1)
                            texto = FONTE_PRINCIPAL.render(tentativa[j].upper(), True, BRANCO)
                            self.tela.blit(texto, (pos_x_celula + largura_celula//2 - texto.get_width()//2, 
                                                celula_y + altura_celula//2 - texto.get_height()//2))
                    else:
                        # Caso normal: mostrar a tentativa com cores baseadas na verificação
                        resultado = self._verificar_tentativa(tentativa, palavra)
                        for j in range(self.num_letras):
                            pos_x_celula = pos_x + j * largura_celula
                            
                            cor_fundo = CINZA_ESCURO
                            if resultado[j] == 1:
                                cor_fundo = AMARELO
                            elif resultado[j] == 2:
                                cor_fundo = VERDE
                            
                            pygame.draw.rect(self.tela, cor_fundo, 
                                            (pos_x_celula, celula_y, largura_celula, altura_celula))
                            pygame.draw.rect(self.tela, CINZA_ESCURO, 
                                            (pos_x_celula, celula_y, largura_celula, altura_celula), 1)
                            texto = FONTE_PRINCIPAL.render(tentativa[j].upper(), True, BRANCO)
                            self.tela.blit(texto, (pos_x_celula + largura_celula//2 - texto.get_width()//2, 
                                                celula_y + altura_celula//2 - texto.get_height()//2))
                else:
                    # Células vazias para tentativas futuras
                    for j in range(self.num_letras):
                        pos_x_celula = pos_x + j * largura_celula
                        pygame.draw.rect(self.tela, BRANCO, 
                                        (pos_x_celula, celula_y, largura_celula, altura_celula))
                        pygame.draw.rect(self.tela, CINZA_ESCURO, 
                                        (pos_x_celula, celula_y, largura_celula, altura_celula), 1)
        
        return altura_tabuleiro
    
    def _renderizar_entrada(self, pos_y):
        """Renderiza a área de entrada de texto."""
        # Texto informativo
        texto_info = FONTE_PEQUENA.render("Digite sua tentativa:", True, PRETO)
        self.tela.blit(texto_info, (self.largura_tela // 2 - texto_info.get_width() // 2, pos_y))
        
        # Área de entrada
        largura_entrada = min(300, self.largura_tela - 60)
        entrada_rect = pygame.Rect(self.largura_tela // 2 - largura_entrada // 2, pos_y + 30, largura_entrada, 40)
        pygame.draw.rect(self.tela, BRANCO, entrada_rect)
        pygame.draw.rect(self.tela, AZUL, entrada_rect, 2)
        
        # Texto da entrada
        texto_entrada = FONTE_PRINCIPAL.render(self.entrada_atual, True, PRETO)
        self.tela.blit(texto_entrada, (entrada_rect.x + 10, entrada_rect.y + 10))
        
        # Desenhar o cursor na posição atual, não apenas no final
        if pygame.time.get_ticks() % 1000 < 500:  # Piscar o cursor
            # Calcula a posição x do cursor
            if self.cursor_pos == 0:
                cursor_x = entrada_rect.x + 10
            else:
                parte_texto = FONTE_PRINCIPAL.render(self.entrada_atual[:self.cursor_pos], True, PRETO)
                cursor_x = entrada_rect.x + 10 + parte_texto.get_width()
            
            # Desenha o cursor como uma linha vertical
            pygame.draw.line(self.tela, PRETO, (cursor_x, entrada_rect.y + 10), 
                           (cursor_x, entrada_rect.y + entrada_rect.height - 10), 2)
    
    def _renderizar_estatisticas(self, pos_y):
        """Renderiza as estatísticas do jogo."""
        # Centraliza as estatísticas na tela
        largura_disponivel = self.largura_tela - 60
        padding_lateral = 30
        
        # Tentativas restantes
        tentativas_restantes = self.num_tentativas - self.tentativa_atual
        texto_tentativas = FONTE_PEQUENA.render(f"Tentativas restantes: {tentativas_restantes}", True, PRETO)
        self.tela.blit(texto_tentativas, (padding_lateral, pos_y))
        
        # Palavras faltantes
        texto_palavras = FONTE_PEQUENA.render(f"Palavras faltantes: {len(self.palavras_chave)}", True, PRETO)
        if TELA_CHEIA:
            # Em tela cheia, coloca ao lado
            pos_x_palavras = padding_lateral + texto_tentativas.get_width() + 40
            self.tela.blit(texto_palavras, (pos_x_palavras, pos_y))
            pos_y_proxima_linha = pos_y
        else:
            # Em janela, coloca abaixo
            self.tela.blit(texto_palavras, (padding_lateral, pos_y + 25))
            pos_y_proxima_linha = pos_y + 25
        
        # Palavras acertadas
        if self.palavras_acertadas:
            acertadas_str = ", ".join(self.palavras_acertadas)
            texto_acertadas = FONTE_PEQUENA.render(f"Palavras acertadas: {acertadas_str}", True, VERDE)
            if TELA_CHEIA and len(self.palavras_acertadas) <= 2:
                # Em tela cheia com poucas palavras, coloca ao lado
                pos_x_acertadas = pos_x_palavras + texto_palavras.get_width() + 40
                self.tela.blit(texto_acertadas, (pos_x_acertadas, pos_y))
            else:
                # Caso contrário, coloca abaixo
                pos_y_proxima_linha += 25
                self.tela.blit(texto_acertadas, (padding_lateral, pos_y_proxima_linha))
        
        # Palavras erradas
        if self.palavras_erradas:
            erradas_exibir = self.palavras_erradas[-5:] if len(self.palavras_erradas) > 5 else self.palavras_erradas
            erradas_str = ", ".join(erradas_exibir)
            texto_erradas = FONTE_PEQUENA.render(f"Últimas palavras erradas: {erradas_str}", True, VERMELHO)
            self.tela.blit(texto_erradas, (padding_lateral, pos_y_proxima_linha + 25))
    
    def _renderizar_mensagem(self):
        """Renderiza uma mensagem temporária."""
        # Fundo semi-transparente
        s = pygame.Surface((self.largura_tela, 50), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.tela.blit(s, (0, self.altura_tela - 50))
        
        # Texto da mensagem
        texto = FONTE_PRINCIPAL.render(self.mensagem, True, BRANCO)
        self.tela.blit(texto, (self.largura_tela // 2 - texto.get_width() // 2, self.altura_tela - 40))
    
    def _renderizar_fim_jogo(self):
        """Renderiza a tela de fim de jogo."""
        # Fundo semi-transparente
        s = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.tela.blit(s, (0, 0))
        
        # Mensagem de fim de jogo
        if self.resultado_jogo == "vitoria":
            mensagem = "VOCÊ VENCEU!"
            cor = VERDE
        else:
            palavras_str = ", ".join(self.palavras_chave_originais)
            mensagem = f"VOCÊ PERDEU! As palavras eram: {palavras_str}"
            cor = VERMELHO
        
        texto = FONTE_GRANDE.render(mensagem, True, cor)
        self.tela.blit(texto, (self.largura_tela // 2 - texto.get_width() // 2, self.altura_tela // 2 - 50))
        
        # Instruções
        instrucoes = FONTE_PEQUENA.render("Pressione ENTER para jogar novamente ou ESC para sair", True, BRANCO)
        self.tela.blit(instrucoes, (self.largura_tela // 2 - instrucoes.get_width() // 2, self.altura_tela // 2 + 20))
    
    def _renderizar_botao_home(self):
        """Renderiza o botão home (ícone de casa)."""
        # Desenha o botão
        pygame.draw.rect(self.tela, BRANCO, self.botao_home_rect)
        pygame.draw.rect(self.tela, CINZA_ESCURO, self.botao_home_rect, 2, border_radius=5)
        
        # Obter posições para o ícone da casa
        x, y = self.botao_home_rect.topleft
        largura, altura = self.botao_home_rect.size
        
        # Desenha um ícone de casa simples
        # Telhado da casa (triângulo)
        pygame.draw.polygon(self.tela, VERMELHO, [
            (x + largura/2, y + 5),           # topo
            (x + 5, y + altura/2 - 2),       # esquerda
            (x + largura - 5, y + altura/2 - 2)  # direita
        ])
        
        # Corpo da casa (retângulo)
        corpo_casa = pygame.Rect(
            x + 8, 
            y + altura/2 - 2, 
            largura - 16, 
            altura/2
        )
        pygame.draw.rect(self.tela, CINZA_ESCURO, corpo_casa)
        
        # Porta da casa
        porta = pygame.Rect(
            x + largura/2 - 5,
            y + altura - 15,
            10,
            12
        )
        pygame.draw.rect(self.tela, VERMELHO, porta)

# Função principal modificada para compatibilidade com Pygbag
async def main():
    """Função principal do jogo com compatibilidade para Pygbag."""
    pygame.init()
    pygame.font.init()
    
    # Tamanho inicial da tela
    tela = pygame.display.set_mode(TAMANHO_JANELA, pygame.RESIZABLE)
    pygame.display.set_caption("Termoo")
    
    # Estados do jogo
    estado_atual = "configuracao"
    tela_config = TelaConfiguracao(tela)
    jogo = None
    
    # Loop principal do jogo
    clock = pygame.time.Clock()
    rodando = True
    
    # Adiciona instruções no console
    print("Pressione F11 ou Alt+Enter para alternar entre modo janela e tela cheia")
    
    while rodando:
        if estado_atual == "configuracao":
            resultado = tela_config.processar_eventos()
            if resultado["acao"] == "sair":
                rodando = False
            elif resultado["acao"] == "iniciar_jogo":
                jogo = TermooPygame(resultado["config"])
                estado_atual = "jogo"
            
            tela_config.renderizar()
        
        elif estado_atual == "jogo":
            resultado = jogo.processar_eventos()
            if resultado == "sair":
                rodando = False
            elif resultado == "reiniciar":
                estado_atual = "configuracao"
                tela = pygame.display.get_surface()  # Obter a superfície atual
                tela_config = TelaConfiguracao(tela)
            
            jogo.renderizar()
        
        # Limita a quantidade de frames por segundo
        clock.tick(60)
        
        # Para compatibilidade com Pygbag
        await asyncio.sleep(0)

if __name__ == "__main__":
    if sys.platform == 'emscripten':
        # No navegador usando Pygbag
        asyncio.run(main())
    else:
        # Execução normal no desktop
        import asyncio  # Garante que asyncio está disponível em ambientes desktop
        try:
            asyncio.run(main())
        except (SystemExit, KeyboardInterrupt):
            pygame.quit()
