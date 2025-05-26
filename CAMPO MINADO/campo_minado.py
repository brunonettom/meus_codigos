import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Constantes
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
MINE_PROBABILITY = 0.15
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (220, 220, 220)
GRID_COLOR = (180, 180, 180)
REVEALED_COLOR = (200, 200, 200)
FLAG_COLOR = (255, 0, 0)
TEXT_COLORS = {
    1: (0, 0, 255),      # Azul
    2: (0, 128, 0),      # Verde
    3: (255, 0, 0),      # Vermelho
    4: (0, 0, 128),      # Azul escuro
    5: (128, 0, 0),      # Marrom
    6: (0, 128, 128),    # Ciano
    7: (0, 0, 0),        # Preto
    8: (128, 128, 128)   # Cinza
}

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Campo Minado Infinito")
font = pygame.font.SysFont(None, 24)

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

class MineSweeper:
    def __init__(self):
        self.cells = {}  # Dicionário de células (x, y) -> Cell
        # Centralize o campo visível inicialmente
        self.offset_x = (SCREEN_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2
        self.game_over = False
        self.first_click = True  # Rastreie se é o primeiro clique
        self.generate_initial_grid()
    
    def generate_initial_grid(self):
        # Gera o grid inicial visível sem minas ainda
        for x in range(-GRID_WIDTH//2, GRID_WIDTH//2):
            for y in range(-GRID_HEIGHT//2, GRID_HEIGHT//2):
                if (x, y) not in self.cells:
                    self.cells[(x, y)] = Cell()
    
    def get_cell(self, x, y):
        # Retorna a célula nas coordenadas x, y, criando-a se não existir
        if (x, y) not in self.cells:
            self.cells[(x, y)] = Cell()
            
            # Determina probabilisticamente se é uma mina (apenas se não for primeiro clique)
            if not self.first_click and random.random() < MINE_PROBABILITY:
                self.cells[(x, y)].is_mine = True
                
                # Atualiza o contador de minas vizinhas para as células adjacentes
                self.update_neighbors(x, y)
        
        return self.cells[(x, y)]
    
    def update_neighbors(self, x, y):
        # Atualiza o contador de minas vizinhas para todas as células adjacentes
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor_pos = (x + dx, y + dy)
                # Cria a célula vizinha se não existir
                if neighbor_pos not in self.cells:
                    self.cells[neighbor_pos] = Cell()
                
                if not self.cells[neighbor_pos].is_mine:
                    self.cells[neighbor_pos].neighbor_mines += 1
    
    def add_mines(self, safe_x, safe_y):
        # Adiciona minas ao campo, evitando o primeiro clique e vizinhos
        safe_cells = [(safe_x + dx, safe_y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
        
        for pos, cell in list(self.cells.items()):
            if pos not in safe_cells and random.random() < MINE_PROBABILITY:
                cell.is_mine = True
                self.update_neighbors(pos[0], pos[1])
    
    def reveal_cell(self, x, y):
        if (x, y) not in self.cells:
            return
        
        cell = self.cells[(x, y)]
        
        if cell.is_flagged or cell.is_revealed or self.game_over:
            return
        
        # Se for o primeiro clique, garante que não seja uma mina
        if self.first_click:
            self.first_click = False
            self.add_mines(x, y)
        
        cell.is_revealed = True
        
        # Verifica se clicou em uma mina
        if cell.is_mine:
            self.game_over = True
            return
        
        # Se não tem minas vizinhas, revela recursivamente
        if cell.neighbor_mines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor_pos = (x + dx, y + dy)
                    # Certifique-se de criar o vizinho se não existir
                    neighbor = self.get_cell(x + dx, y + dy)
                    if not neighbor.is_revealed and not neighbor.is_flagged:
                        self.reveal_cell(x + dx, y + dy)
    
    def toggle_flag(self, x, y):
        if (x, y) not in self.cells or self.game_over:
            return
        
        cell = self.cells[(x, y)]
        
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged
    
    def draw(self, screen):
        # Limpa a tela
        screen.fill(BG_COLOR)
        
        # Calcula a janela de visualização
        cells_x = SCREEN_WIDTH // CELL_SIZE
        cells_y = SCREEN_HEIGHT // CELL_SIZE
        
        start_x = self.offset_x // CELL_SIZE - 1
        start_y = self.offset_y // CELL_SIZE - 1
        end_x = start_x + cells_x + 2
        end_y = start_y + cells_y + 2
        
        # Desenha as células visíveis
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                # Certifique-se de que a célula existe
                cell = self.get_cell(x, y)
                
                # Calcula a posição na tela
                rect_x = x * CELL_SIZE - self.offset_x
                rect_y = y * CELL_SIZE - self.offset_y
                
                # Desenha o fundo da célula
                if cell.is_revealed:
                    pygame.draw.rect(screen, REVEALED_COLOR, (rect_x, rect_y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, BG_COLOR, (rect_x, rect_y, CELL_SIZE, CELL_SIZE))
                
                # Desenha a borda da célula
                pygame.draw.rect(screen, GRID_COLOR, (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 1)
                
                # Desenha o conteúdo da célula
                if cell.is_revealed:
                    if cell.is_mine:
                        # Desenha uma mina
                        pygame.draw.circle(screen, (0, 0, 0), 
                                          (rect_x + CELL_SIZE // 2, rect_y + CELL_SIZE // 2), 
                                          CELL_SIZE // 3)
                    elif cell.neighbor_mines > 0:
                        # Desenha o número
                        text = font.render(str(cell.neighbor_mines), True, 
                                          TEXT_COLORS.get(cell.neighbor_mines, (0, 0, 0)))
                        text_rect = text.get_rect(center=(rect_x + CELL_SIZE // 2, rect_y + CELL_SIZE // 2))
                        screen.blit(text, text_rect)
                elif cell.is_flagged:
                    # Desenha uma bandeira
                    pygame.draw.polygon(screen, FLAG_COLOR, [
                        (rect_x + CELL_SIZE // 2, rect_y + CELL_SIZE // 4),
                        (rect_x + CELL_SIZE // 4, rect_y + CELL_SIZE // 2),
                        (rect_x + CELL_SIZE // 2, rect_y + 3 * CELL_SIZE // 4)
                    ])
        
        # Desenha mensagem de Game Over, se necessário
        if self.game_over:
            game_over_surface = font.render("GAME OVER! Pressione R para reiniciar", True, (255, 0, 0))
            game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, 20))
            screen.blit(game_over_surface, game_over_rect)

def main():
    game = MineSweeper()
    clock = pygame.time.Clock()
    dragging = False
    last_pos = None
    drag_threshold = 5  # Limite para diferenciar clique de arrasto
    click_pos = None
    drag_distance = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reinicia o jogo
                    game = MineSweeper()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    click_pos = event.pos
                    dragging = True
                    last_pos = event.pos
                    drag_distance = 0
                elif event.button == 3:  # Botão direito
                    if not game.game_over:
                        # Converte posição da tela para coordenadas do grid
                        grid_x = (event.pos[0] + game.offset_x) // CELL_SIZE
                        grid_y = (event.pos[1] + game.offset_y) // CELL_SIZE
                        game.toggle_flag(grid_x, grid_y)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if dragging and drag_distance < drag_threshold and not game.game_over:
                        # Foi um clique, não um arrasto
                        grid_x = (click_pos[0] + game.offset_x) // CELL_SIZE
                        grid_y = (click_pos[1] + game.offset_y) // CELL_SIZE
                        game.reveal_cell(grid_x, grid_y)
                    dragging = False
            
            if event.type == pygame.MOUSEMOTION:
                if dragging and last_pos:
                    # Calcula o deslocamento
                    dx = event.pos[0] - last_pos[0]
                    dy = event.pos[1] - last_pos[1]
                    
                    # Atualiza a distância de arrasto
                    drag_distance += abs(dx) + abs(dy)
                    
                    if drag_distance > drag_threshold:
                        # Considerado como arrasto, não como clique
                        game.offset_x -= dx
                        game.offset_y -= dy
                    
                    last_pos = event.pos
        
        # Desenha o jogo
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
