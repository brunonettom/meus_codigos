from datetime import datetime
import numpy as np
from wordfreq import word_frequency, top_n_list
from filtra_palavras import lista_de_palavras
import random
import unicodedata
import os
import pygame
import sys

# Import palavras (opcional, só se existir)
try:
    from lista_unificada_20_04_2025__20_32 import palavras as possiveis_palavras
except ImportError:
    # Fallback para lista simples se não encontrar o arquivo
    possiveis_palavras = ["casa", "bola", "gato", "pato", "mesa", "tela", "porta", "carro", 
                        "texto", "radio", "letra", "mundo", "tempo", "papel", "terra", 
                        "forno", "pedra", "linha", "claro", "video"]

# Inicialização do PyGame
pygame.init()

# Constantes
WIDTH, HEIGHT = 1200, 800
FPS = 60
PADDING = 20

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

class TermooPygame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Termoo - PyGame")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.big_font = pygame.font.SysFont('Arial', 32)
        
        # Variáveis para interface
        self.input_box = pygame.Rect(WIDTH // 4, HEIGHT - 100, WIDTH // 2, 50)
        self.input_active = False
        self.input_text = ""
        self.message = ""
        self.message_color = WHITE
        self.game_stage = "setup"  # "setup", "game", "end"
        self.current_setup_field = 0  # 0=n_palavras, 1=dificuldade, 2=n_letras, 3=n_chutes, 4=trapaca
        self.setup_values = [4, 50, 5, 9, "N"]  # valores default
        self.setup_prompts = [
            "Quantas palavras? (4)",
            "Qual é o nível de dificuldade desejada? (1 a 100%) (50%)",
            "Quantas letras por palavra? (5)",
            "Quantos chutes você quer? (9)",
            "Quer trapaça? (N/s)"
        ]
        
        # Variáveis do jogo
        self.palavrasChutadas = []
        self.nPalavras = None
        self.nLetras = None
        self.nChutesTotais = None
        self.nLinhasFaltantes = None
        self.lChavesEscolhidas = []
        self.palavrasErradas = []
        self.lChavesEscolhidasOriginais = []
        self.palavrasAcertadasConfere = []
        self.palavrasAcertadas = set()
        self.quer_trapaca = False
        self.running = True
        
    def remover_acentos(self, palavra):
        # Normaliza a palavra para decompor caracteres acentuados
        nfkd = unicodedata.normalize('NFD', palavra)
        # Remove os caracteres de marcação de acentuação
        sem_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        # Substitui 'ç' por 'c'
        sem_acentos = sem_acentos.replace('ç', 'c').replace('Ç', 'C')
        return sem_acentos
        
    def chavesEscolhidas(self):
        ChavesEscolhidas = []
        lPreChavesEscolhidas = [word.lower() for word in self.possiveisChaves if ' ' not in word and '-' not in word]
        
        # Garante que a lista lPreChavesEscolhidas tenha palavras suficientes para seleção
        if len(lPreChavesEscolhidas) < self.nPalavras:
            self.message = "Erro: Não há palavras suficientes para selecionar."
            return []

        for _ in range(self.nPalavras):
            sorteada = random.choice(lPreChavesEscolhidas)
            while len(sorteada) != self.nLetras or sorteada in ChavesEscolhidas:
                sorteada = random.choice(lPreChavesEscolhidas)

            ChavesEscolhidas.append(sorteada)

        self.lChavesEscolhidasOriginais0 = ChavesEscolhidas
        lChavesEscolhidas = [self.remover_acentos(palavra) for palavra in ChavesEscolhidas]
        return lChavesEscolhidas
        
    def conferir_chute(self, chute, chave):
        """Verifica o status de cada letra do chute em relação à chave"""
        if len(chute) != self.nLetras or len(chave) != self.nLetras:
            return [0] * self.nLetras, 0  # 0 = cinza
        
        # 0=cinza, 1=amarelo, 2=verde
        status_letras = [0] * self.nLetras
        letras_restantes = list(chave)
        
        # Primeiro marca verdes
        for i in range(self.nLetras):
            if chute[i] == chave[i]:
                status_letras[i] = 2
                if chute[i] in letras_restantes:
                    letras_restantes.remove(chute[i])
        
        # Depois marca amarelos
        for i in range(self.nLetras):
            if status_letras[i] == 0 and chute[i] in letras_restantes:
                status_letras[i] = 1
                letras_restantes.remove(chute[i])
                
        # Conta número de verdes
        return status_letras, status_letras.count(2)
    
    def handle_setup_input(self, event):
        """Processa a entrada durante a fase de configuração"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Valide e salve o valor
                if self.current_setup_field < 4:  # Campos numéricos
                    try:
                        val = self.input_text.strip()
                        if val:  # Se não estiver vazio
                            self.setup_values[self.current_setup_field] = int(val)
                    except ValueError:
                        pass  # Mantém o valor padrão se for inválido
                else:  # Campo sim/não
                    val = self.input_text.strip().lower()
                    if val in ["s", "y", "sim", "yes"]:
                        self.setup_values[4] = "S"
                
                # Avança para o próximo campo ou inicia o jogo
                self.input_text = ""
                self.current_setup_field += 1
                
                if self.current_setup_field >= len(self.setup_prompts):
                    self.start_game()
                    
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable():
                self.input_text += event.unicode
    
    def handle_game_input(self, event):
        """Processa a entrada durante o jogo"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.process_chute(self.input_text.lower())
                self.input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable():
                if len(self.input_text) < self.nLetras:
                    self.input_text += event.unicode
    
    def initialize_dictionaries(self, difficulty_level):
        """Inicializa os dicionários com base no nível de dificuldade"""
        try:
            self.dicionarioTodo = top_n_list('pt', 300000)
        except:
            self.dicionarioTodo = []
            
        try:
            # Use a dificuldade escolhida (0 a 1)
            difficulty = difficulty_level / 100.0
            self.possiveisChaves = lista_de_palavras(difficulty)
        except:
            self.possiveisChaves = possiveis_palavras
    
    def start_game(self):
        """Inicia o jogo com os valores configurados"""
        self.game_stage = "game"
        self.nPalavras = self.setup_values[0]
        self.nLetras = self.setup_values[2]
        self.nChutesTotais = self.setup_values[3]
        self.quer_trapaca = (self.setup_values[4] == "S")
        
        # Inicializa os dicionários
        self.initialize_dictionaries(self.setup_values[1])
        
        # Escolhe palavras aleatórias
        self.lChavesEscolhidas = self.chavesEscolhidas()
        self.lChavesEscolhidasOriginais = self.lChavesEscolhidas.copy()
        
        self.nLinhasFaltantes = self.nChutesTotais
        self.palavrasChutadas = []
        self.palavrasErradas = []
        self.palavrasAcertadasConfere = []
        self.palavrasAcertadas = set()
        self.input_text = ""
        self.message = "Jogo iniciado! Tente adivinhar as palavras."
        self.message_color = GREEN
    
    def process_chute(self, chute):
        """Processa um chute feito pelo jogador"""
        if not chute:
            self.message = "Por favor, digite um chute válido."
            self.message_color = YELLOW
            return
            
        if chute in ['desisto', 'q', 'quit', 'sair']:
            self.message = f"Você desistiu! As palavras eram: {', '.join(self.lChavesEscolhidasOriginais0)}"
            self.message_color = RED
            self.game_stage = "end"
            return
            
        if len(chute) != self.nLetras:
            self.message = f"Por favor, digite uma palavra com {self.nLetras} letras."
            self.message_color = YELLOW
            return
            
        # Verifica se a palavra existe no dicionário
        if not (chute in self.dicionarioTodo or chute in possiveis_palavras):
            self.message = "Palavra não encontrada no dicionário."
            self.message_color = RED
            return

        self.palavrasChutadas.append(chute)
        self.nLinhasFaltantes = self.nChutesTotais - len(self.palavrasChutadas)
        
        # Verifica se acertou alguma palavra
        if chute in self.lChavesEscolhidas:
            self.message = f"Parabéns! Você acertou a palavra '{chute}'!"
            self.message_color = GREEN
            self.palavrasAcertadasConfere.append(chute)
            self.lChavesEscolhidas.remove(chute)
            self.palavrasAcertadas.add(chute)
            
            if not self.lChavesEscolhidas:
                self.message = "PARABÉNS! VOCÊ ACERTOU TODAS AS PALAVRAS!"
                self.message_color = GREEN
                self.game_stage = "end"
        else:
            self.palavrasErradas.append(chute)
            self.message = f"Tente novamente! {self.nLinhasFaltantes} tentativas restantes."
            self.message_color = WHITE
        
        # Verifica se acabaram as tentativas
        if self.nLinhasFaltantes <= 0:
            self.message = f"Suas vidas acabaram! As palavras eram: {', '.join(self.lChavesEscolhidasOriginais0)}"
            self.message_color = RED
            self.game_stage = "end"
    
    def draw_setup_screen(self):
        """Desenha a tela de configuração"""
        self.screen.fill(BLACK)
        
        # Título
        title = self.big_font.render("TERMOO - Configuração do Jogo", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Prompt atual
        prompt = self.font.render(self.setup_prompts[self.current_setup_field], True, WHITE)
        self.screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//3))
        
        # Caixa de entrada
        pygame.draw.rect(self.screen, WHITE if self.input_active else GRAY, self.input_box, 2)
        input_surface = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(input_surface, (self.input_box.x + 5, self.input_box.y + 10))
        
        # Instruções
        instructions = self.small_font.render("Pressione ENTER para confirmar", True, GRAY)
        self.screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT//2 + 100))
    
    def draw_game_board(self):
        """Desenha o tabuleiro de jogo"""
        self.screen.fill(BLACK)
        
        # Título
        title = self.big_font.render("TERMOO", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        # Informações do jogo
        info_y = 70
        info_texts = [
            f"Tentativas restantes: {self.nLinhasFaltantes}",
            f"Palavras faltantes: {len(self.lChavesEscolhidas)}"
        ]
        
        if self.palavrasAcertadasConfere:
            info_texts.append(f"Palavras acertadas: {', '.join(p.upper() for p in self.palavrasAcertadasConfere)}")
        
        if self.palavrasErradas:
            info_texts.append(f"Palavras erradas: {', '.join(p.upper() for p in self.palavrasErradas)}")
        
        for text in info_texts:
            info_surf = self.small_font.render(text, True, WHITE)
            self.screen.blit(info_surf, (PADDING, info_y))
            info_y += 25
            
        # Se trapaça ativada, mostrar palavras
        if self.quer_trapaca:
            cheat_text = self.small_font.render(f"CHAVES: {self.lChavesEscolhidas}", True, RED)
            self.screen.blit(cheat_text, (PADDING, info_y))
            info_y += 25
            
        # Desenha tabuleiro de jogo
        self.draw_word_grid()
        
        # Status do alfabeto
        self.draw_alphabet_status()
        
        # Área de entrada
        pygame.draw.rect(self.screen, WHITE if self.input_active else GRAY, self.input_box, 2)
        input_surface = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(input_surface, (self.input_box.x + 5, self.input_box.y + 10))
        
        # Mensagem
        message_surf = self.font.render(self.message, True, self.message_color)
        self.screen.blit(message_surf, (WIDTH//2 - message_surf.get_width()//2, HEIGHT - 40))
    
    def draw_word_grid(self):
        """Desenha a grade de palavras e chutes"""
        # Calcular largura da célula
        cell_width = 40
        cell_height = 40
        grid_padding = 10
        
        start_y = 150
        
        # Para cada palavra (coluna)
        for col_idx, chave in enumerate(self.lChavesEscolhidasOriginais):
            start_x = PADDING + col_idx * ((cell_width * self.nLetras) + 40)
            
            # Se já acertou essa palavra, marca toda em verde
            if chave in self.palavrasAcertadas:
                for row_idx in range(self.nChutesTotais):
                    for letter_idx in range(self.nLetras):
                        # Desenha células preenchidas para palavras acertadas
                        rect = pygame.Rect(
                            start_x + letter_idx * cell_width, 
                            start_y + row_idx * cell_height, 
                            cell_width - grid_padding, 
                            cell_height - grid_padding
                        )
                        
                        if row_idx < len(self.palavrasChutadas):
                            # Só pinta de verde se for a palavra acertada
                            if self.palavrasChutadas[row_idx] == chave:
                                pygame.draw.rect(self.screen, GREEN, rect)
                                letra = self.font.render(chave[letter_idx].upper(), True, BLACK)
                                self.screen.blit(letra, (rect.x + 10, rect.y + 5))
                            else:
                                # Para chutes anteriores, usa o esquema normal
                                status, _ = self.conferir_chute(self.palavrasChutadas[row_idx], chave)
                                color = {0: DARK_GRAY, 1: YELLOW, 2: GREEN}[status[letter_idx]]
                                pygame.draw.rect(self.screen, color, rect)
                                letra = self.font.render(self.palavrasChutadas[row_idx][letter_idx].upper(), True, WHITE)
                                self.screen.blit(letra, (rect.x + 10, rect.y + 5))
                        else:
                            # Célula vazia para linhas futuras
                            pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
            else:
                # Para palavras não acertadas, mostra o status de cada letra
                for row_idx in range(self.nChutesTotais):
                    for letter_idx in range(self.nLetras):
                        rect = pygame.Rect(
                            start_x + letter_idx * cell_width, 
                            start_y + row_idx * cell_height, 
                            cell_width - grid_padding, 
                            cell_height - grid_padding
                        )
                        
                        if row_idx < len(self.palavrasChutadas):
                            # Célula com chute
                            status, _ = self.conferir_chute(self.palavrasChutadas[row_idx], chave)
                            color = {0: DARK_GRAY, 1: YELLOW, 2: GREEN}[status[letter_idx]]
                            pygame.draw.rect(self.screen, color, rect)
                            letra = self.font.render(self.palavrasChutadas[row_idx][letter_idx].upper(), True, WHITE)
                            self.screen.blit(letra, (rect.x + 10, rect.y + 5))
                        else:
                            # Célula vazia
                            pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
    
    def draw_alphabet_status(self):
        """Desenha o status de cada letra do alfabeto"""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        letters_per_row = 13
        start_x = WIDTH // 4
        start_y = HEIGHT - 180
        rect_size = 25
        
        for i, letter in enumerate(alphabet):
            row = i // letters_per_row
            col = i % letters_per_row
            
            x = start_x + col * (rect_size + 5)
            y = start_y + row * (rect_size + 5)
            
            # Determina a cor da letra
            color = DARK_GRAY  # padrão para não usadas
            
            # Se a letra foi usada em algum chute
            if any(letter in chute for chute in self.palavrasChutadas):
                # Verifica se está em alguma posição correta (verde)
                if any(chute[i] == letter and chave[i] == letter 
                       for chute in self.palavrasChutadas 
                       for i in range(self.nLetras) 
                       for chave in self.lChavesEscolhidasOriginais):
                    color = GREEN
                # Verifica se está em posição errada (amarelo)
                elif any(letter in chave for chave in self.lChavesEscolhidasOriginais):
                    color = YELLOW
                else:
                    color = RED  # não está em nenhuma palavra
            
            # Desenha o quadrado com a letra
            rect = pygame.Rect(x, y, rect_size, rect_size)
            pygame.draw.rect(self.screen, color, rect)
            letra_surf = self.small_font.render(letter.upper(), True, WHITE if color != GREEN else BLACK)
            self.screen.blit(letra_surf, (x + 5, y + 3))
    
    def draw_end_screen(self):
        """Desenha a tela final do jogo"""
        self.screen.fill(BLACK)
        
        # Título
        title = self.big_font.render("FIM DE JOGO", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Mensagem
        message_surf = self.font.render(self.message, True, self.message_color)
        self.screen.blit(message_surf, (WIDTH//2 - message_surf.get_width()//2, 200))
        
        # Palavras
        if self.lChavesEscolhidasOriginais0:
            words_text = self.font.render(f"Palavras: {', '.join(self.lChavesEscolhidasOriginais0)}", True, WHITE)
            self.screen.blit(words_text, (WIDTH//2 - words_text.get_width()//2, 250))
        
        # Instrução para reiniciar
        restart = self.font.render("Pressione R para jogar novamente", True, WHITE)
        self.screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 350))
        
        # Instrução para sair
        quit_text = self.font.render("Pressione ESC para sair", True, WHITE)
        self.screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 400))
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Input box activation
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                
                # Keyboard input handling
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    # Restart game in end screen
                    elif self.game_stage == "end" and event.key == pygame.K_r:
                        self.game_stage = "setup"
                        self.current_setup_field = 0
                        self.input_text = ""
                    
                    # Handle input based on game stage
                    elif self.input_active:
                        if self.game_stage == "setup":
                            self.handle_setup_input(event)
                        elif self.game_stage == "game":
                            self.handle_game_input(event)
            
            # Drawing based on game stage
            if self.game_stage == "setup":
                self.draw_setup_screen()
            elif self.game_stage == "game":
                self.draw_game_board()
            elif self.game_stage == "end":
                self.draw_end_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TermooPygame()
    game.run()
