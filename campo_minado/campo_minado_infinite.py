import pygame
import sys
import random
import time
import os
import json
import datetime
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Inicializa o sistema de som

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
AUTO_RESIZE = False  # Whether to automatically resize blocks based on window size
show_tips = True  # Whether to show tips and hints during gameplay

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
DARKBLUE = (25, 25, 112)     # Dark blue for dark theme
LIGHTGRAY = (220, 220, 220)  # Light gray for dark theme cells

# Color themes
THEMES = {
    "LIGHT": {
        "background": WHITE,
        "cell_revealed": WHITE,
        "cell_hidden": GRAY,
        "grid": DARKGRAY,
        "text": BLACK,
        "scoreboard": GRAY,
        "button": LIGHTBLUE
    },
    "DARK": {
        "background": DARKGRAY,
        "cell_revealed": DARKBLUE,
        "cell_hidden": BLACK,
        "grid": BLACK,
        "text": WHITE,
        "scoreboard": BLACK,
        "button": DARKBLUE
    }
}

# Current theme
CURRENT_THEME = "LIGHT"

# Number colors
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

# Dark theme number colors
COLORS_DARK = {
    1: (100, 149, 237),  # Cornflower Blue
    2: (144, 238, 144),  # Light Green
    3: (255, 99, 71),    # Tomato
    4: (135, 206, 250),  # Light Blue
    5: (255, 160, 122),  # Light Salmon
    6: (64, 224, 208),   # Turquoise
    7: (255, 255, 255),  # White
    8: (211, 211, 211)   # Light Grey
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
    ORIGINAL_HEART_IMG = pygame.image.load(os.path.join(script_dir, 'img', 'coracao.png'))
    base_dir = script_dir
except FileNotFoundError:
    # Fallback to full path if relative path doesn't work
    base_dir = "c:\\Users\\BrunoLocal.BRUNO-note.000\\Downloads\\x\\CÓDIGOS\\campo_minado"
    ORIGINAL_BOMBA_IMG = pygame.image.load(os.path.join(base_dir, 'img', 'bomba.png'))
    ORIGINAL_FLAG_IMG = pygame.image.load(os.path.join(base_dir, 'img', 'flag.png'))
    ORIGINAL_HEART_IMG = pygame.image.load(os.path.join(base_dir, 'img', 'coracao.png'))

# Scale images according to current BLOCKSIZE
BOMBA_IMG = pygame.transform.scale(ORIGINAL_BOMBA_IMG, (BLOCKSIZE-6, BLOCKSIZE-6))
FLAG_IMG = pygame.transform.scale(ORIGINAL_FLAG_IMG, (BLOCKSIZE-6, BLOCKSIZE-6))
HEART_IMG = pygame.transform.scale(ORIGINAL_HEART_IMG, (25, 25))  # Fixed size for hearts

# Create sound effects
try:
    # Create sounds directory if it doesn't exist
    sounds_dir = os.path.join(base_dir, 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Define sound file paths
    click_sound_path = os.path.join(sounds_dir, 'click.wav')
    explosion_sound_path = os.path.join(sounds_dir, 'explosion.wav')
    flag_sound_path = os.path.join(sounds_dir, 'flag.wav')
    win_sound_path = os.path.join(sounds_dir, 'win.wav')
    
    # Create default sounds if they don't exist
    if not os.path.exists(click_sound_path):
        # Create simple placeholder sound (beep)
        import wave
        import struct
        
        # Parameters for a simple beep sound
        for path, params in [
            (click_sound_path, {"duration": 0.1, "freq": 1000, "volume": 0.1}),
            (explosion_sound_path, {"duration": 0.5, "freq": 200, "volume": 0.3}),
            (flag_sound_path, {"duration": 0.1, "freq": 1500, "volume": 0.1}),
            (win_sound_path, {"duration": 1.0, "freq": 800, "volume": 0.2})
        ]:
            if not os.path.exists(path):
                duration = params["duration"]  # seconds
                freq = params["freq"]  # Hz
                volume = params["volume"]  # 0.0 to 1.0
                samplerate = 44100
                samples = int(duration * samplerate)
                
                with wave.open(path, 'wb') as wave_file:
                    wave_file.setnchannels(1)  # Mono
                    wave_file.setsampwidth(2)  # 2 bytes (16 bits)
                    wave_file.setframerate(samplerate)
                    
                    for i in range(samples):
                        # Simple sine wave
                        value = int(32767.0 * volume * math.sin(2 * math.pi * freq * i / samplerate))
                        data = struct.pack('<h', value)
                        wave_file.writeframes(data)
    
    # Load sound effects
    SOUNDS = {
        "click": pygame.mixer.Sound(click_sound_path),
        "explosion": pygame.mixer.Sound(explosion_sound_path),
        "flag": pygame.mixer.Sound(flag_sound_path),
        "win": pygame.mixer.Sound(win_sound_path)
    }
    
    # Set volume
    for sound in SOUNDS.values():
        sound.set_volume(0.3)
        
    # Sound enabled flag
    SOUND_ENABLED = True
    
except Exception as e:
    print(f"Could not load sounds: {e}")
    SOUNDS = {}
    SOUND_ENABLED = False

# Create saves directory
SAVES_DIR = os.path.join(base_dir, 'saves')
os.makedirs(SAVES_DIR, exist_ok=True)

# Stats file
STATS_FILE = os.path.join(base_dir, 'stats.json')

# Game statistics
STATISTICS = {
    "games_played": 0,
    "games_won": 0,
    "best_times": {
        "EASY": 999,
        "MEDIUM": 999,
        "HARD": 999,
        "INFINITE": 999
    },
    "total_cells_revealed": 0,
    "total_flags_placed": 0,
    "total_mines_exploded": 0
}

# Load statistics if available
try:
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            loaded_stats = json.load(f)
            STATISTICS.update(loaded_stats)
except Exception as e:
    print(f"Could not load statistics: {e}")

# Function to update images when zoom changes
def update_images_for_zoom():
    global BOMBA_IMG, FLAG_IMG, HEART_IMG
    BOMBA_IMG = pygame.transform.scale(ORIGINAL_BOMBA_IMG, (BLOCKSIZE-6, BLOCKSIZE-6))
    FLAG_IMG = pygame.transform.scale(ORIGINAL_FLAG_IMG, (BLOCKSIZE-6, BLOCKSIZE-6))
    HEART_IMG = pygame.transform.scale(ORIGINAL_HEART_IMG, (25, 25))  # Keep heart size consistent

def apply_auto_resize():
    """Apply auto-resize based on current window size and board dimensions."""
    global BLOCKSIZE, ZOOM_FACTOR, SCROLL_OFFSET_X, SCROLL_OFFSET_Y
    
    if not 'game_board' in globals() or not globals()['game_board']:
        return
        
    game_board = globals()['game_board']
    
    # Calculate the ideal block size to fit the board in the window
    max_width = WINDOWWIDTH / game_board.width
    max_height = (WINDOWHEIGHT - 60) / game_board.height  # Account for scoreboard
    
    # Choose the smaller dimension to ensure entire board fits
    new_blocksize = min(max_width, max_height, MAX_BLOCKSIZE)
    new_blocksize = max(new_blocksize, MIN_BLOCKSIZE)  # Don't go below minimum size
    
    # Apply the new block size
    BLOCKSIZE = int(new_blocksize)
    ZOOM_FACTOR = BLOCKSIZE / DEFAULT_BLOCKSIZE
    
    # Update images with new size
    update_images_for_zoom()
    
    # Center the board
    SCROLL_OFFSET_X = (WINDOWWIDTH - (game_board.width * BLOCKSIZE)) // 2
    SCROLL_OFFSET_Y = (WINDOWHEIGHT - 60 - (game_board.height * BLOCKSIZE)) // 2
    
    # Ensure minimum offset of 0
    SCROLL_OFFSET_X = max(0, SCROLL_OFFSET_X)
    SCROLL_OFFSET_Y = max(0, SCROLL_OFFSET_Y)

# Game state
HIDDEN = 0
REVEALED = 1
FLAGGED = 2

class Board:
    def __init__(self, width, height, mines, difficulty="MEDIUM"):
        self.width = width
        self.height = height
        self.mines = mines
        self.difficulty = difficulty  # Track difficulty level
        self.board = [[{'state': HIDDEN, 'value': 0, 'marked_for_hint': False} for _ in range(width)] for _ in range(height)]
        self.lives = 3  # Start with 3 lives
        self.started = False
        self.game_over = False
        self.win = False
        self.start_time = 0
        self.flags_placed = 0
        self.revealed_cells = 0
        self.total_cells = width * height
        self.hints_used = 0
        self.hints_available = 999  # Unlimited hints
        self.hint_mode_active = False  # New property to track if hint mode is active
        self.paused = False
        self.pause_start_time = 0
        self.total_pause_time = 0
        self.last_action = ""  # Track last action for undo
        
        # Set hints based on difficulty
        if difficulty == "EASY":
            self.hints_available = 5
        elif difficulty == "MEDIUM":
            self.hints_available = 3
        elif difficulty == "HARD":
            self.hints_available = 1
        elif difficulty == "INFINITE":
            self.hints_available = 10  # More hints for infinite mode
        
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
        
        # If it's a mine, lose a life or game over
        if cell['value'] == -1:
            if self.lives > 1:
                self.lives -= 1
                # Mark this mine as "defused" by changing its value
                cell['value'] = -2  # Special value for defused mine
                
                # Play explosion sound but don't end game
                if "explosion" in SOUNDS and SOUND_ENABLED:
                    SOUNDS["explosion"].play()
                
                # Create an explosion effect for feedback
                # But don't end the game yet
                return
            else:
                # No more lives left, game over
                self.lives = 0
                self.game_over = True
                self.end_game()  # Call end_game to set end_time properly
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
                # Reveal all mines except those already defused
                if self.board[y][x]['value'] == -1:
                    self.board[y][x]['state'] = REVEALED
                # Note: we leave defused mines (-2) as they are

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
        """End the current game and set the end time."""
        self.game_over = True
        self.end_time = time.time()
        
        # Turn off hint mode when the game ends
        if self.hint_mode_active:
            self.hint_mode_active = False
            self.clear_hints()
        
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
    
    def get_hint(self):
        """Provide a hint to the player by finding a safe move."""
        if not self.started or self.game_over or self.hints_available <= 0:
            return None
            
        # First, check for obvious places where flags should be placed
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                if cell['state'] == REVEALED and cell['value'] > 0:
                    # Count hidden and flagged cells around
                    hidden_count = 0
                    flag_count = 0
                    hidden_cells = []
                    
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                if self.board[ny][nx]['state'] == HIDDEN:
                                    hidden_count += 1
                                    hidden_cells.append((nx, ny))
                                elif self.board[ny][nx]['state'] == FLAGGED:
                                    flag_count += 1
                                    
                    # If remaining hidden cells equal remaining mines, they should all be flags
                    if hidden_count > 0 and cell['value'] - flag_count == hidden_count:
                        hx, hy = random.choice(hidden_cells)
                        self.board[hy][hx]['marked_for_hint'] = True
                        self.hints_available -= 1
                        return (hx, hy, "flag")
        
        # Next, look for places where it's safe to click
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                if cell['state'] == REVEALED and cell['value'] > 0:
                    if self.count_adjacent_flags(x, y) == cell['value']:
                        # All mines around this cell are flagged, so other cells are safe
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                if dx == 0 and dy == 0:
                                    continue
                                nx, ny = x + dx, y + dy
                                if (0 <= nx < self.width and 0 <= ny < self.height and 
                                    self.board[ny][nx]['state'] == HIDDEN):
                                    self.board[ny][nx]['marked_for_hint'] = True
                                    self.hints_available -= 1
                                    return (nx, ny, "safe")
        
        # If no obvious hint found, just find a random safe cell as a last resort
        safe_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]['state'] == HIDDEN and self.board[y][x]['value'] != -1:
                    safe_cells.append((x, y))
                    
        if safe_cells:
            hx, hy = random.choice(safe_cells)
            self.board[hy][hx]['marked_for_hint'] = True
            self.hints_available -= 1
            return (hx, hy, "guaranteed")
            
        # No safe cells found (unlikely but possible)
        return None
    
    def clear_hints(self):
        """Clear all hint markers."""
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x]['marked_for_hint'] = False
    
    def peek_cell(self, x, y):
        """Show cell content as hint without exploding mines or changing game state."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        
        # Only allow peeking if there are hints available
        if self.hints_available <= 0:
            return
        
        cell = self.board[y][x]
        
        # If the cell is already revealed or marked for hint, do nothing
        if cell['state'] == REVEALED or cell['marked_for_hint']:
            return
        
        # Mark the cell for visualization in hint mode
        cell['marked_for_hint'] = True
        
        # Decrement available hints
        self.hints_available -= 1
        self.hints_used += 1
        
        # No need to check game over or win condition since we're just peeking
        return cell['value']
    
    def save_game(self, filename=None):
        """Save the current game state to a file."""
        if not self.started:
            return False
            
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"game_{self.difficulty}_{timestamp}.json"
            
        save_path = os.path.join(SAVES_DIR, filename)
        
        # Calculate elapsed time accounting for pauses
        elapsed_time = 0
        if self.started:
            if self.paused:
                elapsed_time = self.pause_start_time - self.start_time - self.total_pause_time
            else:
                elapsed_time = time.time() - self.start_time - self.total_pause_time
                
        # Create a serializable version of the board
        serializable_board = []
        for row in self.board:
            serializable_row = []
            for cell in row:
                # Copy the cell dict without marked_for_hint which is temporary
                cell_copy = {k: v for k, v in cell.items() if k != 'marked_for_hint'}
                serializable_row.append(cell_copy)
            serializable_board.append(serializable_row)
        
        game_data = {
            "width": self.width,
            "height": self.height,
            "mines": self.mines,
            "difficulty": self.difficulty,
            "board": serializable_board,
            "started": self.started,
            "game_over": self.game_over,
            "win": self.win,
            "elapsed_time": elapsed_time,
            "flags_placed": self.flags_placed,
            "revealed_cells": self.revealed_cells,
            "hints_available": self.hints_available,
            "hints_used": self.hints_used,
            "save_date": datetime.datetime.now().isoformat()        }
        
        try:
            with open(save_path, 'w') as f:
                json.dump(game_data, f)
            return filename
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def pause_game(self):
        """Pause the game timer."""
        if self.started and not self.game_over and not self.paused:
            self.paused = True
            self.pause_start_time = time.time()
            
            # Automatically turn off hint mode when pausing
            if self.hint_mode_active:
                self.hint_mode_active = False
                self.clear_hints()
            
    def unpause_game(self):
        """Unpause the game timer."""
        if self.paused:
            self.paused = False
            pause_duration = time.time() - self.pause_start_time
            self.total_pause_time += pause_duration
    
    def get_completion_percentage(self):
        """Get the percentage of the board that has been completed."""
        if not self.started:
            return 0
        
        total_non_mine_cells = self.total_cells - self.mines
        if total_non_mine_cells == 0:  # Avoid division by zero
            return 100
            
        return (self.revealed_cells / total_non_mine_cells) * 100
    
    def load_game(self, filename):
        """Load a saved game from a file."""
        load_path = os.path.join(SAVES_DIR, filename)
        
        try:
            with open(load_path, 'r') as f:
                game_data = json.load(f)
                
            # Update basic properties
            self.width = game_data["width"]
            self.height = game_data["height"]
            self.mines = game_data["mines"]
            self.difficulty = game_data.get("difficulty", "MEDIUM")
            self.started = game_data["started"]
            self.game_over = game_data["game_over"]
            self.win = game_data["win"]
            self.flags_placed = game_data["flags_placed"]
            self.revealed_cells = game_data["revealed_cells"]
            self.hints_available = game_data.get("hints_available", 3)
            self.hints_used = game_data.get("hints_used", 0)
            self.total_cells = self.width * self.height
            
            # Recreate board with loaded state
            self.board = []
            for row in game_data["board"]:
                new_row = []
                for cell in row:
                    # Add marked_for_hint which isn't saved
                    cell["marked_for_hint"] = False
                    new_row.append(cell)
                self.board.append(new_row)
                
            # Set up timing info
            self.start_time = time.time() - game_data["elapsed_time"]
            self.paused = False
            self.total_pause_time = 0
            
            return True
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    @staticmethod
    def list_saved_games():
        """List all saved games."""
        try:
            saved_games = []
            for filename in os.listdir(SAVES_DIR):
                if filename.endswith('.json'):
                    file_path = os.path.join(SAVES_DIR, filename)
                    with open(file_path, 'r') as f:
                        try:
                            game_data = json.load(f)
                            # Create a display entry with useful info
                            save_info = {
                                "filename": filename,
                                "difficulty": game_data.get("difficulty", "Unknown"),
                                "dimensions": f"{game_data.get('width', '?')}x{game_data.get('height', '?')}",
                                "mines": game_data.get("mines", "?"),
                                "save_date": game_data.get("save_date", "Unknown"),
                                "elapsed_time": game_data.get("elapsed_time", 0),
                                "completion": f"{game_data.get('revealed_cells', 0)}/{game_data.get('width', 1) * game_data.get('height', 1) - game_data.get('mines', 0)}"
                            }
                            saved_games.append(save_info)
                        except:
                            # Skip invalid files
                            continue
        
            # Sort by save date, newest first
            saved_games.sort(key=lambda x: x.get("save_date", ""), reverse=True)
            return saved_games
            
        except Exception as e:
            print(f"Error listing saved games: {e}")
            return []
        
def draw_board(board):
    theme = THEMES[CURRENT_THEME]
    
    # Clear the screen
    DISPLAYSURF.fill(theme["background"])
    
    # Draw the scoreboard
    pygame.draw.rect(DISPLAYSURF, theme["scoreboard"], (0, 0, WINDOWWIDTH, 60))
    pygame.draw.rect(DISPLAYSURF, theme["grid"], (0, 0, WINDOWWIDTH, 60), 2)
    
    # Draw mines counter (left side)
    mines_left = board.mines - board.flags_placed
    mines_font = pygame.font.Font(None, 48)
    mines_text = mines_font.render(f"{mines_left:03d}", True, RED)
    DISPLAYSURF.blit(mines_text, (20, 15))
    
    # Draw lives (hearts) to the right of the mine counter
    heart_x = 110
    for i in range(board.lives):
        DISPLAYSURF.blit(HEART_IMG, (heart_x + i * 30, 18))
    
    # Draw smiley face in the middle
    face_size = 40
    face_x = (WINDOWWIDTH - face_size) // 2
    face_y = (60 - face_size) // 2
    pygame.draw.rect(DISPLAYSURF, WHITE, (face_x, face_y, face_size, face_size))
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, (face_x, face_y, face_size, face_size), 2)
    
    # Draw different face based on game state
    if board.paused:
        # Paused face
        pygame.draw.circle(DISPLAYSURF, YELLOW, (face_x + face_size//2, face_y + face_size//2), face_size//2 - 4)
        # Draw pause symbol
        pygame.draw.rect(DISPLAYSURF, BLACK, (face_x + face_size//3 - 2, face_y + face_size//3, 4, face_size//3))
        pygame.draw.rect(DISPLAYSURF, BLACK, (face_x + 2*face_size//3 - 2, face_y + face_size//3, 4, face_size//3))
    elif board.game_over and not board.win:
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
      # Draw timer (right side) with pulsing effect when game is active
    timer_font = pygame.font.Font(None, 48)
    timer_value = min(board.get_elapsed_time(), 999)
    
    # Add pulsing color effect when game is in progress
    timer_color = RED
    if board.started and not board.game_over and not board.paused:
        # Pulse effect - change brightness of red based on seconds
        pulse_value = min(255, 150 + int(abs(math.sin(time.time() * 2)) * 105))
        timer_color = (pulse_value, 0, 0)
    
    timer_text = timer_font.render(f"{timer_value:03d}", True, timer_color)
    DISPLAYSURF.blit(timer_text, (WINDOWWIDTH - 20 - timer_text.get_width(), 15))
    
    # Draw hint button (right side)
    hint_font = pygame.font.Font(None, 24)
    hint_text = hint_font.render(f"Dicas: {board.hints_available}", True, theme["text"])
    hint_width = hint_text.get_width() + 10
    DISPLAYSURF.blit(hint_text, (WINDOWWIDTH - 20 - hint_width, 40))
      # Draw zoom level indicator (bottom-left of scoreboard)
    zoom_font = pygame.font.Font(None, 24)
    zoom_text = zoom_font.render(f"Zoom: {int(ZOOM_FACTOR * 100)}%", True, theme["text"])
    DISPLAYSURF.blit(zoom_text, (20, 40))
    
    # Draw difficulty indicator (center-bottom of scoreboard)
    diff_font = pygame.font.Font(None, 24)
    diff_color = {
        "EASY": GREEN,
        "MEDIUM": YELLOW,
        "HARD": RED,
        "INFINITE": BLUE,
        "CUSTOM": LIGHTBLUE
    }.get(board.difficulty, WHITE)
    
    diff_text = diff_font.render(f"Dificuldade: {board.difficulty}", True, diff_color)
    diff_rect = diff_text.get_rect(center=(WINDOWWIDTH // 2, 45))
    DISPLAYSURF.blit(diff_text, diff_rect)
    
    # Draw progress bar
    if board.started and not board.game_over:
        completion = board.get_completion_percentage()
        progress_width = int((WINDOWWIDTH - 100) * (completion / 100))
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, (50, 55, WINDOWWIDTH - 100, 3))
        pygame.draw.rect(DISPLAYSURF, GREEN, (50, 55, progress_width, 3))
      # Draw the game grid with offsets for scrolling
    for y in range(board.height):
        for x in range(board.width):
            cell = board.board[y][x]
            rect = (x * BLOCKSIZE + SCROLL_OFFSET_X, 
                   y * BLOCKSIZE + 60 + SCROLL_OFFSET_Y, 
                   BLOCKSIZE, BLOCKSIZE)
            
            # Check if cell is visible within the window
            if (rect[0] > WINDOWWIDTH or rect[1] > WINDOWHEIGHT or 
                rect[0] + BLOCKSIZE < 0 or rect[1] + BLOCKSIZE < 60):
                continue  # Skip drawing this cell
            
            # Check if the game is paused (only draw revealed cells)
            if board.paused and cell['state'] != REVEALED:
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, rect)
                pygame.draw.rect(DISPLAYSURF, BLACK, rect, 1)
                continue
                
            # Draw cell background
            if cell['state'] == REVEALED:
                pygame.draw.rect(DISPLAYSURF, theme["cell_revealed"], rect)
                pygame.draw.rect(DISPLAYSURF, theme["grid"], rect, 1)
                
                # Draw mine if revealed
                if cell['value'] == -1:
                    DISPLAYSURF.blit(BOMBA_IMG, (rect[0] + 3, rect[1] + 3))
                # Draw defused mine (special case)
                elif cell['value'] == -2:
                    # Draw a defused mine (crossed out)
                    DISPLAYSURF.blit(BOMBA_IMG, (rect[0] + 3, rect[1] + 3))
                    # Draw an X over it
                    pygame.draw.line(DISPLAYSURF, RED, (rect[0] + 5, rect[1] + 5), 
                                   (rect[0] + BLOCKSIZE - 5, rect[1] + BLOCKSIZE - 5), 3)
                    pygame.draw.line(DISPLAYSURF, RED, (rect[0] + BLOCKSIZE - 5, rect[1] + 5), 
                                   (rect[0] + 5, rect[1] + BLOCKSIZE - 5), 3)
                # Draw number if it's a number cell
                elif cell['value'] > 0:
                    number_font = pygame.font.Font(None, 28)
                    # Use appropriate color scheme based on theme
                    color = COLORS[cell['value']] if CURRENT_THEME == "LIGHT" else COLORS_DARK[cell['value']]
                    text = number_font.render(str(cell['value']), True, color)
                    text_rect = text.get_rect(center=(rect[0] + BLOCKSIZE//2, rect[1] + BLOCKSIZE//2))
                    DISPLAYSURF.blit(text, text_rect)
            else:  # HIDDEN or FLAGGED
                pygame.draw.rect(DISPLAYSURF, theme["cell_hidden"], rect)
                pygame.draw.rect(DISPLAYSURF, theme["grid"], rect, 1)
                
                # Draw 3D effect - adjust colors based on theme
                top_color = WHITE if CURRENT_THEME == "LIGHT" else GRAY
                bottom_color = DARKGRAY if CURRENT_THEME == "LIGHT" else BLACK
                
                pygame.draw.line(DISPLAYSURF, top_color, (rect[0], rect[1]), (rect[0] + BLOCKSIZE - 1, rect[1]), 2)
                pygame.draw.line(DISPLAYSURF, top_color, (rect[0], rect[1]), (rect[0], rect[1] + BLOCKSIZE - 1), 2)
                pygame.draw.line(DISPLAYSURF, bottom_color, (rect[0] + BLOCKSIZE - 1, rect[1]), (rect[0] + BLOCKSIZE - 1, rect[1] + BLOCKSIZE - 1), 2)
                pygame.draw.line(DISPLAYSURF, bottom_color, (rect[0], rect[1] + BLOCKSIZE - 1), (rect[0] + BLOCKSIZE - 1, rect[1] + BLOCKSIZE - 1), 2)
                
                if cell['state'] == FLAGGED:
                    DISPLAYSURF.blit(FLAG_IMG, (rect[0] + 3, rect[1] + 3))
                
            # Draw hint highlight if cell is marked for hint
            if cell['marked_for_hint']:
                # If it's a mine, show the mine with a hint overlay
                if cell['value'] == -1:
                    # Draw mine with hint overlay
                    DISPLAYSURF.blit(BOMBA_IMG, (rect[0] + 3, rect[1] + 3))
                    # Draw semi-transparent hint overlay
                    hint_overlay = pygame.Surface((BLOCKSIZE, BLOCKSIZE), pygame.SRCALPHA)
                    hint_overlay.fill((0, 255, 0, 100))  # Semi-transparent green
                    DISPLAYSURF.blit(hint_overlay, rect)
                # If it's a number, show the number with a hint overlay
                elif cell['value'] > 0:
                    # Draw number
                    number_font = pygame.font.Font(None, 28)
                    color = COLORS[cell['value']] if CURRENT_THEME == "LIGHT" else COLORS_DARK[cell['value']]
                    text = number_font.render(str(cell['value']), True, color)
                    text_rect = text.get_rect(center=(rect[0] + BLOCKSIZE//2, rect[1] + BLOCKSIZE//2))
                    DISPLAYSURF.blit(text, text_rect)
                    # Draw hint overlay
                    hint_overlay = pygame.Surface((BLOCKSIZE, BLOCKSIZE), pygame.SRCALPHA)
                    hint_overlay.fill((0, 255, 0, 100))  # Semi-transparent green
                    DISPLAYSURF.blit(hint_overlay, rect)
                # If it's empty, show with a hint overlay
                else:
                    # Draw hint overlay
                    hint_overlay = pygame.Surface((BLOCKSIZE, BLOCKSIZE), pygame.SRCALPHA)
                    hint_overlay.fill((0, 255, 0, 100))  # Semi-transparent green
                    DISPLAYSURF.blit(hint_overlay, rect)
                
    # Draw game end or pause overlay
    if board.game_over or board.paused:
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # More opaque black for better readability
        DISPLAYSURF.blit(overlay, (0, 0))
        
        button_font = pygame.font.Font(None, 36)
        
        if board.paused:
            # Draw "PAUSED" text
            pause_font = pygame.font.Font(None, 72)
            pause_text = pause_font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 3))
            DISPLAYSURF.blit(pause_text, text_rect)
            
            # Draw "Continue" button
            button_x = (WINDOWWIDTH - 200) // 2
            button_y = WINDOWHEIGHT // 2 - 60
            pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, 200, 50))
            pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, 200, 50), 2)
            
            button_text = button_font.render("Continuar", True, theme["text"])
            text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
            DISPLAYSURF.blit(button_text, text_rect)
              # Draw "Sound Toggle" button
            button_y = WINDOWHEIGHT // 2
            pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, 200, 50))
            pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, 200, 50), 2)
            
            sound_status = "Ligar Sons" if not SOUND_ENABLED else "Silenciar"
            button_text = button_font.render(sound_status, True, theme["text"])
            text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
            DISPLAYSURF.blit(button_text, text_rect)
            
            # Draw "Save Game" button
            button_y = WINDOWHEIGHT // 2 + 60
            pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, 200, 50))
            pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, 200, 50), 2)
            
            button_text = button_font.render("Salvar Jogo", True, theme["text"])
            text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
            DISPLAYSURF.blit(button_text, text_rect)
              # Draw "Screenshot" button
            button_y = WINDOWHEIGHT // 2 + 120
            pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, 200, 50))
            pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, 200, 50), 2)
            
            button_text = button_font.render("Capturar Tela", True, theme["text"])
            text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
            DISPLAYSURF.blit(button_text, text_rect)
            
            # Draw "Quit to Menu" button
            button_y = WINDOWHEIGHT // 2 + 180
            pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, 200, 50))
            pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, 200, 50), 2)
            
            button_text = button_font.render("Menu Principal", True, theme["text"])
            text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
            DISPLAYSURF.blit(button_text, text_rect)
            
        elif board.game_over:
            # Draw appropriate game over message
            message_font = pygame.font.Font(None, 72)
            if board.win:
                message_text = message_font.render("VITÓRIA!", True, GREEN)
                
                # Draw stats
                stats_font = pygame.font.Font(None, 24)
                stats_texts = [
                    f"Tempo: {board.get_elapsed_time()} segundos",
                    f"Dificuldade: {board.difficulty}",
                    f"Dimensões: {board.width}x{board.height}",
                    f"Minas: {board.mines}",
                    f"Dicas usadas: {board.hints_used}"
                ]
                
                for i, text in enumerate(stats_texts):
                    stats_text = stats_font.render(text, True, WHITE)
                    DISPLAYSURF.blit(stats_text, (WINDOWWIDTH // 2 - 100, WINDOWHEIGHT // 3 + 50 + i * 25))
    
            else:
                message_text = message_font.render("GAME OVER", True, RED)
                
                # Draw some details about the game
                stats_font = pygame.font.Font(None, 24)
                stats_texts = [
                    f"Todas as vidas perdidas!",
                    f"Tempo: {board.get_elapsed_time()} segundos",
                    f"Células reveladas: {board.revealed_cells} / {board.total_cells - board.mines}",
                    f"Bandeiras colocadas: {board.flags_placed} / {board.mines}"
                ]
                
                for i, text in enumerate(stats_texts):
                    stats_text = stats_font.render(text, True, WHITE)
                    DISPLAYSURF.blit(stats_text, (WINDOWWIDTH // 2 - 100, WINDOWHEIGHT // 3 + 30 + i * 25))
    
            # Display the message text that was set above
            text_rect = message_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4))
            DISPLAYSURF.blit(message_text, text_rect)
    
    # Draw buttons only if the game is over (not when paused)
    if board.game_over:
        # Draw "Try Again" button
        button_x = (WINDOWWIDTH - 200) // 2
        button_y = WINDOWHEIGHT // 2 + 30
        pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, 200, 50))
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, 200, 50), 2)
        
        button_text = button_font.render("Tentar Novamente", True, theme["text"])
        text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
        DISPLAYSURF.blit(button_text, text_rect)
        
        # Draw "Choose Difficulty" button
        button_y = WINDOWHEIGHT // 2 + 90
        pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, 200, 50))
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, 200, 50), 2)
        
        button_text = button_font.render("Escolher Dificuldade", True, theme["text"])
        text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
        DISPLAYSURF.blit(button_text, text_rect)
        
        # Draw "Main Menu" button
        button_y = WINDOWHEIGHT // 2 + 150
        pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, 200, 50))
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, 200, 50), 2)
        
        button_text = button_font.render("Menu Principal", True, theme["text"])
        text_rect = button_text.get_rect(center=(button_x + 100, button_y + 25))
        DISPLAYSURF.blit(button_text, text_rect)
    
    # Draw control buttons in the game
    if not board.paused and not board.game_over:
        # Menu button (top right)
        menu_button_x = WINDOWWIDTH - 90
        menu_button_y = 15
        pygame.draw.rect(DISPLAYSURF, theme["button"], (menu_button_x, menu_button_y, 70, 30))
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (menu_button_x, menu_button_y, 70, 30), 2)
        
        menu_font = pygame.font.Font(None, 24)
        menu_text = menu_font.render("Pausa", True, theme["text"])
        text_rect = menu_text.get_rect(center=(menu_button_x + 35, menu_button_y + 15))
        DISPLAYSURF.blit(menu_text, text_rect)
        
        # Theme toggle button
        theme_button_x = menu_button_x - 80
        theme_button_y = menu_button_y
        pygame.draw.rect(DISPLAYSURF, theme["button"], (theme_button_x, theme_button_y, 70, 30))
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (theme_button_x, theme_button_y, 70, 30), 2)
        
        theme_text = menu_font.render("Tema", True, theme["text"])
        text_rect = theme_text.get_rect(center=(theme_button_x + 35, theme_button_y + 15))
        DISPLAYSURF.blit(theme_text, text_rect)
          # Hint button
        hint_button_x = theme_button_x - 80
        hint_button_y = theme_button_y
        
        # Highlight button if hint mode is active
        if board.hint_mode_active and board.hints_available > 0:
            pygame.draw.rect(DISPLAYSURF, (100, 200, 100), (hint_button_x, hint_button_y, 70, 30))  # Green when active
        elif board.hints_available > 0:
            pygame.draw.rect(DISPLAYSURF, theme["button"], (hint_button_x, hint_button_y, 70, 30))
        else:
            pygame.draw.rect(DISPLAYSURF, DARKGRAY, (hint_button_x, hint_button_y, 70, 30))
        
        # Draw border with emphasis if hint mode is active
        border_width = 2 if not board.hint_mode_active else 3
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (hint_button_x, hint_button_y, 70, 30), border_width)
        
        hint_label = "Ativo (H)" if board.hint_mode_active else "Dica (H)"
        hint_text = menu_font.render(hint_label, True, theme["text"] if board.hints_available > 0 else DARKGRAY)
        text_rect = hint_text.get_rect(center=(hint_button_x + 35, hint_button_y + 15))
        DISPLAYSURF.blit(hint_text, text_rect)

def draw_start_screen():
    """Draw the start screen with difficulty options."""
    theme = THEMES[CURRENT_THEME]
    DISPLAYSURF.fill(theme["background"])
    
    # Title
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Campo Minado", True, theme["text"])
    title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 80))
    DISPLAYSURF.blit(title_text, title_rect)
    
    # Subtitle
    subtitle_font = pygame.font.Font(None, 36)
    subtitle_text = subtitle_font.render("Selecione uma opção:", True, DARKGRAY)
    subtitle_rect = subtitle_text.get_rect(center=(WINDOWWIDTH // 2, 140))
    DISPLAYSURF.blit(subtitle_text, subtitle_rect)
    
    # Buttons
    button_width, button_height = 200, 50
    button_margin = 15
    button_start_y = 200
    
    # Main menu options with icons
    menu_options = [
        ("Novo Jogo", "NEW_GAME"),
        ("Carregar Jogo", "LOAD_GAME"),
        ("Estatísticas", "STATISTICS"),
        ("Configurações", "SETTINGS"),
        ("Sair", "EXIT")
    ]
    
    buttons = []
    for i, (text, action) in enumerate(menu_options):
        button_x = (WINDOWWIDTH - button_width) // 2
        button_y = button_start_y + i * (button_height + button_margin)
        
        # Draw button
        pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, button_width, button_height))
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, button_width, button_height), 2)
        
        # Button text
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render(text, True, theme["text"])
        text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        DISPLAYSURF.blit(button_text, text_rect)
        
        buttons.append((button_x, button_y, button_width, button_height, action))
          # Version info
    version_font = pygame.font.Font(None, 20)
    version_text = version_font.render("v1.2.0", True, DARKGRAY)
    DISPLAYSURF.blit(version_text, (WINDOWWIDTH - 50, WINDOWHEIGHT - 20))
    
    # Developer credit
    credit_text = version_font.render("Melhorado em 2025", True, DARKGRAY)
    DISPLAYSURF.blit(credit_text, (WINDOWWIDTH - 140, WINDOWHEIGHT - 40))
    
    return buttons

def draw_difficulty_screen():
    """Draw the difficulty selection screen."""
    theme = THEMES[CURRENT_THEME]
    DISPLAYSURF.fill(theme["background"])
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Selecione a Dificuldade", True, theme["text"])
    title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 80))
    DISPLAYSURF.blit(title_text, title_rect)
    
    # Difficulty buttons
    button_width, button_height = 200, 50
    button_margin = 20
    button_start_y = 150
    
    difficulties = [
        ("Fácil", "EASY", "9x9, 10 minas"),
        ("Médio", "MEDIUM", "16x16, 40 minas"),
        ("Difícil", "HARD", "30x16, 99 minas"),
        ("Infinito", "INFINITE", "50x50, 400 minas"),
        ("Personalizado", "CUSTOM", "Defina o tamanho")
    ]
    
    buttons = []
    for i, (text, diff, desc) in enumerate(difficulties):
        button_x = (WINDOWWIDTH - button_width) // 2
        button_y = button_start_y + i * (button_height + button_margin)
        
        # Draw button
        pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, button_width, button_height))
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, button_width, button_height), 2)
        
        # Button text
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render(text, True, theme["text"])
        text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2 - 8))
        DISPLAYSURF.blit(button_text, text_rect)
        
        # Description text
        desc_font = pygame.font.Font(None, 20)
        desc_text = desc_font.render(desc, True, theme["text"])
        desc_rect = desc_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2 + 12))
        DISPLAYSURF.blit(desc_text, desc_rect)
        
        buttons.append((button_x, button_y, button_width, button_height, diff))
    
    # Back button
    back_width, back_height = 100, 40
    back_x = 20
    back_y = 20
    pygame.draw.rect(DISPLAYSURF, theme["button"], (back_x, back_y, back_width, back_height))
    pygame.draw.rect(DISPLAYSURF, theme["grid"], (back_x, back_y, back_width, back_height), 2)
    
    back_font = pygame.font.Font(None, 30)
    back_text = back_font.render("Voltar", True, theme["text"])
    back_rect = back_text.get_rect(center=(back_x + back_width // 2, back_y + back_height // 2))
    DISPLAYSURF.blit(back_text, back_rect)
    
    buttons.append((back_x, back_y, back_width, back_height, "BACK"))
    
    return buttons

def draw_settings_screen():
    """Draw the settings screen."""
    theme = THEMES[CURRENT_THEME]
    DISPLAYSURF.fill(theme["background"])
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Configurações", True, theme["text"])
    title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 80))
    DISPLAYSURF.blit(title_text, title_rect)
      # Settings options
    button_width, button_height = 250, 50
    button_margin = 20
    button_start_y = 150
    settings = [
        ("Tema: " + CURRENT_THEME, "TOGGLE_THEME"),
        ("Sons: " + ("Ligado" if SOUND_ENABLED else "Desligado"), "TOGGLE_SOUND"),
        ("Auto-Redimensionar: " + ("Ligado" if AUTO_RESIZE else "Desligado"), "TOGGLE_RESIZE"),
        ("Dicas: " + ("Ligado" if show_tips else "Desligado"), "TOGGLE_TIPS"),
        ("Redefinir Estatísticas", "RESET_STATS")
    ]
    
    buttons = []
    for i, (text, action) in enumerate(settings):
        button_x = (WINDOWWIDTH - button_width) // 2
        button_y = button_start_y + i * (button_height + button_margin)
        
        # Draw button
        pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, button_width, button_height))
        pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, button_width, button_height), 2)
        
        # Button text
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render(text, True, theme["text"])
        text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        DISPLAYSURF.blit(button_text, text_rect)
        
        buttons.append((button_x, button_y, button_width, button_height, action))
    
    # Back button
    back_width, back_height = 100, 40
    back_x = 20
    back_y = 20
    pygame.draw.rect(DISPLAYSURF, theme["button"], (back_x, back_y, back_width, back_height))
    pygame.draw.rect(DISPLAYSURF, theme["grid"], (back_x, back_y, back_width, back_height), 2)
    
    back_font = pygame.font.Font(None, 30)
    back_text = back_font.render("Voltar", True, theme["text"])
    back_rect = back_text.get_rect(center=(back_x + back_width // 2, back_y + back_height // 2))
    DISPLAYSURF.blit(back_text, back_rect)
    
    buttons.append((back_x, back_y, back_width, back_height, "BACK"))
    
    return buttons

def draw_statistics_screen():
    """Draw the statistics screen."""
    theme = THEMES[CURRENT_THEME]
    DISPLAYSURF.fill(theme["background"])
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Estatísticas", True, theme["text"])
    title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 80))
    DISPLAYSURF.blit(title_text, title_rect)
    
    # Statistics
    stats_font = pygame.font.Font(None, 32)
    stats_y = 150
    stats_spacing = 40
    
    stats_list = [
        f"Partidas jogadas: {STATISTICS['games_played']}",
        f"Partidas vencidas: {STATISTICS['games_won']}",
        f"Taxa de vitórias: {int(STATISTICS['games_won'] / max(1, STATISTICS['games_played']) * 100)}%",
        f"Melhor tempo (Fácil): {STATISTICS['best_times']['EASY']}s",
        f"Melhor tempo (Médio): {STATISTICS['best_times']['MEDIUM']}s",
        f"Melhor tempo (Difícil): {STATISTICS['best_times']['HARD']}s",
        f"Melhor tempo (Infinito): {STATISTICS['best_times']['INFINITE']}s",
        f"Total de células reveladas: {STATISTICS['total_cells_revealed']}",
        f"Total de bandeiras colocadas: {STATISTICS['total_flags_placed']}",
        f"Total de minas explodidas: {STATISTICS['total_mines_exploded']}"
    ]
    
    for i, stat in enumerate(stats_list):
        stat_text = stats_font.render(stat, True, theme["text"])
        stat_rect = stat_text.get_rect(midleft=(WINDOWWIDTH // 4, stats_y + i * stats_spacing))
        DISPLAYSURF.blit(stat_text, stat_rect)
    
    # Back button
    button_width, button_height = 200, 50
    button_x = (WINDOWWIDTH - button_width) // 2
    button_y = WINDOWHEIGHT - 100
    pygame.draw.rect(DISPLAYSURF, theme["button"], (button_x, button_y, button_width, button_height))
    pygame.draw.rect(DISPLAYSURF, theme["grid"], (button_x, button_y, button_width, button_height), 2)
    
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Voltar ao Menu", True, theme["text"])
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    DISPLAYSURF.blit(button_text, text_rect)
    
    return [(button_x, button_y, button_width, button_height, "BACK")]

def draw_load_game_screen():
    """Draw the load game screen with saved games."""
    theme = THEMES[CURRENT_THEME]
    DISPLAYSURF.fill(theme["background"])
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Carregar Jogo", True, theme["text"])
    title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 80))
    DISPLAYSURF.blit(title_text, title_rect)
    
    # Get saved games
    saved_games = Board.list_saved_games()
    
    # Fix: Define button_width and button_height as separate variables
    button_width = WINDOWWIDTH - 100
    button_height = 80  # Define an appropriate height
    button_margin = 10
    button_start_y = 150
    
    buttons = []
    
    # No saved games
    if not saved_games:
        no_games_font = pygame.font.Font(None, 36)
        no_games_text = no_games_font.render("Nenhum jogo salvo encontrado", True, theme["text"])
        no_games_rect = no_games_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
        DISPLAYSURF.blit(no_games_text, no_games_rect)
    else:
        # List saved games (show only up to 5)
        list_font = pygame.font.Font(None, 24)
        display_count = min(5, len(saved_games))
        
        for i in range(display_count):
            game = saved_games[i]
            button_y = button_start_y + i * (button_height + button_margin)
            
            # Draw button background
            pygame.draw.rect(DISPLAYSURF, theme["button"], (50, button_y, button_width, button_height))
            pygame.draw.rect(DISPLAYSURF, theme["grid"], (50, button_y, button_width, button_height), 2)
            
            # Format save date nicely
            try:
                save_date = datetime.datetime.fromisoformat(game["save_date"]).strftime("%d/%m/%Y %H:%M")
            except:
                save_date = "Data desconhecida"
                
            # Format elapsed time
            elapsed_minutes = int(game["elapsed_time"]) // 60
            elapsed_seconds = int(game["elapsed_time"]) % 60
            time_str = f"{elapsed_minutes}:{elapsed_seconds:02d}"
            
            # Display game info
            info_texts = [
                f"Dificuldade: {game['difficulty']} - Tamanho: {game['dimensions']} - Minas: {game['mines']}",
                f"Salvo em: {save_date} - Tempo jogado: {time_str}",
                f"Progresso: {game['completion']}"
            ]
            
            for j, text in enumerate(info_texts):
                info_text = list_font.render(text, True, theme["text"])
                DISPLAYSURF.blit(info_text, (70, button_y + 10 + j * 25))
            
            buttons.append((50, button_y, button_width, button_height, f"LOAD:{game['filename']}"))
    
    # Back button
    back_width, back_height = 100, 40
    back_x = 20
    back_y = 20
    pygame.draw.rect(DISPLAYSURF, theme["button"], (back_x, back_y, back_width, back_height))
    pygame.draw.rect(DISPLAYSURF, theme["grid"], (back_x, back_y, back_width, back_height), 2)
    
    back_font = pygame.font.Font(None, 30)
    back_text = back_font.render("Voltar", True, theme["text"])
    back_rect = back_text.get_rect(center=(back_x + back_width // 2, back_y + back_height // 2))
    DISPLAYSURF.blit(back_text, back_rect)
    
    buttons.append((back_x, back_y, back_width, back_height, "BACK"))
    
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

def save_statistics():
    """Save game statistics to a file."""
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(STATISTICS, f)
    except Exception as e:
        print(f"Error saving statistics: {e}")

def toggle_theme():
    """Toggle between light and dark themes with smooth transition."""
    global CURRENT_THEME
    old_theme = CURRENT_THEME
    new_theme = "DARK" if CURRENT_THEME == "LIGHT" else "LIGHT"
    CURRENT_THEME = new_theme
    
    # Create a smooth transition effect
    if pygame.display.get_init():  # Check if pygame display is initialized
        old_colors = THEMES[old_theme]
        new_colors = THEMES[new_theme]
        
        # Store current display
        current_surface = DISPLAYSURF.copy()
        
        # Create 10 transition frames
        for i in range(1, 11):
            # Clear the screen with transitional background color
            transition_factor = i / 10
            
            # Only use the main function if we're in the game
            try:
                DISPLAYSURF.fill(new_colors["background"])
                # Draw a fading overlay
                overlay = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
                alpha = 255 - int(255 * transition_factor)
                overlay.fill((0, 0, 0, alpha))
                DISPLAYSURF.blit(current_surface, (0, 0))
                DISPLAYSURF.blit(overlay, (0, 0))
                pygame.display.update()
                pygame.time.delay(20)  # Short delay for transition
            except:
                pass  # If there's any error, just skip the animation

def toggle_sound():
    """Toggle sound on/off."""
    global SOUND_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED

def toggle_resize():
    """Toggle auto-resize mode."""
    global AUTO_RESIZE
    AUTO_RESIZE = not AUTO_RESIZE
    
def toggle_tips():
    """Toggle game tips on/off."""
    global show_tips
    show_tips = not show_tips
    
    # Apply resize if enabled
    if AUTO_RESIZE and 'game_board' in globals() and globals()['game_board']:
        apply_auto_resize()

def play_sound(sound_name):
    """Play a sound effect if sound is enabled."""
    if SOUND_ENABLED and sound_name in SOUNDS:
        SOUNDS[sound_name].play()


def update_statistics(board, won=False):
    """Update game statistics based on board state."""
    STATISTICS["games_played"] += 1
    
    if won:
        STATISTICS["games_won"] += 1
        # Update best time if better
        elapsed_time = board.get_elapsed_time()
        if elapsed_time < STATISTICS["best_times"][board.difficulty]:
            STATISTICS["best_times"][board.difficulty] = elapsed_time
    
    STATISTICS["total_cells_revealed"] += board.revealed_cells
    STATISTICS["total_flags_placed"] += board.flags_placed
    
    if not won and board.game_over:
        STATISTICS["total_mines_exploded"] += 1
        
    save_statistics()

def main():
    """Main game function"""
    global BOARDWIDTH, BOARDHEIGHT, MINES, WINDOWWIDTH, WINDOWHEIGHT, DISPLAYSURF
    global BLOCKSIZE, ZOOM_FACTOR, SCROLL_OFFSET_X, SCROLL_OFFSET_Y
    global CURRENT_THEME, SOUND_ENABLED
    
    try:
        # State variables
        current_screen = "START"  # START, DIFFICULTY, GAME, CUSTOM, SETTINGS, STATISTICS, LOAD_GAME
        custom_values = {"width": "16", "height": "16", "mines": "40"}
        active_field = None
        game_board = None
        hint_active = False
        last_tip_time = 0  # Track when the last tip was shown
        game_start_time = 0  # Track when the game was started
          # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    if game_board and game_board.started and not game_board.game_over:
                        # Auto-save on exit
                        game_board.save_game()
                    running = False
                    pygame.quit()
                    sys.exit()                # Handle window resize events
                if event.type == VIDEORESIZE:
                    # Update window size while maintaining minimum dimensions
                    WINDOWWIDTH = max(event.w, 480)
                    WINDOWHEIGHT = max(event.h, 60 + MIN_BLOCKSIZE)
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
                    
                    # Apply auto-resize if enabled
                    if AUTO_RESIZE and game_board and current_screen == "GAME":
                        apply_auto_resize()
                    # Otherwise just adjust the view to center the board if needed
                    elif game_board and current_screen == "GAME":
                        # Auto-adjust scroll to ensure board is centered if window is larger than board
                        visible_board_width = game_board.width * BLOCKSIZE
                        visible_board_height = game_board.height * BLOCKSIZE
                        
                        if WINDOWWIDTH > visible_board_width:
                            # Center board horizontally if window is wider
                            SCROLL_OFFSET_X = (WINDOWWIDTH - visible_board_width) // 2
                        
                        if WINDOWHEIGHT - 60 > visible_board_height:
                            # Center board vertically if window is taller
                            SCROLL_OFFSET_Y = (WINDOWHEIGHT - 60 - visible_board_height) // 2
                  # Handle keyboard shortcuts
                if event.type == KEYDOWN:
                    ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL
                    
                    # Take screenshot with F12 or Ctrl+S
                    if event.key == K_F12 or (ctrl_pressed and event.key == K_PRINT):
                        saved = save_screenshot()
                        if saved and SOUND_ENABLED:
                            play_sound("click")
                    
                    # Zoom in with Ctrl+ or +
                    elif (ctrl_pressed and (event.key == K_PLUS or event.key == K_EQUALS)) or event.key == K_PLUS or event.key == K_EQUALS:
                        if BLOCKSIZE < MAX_BLOCKSIZE:
                            BLOCKSIZE += ZOOM_STEP
                            ZOOM_FACTOR = BLOCKSIZE / DEFAULT_BLOCKSIZE
                            update_images_for_zoom()
                            
                    # Zoom out with Ctrl- or -
                    elif (ctrl_pressed and event.key == K_MINUS) or event.key == K_MINUS:
                        if BLOCKSIZE > MIN_BLOCKSIZE:
                            BLOCKSIZE -= ZOOM_STEP
                            ZOOM_FACTOR = BLOCKSIZE / DEFAULT_BLOCKSIZE
                            update_images_for_zoom()
                    
                    # Toggle theme with T
                    elif event.key == K_t:
                        toggle_theme()
                          # Toggle sound with S
                    elif event.key == K_s and ctrl_pressed:
                        toggle_sound()
                    
                    # Toggle tips with T+Ctrl
                    elif event.key == K_t and ctrl_pressed:
                        toggle_tips()
                        if show_tips:
                            show_tip("Dicas ativadas! Você receberá sugestões durante o jogo.")
                            
                    # Center the view with C
                    elif event.key == K_c:
                        SCROLL_OFFSET_X = 0
                        SCROLL_OFFSET_Y = 0
                        
                    # Auto-resize with A
                    elif event.key == K_a and ctrl_pressed and current_screen == "GAME" and game_board:
                        toggle_resize()
                        if AUTO_RESIZE:
                            apply_auto_resize()
                            if show_tips:
                                show_tip("Auto-redimensionamento ativado. O jogo se ajustará automaticamente ao tamanho da janela.")
                    
                    # Pause game with P
                    elif event.key == K_p and current_screen == "GAME" and game_board and game_board.started and not game_board.game_over:
                        if not game_board.paused:
                            game_board.pause_game()
                        else:
                            game_board.unpause_game()
                            
                    # Save game with Ctrl+S
                    elif event.key == K_s and ctrl_pressed and current_screen == "GAME" and game_board and game_board.started and not game_board.game_over:
                        game_board.save_game()
                          # Get hint with H - modified to toggle hint mode
                    elif event.key == K_h and current_screen == "GAME" and game_board and game_board.started and not game_board.game_over and not game_board.paused:
                        game_board.hint_mode_active = not game_board.hint_mode_active
                        game_board.clear_hints()
                        hint_active = game_board.hint_mode_active
                        play_sound("click")
                    
                    # Show help with F1
                    elif event.key == K_F1:
                        if current_screen == "GAME" and game_board:
                            # Pause game temporarily to show help
                            was_paused = game_board.paused
                            if not was_paused:
                                game_board.pause_game()
                            
                            # Draw help overlay
                            help_overlay = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
                            help_overlay.fill((0, 0, 0, 200))  # Darker overlay for help
                            DISPLAYSURF.blit(help_overlay, (0, 0))
                            
                            # Draw help title
                            help_font = pygame.font.Font(None, 36)
                            title_text = help_font.render("Atalhos de Teclado", True, WHITE)
                            title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 80))
                            DISPLAYSURF.blit(title_text, title_rect)
                            
                            # Draw shortcuts
                            shortcut_font = pygame.font.Font(None, 24)
                            shortcuts = [
                                "F1 - Mostrar esta ajuda",
                                "Esc - Pausar/Menu",
                                "H - Ativar/desativar modo de dica (permite ver conteúdo das células)",
                                "Ctrl+S - Salvar jogo",
                                "Ctrl+T - Ativar/desativar dicas automáticas",
                                "Ctrl+A - Ativar/desativar auto-redimensionamento",
                                "F12 / Ctrl+Print - Capturar tela",
                                "+ / - - Aumentar/diminuir zoom",
                                "Botão direito / Shift+Clique - Colocar bandeira"
                            ]
                            
                            for i, shortcut in enumerate(shortcuts):
                                shortcut_text = shortcut_font.render(shortcut, True, WHITE)
                                DISPLAYSURF.blit(shortcut_text, (WINDOWWIDTH // 4, 130 + i * 30))
                              # Add hint system explanation
                            hint_title = help_font.render("Sistema de Dicas:", True, GREEN)
                            DISPLAYSURF.blit(hint_title, (WINDOWWIDTH // 4, 400))
                            
                            hint_info = [
                                "• Pressione H ou clique no botão Dica para ativar o modo de dica",
                                "• No modo de dica, você pode revelar o conteúdo de células sem risco",
                                "• Cada célula revelada custa 1 dica",
                                "• A quantidade de dicas disponíveis depende da dificuldade"
                            ]
                            
                            for i, info in enumerate(hint_info):
                                info_text = shortcut_font.render(info, True, WHITE)
                                DISPLAYSURF.blit(info_text, (WINDOWWIDTH // 4, 430 + i * 25))
                            
                            # Draw continue message
                            continue_text = help_font.render("Pressione qualquer tecla para voltar ao jogo", True, WHITE)
                            continue_rect = continue_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT - 40))
                            DISPLAYSURF.blit(continue_text, continue_rect)
                            
                            pygame.display.update()
                            
                            # Wait for key press to continue, but handle this properly
                            waiting_for_key = True
                            while waiting_for_key:
                                for evt in pygame.event.get():
                                    if evt.type == QUIT:
                                        waiting_for_key = False
                                        running = False
                                        pygame.quit()
                                        sys.exit()
                                    elif evt.type == KEYDOWN or evt.type == MOUSEBUTTONDOWN:
                                        waiting_for_key = False
                                pygame.time.delay(10)
                            
                            # Restore game if it wasn't paused before
                            if not was_paused and game_board:
                                game_board.unpause_game()
                    
                    # Handle escape key
                    elif event.key == K_ESCAPE:
                        if current_screen == "GAME" and game_board and not game_board.game_over:
                            # Pause the game
                            if not game_board.paused:
                                game_board.pause_game()
                        elif current_screen in ["DIFFICULTY", "SETTINGS", "STATISTICS", "LOAD_GAME", "CUSTOM"]:
                            # Go back to main menu
                            current_screen = "START"
                        elif current_screen == "START":
                            # Exit game
                            running = False
                            pygame.quit()
                            sys.exit()
                
                # Handle touchpad/mouse wheel for navigation
                if event.type == pygame.MOUSEWHEEL and current_screen == "GAME":
                    shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                    
                    if shift_pressed:
                        # Zoom with Shift+wheel
                        if event.y > 0 and BLOCKSIZE < MAX_BLOCKSIZE:
                            BLOCKSIZE += ZOOM_STEP
                            ZOOM_FACTOR = BLOCKSIZE / DEFAULT_BLOCKSIZE
                            update_images_for_zoom()
                        elif event.y < 0 and BLOCKSIZE > MIN_BLOCKSIZE:
                            BLOCKSIZE -= ZOOM_STEP
                            ZOOM_FACTOR = BLOCKSIZE / DEFAULT_BLOCKSIZE
                            update_images_for_zoom()
                    else:
                        # Normal scrolling
                        if event.y != 0:
                            SCROLL_OFFSET_Y += event.y * BLOCKSIZE * 2  # Scroll faster
                        if hasattr(event, 'x') and event.x != 0:
                            SCROLL_OFFSET_X += event.x * BLOCKSIZE * 2  # Scroll faster
                
                # Mouse button event handling
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    # Start screen
                    if current_screen == "START":
                        buttons = draw_start_screen()
                        action = check_button_click(event.pos, buttons)
                        
                        if action:
                            if action == "NEW_GAME":
                                current_screen = "DIFFICULTY"
                            elif action == "LOAD_GAME":
                                current_screen = "LOAD_GAME"
                            elif action == "STATISTICS":
                                current_screen = "STATISTICS"
                            elif action == "SETTINGS":
                                current_screen = "SETTINGS"
                            elif action == "EXIT":
                                running = False
                                pygame.quit()
                                sys.exit()
                    
                    # Difficulty screen
                    elif current_screen == "DIFFICULTY":
                        buttons = draw_difficulty_screen()
                        action = check_button_click(event.pos, buttons)
                        
                        if action:
                            if action == "BACK":
                                current_screen = "START"
                            elif action == "CUSTOM":
                                current_screen = "CUSTOM"
                            elif action in DIFFICULTY:
                                # Set difficulty from presets
                                BOARDWIDTH = DIFFICULTY[action]["width"]
                                BOARDHEIGHT = DIFFICULTY[action]["height"]
                                MINES = DIFFICULTY[action]["mines"]
                                
                                # Reset scrolling and zoom for new game
                                SCROLL_OFFSET_X = 0
                                SCROLL_OFFSET_Y = 0
                                BLOCKSIZE = DEFAULT_BLOCKSIZE
                                ZOOM_FACTOR = 1.0
                                update_images_for_zoom()
                                
                                # Update window size
                                WINDOWWIDTH = max(BOARDWIDTH * BLOCKSIZE, 480)
                                WINDOWHEIGHT = BOARDHEIGHT * BLOCKSIZE + 60
                                DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
                                
                                # Start game
                                game_board = Board(BOARDWIDTH, BOARDHEIGHT, MINES, action)
                                current_screen = "GAME"
                                play_sound("click")                    # Settings screen
                    elif current_screen == "SETTINGS":
                        buttons = draw_settings_screen()
                        action = check_button_click(event.pos, buttons)
                        if action:
                            if action == "BACK":
                                current_screen = "START"
                            elif action == "TOGGLE_THEME":
                                toggle_theme()
                            elif action == "TOGGLE_SOUND":
                                toggle_sound()
                            elif action == "TOGGLE_RESIZE":
                                toggle_resize()
                                if AUTO_RESIZE and game_board:
                                    apply_auto_resize()
                            elif action == "TOGGLE_TIPS":
                                toggle_tips()
                            elif action == "RESET_STATS":
                                # Reset statistics
                                STATISTICS["games_played"] = 0
                                STATISTICS["games_won"] = 0
                                STATISTICS["best_times"] = {"EASY": 999, "MEDIUM": 999, "HARD": 999, "INFINITE": 999}
                                STATISTICS["total_cells_revealed"] = 0
                                STATISTICS["total_flags_placed"] = 0
                                STATISTICS["total_mines_exploded"] = 0
                                save_statistics()
                                play_sound("click")

                    # Statistics screen
                    elif current_screen == "STATISTICS":
                        buttons = draw_statistics_screen()
                        action = check_button_click(event.pos, buttons)
                        
                        if action == "BACK":
                            current_screen = "START"

                    # Load game screen
                    elif current_screen == "LOAD_GAME":
                        buttons = draw_load_game_screen()
                        action = check_button_click(event.pos, buttons)
                        
                        if action:
                            if action == "BACK":
                                current_screen = "START"
                            elif action.startswith("LOAD:"):
                                # Extract filename
                                filename = action.split(":", 1)[1]
                                
                                # Create new board with default values
                                game_board = Board(16, 16, 40)
                                
                                # Load saved game
                                if game_board.load_game(filename):
                                    # Update global variables
                                    BOARDWIDTH = game_board.width
                                    BOARDHEIGHT = game_board.height
                                    MINES = game_board.mines
                                    
                                    # Update window size
                                    WINDOWWIDTH = max(BOARDWIDTH * BLOCKSIZE, 480)
                                    WINDOWHEIGHT = BOARDHEIGHT * BLOCKSIZE + 60
                                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
                                    
                                    # Switch to game
                                    current_screen = "GAME"
                                    play_sound("click")

                    # Custom screen logic
                    elif current_screen == "CUSTOM":
                        if event.type == MOUSEBUTTONUP and event.button == 1:
                            # Removed this line since we're now calling it correctly later
                              # Get buttons from draw_custom_screen
                            input_fields, _, _ = draw_custom_screen()
                            
                            # Check if back button was clicked
                            if check_rect_click(event.pos, back_button):
                                current_screen = "DIFFICULTY"
                                active_field = None
                                play_sound("click")
                            
                            # Check if start button was clicked
                            elif check_rect_click(event.pos, start_button):
                                # Validate and convert custom values
                                try:
                                    width = max(9, min(100, int(custom_values["width"])))
                                    height = max(9, min(100, int(custom_values["height"])))
                                    max_mines = (width * height) - 9  # Leave space for first click
                                    mines = max(1, min(max_mines, int(custom_values["mines"])))
                                    
                                    # Set board dimensions
                                    BOARDWIDTH = width
                                    BOARDHEIGHT = height
                                    MINES = mines
                                    
                                    # Reset scrolling and zoom
                                    SCROLL_OFFSET_X = 0
                                    SCROLL_OFFSET_Y = 0
                                    BLOCKSIZE = DEFAULT_BLOCKSIZE
                                    ZOOM_FACTOR = 1.0
                                    update_images_for_zoom()
                                    
                                    # Update window size
                                    WINDOWWIDTH = max(BOARDWIDTH * BLOCKSIZE, 480)
                                    WINDOWHEIGHT = BOARDHEIGHT * BLOCKSIZE + 60
                                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
                                    
                                    # Start game
                                    game_board = Board(BOARDWIDTH, BOARDHEIGHT, MINES, "CUSTOM")
                                    current_screen = "GAME"
                                    play_sound("click")
                                    
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
                                max_length = 3  # Allow up to 3 digits for all fields
                                if len(custom_values[active_field]) < max_length:
                                    custom_values[active_field] += event.unicode
                                    # Game screen logic
                    elif current_screen == "GAME" and game_board:
                        if event.type == MOUSEBUTTONUP:
                            mouse_x, mouse_y = event.pos
                              # If game is paused, handle pause menu buttons
                            if game_board.paused:
                                button_x = (WINDOWWIDTH - 200) // 2
                                
                                # Resume button
                                resume_button = (button_x, WINDOWHEIGHT // 2 - 60, 200, 50)
                                if check_rect_click(event.pos, resume_button):
                                    game_board.unpause_game()
                                    play_sound("click")
                                
                                # Toggle sound button
                                sound_button = (button_x, WINDOWHEIGHT // 2, 200, 50)
                                if check_rect_click(event.pos, sound_button):
                                    toggle_sound()
                                    if SOUND_ENABLED:
                                        play_sound("click")
                                      # Save game button
                                save_button = (button_x, WINDOWHEIGHT // 2 + 60, 200, 50)
                                if check_rect_click(event.pos, save_button):
                                    saved_file = game_board.save_game()
                                    if saved_file:
                                        play_sound("click")
                                
                                # Screenshot button
                                screenshot_button = (button_x, WINDOWHEIGHT // 2 + 120, 200, 50)
                                if check_rect_click(event.pos, screenshot_button):
                                    # Unpause temporarily to take screenshot without overlay
                                    game_board.paused = False
                                    draw_board(game_board)
                                    pygame.display.update()
                                    save_screenshot()
                                    game_board.paused = True
                                    play_sound("click")
                                
                                # Quit button
                                quit_button = (button_x, WINDOWHEIGHT // 2 + 180, 200, 50)
                                if check_rect_click(event.pos, quit_button):
                                    # Save game before quitting
                                    game_board.save_game()
                                    current_screen = "START"
                                    play_sound("click")
                            
                            # When game is over, handle game over buttons
                            elif game_board.game_over:
                                button_x = (WINDOWWIDTH - 200) // 2
                                
                                # Restart button
                                restart_button = (button_x, WINDOWHEIGHT // 2 + 30, 200, 50)
                                if check_rect_click(event.pos, restart_button):
                                    # Start a new game with same settings
                                    game_board = Board(BOARDWIDTH, BOARDHEIGHT, MINES, game_board.difficulty)
                                    play_sound("click")
                                    hint_active = False
                                    continue
                                
                                # Choose difficulty button (new)
                                difficulty_button = (button_x, WINDOWHEIGHT // 2 + 90, 200, 50)
                                if check_rect_click(event.pos, difficulty_button):
                                    current_screen = "DIFFICULTY"
                                    play_sound("click")
                                    continue
                                
                                # Menu button
                                menu_button = (button_x, WINDOWHEIGHT // 2 + 150, 200, 50)
                                if check_rect_click(event.pos, menu_button):
                                    current_screen = "START"
                                    play_sound("click")
                                    continue
                            
                            # Normal gameplay
                            else:
                                # Check for UI buttons first
                                menu_button_x = WINDOWWIDTH - 90
                                menu_button_y = 15
                                menu_button = (menu_button_x, menu_button_y, 70, 30)
                                
                                # Pause button
                                if check_rect_click(event.pos, menu_button):
                                    game_board.pause_game()
                                    play_sound("click")
                                    continue
                                    
                                # Theme toggle button
                                theme_button_x = menu_button_x - 80
                                theme_button_y = menu_button_y
                                theme_button = (theme_button_x, theme_button_y, 70, 30)
                                
                                if check_rect_click(event.pos, theme_button):
                                    toggle_theme()
                                    play_sound("click")
                                    continue
                                      # Hint button
                                hint_button_x = theme_button_x - 80
                                hint_button_y = theme_button_y
                                hint_button = (hint_button_x, hint_button_y, 70, 30)
                                if check_rect_click(event.pos, hint_button):
                                    # Toggle hint mode
                                    game_board.hint_mode_active = not game_board.hint_mode_active
                                    # Clear any existing hints when toggling
                                    game_board.clear_hints()
                                    hint_active = game_board.hint_mode_active
                                    play_sound("click")
                                    continue
                                
                                # Process cell clicks
                                cell_pos = get_cell_at_pixel(event.pos[0], event.pos[1])
                                if cell_pos:
                                    cell_x, cell_y = cell_pos
                                    
                                    # When hint mode is active, just reveal the cell content without consequences
                                    if hint_active:
                                        game_board.peek_cell(cell_x, cell_y)
                                        play_sound("click")
                                    # Normal left click to reveal cell
                                    elif event.button == 1:
                                        # Check for Shift+Click
                                        shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                                        if shift_pressed:  # Shift+Click acts as right-click
                                            game_board.toggle_flag(cell_x, cell_y)
                                            play_sound("flag")
                                        else:  # Normal left click
                                            # If the cell is a revealed number, try auto-reveal around it
                                            cell = game_board.board[cell_y][cell_x]
                                            if cell['state'] == REVEALED and cell['value'] > 0:
                                                game_board.auto_reveal_around(cell_x, cell_y)
                                            else:
                                                game_board.reveal_cell(cell_x, cell_y)
                                                if game_board.game_over:
                                                    if game_board.win:
                                                        play_sound("win")
                                                    else:
                                                        play_sound("explosion")
                                                else:
                                                    play_sound("click")
                                    # Right click to place flag
                                    elif event.button == 3:  # Right click
                                        game_board.toggle_flag(cell_x, cell_y)
                                        play_sound("flag")
            
            # Draw the appropriate screen
            if current_screen == "START":
                buttons = draw_start_screen()
            elif current_screen == "DIFFICULTY":
                buttons = draw_difficulty_screen()
            elif current_screen == "CUSTOM":
                input_fields, start_button, back_button = draw_custom_screen()
                draw_input_field_values(input_fields, custom_values)
            elif current_screen == "SETTINGS":
                buttons = draw_settings_screen()
            elif current_screen == "STATISTICS":
                buttons = draw_statistics_screen()
            elif current_screen == "LOAD_GAME":
                buttons = draw_load_game_screen()
            elif current_screen == "GAME" and game_board:
                draw_board(game_board)
                # Check if we need to clear hints after some time
                if hint_active and game_board:                    # Show hint mode indicator on screen
                    hint_font = pygame.font.Font(None, 24)
                    cost_text = f" (Custo: 1 dica por célula, disponíveis: {game_board.hints_available})"
                    hint_text = hint_font.render(f"Modo Dica: Clique em uma célula para revelar seu conteúdo sem consequências{cost_text}", True, (0, 150, 0))
                    hint_bg = pygame.Surface((hint_text.get_width() + 10, hint_text.get_height() + 6), pygame.SRCALPHA)
                    hint_bg.fill((255, 255, 255, 180))  # Semi-transparent white background
                    DISPLAYSURF.blit(hint_bg, (10, WINDOWHEIGHT - 40))
                    DISPLAYSURF.blit(hint_text, (15, WINDOWHEIGHT - 37))
                      # Use a custom cursor for hint mode
                    if not pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_CROSSHAIR:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                else:
                    # Reset cursor when not in hint mode
                    if pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_CROSSHAIR:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            # Update the display
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

def show_tip_of_the_day():
    """Show a random tip of the day at startup."""
    # List of tips
    tips = [
        "Use o botão direito do mouse para marcar minas com bandeiras.",
        "Quando um número 1 estiver próximo de uma bandeira, as células ao redor são seguras.",
        "Pressione F1 para ver todos os atalhos de teclado disponíveis.",
        "Use o modo auto-redimensionar (Ctrl+A) para adaptar o jogo à janela.",
        "Em caso de dúvida, use uma dica pressionando H.",
        "Quando você marcar todas as minas ao redor de um número, clique nele para revelar o restante.",
        "Números indicam quantas minas estão adjacentes a essa célula.",
        "Pressione F12 para capturar uma tela do seu jogo.",
        "Use Shift+Clique como alternativa ao botão direito para marcar bandeiras.",
        "Se a janela ficar grande demais, use o zoom - para reduzir o tamanho das células."
    ]
    
    # Select random tip
    import random
    tip = random.choice(tips)
    
    # Create overlay
    overlay = pygame.Surface((480, 480), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    DISPLAYSURF.blit(overlay, (0, 0))
    
    # Draw tip box
    pygame.draw.rect(DISPLAYSURF, DARKBLUE, (40, 180, 400, 120), 0)
    pygame.draw.rect(DISPLAYSURF, WHITE, (40, 180, 400, 120), 3)
    
    # Draw title
    tip_font = pygame.font.Font(None, 28)
    title_text = tip_font.render("Dica do Dia", True, YELLOW)
    title_rect = title_text.get_rect(center=(240, 205))
    DISPLAYSURF.blit(title_text, title_rect)
    
    # Draw tip text (wrap if needed)
    tip_font = pygame.font.Font(None, 24)
    words = tip.split(' ')
    lines = []
    current_line = words[0]
    
    for word in words[1:]:
        test_line = current_line + " " + word
        test_surface = tip_font.render(test_line, True, WHITE)
        if test_surface.get_width() < 380:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    
    for i, line in enumerate(lines):
        line_text = tip_font.render(line, True, WHITE)
        DISPLAYSURF.blit(line_text, (60, 230 + i * 25))
    
    # Draw continue message
    continue_font = pygame.font.Font(None, 20)
    continue_text = continue_font.render("Pressione qualquer tecla para continuar", True, LIGHTGRAY)
    continue_rect = continue_text.get_rect(center=(240, 280))
    DISPLAYSURF.blit(continue_text, continue_rect)
    
    pygame.display.update()
    
    # Wait for key or mouse press
    waiting = True
    while waiting:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN or evt.type == MOUSEBUTTONUP or evt.type == QUIT:
                waiting = False
                break
        pygame.time.delay(10)

def show_splash_screen():
    """Show a splash screen on startup."""
    global DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT
    
    # Create a temporary display for the splash screen with a larger size
    WINDOWWIDTH, WINDOWHEIGHT = 800, 600  # Larger initial window size
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Campo Minado')
    
    # Fill background
    DISPLAYSURF.fill(WHITE)
    
    # Draw title
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    
    title_text = font_large.render("Campo Minado", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 120))
    DISPLAYSURF.blit(title_text, title_rect)
    
    # Draw version
    version_text = font_medium.render("Edição Melhorada", True, DARKGRAY)
    version_rect = version_text.get_rect(center=(WINDOWWIDTH // 2, 180))
    DISPLAYSURF.blit(version_text, version_rect)
    
    # Draw loading text
    loading_text = font_small.render("Carregando...", True, BLACK)
    loading_rect = loading_text.get_rect(center=(WINDOWWIDTH // 2, 360))
    DISPLAYSURF.blit(loading_text, loading_rect)
    
    # Draw a mini minesweeper board for decoration
    mini_blocksize = 30
    for y in range(5):
        for x in range(5):
            rect = (WINDOWWIDTH // 2 - 2.5 * mini_blocksize + x * mini_blocksize, 
                   240 + y * mini_blocksize,
                   mini_blocksize, mini_blocksize)
            
            # Alternate between revealed and hidden cells
            if (x + y) % 2 == 0:
                pygame.draw.rect(DISPLAYSURF, GRAY, rect)
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, rect, 1)
                
                # 3D effect
                pygame.draw.line(DISPLAYSURF, WHITE, (rect[0], rect[1]), (rect[0] + mini_blocksize - 1, rect[1]), 2)
                pygame.draw.line(DISPLAYSURF, WHITE, (rect[0], rect[1]), (rect[0], rect[1] + mini_blocksize - 1), 2)
            else:
                pygame.draw.rect(DISPLAYSURF, WHITE, rect)
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, rect, 1)
                
                # Draw some numbers/mines
                if x == 2 and y == 2:
                    # Draw mini bomb in the center
                    pygame.draw.circle(DISPLAYSURF, BLACK, (rect[0] + mini_blocksize // 2, rect[1] + mini_blocksize // 2), mini_blocksize // 3)
                elif (x, y) in [(1, 1), (3, 1), (1, 3), (3, 3)]:
                    # Draw 1's in corners
                    text = font_small.render("1", True, BLUE)
                    text_rect = text.get_rect(center=(rect[0] + mini_blocksize // 2, rect[1] + mini_blocksize // 2))
                    DISPLAYSURF.blit(text, text_rect)
    
    # Draw progress bar
    for i in range(101):
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, (80, 400, 320, 20), 2)
        pygame.draw.rect(DISPLAYSURF, BLUE, (80, 400, int(i * 3.2), 20))
        
        # Update display
        pygame.display.update()
        pygame.time.delay(10)  # Small delay for animation
        
        # Handle quit event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
    # Short delay to show completed loading
    pygame.time.delay(500)

def show_tip(text):
    """Show a gameplay tip to the user if tips are enabled."""
    if not show_tips:
        return
    
    # Create a semi-transparent overlay for the tip
    tip_overlay = pygame.Surface((WINDOWWIDTH, 80), pygame.SRCALPHA)
    tip_overlay.fill((0, 0, 128, 180))  # Semi-transparent blue
    DISPLAYSURF.blit(tip_overlay, (0, WINDOWHEIGHT - 80))
    
    # Draw the tip text
    tip_font = pygame.font.Font(None, 24)
    tip_text = tip_font.render(text, True, WHITE)
    tip_rect = tip_text.get_rect(center=(WINDOWWIDTH // 2, 40))
    
    # Display the tip at the bottom of the screen        
    DISPLAYSURF.blit(tip_text, (tip_rect.x, WINDOWHEIGHT - 50))
    
    # Update only the tip area
    pygame.display.update(pygame.Rect(0, WINDOWHEIGHT - 80, WINDOWWIDTH, 80))
    
    # Show the tip for a short time
    pygame.time.delay(3000)  # Show for 3 seconds

def save_screenshot():
    """Save a screenshot of the current game."""
    try:
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(base_dir, 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generate a unique filename based on timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_dir, filename)
        
        # Save the screenshot
        pygame.image.save(DISPLAYSURF, screenshot_path)
        
        # Flash effect to indicate screenshot was taken
        flash = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)    
        flash.fill((255, 255, 255, 100))  # Semi-transparent white
        
        # Show the flash
        original_surface = DISPLAYSURF.copy()
        DISPLAYSURF.blit(flash, (0, 0))    
        
        # Show messages
        msg_font = pygame.font.Font(None, 36)
        msg_text = msg_font.render("Captura de tela salva!", True, (0, 128, 0))
        msg_rect = msg_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4))
        
        # Add shadow for better visibility
        shadow_text = msg_font.render("Captura de tela salva!", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(WINDOWWIDTH // 2 + 2, WINDOWHEIGHT // 4 + 2))
        DISPLAYSURF.blit(shadow_text, shadow_rect)
        DISPLAYSURF.blit(msg_text, msg_rect)
        
        # Show path message
        path_font = pygame.font.Font(None, 24)
        path_text = path_font.render(f"Salvo em: {screenshots_dir}", True, (0, 0, 0))
        path_rect = path_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4 + 30))
        DISPLAYSURF.blit(path_text, path_rect)
        
        # Update display
        pygame.display.update()
        
        # Short delay to show message
        pygame.time.delay(800)  # Show message for 0.8 seconds
        
        # Restore original display
        DISPLAYSURF.blit(original_surface, (0, 0))
        
        return True
        
    except Exception as e:
        print(f"Error saving screenshot: {e}")
        return False

# Skip tip of the day to start faster
show_splash_screen()    # Show splash screen
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
WINDOWHEIGHT = 600
WINDOWWIDTH = 800    # Set default window size to something larger
if __name__ == "__main__":
    main()