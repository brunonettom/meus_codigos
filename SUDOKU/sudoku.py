import pygame
import random
import time
import math  # Novo import para funções matemáticas

# Inicializando o pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (96, 216, 232)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GRAY = (100, 100, 100)
HIGHLIGHT_GRAY = (150, 150, 220)  # Cor para destacar anotações

# Configurações iniciais da tela
INITIAL_WIDTH, INITIAL_HEIGHT = 540, 600
MIN_WIDTH, MIN_HEIGHT = 540, 600  # Tamanhos mínimos da janela

# Configuração da janela redimensionável
screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sudoku")

# Variáveis globais para dimensões atuais da tela
WIDTH, HEIGHT = INITIAL_WIDTH, INITIAL_HEIGHT
GRID_SIZE = 9
# Controle de exibição do tabuleiro
board_offset_x = 0
board_offset_y = 0
MAX_CELL_SIZE = 80  # Tamanho máximo para as células
MIN_CELL_SIZE = 40  # Tamanho mínimo para as células
CELL_SIZE = WIDTH // GRID_SIZE  # Será recalculado em update_dimensions
FONT_SIZE = 36
STATUS_BAR_HEIGHT = 60

# Fontes - serão redefinidas em update_dimensions
font = pygame.font.SysFont("Arial", FONT_SIZE)
small_font = pygame.font.SysFont("Arial", 20)
medium_font = pygame.font.SysFont("Arial", 28)
large_font = pygame.font.SysFont("Arial", 42)

# Mapeamento de teclas numéricas para valores
NUMERIC_KEYS = {
    pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4,
    pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9,
    pygame.K_KP0: 0, pygame.K_KP1: 1, pygame.K_KP2: 2, pygame.K_KP3: 3, pygame.K_KP4: 4,
    pygame.K_KP5: 5, pygame.K_KP6: 6, pygame.K_KP7: 7, pygame.K_KP8: 8, pygame.K_KP9: 9
}

# Teclas de navegação
ARROW_KEYS = {
    pygame.K_UP: (-1, 0),     # Cima
    pygame.K_DOWN: (1, 0),    # Baixo
    pygame.K_LEFT: (0, -1),   # Esquerda
    pygame.K_RIGHT: (0, 1),   # Direita
    pygame.K_w: (-1, 0),      # W - Cima
    pygame.K_s: (1, 0),       # S - Baixo
    pygame.K_a: (0, -1),      # A - Esquerda
    pygame.K_d: (0, 1)        # D - Direita
}

# Botão de dicas
HINT_BUTTON = pygame.Rect(WIDTH // 2 - 70, HEIGHT - STATUS_BAR_HEIGHT + 15, 140, 30)
# Botão de dica única
SOLVE_HINT_BUTTON = pygame.Rect(WIDTH // 2 - 70 - 150, HEIGHT - STATUS_BAR_HEIGHT + 15, 140, 30)

# Estado das dicas
HINTS_ENABLED = False

# Auto highlight quando o cursor passa sobre números
AUTO_HIGHLIGHT = True

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3  # Novo estado para tela de vitória
HINT_MODE = 4  # Novo estado para modo de seleção de dica
FULLSCREEN = False  # Estado para controlar tela cheia

# Imagem de coração (vida)
heart_img = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.polygon(heart_img, RED, [(15, 5), (25, 15), (15, 25), (5, 15)])

class Sudoku:
    def __init__(self, difficulty='medium'):
        # Tabuleiro inicial com zeros (células vazias)
        self.board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.original_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected_cell = None
        self.notes = [[set() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.highlight_number = None
        self.lives = 3
        self.difficulty = difficulty
        self.solution = None
        self.saved_notes = None  # Para guardar o estado anterior das dicas
        
        # Histórico para undo/redo
        self.history = []
        self.future = []
        
        # Primeiro gera o puzzle, depois salva o estado inicial
        self.generate_puzzle()
        self.save_state()  # Salva o estado inicial após gerar o puzzle, não antes
    
    def is_valid(self, row, col, num):
        # Verifica se o número é válido na linha
        for x in range(GRID_SIZE):
            if self.board[row][x] == num:
                return False
                
        # Verifica se o número é válido na coluna
        for x in range(GRID_SIZE):
            if self.board[x][col] == num:
                return False
                
        # Verifica se o número é válido no quadrante 3x3
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + startRow][j + startCol] == num:
                    return False
        return True
    
    def solve(self, board=None):
        if board is None:
            board = [[self.board[row][col] for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
            
        # Encontra uma célula vazia (com valor 0)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == 0:
                    # Tenta colocar um número de 1 a 9
                    for num in range(1, 10):
                        # Verifica se o número é válido nesta posição
                        if self._is_valid_num(board, row, col, num):
                            board[row][col] = num
                            
                            # Recursivamente tenta preencher o resto do tabuleiro
                            if self.solve(board):
                                return board
                            
                            # Se não der, volta atrás
                            board[row][col] = 0
                    
                    # Nenhum número funcionou, então retorna False
                    return None
        
        # Se chegou aqui, todas as células foram preenchidas com sucesso
        return board
    
    def _is_valid_num(self, board, row, col, num):
        # Verifica linha
        for x in range(GRID_SIZE):
            if board[row][x] == num:
                return False
        
        # Verifica coluna
        for x in range(GRID_SIZE):
            if board[x][col] == num:
                return False
        
        # Verifica caixa 3x3
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
                    
        return True
    
    def generate_puzzle(self):
        # Cria um tabuleiro resolvido
        solved_board = self.solve([[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])
        if solved_board:
            # Salva a solução completa
            self.solution = [row[:] for row in solved_board]
            self.board = [row[:] for row in solved_board]
            
            # Remove números para criar o puzzle com base na dificuldade
            cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
            random.shuffle(cells)
            
            # Define o número de células vazias com base na dificuldade
            removed_cells = {
                'easy': random.randint(30, 35),
                'medium': random.randint(45, 50),
                'hard': random.randint(55, 60)
            }
            
            for i, j in cells[:removed_cells[self.difficulty]]:
                self.board[i][j] = 0
                
            # Salva o tabuleiro original para verificar quais células são editáveis
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    self.original_board[i][j] = self.board[i][j]

    def is_complete(self):
        # Verifica se o tabuleiro está preenchido corretamente
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 0:
                    return False
                
                # Temporariamente remove o número para verificar sua validade
                temp = self.board[row][col]
                self.board[row][col] = 0
                if not self.is_valid(row, col, temp):
                    self.board[row][col] = temp
                    return False
                self.board[row][col] = temp
                
        return True

    def lose_life(self):
        self.lives -= 1
        return self.lives <= 0

    def update_notes(self):
        """Atualiza automaticamente as anotações de todas as células"""
        # Percorre todas as células do tabuleiro
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Pula células já preenchidas
                if self.board[row][col] != 0:
                    self.notes[row][col].clear()
                    continue
                
                # Se a célula está vazia, atualiza suas anotações
                # Primeiro verifica se já tem anotações, caso não tenha, adiciona todas possibilidades
                if not self.notes[row][col]:
                    self.notes[row][col] = set(range(1, 10))
                
                # Remove números que já aparecem na linha, coluna ou quadrado 3x3
                # Linha
                for x in range(GRID_SIZE):
                    if self.board[row][x] != 0 and self.board[row][x] in self.notes[row][col]:
                        self.notes[row][col].remove(self.board[row][x])
                
                # Coluna
                for x in range(GRID_SIZE):
                    if self.board[x][col] != 0 and self.board[x][col] in self.notes[row][col]:
                        self.notes[row][col].remove(self.board[x][col])
                
                # Quadrado 3x3
                start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                for i in range(3):
                    for j in range(3):
                        r, c = start_row + i, start_col + j
                        if self.board[r][c] != 0 and self.board[r][c] in self.notes[row][col]:
                            self.notes[row][col].remove(self.board[r][c])

    def save_state(self):
        """Salva o estado atual do tabuleiro e notas no histórico"""
        # Copia o tabuleiro atual e as notas
        board_copy = [row[:] for row in self.board]
        notes_copy = [[self.notes[row][col].copy() for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
        
        # Adiciona ao histórico
        self.history.append({
            'board': board_copy,
            'notes': notes_copy,
            'hints_enabled': HINTS_ENABLED  # Salva também o estado das dicas
        })
        
        # Limpa o futuro ao fazer uma nova ação
        self.future = []
        
        # Limita o tamanho do histórico para evitar uso excessivo de memória
        if len(self.history) > 100:
            self.history.pop(0)

    def undo(self):
        """Desfaz a última jogada"""
        global HINTS_ENABLED
        
        if len(self.history) <= 1:
            return False  # Não há o que desfazer
        
        # Move o estado atual para o futuro
        current_state = self.history.pop()
        self.future.append(current_state)
        
        # Restaura o estado anterior
        previous_state = self.history[-1]
        self.board = [row[:] for row in previous_state['board']]
        self.notes = [[previous_state['notes'][row][col].copy() for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
        
        # Restaura o estado das dicas se estiver armazenado
        if 'hints_enabled' in previous_state:
            HINTS_ENABLED = previous_state['hints_enabled']
        
        return True

    def redo(self):
        """Refaz a última jogada desfeita"""
        global HINTS_ENABLED
        
        if not self.future:
            return False  # Não há o que refazer
        
        # Restaura o próximo estado
        next_state = self.future.pop()
        self.history.append(next_state)
        
        # Aplica o estado
        self.board = [row[:] for row in next_state['board']]
        self.notes = [[next_state['notes'][row][col].copy() for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
        
        # Restaura o estado das dicas se estiver armazenado
        if 'hints_enabled' in next_state:
            HINTS_ENABLED = next_state['hints_enabled']
        
        return True

    def toggle_notes(self):
        """Alterna entre mostrar e esconder as dicas"""
        global HINTS_ENABLED
        
        # Salvar o estado antes de alterá-lo
        self.save_state()
        
        if not HINTS_ENABLED:  # Se as dicas estiverem desativadas, vamos ativá-las
            # Guarda o estado atual das anotações
            self.saved_notes = [[self.notes[row][col].copy() for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
            # Atualiza as anotações conforme as regras do Sudoku
            self.update_notes()
            HINTS_ENABLED = True
        else:  # Se as dicas estiverem ativadas, vamos desativá-las
            # Restaura o estado anterior das anotações, se disponível
            if self.saved_notes is not None:
                self.notes = [[self.saved_notes[row][col].copy() for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
            else:
                # Limpa todas as anotações se não houver estado salvo
                self.notes = [[set() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            HINTS_ENABLED = False
            
    # Adicionar método para atualizar as dicas quando necessário
    def update_if_hints_enabled(self):
        """Atualiza as dicas automaticamente se estiverem habilitadas"""
        if HINTS_ENABLED:
            self.update_notes()

    def get_hint(self, row=None, col=None):
        """Fornece uma dica preenchendo uma célula vazia com o valor correto"""
        # Se row e col forem fornecidos, dá dica para célula específica
        if row is not None and col is not None:
            if self.board[row][col] == 0:  # Verifica se a célula está vazia
                self.save_state()  # Salva o estado para poder desfazer
                self.board[row][col] = self.solution[row][col]
                self.notes[row][col].clear()
                self.update_if_hints_enabled()
                return (row, col, self.solution[row][col])
            return False  # Célula não está vazia
            
        # Comportamento original - escolhe célula aleatória
        empty_cells = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == 0:
                    empty_cells.append((r, c))
        
        if not empty_cells:
            return False  # Não há células vazias
            
        # Escolhe uma célula vazia aleatória
        r, c = random.choice(empty_cells)
        
        # Preenche com o valor correto
        self.save_state()
        self.board[r][c] = self.solution[r][c]
        self.notes[r][c].clear()
        self.update_if_hints_enabled()
        
        return (r, c, self.solution[r][c])

def update_dimensions(new_width, new_height):
    """Atualiza as dimensões da janela e recalcula outros valores dependentes"""
    global WIDTH, HEIGHT, CELL_SIZE, HINT_BUTTON, SOLVE_HINT_BUTTON, board_offset_x, board_offset_y, font, small_font, medium_font, large_font, FONT_SIZE
    
    WIDTH = max(new_width, MIN_WIDTH)
    HEIGHT = max(new_height, MIN_HEIGHT)
    
    # Calcula o tamanho da célula baseado no espaço disponível
    available_size_x = WIDTH // GRID_SIZE
    available_size_y = (HEIGHT - STATUS_BAR_HEIGHT) // GRID_SIZE
    
    # Determina o tamanho da célula (mantendo-o quadrado)
    CELL_SIZE = min(available_size_x, available_size_y)
    
    # Limita o tamanho da célula entre mínimo e máximo
    CELL_SIZE = max(min(CELL_SIZE, MAX_CELL_SIZE), MIN_CELL_SIZE)
    
    # Calcula os offsets para centralizar o tabuleiro
    board_width = CELL_SIZE * GRID_SIZE
    board_height = CELL_SIZE * GRID_SIZE
    board_offset_x = (WIDTH - board_width) // 2
    board_offset_y = ((HEIGHT - STATUS_BAR_HEIGHT) - board_height) // 2
    
    # Recalcula o tamanho da fonte baseado no tamanho da célula
    FONT_SIZE = int(CELL_SIZE * 0.6)  # 60% do tamanho da célula
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    small_font = pygame.font.SysFont("Arial", max(int(CELL_SIZE * 0.2), 12))
    medium_font = pygame.font.SysFont("Arial", int(CELL_SIZE * 0.4))
    large_font = pygame.font.SysFont("Arial", int(CELL_SIZE * 0.8))
    
    # Recalcula a posição dos botões - centralizados na barra de status
    button_width = 140
    button_height = 30
    button_spacing = 20  # Espaço entre os botões
    
    # Botão de dicas (à direita)
    HINT_BUTTON = pygame.Rect(
        (WIDTH // 2) + button_spacing//2, 
        HEIGHT - STATUS_BAR_HEIGHT + (STATUS_BAR_HEIGHT - button_height) // 2, 
        button_width, 
        button_height
    )
    
    # Botão de dica única (à esquerda)
    SOLVE_HINT_BUTTON = pygame.Rect(
        (WIDTH // 2) - button_width - button_spacing//2, 
        HEIGHT - STATUS_BAR_HEIGHT + (STATUS_BAR_HEIGHT - button_height) // 2, 
        button_width, 
        button_height
    )

    # Também recria as fontes com tamanhos proporcionais à tela para maior responsividade
    title_font_size = int(min(WIDTH, HEIGHT) * 0.08)  # 8% da dimensão menor da tela
    large_font = pygame.font.SysFont("Arial", title_font_size)
    
    medium_font_size = int(min(WIDTH, HEIGHT) * 0.045)  # 4.5% da dimensão menor da tela
    medium_font = pygame.font.SysFont("Arial", medium_font_size)
    
# Chame update_dimensions imediatamente para calcular os valores iniciais
update_dimensions(INITIAL_WIDTH, INITIAL_HEIGHT)

def toggle_fullscreen():
    """Alterna entre modo janela e tela cheia"""
    global FULLSCREEN, screen, WIDTH, HEIGHT
    
    FULLSCREEN = not FULLSCREEN
    
    if FULLSCREEN:
        # Guarda as dimensões atuais da janela antes de entrar em tela cheia
        window_info = pygame.display.Info()
        stored_width, stored_height = window_info.current_w, window_info.current_h
        
        # Muda para tela cheia
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        # Atualiza dimensões para o tamanho da tela cheia
        window_info = pygame.display.Info()
        update_dimensions(window_info.current_w, window_info.current_h)
    else:
        # Volta para o modo janela
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

def draw_grid():
    # Desenha as linhas do grid
    for i in range(GRID_SIZE + 1):
        line_width = 3 if i % 3 == 0 else 1
        
        # Linha horizontal
        pygame.draw.line(screen, BLACK, 
                        (board_offset_x, board_offset_y + i * CELL_SIZE), 
                        (board_offset_x + GRID_SIZE * CELL_SIZE, board_offset_y + i * CELL_SIZE), 
                        line_width)
        
        # Linha vertical
        pygame.draw.line(screen, BLACK, 
                        (board_offset_x + i * CELL_SIZE, board_offset_y), 
                        (board_offset_x + i * CELL_SIZE, board_offset_y + GRID_SIZE * CELL_SIZE), 
                        line_width)

def draw_numbers(sudoku):
    # Desenha os números no tabuleiro
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = sudoku.board[row][col]
            note = sudoku.notes[row][col]
            highlight = (sudoku.highlight_number is not None and value == sudoku.highlight_number)
            
            # Cor azul se for número destacado
            if value != 0:
                if highlight:
                    color = LIGHT_BLUE
                else:
                    color = BLACK if sudoku.original_board[row][col] != 0 else (0, 100, 200)
                num_surface = font.render(str(value), True, color)
                x = board_offset_x + col * CELL_SIZE + (CELL_SIZE - num_surface.get_width()) // 2
                y = board_offset_y + row * CELL_SIZE + (CELL_SIZE - num_surface.get_height()) // 2
                screen.blit(num_surface, (x, y))
            elif note:
                # Ajusta tamanho da fonte para anotações baseado no tamanho da célula
                note_font_size = max(int(CELL_SIZE * 0.2), 10)  # 20% do tamanho da célula, mínimo 10px
                note_font = pygame.font.SysFont("Arial", note_font_size)
                
                # Desenha as anotações pequenas
                notes_text = ""
                for n in range(1, 10):
                    if n in note:
                        notes_text += str(n)
                    else:
                        notes_text += " "
                        
                for idx, n in enumerate(notes_text):
                    if n != " ":
                        # Verifica se a anotação deve ser destacada
                        note_color = HIGHLIGHT_GRAY if sudoku.highlight_number is not None and int(n) == sudoku.highlight_number else GRAY
                        note_surface = note_font.render(n, True, note_color)
                        
                        # Posição exata dentro da célula para cada anotação
                        cell_third = CELL_SIZE / 3
                        nx = board_offset_x + col * CELL_SIZE + (idx % 3) * cell_third + (cell_third - note_surface.get_width()) / 2
                        ny = board_offset_y + row * CELL_SIZE + (idx // 3) * cell_third + (cell_third - note_surface.get_height()) / 2
                        
                        # Opcional: desenha um fundo para destacar ainda mais as anotações
                        if sudoku.highlight_number is not None and int(n) == sudoku.highlight_number:
                            note_rect = note_surface.get_rect(topleft=(nx, ny))
                            note_rect.inflate_ip(2, 2)  # Aumenta ligeiramente o tamanho do retângulo
                            pygame.draw.rect(screen, (230, 230, 255), note_rect)  # Fundo claro para destacar
                            
                        screen.blit(note_surface, (nx, ny))

def draw_selected_cell(pos, sudoku):
    # Destaca a célula selecionada
    if pos:
        # Ajusta as coordenadas com base no offset do tabuleiro
        adjusted_x = pos[0] - board_offset_x
        adjusted_y = pos[1] - board_offset_y
        
        # Verifica se o clique foi dentro do tabuleiro
        if 0 <= adjusted_x <= CELL_SIZE * GRID_SIZE and 0 <= adjusted_y <= CELL_SIZE * GRID_SIZE:
            col = adjusted_x // CELL_SIZE
            row = adjusted_y // CELL_SIZE
            
            # Verifica se a posição está dentro do tabuleiro
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                # Se a posição tem um número, destaca todos os números iguais
                value = sudoku.board[row][col]
                if value != 0 and AUTO_HIGHLIGHT:
                    sudoku.highlight_number = value
                
                # Se a célula é editável, destaca com cor azul claro
                if sudoku.original_board[row][col] == 0:
                    pygame.draw.rect(screen, LIGHT_BLUE, 
                                    (board_offset_x + col * CELL_SIZE, board_offset_y + row * CELL_SIZE, 
                                     CELL_SIZE, CELL_SIZE), 4)
                    return (row, col)
                # Se a célula não é editável (número fixo), destaca com uma cor diferente
                else:
                    pygame.draw.rect(screen, DARK_GRAY, 
                                    (board_offset_x + col * CELL_SIZE, board_offset_y + row * CELL_SIZE, 
                                     CELL_SIZE, CELL_SIZE), 2)
                    return None
    return None

def draw_status_bar(message, color=BLACK, hint_mode=False):
    # Desenha a barra de status na parte inferior da tela com um fundo limpo
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - STATUS_BAR_HEIGHT, WIDTH, STATUS_BAR_HEIGHT))
    
    # Texto da mensagem principal (à esquerda)
    if message:
        # Limita o tamanho da mensagem para não sobrepor os botões
        max_message_width = min(SOLVE_HINT_BUTTON.left - 20, WIDTH // 3)
        
        # Se a mensagem for muito longa, corta ou reduz o tamanho da fonte
        status_text = small_font.render(message, True, color)
        if status_text.get_width() > max_message_width:
            # Tenta reduzir o tamanho da fonte
            smaller_font = pygame.font.SysFont("Arial", small_font.get_height() - 2)
            status_text = smaller_font.render(message, True, color)
            
            # Se ainda for muito grande, corta a mensagem
            if status_text.get_width() > max_message_width:
                # Encontra quantos caracteres cabem
                char_width = status_text.get_width() / len(message)
                chars_that_fit = int(max_message_width / char_width) - 3  # -3 para "..."
                message = message[:chars_that_fit] + "..."
                status_text = smaller_font.render(message, True, color)
        
        screen.blit(status_text, (10, HEIGHT - STATUS_BAR_HEIGHT + (STATUS_BAR_HEIGHT - status_text.get_height()) // 2))
    
    # Desenha o botão de dicas com texto apropriado
    button_color = LIGHT_BLUE if not HINTS_ENABLED else (150, 255, 150)  # Verde claro se ativado
    pygame.draw.rect(screen, button_color, HINT_BUTTON)
    pygame.draw.rect(screen, BLACK, HINT_BUTTON, 2)
    
    hint_text = small_font.render("Dicas " + ("ON" if HINTS_ENABLED else "OFF"), True, BLACK)
    screen.blit(hint_text, (HINT_BUTTON.centerx - hint_text.get_width() // 2, 
                           HINT_BUTTON.centery - hint_text.get_height() // 2))
    
    # Desenha o botão de dica única (com texto alterado se estiver no modo de dica)
    hint_button_color = (255, 180, 100) if hint_mode else (255, 220, 100)  # Laranja mais forte no modo de dica
    pygame.draw.rect(screen, hint_button_color, SOLVE_HINT_BUTTON)
    pygame.draw.rect(screen, BLACK, SOLVE_HINT_BUTTON, 2)
    
    solve_text = small_font.render("Clique em uma célula" if hint_mode else "Pedir Dica", True, BLACK)
    screen.blit(solve_text, (SOLVE_HINT_BUTTON.centerx - solve_text.get_width() // 2, 
                            SOLVE_HINT_BUTTON.centery - solve_text.get_height() // 2))
    
    # Removido o texto "F11: Tela Cheia" da interface

def draw_menu():
    """
    Desenha a tela de menu completamente responsiva e centralizada
    independentemente do tamanho da janela
    """
    screen.fill(WHITE)
    
    # Recalcula as fontes para o menu específicamente, garantindo melhor responsividade
    title_font_size = int(min(WIDTH, HEIGHT) * 0.08)
    title_font = pygame.font.SysFont("Arial", title_font_size)
    
    instruction_font_size = int(min(WIDTH, HEIGHT) * 0.045)
    instruction_font = pygame.font.SysFont("Arial", instruction_font_size)
    
    button_font_size = int(min(WIDTH, HEIGHT) * 0.04)
    button_font = pygame.font.SysFont("Arial", button_font_size)
    
    # Calcula as dimensões dos elementos
    button_width = min(WIDTH * 0.6, 400)  # Limitado para não ficar muito largo
    button_height = min(HEIGHT * 0.08, 60)  # Limitado para não ficar muito alto
    
    # Espaçamento vertical entre os elementos
    vertical_spacing = HEIGHT * 0.05
    
    # Calcula proporcionalmente o espaçamento entre botões
    button_spacing = min(HEIGHT * 0.03, 30)
    
    # Título centralizado
    title = title_font.render("SUDOKU", True, BLACK)
    
    # Instruções centralizadas
    instructions = instruction_font.render("Selecione a dificuldade", True, DARK_GRAY)
    
    # Calcula a altura total do conteúdo
    total_content_height = (title.get_height() + instructions.get_height() + 
                           (3 * button_height) + (2 * button_spacing) + (2 * vertical_spacing))
    
    # Posição inicial Y para centralizar todo o conteúdo verticalmente
    start_y = (HEIGHT - total_content_height) / 2
    
    # Renderiza o título
    title_y = start_y
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, title_y))
    
    # Renderiza as instruções
    instructions_y = title_y + title.get_height() + vertical_spacing
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, instructions_y))
    
    # Inicializa o ponto de partida dos botões
    button_start_y = instructions_y + instructions.get_height() + vertical_spacing
    
    # Prepara as opções de dificuldade
    difficulties = ['easy', 'medium', 'hard']
    difficulty_texts = ['Fácil', 'Médio', 'Difícil']
    button_rects = []
    
    # Desenha cada botão centralizado
    for i, (diff, text) in enumerate(zip(difficulties, difficulty_texts)):
        # Posição Y com espaçamento adequado
        y_pos = button_start_y + i * (button_height + button_spacing)
        
        # Cria um retângulo para o botão centralizado na tela
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, y_pos, button_width, button_height)
        button_rects.append(button_rect)
        
        # Desenha o botão
        pygame.draw.rect(screen, LIGHT_BLUE, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        
        # Texto do botão centralizado
        diff_text = button_font.render(text, True, BLACK)
        screen.blit(diff_text, (button_rect.centerx - diff_text.get_width() // 2, 
                               button_rect.centery - diff_text.get_height() // 2))
    
    # Retorna uma lista com os botões e suas dificuldades
    return [(diff, rect) for diff, rect in zip(difficulties, button_rects)]

def draw_lives(sudoku):
    # Desenha os corações representando as vidas (no canto superior direito)
    heart_x_start = WIDTH - 130  # Corrigido: Afastado mais à direita para evitar sobreposição
    heart_y = HEIGHT - STATUS_BAR_HEIGHT + (STATUS_BAR_HEIGHT - heart_img.get_height()) // 2
    
    for i in range(3):
        if i < sudoku.lives:
            screen.blit(heart_img, (heart_x_start + i * 35, heart_y))
        else:
            # Coração vazio (contorno)
            pygame.draw.polygon(screen, RED, 
                [(heart_x_start + i * 35 + 15, heart_y + 5),
                 (heart_x_start + i * 35 + 25, heart_y + 15),
                 (heart_x_start + i * 35 + 15, heart_y + 25),
                 (heart_x_start + i * 35 + 5, heart_y + 15)], 1)

def draw_game_over(sudoku):
    # Desenha uma camada semitransparente sobre o jogo
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Mensagem de game over centralizada vertical e horizontalmente
    game_over_text = large_font.render("GAME OVER", True, RED)
    game_over_y = HEIGHT * 0.15  # Posição baseada em porcentagem da altura
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, game_over_y))
    
    # Instruções
    press_any_key = small_font.render("Pressione qualquer tecla para voltar ao menu", True, WHITE)
    screen.blit(press_any_key, (WIDTH // 2 - press_any_key.get_width() // 2, game_over_y + 50))
    
    # Mostra a solução correta
    solution_text = medium_font.render("Solução:", True, WHITE)
    solution_y = game_over_y + 100
    screen.blit(solution_text, (WIDTH // 2 - solution_text.get_width() // 2, solution_y))
    
    # Calcula o tamanho apropriado para o tabuleiro de solução
    available_height = HEIGHT - solution_y - 50
    solution_cell_size = min(available_height / 9, WIDTH / 12)  # Garante que caiba na tela
    
    # Desenha o tabuleiro resolvido em tamanho apropriado
    solution_grid_size = solution_cell_size * 9
    solution_x = WIDTH // 2 - solution_grid_size // 2
    solution_y += 30  # Espaço abaixo do texto "Solução:"
    
    for i in range(9):
        for j in range(9):
            value = sudoku.solution[i][j]
            # Calcula posição para tabuleiro centralizado
            x = solution_x + j * solution_cell_size
            y = solution_y + i * solution_cell_size
            
            # Fundo da célula para melhorar visibilidade
            pygame.draw.rect(screen, (50, 50, 50), 
                            (x, y, solution_cell_size, solution_cell_size))
            
            # Desenha o número em fonte apropriada
            font_size = int(solution_cell_size * 0.6)
            mini_font = pygame.font.SysFont("Arial", font_size)
            num_surface = mini_font.render(str(value), True, WHITE)
            screen.blit(num_surface, (x + (solution_cell_size - num_surface.get_width()) // 2, 
                                     y + (solution_cell_size - num_surface.get_height()) // 2))
            
    # Desenha as linhas da grade
    for i in range(10):
        line_width = 2 if i % 3 == 0 else 1
        pygame.draw.line(screen, WHITE, 
                        (solution_x + i * solution_cell_size, solution_y), 
                        (solution_x + i * solution_cell_size, solution_y + 9 * solution_cell_size), line_width)
        pygame.draw.line(screen, WHITE, 
                        (solution_x, solution_y + i * solution_cell_size), 
                        (solution_x + 9 * solution_cell_size, solution_y + i * solution_cell_size), line_width)

def draw_victory_screen(sudoku):
    """Desenha a tela de vitória quando o jogador completa o sudoku corretamente"""
    # Desenha uma camada semitransparente verde sobre o jogo
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 100, 0, 180))  # Verde escuro semitransparente
    screen.blit(overlay, (0, 0))
    
    # Calcula proporções e espaçamentos responsivos
    top_margin = HEIGHT * 0.12
    content_spacing = HEIGHT * 0.07
    
    # Mensagem de vitória
    victory_text = large_font.render("VITÓRIA!", True, GREEN)
    victory_y = top_margin
    screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, victory_y))
    
    # Mensagem de parabéns
    congrats_text = medium_font.render("Parabéns! Você completou o Sudoku!", True, WHITE)
    congrats_y = victory_y + victory_text.get_height() + content_spacing
    screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, congrats_y))
    
    # Mostrar dificuldade
    difficulty_map = {'easy': 'Fácil', 'medium': 'Médio', 'hard': 'Difícil'}
    diff_text = medium_font.render(f"Dificuldade: {difficulty_map[sudoku.difficulty]}", True, WHITE)
    diff_y = congrats_y + congrats_text.get_height() + content_spacing * 0.7
    screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, diff_y))
    
    # Instruções
    press_any_key = small_font.render("Pressione qualquer tecla para continuar", True, WHITE)
    key_y = diff_y + diff_text.get_height() + content_spacing * 1.5
    screen.blit(press_any_key, (WIDTH // 2 - press_any_key.get_width() // 2, key_y))
    
    # Desenha estrelas decorativas em torno da mensagem
    star_radius = min(WIDTH, HEIGHT) * 0.25  # Raio do círculo onde as estrelas serão colocadas
    num_stars = 5
    
    for i in range(num_stars):
        angle = i * (360 / num_stars)
        x = WIDTH // 2 + star_radius * math.cos(math.radians(angle))
        y = HEIGHT // 2 + star_radius * math.sin(math.radians(angle))
        draw_star(x, y, 20, 10, 5, (255, 255, 0))  # Estrela amarela

def draw_star(x, y, outer_radius, inner_radius, points, color):
    """Desenha uma estrela decorativa"""
    angle = math.pi / points
    star_points = []
    for i in range(2 * points):
        radius = outer_radius if i % 2 == 0 else inner_radius
        px = x + radius * math.cos(i * angle)
        py = y + radius * math.sin(i * angle)
        star_points.append((px, py))
    pygame.draw.polygon(screen, color, star_points)

def main():
    # Jogo principal
    game_state = MENU
    sudoku = None
    running = True
    selected_pos = None
    message = ""
    hint_mode = False  # Controla se estamos no modo de seleção de dica
    
    # Loop principal do jogo
    while running:
        if game_state == MENU:
            # Armazena os botões retornados para detecção de clique
            difficulty_buttons = draw_menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Importante: atualiza as dimensões também no menu quando a janela é redimensionada
                    if not FULLSCREEN:
                        update_dimensions(event.w, event.h)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Verifica se clicou em um dos botões de dificuldade
                    for diff, button_rect in difficulty_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            sudoku = Sudoku(difficulty=diff)
                            game_state = PLAYING
                            message = "Você tem 3 vidas! Cuidado com os erros!"
                            selected_pos = None
                elif event.type == pygame.KEYDOWN:
                    # F11 para tela cheia (mantém a funcionalidade, só remove o texto)
                    if event.key == pygame.K_F11:
                        toggle_fullscreen()
    
        elif game_state == PLAYING:
            screen.fill(WHITE)
            draw_grid()
            draw_numbers(sudoku)
            
            # Gerencia a célula selecionada
            if selected_pos:
                selected_cell = draw_selected_cell(selected_pos, sudoku)
            else:
                selected_cell = None
                
            draw_status_bar(message, BLACK, hint_mode)
            draw_lives(sudoku)
            
            # Verificação automática após cada alteração do tabuleiro
            # Se o tabuleiro estiver completo, avança para tela de vitória
            if all(all(cell != 0 for cell in row) for row in sudoku.board) and sudoku.is_complete():
                game_state = VICTORY
                message = "Parabéns! Você completou o Sudoku corretamente!"
                pygame.time.delay(500)  # Pequeno atraso para perceber que finalizou
                continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Evento de redimensionamento da janela
                elif event.type == pygame.VIDEORESIZE:
                    if not FULLSCREEN:  # Ignora eventos de redimensionamento em tela cheia
                        update_dimensions(event.w, event.h)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        # Verifica se clicou no botão de dicas
                        if HINT_BUTTON.collidepoint(mouse_pos):
                            sudoku.toggle_notes()
                            message = f"Dicas {'ativadas' if HINTS_ENABLED else 'desativadas'}!"
                        # Verifica se clicou no botão de dica única
                        elif SOLVE_HINT_BUTTON.collidepoint(mouse_pos):
                            if not hint_mode:  # Se não está no modo dica, ativa
                                hint_mode = True
                                message = "Selecione uma célula vazia para receber a dica"
                            else:  # Se já está no modo dica, cancela
                                hint_mode = False
                                message = "Modo de dica cancelado"
                        # Verifica se clicou no tabuleiro
                        elif mouse_pos[1] < HEIGHT - STATUS_BAR_HEIGHT:
                            # Ajusta as coordenadas com base no offset do tabuleiro
                            adjusted_x = mouse_pos[0] - board_offset_x
                            adjusted_y = mouse_pos[1] - board_offset_y
                            
                            # Verifica se o clique foi dentro do tabuleiro
                            if (0 <= adjusted_x <= CELL_SIZE * GRID_SIZE and 
                                0 <= adjusted_y <= CELL_SIZE * GRID_SIZE):
                                selected_pos = mouse_pos
                                col = adjusted_x // CELL_SIZE
                                row = adjusted_y // CELL_SIZE
                                
                                # Se estamos no modo dica e clicou em uma célula válida
                                if hint_mode and 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                                    # Verifica se a célula está vazia e pode receber dica
                                    if sudoku.board[row][col] == 0:
                                        hint_result = sudoku.get_hint(row, col)
                                        if hint_result:
                                            r, c, value = hint_result
                                            message = f"Dica: {value} na posição ({r+1},{c+1})"
                                        else:
                                            message = "Não foi possível fornecer dica para esta célula"
                                    else:
                                        message = "Selecione uma célula vazia para receber a dica"
                                # Comportamento normal quando não está no modo dica
                                elif not hint_mode and 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                                    value = sudoku.board[row][col]
                                    if value != 0:
                                        # Ao clicar, alterna entre destacar ou não
                                        if sudoku.highlight_number == value:
                                            sudoku.highlight_number = None
                                        else:
                                            sudoku.highlight_number = value
                                    else:
                                        sudoku.highlight_number = None
                                
                                    if not hint_mode:
                                        message = "Digite um número (1-9) para preencher. Shift+1..9 para anotar."
                # Adiciona tratamento para movimento do mouse
                elif event.type == pygame.MOUSEMOTION:
                    # Se o mouse sai do tabuleiro, cancela o highlight automático
                    if event.pos[1] >= HEIGHT - STATUS_BAR_HEIGHT:
                        if sudoku.highlight_number is not None and AUTO_HIGHLIGHT:
                            sudoku.highlight_number = None
                elif event.type == pygame.KEYDOWN:
                    # Tecla F11 para alternar tela cheia
                    if event.key == pygame.K_F11:
                        toggle_fullscreen()
                        
                    # Tecla ESC para sair da tela cheia, se estiver nela
                    elif event.key == pygame.K_ESCAPE and FULLSCREEN:
                        toggle_fullscreen()
                        continue  # Não processa ESC como "voltar ao menu" se estiver em tela cheia
                    
                    # Navegação com setas
                    if event.key in ARROW_KEYS:
                        if selected_pos is None:
                            # Se nenhuma célula estiver selecionada, começa na primeira célula
                            selected_pos = (board_offset_x + CELL_SIZE // 2, board_offset_y + CELL_SIZE // 2)
                        else:
                            # Calcula a célula atual
                            adjusted_x = selected_pos[0] - board_offset_x
                            adjusted_y = selected_pos[1] - board_offset_y
                            col = adjusted_x // CELL_SIZE 
                            row = adjusted_y // CELL_SIZE
                            
                            # Move para a próxima célula na direção indicada
                            drow, dcol = ARROW_KEYS[event.key]
                            new_row = max(0, min(GRID_SIZE - 1, row + drow))
                            new_col = max(0, min(GRID_SIZE - 1, col + dcol))
                            
                            # Atualiza a posição selecionada
                            selected_pos = (board_offset_x + new_col * CELL_SIZE + CELL_SIZE // 2, 
                                          board_offset_y + new_row * CELL_SIZE + CELL_SIZE // 2)

                            message = f"Célula selecionada: ({new_row+1}, {new_col+1})"
                    
                    # Processamento de entrada numérica e outras teclas
                    if selected_cell:
                        row, col = selected_cell
                        # Corrigido: detecta shift + teclado numérico corretamente
                        mods = pygame.key.get_mods()
                        is_shift_pressed = mods & pygame.KMOD_SHIFT
                        is_ctrl_pressed = mods & pygame.KMOD_CTRL
                        
                        # Verifica se é Ctrl+Z (desfazer) ou Ctrl+Shift+Z (refazer)
                        if is_ctrl_pressed:
                            if event.key == pygame.K_z:
                                if is_shift_pressed:
                                    # Ctrl+Shift+Z = Refazer
                                    if sudoku.redo():
                                        message = "Ação refeita"
                                    else:
                                        message = "Não há ações para refazer"
                                else:
                                    # Ctrl+Z = Desfazer
                                    if sudoku.undo():
                                        message = "Ação desfeita"
                                    else:
                                        message = "Não há ações para desfazer"
                                continue
                        
                        # Anotação: Shift+número (incluindo teclado numérico)
                        # Verificação melhorada para reconhecer corretamente Shift+teclado numérico
                        if event.key in NUMERIC_KEYS and NUMERIC_KEYS[event.key] > 0:
                            num = NUMERIC_KEYS[event.key]
                            
                            # Modo de anotação (Shift pressionado)
                            if is_shift_pressed:
                                if sudoku.original_board[row][col] == 0 and sudoku.board[row][col] == 0:
                                    # Salva o estado antes de modificar
                                    sudoku.save_state()
                                    
                                    if num in sudoku.notes[row][col]:
                                        sudoku.notes[row][col].remove(num)
                                    else:
                                        sudoku.notes[row][col].add(num)
                                    message = f"Anotação {num} {'removida' if num not in sudoku.notes[row][col] else 'adicionada'}."
                            # Modo de inserção normal (sem Shift)
                            else:
                                # Salva o estado antes de tentar inserir um número
                                sudoku.save_state()
                                
                                if sudoku.original_board[row][col] == 0:
                                    correct_num = sudoku.solution[row][col]
                                    
                                    if num == correct_num:  # Resposta correta
                                        sudoku.board[row][col] = num
                                        sudoku.notes[row][col].clear()
                                        # Atualiza as dicas automaticamente quando inserimos um número correto
                                        sudoku.update_if_hints_enabled()
                                        message = f"Número {num} inserido corretamente!"
                                    else:  # Resposta errada
                                        if sudoku.lose_life():  # Perde uma vida
                                            message = "Você perdeu todas as vidas!"
                                            game_state = GAME_OVER
                                        else:
                                            message = f"Número errado! Você perdeu uma vida! ({sudoku.lives} restantes)"
                        elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                            if sudoku.original_board[row][col] == 0:
                                # Salva o estado antes de apagar
                                sudoku.save_state()
                                
                                sudoku.board[row][col] = 0
                                sudoku.notes[row][col].clear()
                                # Atualiza as dicas automaticamente quando removemos um número
                                sudoku.update_if_hints_enabled()
                                message = "Número apagado."
                    # Tecla V para verificar se o tabuleiro está completo
                    elif event.key == pygame.K_v:
                        if sudoku.is_complete():
                            message = "Parabéns! Você completou o Sudoku corretamente!"
                            # Mudança aqui: em vez de mostrar brevemente uma mensagem,
                            # vamos para a tela de vitória
                            game_state = VICTORY
                        else:
                            message = "O tabuleiro ainda não está completamente correto."
                    # Tecla R para reiniciar o jogo
                    elif event.key == pygame.K_r:
                        sudoku = Sudoku(sudoku.difficulty)
                        selected_pos = None
                        message = "Jogo reiniciado com um novo tabuleiro!"
                    # Tecla ESC para voltar ao menu
                    elif event.key == pygame.K_ESCAPE:
                        game_state = MENU

        elif game_state == GAME_OVER:
            # Mantém o tabuleiro atual no fundo
            draw_game_over(sudoku)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Qualquer tecla volta para o menu
                elif event.type == pygame.KEYDOWN:
                    game_state = MENU

        elif game_state == VICTORY:
            # Desenha a tela de vitória
            draw_victory_screen(sudoku)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Qualquer tecla volta para o menu
                elif event.type == pygame.KEYDOWN:
                    game_state = MENU

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
