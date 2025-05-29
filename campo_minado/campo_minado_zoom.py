import pygame
import sys
import random
import time
import os
from pygame.locals import *
# Define VIDEORESIZE for window resizing
from pygame.constants import VIDEORESIZE

# Initialize Pygame
pygame.init()

# Difficulty presets
DIFFICULTY = {
    "EASY": {"width": 9, "height": 9, "mines": 10},
    "MEDIUM": {"width": 16, "height": 16, "mines": 40},
    "HARD": {"width": 30, "height": 16, "mines": 99},
    "INFINITE": {"width": 50, "height": 50, "mines": 400}
}

# Default to medium difficulty
DEFAULT_BLOCKSIZE = 30  # Default size of each cell in pixels
MIN_BLOCKSIZE = 15  # Minimum block size when zooming out
MAX_BLOCKSIZE = 60  # Maximum block size when zooming in
BLOCKSIZE = DEFAULT_BLOCKSIZE  # Current size of each cell in pixels
ZOOM_FACTOR = 1.0  # Current zoom level
SCROLL_OFFSET_X = 0  # Offset for navigating around the board with touchpad
SCROLL_OFFSET_Y = 0  # Offset for navigating around the board with touchpad
ZOOM_STEP = 3  # How much to change block size with each zoom action

BOARDWIDTH = DIFFICULTY["MEDIUM"]["width"]
BOARDHEIGHT = DIFFICULTY["MEDIUM"]["height"]
MINES = DIFFICULTY["MEDIUM"]["mines"]
WINDOWWIDTH = max(BOARDWIDTH * BLOCKSIZE, 480)  # Make sure window is at least 480px wide
WINDOWHEIGHT = BOARDHEIGHT * BLOCKSIZE + 60  # Extra space for the scoreboard

# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARKGRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (173, 216, 230)  # New color for the restart button
COLORS = {
    1: (0, 0, 255),     # Blue
    2: (0, 128, 0),     # Green
    3: (255, 0, 0),     # Red
    4: (0, 0, 128),     # Dark Blue
    5: (128, 0, 0),     # Maroon
    6: (0, 128, 128),   # Teal
    7: (0, 0, 0),       # Black
    8: (128, 128, 128)  # Gray
}

# Set up the window with resizable flag
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Campo Minado')
FPSCLOCK = pygame.time.Clock()
FPS = 30

# Load images
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load images using absolute paths
try:
    ORIGINAL_BOMBA_IMG = pygame.image.load(os.path.join(script_dir, 'img', 'bomba.png'))
    ORIGINAL_FLAG_IMG = pygame.image.load(os.path.join(script_dir, 'img', 'flag.png'))
except FileNotFoundError:
    # Fallback to full path if relative path doesn't work
    base_dir = "c:\\Users\\BrunoLocal.BRUNO-note.000\\Downloads\\x\\CÓDIGOS\\campo_minado"
    ORIGINAL_BOMBA_IMG = pygame.image.load(os.path.join(base_dir, 'img', 'bomba.png'))
    ORIGINAL_FLAG_IMG = pygame.image.load(os.path.join(base_dir, 'img', 'flag.png'))

# Scale images according to current BLOCKSIZE
BOMBA_IMG = pygame.transform.scale(ORIGINAL_BOMBA_IMG, (BLOCKSIZE-6, BLOCKSIZE-6))
FLAG_IMG = pygame.transform.scale(ORIGINAL_FLAG_IMG, (BLOCKSIZE-6, BLOCKSIZE-6))

# Function to update images when zoom changes
def update_images_for_zoom():
    global BOMBA_IMG, FLAG_IMG
    BOMBA_IMG = pygame.transform.scale(ORIGINAL_BOMBA_IMG, (BLOCKSIZE-6, BLOCKSIZE-6))
    FLAG_IMG = pygame.transform.scale(ORIGINAL_FLAG_IMG, (BLOCKSIZE-6, BLOCKSIZE-6))

# Game state
HIDDEN = 0
REVEALED = 1
FLAGGED = 2

class Board:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [[{'state': HIDDEN, 'value': 0} for _ in range(width)] for _ in range(height)]
        self.started = False
        self.game_over = False
        self.win = False
        self.start_time = 0
        self.flags_placed = 0
        self.revealed_cells = 0
        self.total_cells = width * height
        
    def start_game(self, first_x, first_y):
        # Create a list of cells to avoid (first clicked cell and its neighbors)
        # This ensures first click is always on an empty cell (no number, no mine)
        cells_to_avoid = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = first_x + dx, first_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    cells_to_avoid.append((nx, ny))
        
        # Place mines (avoid the first clicked cell and its neighbors)
        mines_placed = 0
        available_cells = [(x, y) for x in range(self.width) for y in range(self.height) 
                          if (x, y) not in cells_to_avoid]
        
        # Make sure we have enough cells to place mines
        max_mines = min(self.mines, len(available_cells))
        
        # Randomly select cells for mines
        mine_positions = random.sample(available_cells, max_mines)
        
        for x, y in mine_positions:
            self.board[y][x]['value'] = -1  # -1 represents a mine
            mines_placed += 1
            
            # Increment the value of adjacent cells
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx]['value'] != -1:
                        self.board[ny][nx]['value'] += 1
        
        self.started = True
        self.start_time = time.time()
    
    def reveal_cell(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        
        cell = self.board[y][x]
        
        # If the cell is already revealed or flagged, do nothing
        if cell['state'] != HIDDEN:
            return
        
        # If this is the first cell clicked, initialize the game
        if not self.started:
            self.start_game(x, y)
        
        # Reveal the cell
        cell['state'] = REVEALED
        self.revealed_cells += 1
        
        # If it's a mine, game over
        if cell['value'] == -1:
            self.game_over = True
            self.reveal_all_mines()
            return
            
        # If it's an empty cell (no neighboring mines), reveal neighboring cells
        if cell['value'] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    self.reveal_cell(x + dx, y + dy)
        
        # Check for win condition
        if self.revealed_cells == self.total_cells - self.mines:
            self.win = True
            self.game_over = True
            self.flag_all_mines()
    
    def toggle_flag(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
            
        cell = self.board[y][x]
        
        # Can only flag hidden cells
        if cell['state'] == HIDDEN:
            cell['state'] = FLAGGED
            self.flags_placed += 1
        elif cell['state'] == FLAGGED:
            cell['state'] = HIDDEN
            self.flags_placed -= 1
    
    def reveal_all_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]['value'] == -1:
                    self.board[y][x]['state'] = REVEALED
    
    def flag_all_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]['value'] == -1 and self.board[y][x]['state'] != FLAGGED:
                    self.board[y][x]['state'] = FLAGGED
                    self.flags_placed += 1
    
    def get_elapsed_time(self):
        if not self.started:
            return 0
        if self.game_over:
            return int(self.end_time - self.start_time)
        return int(time.time() - self.start_time)
    
    def end_game(self):
        self.game_over = True
        self.end_time = time.time()
        
    def count_adjacent_flags(self, x, y):
        """Count the number of flagged cells around the given position."""
        flag_count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.board[ny][nx]['state'] == FLAGGED):
                    flag_count += 1
        return flag_count
    
    def auto_reveal_around(self, x, y):
        """Auto-reveal cells around a number if flags match the number."""
        # Only works on revealed cells with a number
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
            
        cell = self.board[y][x]
        if cell['state'] != REVEALED or cell['value'] <= 0:
            return
            
        # Check if the number of flags matches the cell value
        if self.count_adjacent_flags(x, y) == cell['value']:
            # Reveal all non-flagged cells around
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height and 
                        self.board[ny][nx]['state'] == HIDDEN):
                        self.reveal_cell(nx, ny)
                        # If game over after revealing a cell, stop the process
                        if self.game_over:
                            return

def draw_board(board):
    # Clear the screen
    DISPLAYSURF.fill(WHITE)
    
    # Draw the scoreboard
    pygame.draw.rect(DISPLAYSURF, GRAY, (0, 0, WINDOWWIDTH, 60))
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, (0, 0, WINDOWWIDTH, 60), 2)
    
    # Draw mines counter (left side)
    mines_left = board.mines - board.flags_placed
    mines_font = pygame.font.Font(None, 48)
    mines_text = mines_font.render(f"{mines_left:03d}", True, RED)
    DISPLAYSURF.blit(mines_text, (20, 15))
    
    # Draw smiley face in the middle
    face_size = 40
    face_x = (WINDOWWIDTH - face_size) // 2
    face_y = (60 - face_size) // 2
    pygame.draw.rect(DISPLAYSURF, WHITE, (face_x, face_y, face_size, face_size))
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, (face_x, face_y, face_size, face_size), 2)
    
    # Draw different face based on game state
    if board.game_over and not board.win:
        # Dead face
        pygame.draw.circle(DISPLAYSURF, YELLOW, (face_x + face_size//2, face_y + face_size//2), face_size//2 - 4)
        pygame.draw.circle(DISPLAYSURF, BLACK, (face_x + face_size//3, face_y + face_size//3), 3)  # Left eye - X
        pygame.draw.circle(DISPLAYSURF, BLACK, (face_x + 2*face_size//3, face_y + face_size//3), 3)  # Right eye - X
        pygame.draw.arc(DISPLAYSURF, BLACK, (face_x + face_size//4, face_y + face_size//2, face_size//2, face_size//3), 3.14, 2*3.14, 2)  # Sad mouth
    elif board.win:
        # Cool face
        pygame.draw.circle(DISPLAYSURF, YELLOW, (face_x + face_size//2, face_y + face_size//2), face_size//2 - 4)
        pygame.draw.circle(DISPLAYSURF, BLACK, (face_x + face_size//3, face_y + face_size//3), 3)  # Left eye
        pygame.draw.circle(DISPLAYSURF, BLACK, (face_x + 2*face_size//3, face_y + face_size//3), 3)  # Right eye
        pygame.draw.arc(DISPLAYSURF, BLACK, (face_x + face_size//4, face_y + face_size//2, face_size//2, face_size//3), 0, 3.14, 2)  # Happy mouth
    else:
        # Normal face
        pygame.draw.circle(DISPLAYSURF, YELLOW, (face_x + face_size//2, face_y + face_size//2), face_size//2 - 4)
        pygame.draw.circle(DISPLAYSURF, BLACK, (face_x + face_size//3, face_y + face_size//3), 3)  # Left eye
        pygame.draw.circle(DISPLAYSURF, BLACK, (face_x + 2*face_size//3, face_y + face_size//3), 3)  # Right eye
        pygame.draw.circle(DISPLAYSURF, BLACK, (face_x + face_size//2, face_y + 2*face_size//3), 2)  # Mouth
    
    # Draw timer (right side)
    timer_font = pygame.font.Font(None, 48)
    timer_text = timer_font.render(f"{min(board.get_elapsed_time(), 999):03d}", True, RED)
    DISPLAYSURF.blit(timer_text, (WINDOWWIDTH - 20 - timer_text.get_width(), 15))
    
    # Draw zoom level indicator (bottom-left of scoreboard)
    zoom_font = pygame.font.Font(None, 24)
    zoom_text = zoom_font.render(f"Zoom: {int(ZOOM_FACTOR * 100)}%", True, BLACK)
    DISPLAYSURF.blit(zoom_text, (20, 40))
    
    # Draw the game grid with offsets for scrolling
    for y in range(board.height):
        for x in range(board.width):
            cell = board.board[y][x]
            rect = (x * BLOCKSIZE + SCROLL_OFFSET_X, 
                   y * BLOCKSIZE + 60 + SCROLL_OFFSET_Y, 
                   BLOCKSIZE, BLOCKSIZE)
            
            # Draw cell background
            if cell['state'] == REVEALED:
                pygame.draw.rect(DISPLAYSURF, WHITE, rect)
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, rect, 1)
                
                # Draw mine if revealed
                if cell['value'] == -1:
                    DISPLAYSURF.blit(BOMBA_IMG, (rect[0] + 3, rect[1] + 3))
                # Draw number if it's a number cell
                elif cell['value'] > 0:
                    number_font = pygame.font.Font(None, 28)
                    text = number_font.render(str(cell['value']), True, COLORS[cell['value']])
                    text_rect = text.get_rect(center=(rect[0] + BLOCKSIZE//2, rect[1] + BLOCKSIZE//2))
                    DISPLAYSURF.blit(text, text_rect)
            else:  # HIDDEN or FLAGGED
                pygame.draw.rect(DISPLAYSURF, GRAY, rect)
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, rect, 1)
                
                # Draw 3D effect
                pygame.draw.line(DISPLAYSURF, WHITE, (rect[0], rect[1]), (rect[0] + BLOCKSIZE - 1, rect[1]), 2)
                pygame.draw.line(DISPLAYSURF, WHITE, (rect[0], rect[1]), (rect[0], rect[1] + BLOCKSIZE - 1), 2)
                pygame.draw.line(DISPLAYSURF, DARKGRAY, (rect[0] + BLOCKSIZE - 1, rect[1]), (rect[0] + BLOCKSIZE - 1, rect[1] + BLOCKSIZE - 1), 2)
                pygame.draw.line(DISPLAYSURF, DARKGRAY, (rect[0], rect[1] + BLOCKSIZE - 1), (rect[0] + BLOCKSIZE - 1, rect[1] + BLOCKSIZE - 1), 2)
                
                if cell['state'] == FLAGGED:
                    DISPLAYSURF.blit(FLAG_IMG, (rect[0] + 3, rect[1] + 3))

    # Draw "Tentar Novamente" button if game is over
    if board.game_over:
        button_x = (WINDOWWIDTH - 200) // 2
        button_y = (WINDOWHEIGHT - 50) // 2
        pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (button_x, button_y, 200, 50))
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, (button_x, button_y, 200, 50), 2)
        # Button text
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render("Tentar Novamente", True, BLACK)
        text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
        DISPLAYSURF.blit(button_text, text_rect)

def draw_start_screen():
    """Draw the start screen with difficulty options."""
    DISPLAYSURF.fill(WHITE)
    
    # Title
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Campo Minado", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 80))
    DISPLAYSURF.blit(title_text, title_rect)
    
    # Subtitle
    subtitle_font = pygame.font.Font(None, 36)
    subtitle_text = subtitle_font.render("Selecione a dificuldade:", True, DARKGRAY)
    subtitle_rect = subtitle_text.get_rect(center=(WINDOWWIDTH // 2, 140))
    DISPLAYSURF.blit(subtitle_text, subtitle_rect)
    
    # Difficulty buttons
    button_width, button_height = 200, 50
    button_margin = 20
    button_start_y = 200
    
    difficulties = [
        ("Fácil", "EASY"),
        ("Médio", "MEDIUM"),
        ("Difícil", "HARD"),
        ("Infinito", "INFINITE"),
        ("Personalizado", "CUSTOM")
    ]
    
    buttons = []
    for i, (text, diff) in enumerate(difficulties):
        button_x = (WINDOWWIDTH - button_width) // 2
        button_y = button_start_y + i * (button_height + button_margin)
        
        # Draw button
        pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, (button_x, button_y, button_width, button_height), 2)
        
        # Button text
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render(text, True, BLACK)
        text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        DISPLAYSURF.blit(button_text, text_rect)
        
        buttons.append((button_x, button_y, button_width, button_height, diff))
    
    return buttons

def draw_custom_screen():
    """Draw the custom difficulty setup screen."""
    DISPLAYSURF.fill(WHITE)
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Configuração Personalizada", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 80))
    DISPLAYSURF.blit(title_text, title_rect)
    
    # Input fields
    field_width, field_height = 100, 40
    label_font = pygame.font.Font(None, 32)
    input_fields = []
    
    # Width field
    width_label = label_font.render("Largura:", True, BLACK)
    DISPLAYSURF.blit(width_label, (WINDOWWIDTH // 2 - 150, 150))
    width_field = pygame.Rect(WINDOWWIDTH // 2 - 30, 150, field_width, field_height)
    pygame.draw.rect(DISPLAYSURF, WHITE, width_field)
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, width_field, 2)
    input_fields.append(("width", width_field))
    
    # Height field
    height_label = label_font.render("Altura:", True, BLACK)
    DISPLAYSURF.blit(height_label, (WINDOWWIDTH // 2 - 150, 210))
    height_field = pygame.Rect(WINDOWWIDTH // 2 - 30, 210, field_width, field_height)
    pygame.draw.rect(DISPLAYSURF, WHITE, height_field)
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, height_field, 2)
    input_fields.append(("height", height_field))
    
    # Mines field
    mines_label = label_font.render("Minas:", True, BLACK)
    DISPLAYSURF.blit(mines_label, (WINDOWWIDTH // 2 - 150, 270))
    mines_field = pygame.Rect(WINDOWWIDTH // 2 - 30, 270, field_width, field_height)
    pygame.draw.rect(DISPLAYSURF, WHITE, mines_field)
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, mines_field, 2)
    input_fields.append(("mines", mines_field))
    
    # Start button
    button_width, button_height = 200, 50
    button_x = (WINDOWWIDTH - button_width) // 2
    button_y = 340
    pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, (button_x, button_y, button_width, button_height), 2)
    
    # Button text
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Iniciar Jogo", True, BLACK)
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    DISPLAYSURF.blit(button_text, text_rect)
    
    start_button = (button_x, button_y, button_width, button_height)
    
    # Back button
    back_width, back_height = 100, 40
    back_x = 20
    back_y = 20
    pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (back_x, back_y, back_width, back_height))
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, (back_x, back_y, back_width, back_height), 2)
    
    back_text = button_font.render("Voltar", True, BLACK)
    back_rect = back_text.get_rect(center=(back_x + back_width // 2, back_y + back_height // 2))
    DISPLAYSURF.blit(back_text, back_rect)
    
    back_button = (back_x, back_y, back_width, back_height)
    
    return input_fields, start_button, back_button

def draw_input_field_values(fields, values):
    """Draw the values in input fields"""
    font = pygame.font.Font(None, 32)
    
    for field_name, field_rect in fields:
        if field_name in values:
            value_text = font.render(values[field_name], True, BLACK)
            text_rect = value_text.get_rect(midleft=(field_rect.x + 5, field_rect.centery))
            DISPLAYSURF.blit(value_text, text_rect)

def check_button_click(mouse_pos, buttons):
    """Check if a button was clicked from a list of buttons"""
    x, y = mouse_pos
    for button in buttons:
        button_x, button_y, width, height, value = button
        if button_x <= x <= button_x + width and button_y <= y <= button_y + height:
            return value
    return None

def check_rect_click(mouse_pos, rect):
    """Check if a rectangle was clicked"""
    x, y = mouse_pos
    return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]

def get_cell_at_pixel(x, y):
    """Determine which cell a pixel coordinate belongs to"""
    if y < 60:  # Clicked on scoreboard
        return None
    
    # Apply the scroll offsets and account for zoom
    adjusted_x = (x - SCROLL_OFFSET_X) // BLOCKSIZE
    adjusted_y = ((y - 60) - SCROLL_OFFSET_Y) // BLOCKSIZE
    
    if (0 <= adjusted_x < BOARDWIDTH) and (0 <= adjusted_y < BOARDHEIGHT):
        return (adjusted_x, adjusted_y)
    return None

def check_smiley_click(x, y):
    """Check if the smiley face was clicked"""
    face_size = 40
    face_x = (WINDOWWIDTH - face_size) // 2
    face_y = (60 - face_size) // 2
    return face_x <= x <= face_x + face_size and face_y <= y <= face_y + face_size

def check_restart_button_click(x, y):
    """Check if the "Tentar Novamente" button was clicked"""
    button_x = (WINDOWWIDTH - 200) // 2
    button_y = (WINDOWHEIGHT - 50) // 2
    return button_x <= x <= button_x + 200 and button_y <= y <= button_y + 50

def main():
    """Main game function"""
    global BOARDWIDTH, BOARDHEIGHT, MINES, WINDOWWIDTH, WINDOWHEIGHT, DISPLAYSURF
    global BLOCKSIZE, ZOOM_FACTOR, SCROLL_OFFSET_X, SCROLL_OFFSET_Y
    
    try:
        # State variables
        in_start_screen = True
        in_custom_screen = False
        custom_values = {"width": "16", "height": "16", "mines": "40"}
        active_field = None
        game_board = None
        
        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                    
                # Handle window resize events
                if event.type == VIDEORESIZE:
                    # Update window size while maintaining minimum dimensions
                    WINDOWWIDTH = max(event.w, 480)
                    WINDOWHEIGHT = max(event.h, 60 + MIN_BLOCKSIZE)
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
                
                # Handle keyboard zoom with Ctrl+ and Ctrl-
                if event.type == KEYDOWN:
                    ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL
                    
                    # Zoom in with Ctrl+plus
                    if ctrl_pressed and (event.key == K_PLUS or event.key == K_EQUALS):
                        if BLOCKSIZE < MAX_BLOCKSIZE:
                            BLOCKSIZE += ZOOM_STEP
                            ZOOM_FACTOR = BLOCKSIZE / DEFAULT_BLOCKSIZE
                            update_images_for_zoom()
                            
                    # Zoom out with Ctrl+minus
                    elif ctrl_pressed and event.key == K_MINUS:
                        if BLOCKSIZE > MIN_BLOCKSIZE:
                            BLOCKSIZE -= ZOOM_STEP
                            ZOOM_FACTOR = BLOCKSIZE / DEFAULT_BLOCKSIZE
                            update_images_for_zoom()
                
                # Handle touchpad/mouse wheel for navigation
                if event.type == pygame.MOUSEWHEEL:
                    # Handle vertical scrolling
                    if event.y != 0:
                        SCROLL_OFFSET_Y += event.y * BLOCKSIZE
                    # Handle horizontal scrolling (if supported)
                    if hasattr(event, 'x') and event.x != 0:
                        SCROLL_OFFSET_X += event.x * BLOCKSIZE
                
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    # If in game, go back to start screen
                    if not in_start_screen and not in_custom_screen:
                        in_start_screen = True
                    # If in custom screen, go back to start screen
                    elif in_custom_screen:
                        in_custom_screen = False
                        in_start_screen = True
                    # If in start screen, exit game
                    else:
                        running = False
                        pygame.quit()
                        sys.exit()
                
                # Start screen logic
                if in_start_screen:
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        buttons = draw_start_screen()
                        difficulty = check_button_click(event.pos, buttons)
                        
                        if difficulty:
                            if difficulty == "CUSTOM":
                                # Show custom difficulty screen
                                in_custom_screen = True
                                in_start_screen = False
                            else:
                                # Set difficulty from presets
                                BOARDWIDTH = DIFFICULTY[difficulty]["width"]
                                BOARDHEIGHT = DIFFICULTY[difficulty]["height"]
                                MINES = DIFFICULTY[difficulty]["mines"]
                                
                                # Update window size
                                WINDOWWIDTH = max(BOARDWIDTH * BLOCKSIZE, 480)
                                WINDOWHEIGHT = BOARDHEIGHT * BLOCKSIZE + 60
                                DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                                
                                # Start game
                                game_board = Board(BOARDWIDTH, BOARDHEIGHT, MINES)
                                in_start_screen = False
                
                # Custom screen logic
                elif in_custom_screen:
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        input_fields, start_button, back_button = draw_custom_screen()
                        
                        # Check if back button was clicked
                        if check_rect_click(event.pos, back_button):
                            in_custom_screen = False
                            in_start_screen = True
                            active_field = None
                        
                        # Check if start button was clicked
                        elif check_rect_click(event.pos, start_button):
                            # Validate and convert custom values
                            try:
                                width = max(9, min(50, int(custom_values["width"])))
                                height = max(9, min(30, int(custom_values["height"])))
                                max_mines = (width * height) - 9  # Leave space for first click
                                mines = max(1, min(max_mines, int(custom_values["mines"])))
                                
                                # Set board dimensions
                                BOARDWIDTH = width
                                BOARDHEIGHT = height
                                MINES = mines
                                
                                # Update window size
                                WINDOWWIDTH = max(BOARDWIDTH * BLOCKSIZE, 480)
                                WINDOWHEIGHT = BOARDHEIGHT * BLOCKSIZE + 60
                                DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                                
                                # Start game
                                game_board = Board(BOARDWIDTH, BOARDHEIGHT, MINES)
                                in_custom_screen = False
                                
                            except ValueError:
                                # Handle invalid input (do nothing for now)
                                pass
                        
                        # Check if an input field was clicked
                        else:
                            active_field = None
                            for field_name, field_rect in input_fields:
                                if field_rect.collidepoint(event.pos):
                                    active_field = field_name
                                    break
                    
                    # Handle keyboard input for custom values
                    elif event.type == KEYDOWN and active_field:
                        if event.key == K_BACKSPACE:
                            custom_values[active_field] = custom_values[active_field][:-1]
                        elif event.key in (K_RETURN, K_TAB):
                            # Move to next field or deactivate
                            field_names = ["width", "height", "mines"]
                            current_idx = field_names.index(active_field)
                            next_idx = (current_idx + 1) % len(field_names)
                            active_field = field_names[next_idx]
                        elif event.unicode.isdigit():
                            # Limit input to reasonable values
                            max_length = 2 if active_field == "mines" else 2
                            if len(custom_values[active_field]) < max_length:
                                custom_values[active_field] += event.unicode
                # Game logic
                else:
                    if event.type == MOUSEBUTTONUP:
                        mouse_x, mouse_y = event.pos
                        
                        # Check if the smiley face was clicked (restart game)
                        if check_smiley_click(mouse_x, mouse_y):
                            game_board = Board(BOARDWIDTH, BOARDHEIGHT, MINES)
                            continue
                        
                        # Check if the restart button was clicked
                        if game_board and game_board.game_over and check_restart_button_click(mouse_x, mouse_y):
                            game_board = Board(BOARDWIDTH, BOARDHEIGHT, MINES)
                            continue
                        
                        cell = get_cell_at_pixel(mouse_x, mouse_y)
                        if cell and game_board and not game_board.game_over:
                            x, y = cell
                            # Get keyboard modifiers state
                            shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                            
                            if event.button == 1:  # Left click
                                # Check if clicking on a revealed cell with a number
                                if (0 <= x < game_board.width and 0 <= y < game_board.height and 
                                    game_board.board[y][x]['state'] == REVEALED and
                                    game_board.board[y][x]['value'] > 0):
                                    # Try to auto-reveal surrounding cells
                                    game_board.auto_reveal_around(x, y)
                                    if game_board.game_over:
                                        game_board.end_game()
                                # If Shift is pressed, toggle flag
                                elif shift_pressed:
                                    game_board.toggle_flag(x, y)
                                # Otherwise handle normal click logic
                                else:
                                    # Regular cell reveal
                                    game_board.reveal_cell(x, y)
                                    if game_board.game_over:
                                        game_board.end_game()
                            
                            elif event.button == 3:  # Right click - alternative way to flag
                                game_board.toggle_flag(x, y)
            
            # Draw the appropriate screen
            if in_start_screen:
                buttons = draw_start_screen()
            elif in_custom_screen:
                input_fields, _, _ = draw_custom_screen()
                draw_input_field_values(input_fields, custom_values)
            elif game_board:
                draw_board(game_board)
            
            # Update the display
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
