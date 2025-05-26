import pygame
import random
import time

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

# Imagem de coração (vida)
heart_img = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.polygon(heart_img, RED, [(15, 5), (25, 15), (15, 25), (5, 15)])

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2

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
        self.generate_puzzle()
        
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
                        note_surface = small_font.render(n, True, GRAY)
                        nx = col * CELL_SIZE + 5 + (idx % 3) * (CELL_SIZE // 3)
                        ny = row * CELL_SIZE + 2 + (idx // 3) * (CELL_SIZE // 3)
                        screen.blit(note_surface, (nx, ny))

def draw_selected_cell(pos, sudoku):
    # Destaca a célula selecionada
    if pos:
        col, row = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        
        # Verifica se a posição está dentro do tabuleiro e é editável
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and sudoku.original_board[row][col] == 0:
            pygame.draw.rect(screen, LIGHT_BLUE, 
                            (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)
            
            return (row, col)
    return None

def draw_status_bar(message, color=BLACK):
    # Desenha a barra de status na parte inferior da tela
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - 60, WIDTH, 60))
    status_text = small_font.render(message, True, color)
    screen.blit(status_text, (10, HEIGHT - 40))

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
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 150))
    
    # Instruções
    press_any_key = small_font.render("Pressione qualquer tecla para voltar ao menu", True, WHITE)
    screen.blit(press_any_key, (WIDTH // 2 - press_any_key.get_width() // 2, 220))
    
    # Mostra a solução correta
    solution_text = medium_font.render("Solução:", True, WHITE)
    screen.blit(solution_text, (WIDTH // 2 - solution_text.get_width() // 2, 280))
    
    # Desenha o tabuleiro resolvido
    cell_size_small = CELL_SIZE * 0.6
    for i in range(9):
        for j in range(9):
            value = sudoku.solution[i][j]
            # Calcula posição para tabuleiro centralizado e menor
            x = WIDTH // 2 - (cell_size_small * 9) // 2 + j * cell_size_small
            y = 320 + i * cell_size_small
            
            # Desenha o número
            num_surface = small_font.render(str(value), True, WHITE)
            screen.blit(num_surface, (x + (cell_size_small - num_surface.get_width()) // 2, 
                                     y + (cell_size_small - num_surface.get_height()) // 2))
            
    # Desenha as linhas da grade
    for i in range(10):
        line_width = 2 if i % 3 == 0 else 1
        x = WIDTH // 2 - (cell_size_small * 9) // 2 + i * cell_size_small
        y = 320
        pygame.draw.line(screen, WHITE, (x, y), (x, y + cell_size_small * 9), line_width)
        pygame.draw.line(screen, WHITE, (WIDTH // 2 - (cell_size_small * 9) // 2, y + i * cell_size_small),
                         (WIDTH // 2 + (cell_size_small * 9) // 2, y + i * cell_size_small), line_width)

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
            selected_cell = draw_selected_cell(selected_pos, sudoku)
            draw_status_bar(message)
            draw_lives(sudoku)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if mouse_pos[1] < HEIGHT - 60:
                            selected_pos = mouse_pos
                            col, row = mouse_pos[0] // CELL_SIZE, mouse_pos[1] // CELL_SIZE
                            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                                value = sudoku.board[row][col]
                                if value != 0:
                                    # Destaca todos os iguais
                                    if sudoku.highlight_number == value:
                                        sudoku.highlight_number = None
                                    else:
                                        sudoku.highlight_number = value
                                else:
                                    sudoku.highlight_number = None
                            message = "Digite um número (1-9) para preencher. Shift+1..9 para anotar."
                elif event.type == pygame.KEYDOWN:
                    if selected_cell:
                        row, col = selected_cell
                        # Anotação: Shift+1..9
                        if pygame.K_1 <= event.key <= pygame.K_9 and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                            num = event.key - pygame.K_0
                            if sudoku.original_board[row][col] == 0 and sudoku.board[row][col] == 0:
                                if num in sudoku.notes[row][col]:
                                    sudoku.notes[row][col].remove(num)
                                else:
                                    sudoku.notes[row][col].add(num)
                                message = f"Anotação {num} {'removida' if num not in sudoku.notes[row][col] else 'adicionada'}."
                        # Preenchimento normal
                        elif pygame.K_1 <= event.key <= pygame.K_9:
                            num = event.key - pygame.K_0
                            if sudoku.original_board[row][col] == 0:
                                correct_num = sudoku.solution[row][col]
                                
                                if num == correct_num:  # Resposta correta
                                    sudoku.board[row][col] = num
                                    sudoku.notes[row][col].clear()
                                    message = f"Número {num} inserido corretamente!"
                                else:  # Resposta errada
                                    if sudoku.lose_life():  # Perde uma vida
                                        message = "Você perdeu todas as vidas!"
                                        game_state = GAME_OVER
                                    else:
                                        message = f"Número errado! Você perdeu uma vida! ({sudoku.lives} restantes)"
                        elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                            if sudoku.original_board[row][col] == 0:
                                sudoku.board[row][col] = 0
                                sudoku.notes[row][col].clear()
                                message = "Número apagado."
                    # Tecla V para verificar se o tabuleiro está completo
                    elif event.key == pygame.K_v:
                        if sudoku.is_complete():
                            message = "Parabéns! Você completou o Sudoku corretamente!"
                            draw_status_bar(message, GREEN)
                            pygame.display.flip()
                            time.sleep(2)
                            game_state = MENU
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

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
