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

# Configurações da tela
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
FONT_SIZE = 36

# Configuração da janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Fontes
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
HINT_BUTTON = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 45, 140, 30)
# Botão de dica única
SOLVE_HINT_BUTTON = pygame.Rect(WIDTH // 2 - 70 - 150, HEIGHT - 45, 140, 30)

# Estado das dicas
HINTS_ENABLED = False

# Auto highlight quando o cursor passa sobre números
AUTO_HIGHLIGHT = True

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3  # Novo estado para tela de vitória

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

    def get_hint(self):
        """Fornece uma dica preenchendo uma célula vazia com o valor correto"""
        # Procura por células vazias
        empty_cells = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 0:
                    empty_cells.append((row, col))
        
        if not empty_cells:
            return False  # Não há células vazias
            
        # Escolhe uma célula vazia aleatória
        row, col = random.choice(empty_cells)
        
        # Preenche com o valor correto
        self.save_state()  # Salva o estado para poder desfazer
        self.board[row][col] = self.solution[row][col]
        self.notes[row][col].clear()
        self.update_if_hints_enabled()  # Atualiza as dicas
        
        return (row, col, self.solution[row][col])  # Retorna a posição e o valor preenchido

def draw_grid():
    # Desenha as linhas do grid
    for i in range(GRID_SIZE + 1):
        line_width = 3 if i % 3 == 0 else 1
        
        # Linha horizontal
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), 
                         (WIDTH, i * CELL_SIZE), line_width)
        
        # Linha vertical
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), 
                         (i * CELL_SIZE, HEIGHT - 60), line_width)

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
                x = col * CELL_SIZE + (CELL_SIZE - num_surface.get_width()) // 2
                y = row * CELL_SIZE + (CELL_SIZE - num_surface.get_height()) // 2
                screen.blit(num_surface, (x, y))
            elif note:
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
                        note_surface = small_font.render(n, True, note_color)
                        nx = col * CELL_SIZE + 5 + (idx % 3) * (CELL_SIZE // 3)
                        ny = row * CELL_SIZE + 2 + (idx // 3) * (CELL_SIZE // 3)
                        
                        # Opcional: desenha um fundo para destacar ainda mais as anotações
                        if sudoku.highlight_number is not None and int(n) == sudoku.highlight_number:
                            note_rect = note_surface.get_rect(topleft=(nx, ny))
                            note_rect.inflate_ip(2, 2)  # Aumenta ligeiramente o tamanho do retângulo
                            pygame.draw.rect(screen, (230, 230, 255), note_rect)  # Fundo claro para destacar
                            
                        screen.blit(note_surface, (nx, ny))

def draw_selected_cell(pos, sudoku):
    # Destaca a célula selecionada
    if pos:
        col, row = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        
        # Verifica se a posição está dentro do tabuleiro
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            # Se a posição tem um número, destaca todos os números iguais
            value = sudoku.board[row][col]
            if value != 0 and AUTO_HIGHLIGHT:
                sudoku.highlight_number = value
            
            # Se a célula é editável, destaca com cor azul claro
            if sudoku.original_board[row][col] == 0:
                pygame.draw.rect(screen, LIGHT_BLUE, 
                                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)
                return (row, col)
            # Se a célula não é editável (número fixo), destaca com uma cor diferente ou estilo pontilhado
            else:
                # Usar uma cor mais escura ou estilo diferente para células não editáveis
                # Aqui usamos uma borda mais fina e cor cinza escuro
                pygame.draw.rect(screen, DARK_GRAY, 
                                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
                # Retorna None para células não editáveis pois não podemos modificá-las
                return None
    return None

def draw_status_bar(message, color=BLACK):
    # Desenha a barra de status na parte inferior da tela
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - 60, WIDTH, 60))
    status_text = small_font.render(message, True, color)
    screen.blit(status_text, (10, HEIGHT - 40))
    
    # Desenha o botão de dicas com texto apropriado
    button_color = LIGHT_BLUE if not HINTS_ENABLED else (150, 255, 150)  # Verde claro se ativado
    pygame.draw.rect(screen, button_color, HINT_BUTTON)
    pygame.draw.rect(screen, BLACK, HINT_BUTTON, 2)
    
    hint_text = small_font.render("Dicas " + ("ON" if HINTS_ENABLED else "OFF"), True, BLACK)
    screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 45 + (30 - hint_text.get_height()) // 2))
    
    # Desenha o botão de dica única
    pygame.draw.rect(screen, (255, 220, 100), SOLVE_HINT_BUTTON)  # Amarelo claro para o botão
    pygame.draw.rect(screen, BLACK, SOLVE_HINT_BUTTON, 2)
    
    solve_text = small_font.render("Pedir Dica", True, BLACK)
    screen.blit(solve_text, (SOLVE_HINT_BUTTON.x + (SOLVE_HINT_BUTTON.width - solve_text.get_width()) // 2, 
                            SOLVE_HINT_BUTTON.y + (SOLVE_HINT_BUTTON.height - solve_text.get_height()) // 2))

def draw_lives(sudoku):
    # Desenha os corações representando as vidas
    for i in range(3):
        if i < sudoku.lives:
            screen.blit(heart_img, (WIDTH - 100 + i * 35, HEIGHT - 45))
        else:
            # Coração vazio (contorno)
            pygame.draw.polygon(screen, RED, 
                [(WIDTH - 100 + i * 35 + 15, HEIGHT - 45 + 5),
                 (WIDTH - 100 + i * 35 + 25, HEIGHT - 45 + 15),
                 (WIDTH - 100 + i * 35 + 15, HEIGHT - 45 + 25),
                 (WIDTH - 100 + i * 35 + 5, HEIGHT - 45 + 15)], 1)

def draw_menu():
    # Desenha a tela de menu
    screen.fill(WHITE)
    
    # Título
    title = large_font.render("SUDOKU", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    
    # Opções de dificuldade
    difficulties = ['easy', 'medium', 'hard']
    difficulty_texts = ['Fácil', 'Médio', 'Difícil']
    
    for i, (diff, text) in enumerate(zip(difficulties, difficulty_texts)):
        y_pos = 250 + i * 80
        
        # Cria um retângulo para o botão
        button_rect = pygame.Rect(WIDTH // 2 - 100, y_pos, 200, 50)
        pygame.draw.rect(screen, LIGHT_BLUE, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        
        # Texto do botão
        diff_text = medium_font.render(text, True, BLACK)
        screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, y_pos + 15))
        
    # Instruções
    instructions = small_font.render("Selecione a dificuldade", True, DARK_GRAY)
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 200))

def draw_game_over(sudoku):
    # Desenha uma camada semitransparente sobre o jogo
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Mensagem de game over
    game_over_text = large_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 80))
    
    # Instruções
    press_any_key = small_font.render("Pressione qualquer tecla para voltar ao menu", True, WHITE)
    screen.blit(press_any_key, (WIDTH // 2 - press_any_key.get_width() // 2, 130))
    
    # Mostra a solução correta
    solution_text = medium_font.render("Solução:", True, WHITE)
    screen.blit(solution_text, (WIDTH // 2 - solution_text.get_width() // 2, 170))
    
    # Desenha o tabuleiro resolvido em tamanho reduzido para caber na tela
    cell_size_small = CELL_SIZE * 0.5  # Reduzido para 50% do tamanho original
    for i in range(9):
        for j in range(9):
            value = sudoku.solution[i][j]
            # Calcula posição para tabuleiro centralizado e menor
            x = WIDTH // 2 - (cell_size_small * 9) // 2 + j * cell_size_small
            y = 200 + i * cell_size_small
            
            # Desenha o número em fonte menor
            mini_font = pygame.font.SysFont("Arial", 12)
            num_surface = mini_font.render(str(value), True, WHITE)
            screen.blit(num_surface, (x + (cell_size_small - num_surface.get_width()) // 2, 
                                     y + (cell_size_small - num_surface.get_height()) // 2))
            
    # Desenha as linhas da grade
    for i in range(10):
        line_width = 2 if i % 3 == 0 else 1
        x = WIDTH // 2 - (cell_size_small * 9) // 2 + i * cell_size_small
        y = 200
        pygame.draw.line(screen, WHITE, (x, y), (x, y + cell_size_small * 9), line_width)
        pygame.draw.line(screen, WHITE, (WIDTH // 2 - (cell_size_small * 9) // 2, y + i * cell_size_small),
                         (WIDTH // 2 + (cell_size_small * 9) // 2, y + i * cell_size_small), line_width)

def draw_victory_screen(sudoku, time_taken=None):
    """Desenha a tela de vitória quando o jogador completa o sudoku"""
    # Desenha uma camada semitransparente sobre o jogo (verde para vitória)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 100, 0, 180))  # Verde escuro semitransparente
    screen.blit(overlay, (0, 0))
    
    # Mensagem de vitória
    victory_text = large_font.render("VITÓRIA!", True, GREEN)
    screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, 100))
    
    # Mensagem de parabéns
    congrats_text = medium_font.render("Parabéns! Você completou o Sudoku!", True, WHITE)
    screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, 180))
    
    # Mostrar dificuldade
    difficulty_map = {'easy': 'Fácil', 'medium': 'Médio', 'hard': 'Difícil'}
    diff_text = medium_font.render(f"Dificuldade: {difficulty_map[sudoku.difficulty]}", True, WHITE)
    screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, 240))
    
    # Instruções
    press_any_key = small_font.render("Pressione qualquer tecla para continuar", True, WHITE)
    screen.blit(press_any_key, (WIDTH // 2 - press_any_key.get_width() // 2, 320))
    
    # Desenha estrelas decorativas
    for i in range(5):
        angle = i * (360 / 5)
        x = WIDTH // 2 + 150 * math.cos(math.radians(angle))
        y = HEIGHT // 2 + 150 * math.sin(math.radians(angle))
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
    
    # Loop principal do jogo
    while running:
        if game_state == MENU:
            draw_menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Verifica se clicou em um dos botões de dificuldade
                    for i, diff in enumerate(['easy', 'medium', 'hard']):
                        button_rect = pygame.Rect(WIDTH // 2 - 100, 250 + i * 80, 200, 50)
                        if button_rect.collidepoint(mouse_pos):
                            sudoku = Sudoku(difficulty=diff)
                            game_state = PLAYING
                            message = "Você tem 3 vidas! Cuidado com os erros!"
                            selected_pos = None
        
        elif game_state == PLAYING:
            screen.fill(WHITE)
            draw_grid()
            draw_numbers(sudoku)
            
            # Gerencia a célula selecionada
            if selected_pos:
                selected_cell = draw_selected_cell(selected_pos, sudoku)
            else:
                selected_cell = None
                
            draw_status_bar(message)
            draw_lives(sudoku)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        # Verifica se clicou no botão de dicas
                        if HINT_BUTTON.collidepoint(mouse_pos):
                            sudoku.toggle_notes()
                            message = f"Dicas {'ativadas' if HINTS_ENABLED else 'desativadas'}!"
                        # Verifica se clicou no botão de dica única
                        elif SOLVE_HINT_BUTTON.collidepoint(mouse_pos):
                            hint_result = sudoku.get_hint()
                            if hint_result:
                                row, col, value = hint_result
                                message = f"Dica: {value} na posição ({row+1},{col+1})"
                                # Destaca a posição da dica
                                selected_pos = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
                            else:
                                message = "Não há células vazias para receber dicas!"
                        # Verifica se clicou no tabuleiro
                        elif mouse_pos[1] < HEIGHT - 60:
                            selected_pos = mouse_pos
                            col, row = mouse_pos[0] // CELL_SIZE, mouse_pos[1] // CELL_SIZE
                            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                                value = sudoku.board[row][col]
                                if value != 0:
                                    # Ao clicar, alterna entre destacar ou não
                                    if sudoku.highlight_number == value:
                                        sudoku.highlight_number = None
                                    else:
                                        sudoku.highlight_number = value
                                else:
                                    sudoku.highlight_number = None
                            message = "Digite um número (1-9) para preencher. Shift+1..9 para anotar."
                # Adiciona tratamento para movimento do mouse
                elif event.type == pygame.MOUSEMOTION:
                    # Se o mouse sai do tabuleiro, cancela o highlight automático
                    if event.pos[1] >= HEIGHT - 60:
                        if sudoku.highlight_number is not None and AUTO_HIGHLIGHT:
                            sudoku.highlight_number = None
                elif event.type == pygame.KEYDOWN:
                    # Navegação com setas
                    if event.key in ARROW_KEYS:
                        if selected_pos is None:
                            # Se nenhuma célula estiver selecionada, começa na primeira célula
                            selected_pos = (CELL_SIZE // 2, CELL_SIZE // 2)
                        else:
                            # Calcula a célula atual
                            col, row = selected_pos[0] // CELL_SIZE, selected_pos[1] // CELL_SIZE
                            
                            # Move para a próxima célula na direção indicada
                            drow, dcol = ARROW_KEYS[event.key]
                            new_row = max(0, min(GRID_SIZE - 1, row + drow))
                            new_col = max(0, min(GRID_SIZE - 1, col + dcol))
                            
                            # Atualiza a posição selecionada
                            selected_pos = (new_col * CELL_SIZE + CELL_SIZE // 2, 
                                           new_row * CELL_SIZE + CELL_SIZE // 2)
                            

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
                        if event.key in NUMERIC_KEYS and NUMERIC_KEYS[event.key] > 0 and is_shift_pressed and not is_ctrl_pressed:
                            num = NUMERIC_KEYS[event.key]
                            if sudoku.original_board[row][col] == 0 and sudoku.board[row][col] == 0:
                                # Salva o estado antes de modificar
                                sudoku.save_state()
                                

                                if num in sudoku.notes[row][col]:
                                    sudoku.notes[row][col].remove(num)
                                else:
                                    sudoku.notes[row][col].add(num)
                                message = f"Anotação {num} {'removida' if num not in sudoku.notes[row][col] else 'adicionada'}."
                        # Preenchimento normal (incluindo teclado numérico)
                        elif event.key in NUMERIC_KEYS and NUMERIC_KEYS[event.key] > 0:
                            # Salva o estado antes de tentar inserir um número
                            sudoku.save_state()
                            
                            num = NUMERIC_KEYS[event.key]
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
