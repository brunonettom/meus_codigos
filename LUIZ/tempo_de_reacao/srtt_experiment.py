import pygame
import sys
import random
import time
import csv
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (240, 240, 240)
STIMULUS_COLOR = (0, 0, 255)
STIMULUS_ACTIVE_COLOR = (255, 0, 0)
STIMULUS_SIZE = 50
STIMULUS_DISTANCE = 120  # Space between stimuli
SEQUENCE_LENGTH = 10  # Length of the structured sequence
FEEDBACK_DURATION = 500  # Feedback duration in milliseconds

# Default experiment settings (now modifiable)
DEFAULT_POSITIONS = 4  # Default number of stimulus positions
DEFAULT_BLOCKS = 8  # Default number of blocks
DEFAULT_TRIALS_PER_BLOCK = 60  # Default trials per block

# Maximum number of positions and keys
MAX_POSITIONS = 8
POSITION_KEYS = ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',']  # Keys for each position
KEY_MAPPING = {
    pygame.K_z: 0,
    pygame.K_x: 1,
    pygame.K_c: 2,
    pygame.K_v: 3,
    pygame.K_b: 4,
    pygame.K_n: 5,
    pygame.K_m: 6,
    pygame.K_COMMA: 7
}

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tarefa de Tempo de Reação em Série (SRTT)")

# Font setup
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 22)

# Create structured sequence (with second-order dependencies)
# This is a 10-item sequence with balanced transitions
DEFAULT_STRUCTURED_SEQUENCE = [0, 2, 1, 0, 3, 1, 2, 3, 0, 1]

class SRTTExperiment:
    def __init__(self):
        self.participant_id = None
        self.results = []
        self.current_block = 0
        self.current_trial = 0
        self.start_time = 0
        self.reaction_time = 0
        self.current_position = 0
        self.correct_responses = 0
        self.is_structured_block = True
        self.running = True
        self.state = "participant_info"  # Start with participant info screen
        self.blocks_data = []
        self.show_stimulus = False
        self.block_sequence = []
        
        # Experiment settings (can be changed in settings screen)
        self.positions = DEFAULT_POSITIONS
        self.blocks = DEFAULT_BLOCKS
        self.trials_per_block = DEFAULT_TRIALS_PER_BLOCK
        
    def generate_structured_sequence(self):
        """Generate a structured sequence for the current number of positions"""
        if self.positions <= 4:
            # For 4 positions or less, use the default sequence
            return DEFAULT_STRUCTURED_SEQUENCE
        else:
            # For more positions, create a new balanced sequence
            seq = []
            for i in range(SEQUENCE_LENGTH):
                # Avoid consecutive repetitions
                if i > 0:
                    options = list(range(self.positions))
                    if seq:
                        options.remove(seq[-1])  # Don't repeat last position
                    pos = random.choice(options)
                else:
                    pos = random.randint(0, self.positions - 1)
                seq.append(pos)
            return seq
            
    def get_experiment_settings(self):
        """Display settings screen for configuration"""
        pygame.display.set_caption("Configurações do Experimento")
        
        # Position slider (number of circles)
        position_slider = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 160, 200, 20)
        position_value = self.positions
        
        # Blocks slider (number of blocks/batches)
        blocks_slider = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 100, 200, 20)
        blocks_value = self.blocks
        
        # Trials slider (number of trials per block)
        trials_slider = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 40, 200, 20)
        trials_value = self.trials_per_block
        
        position_slider_active = False
        blocks_slider_active = False
        trials_slider_active = False
        done = False
        
        while not done and self.running:
            screen.fill(BACKGROUND_COLOR)
            
            # Draw title
            title = font.render("Configurações do Experimento", True, (0, 0, 0))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
            
            # Draw position slider
            slider_text = font.render(f"Número de posições: {position_value}", True, (0, 0, 0))
            screen.blit(slider_text, (SCREEN_WIDTH//2 - slider_text.get_width()//2, SCREEN_HEIGHT//2 - 180))
            
            pygame.draw.rect(screen, (200, 200, 200), position_slider)
            pygame.draw.rect(screen, (0, 0, 0), position_slider, 1)
            
            # Draw slider marker
            marker_x = position_slider.x + int((position_value - 2) * position_slider.width / (MAX_POSITIONS - 2))
            marker_rect = pygame.Rect(marker_x - 5, position_slider.y - 5, 10, position_slider.height + 10)
            pygame.draw.rect(screen, (0, 0, 255), marker_rect)
            
            # Draw min/max values
            min_text = small_font.render("2", True, (0, 0, 0))
            screen.blit(min_text, (position_slider.x - min_text.get_width()//2, position_slider.y + 25))
            
            max_text = small_font.render(str(MAX_POSITIONS), True, (0, 0, 0))
            screen.blit(max_text, (position_slider.x + position_slider.width - max_text.get_width()//2, position_slider.y + 25))
            
            # Draw blocks slider
            blocks_text = font.render(f"Número de blocos: {blocks_value}", True, (0, 0, 0))
            screen.blit(blocks_text, (SCREEN_WIDTH//2 - blocks_text.get_width()//2, SCREEN_HEIGHT//2 - 120))
            
            pygame.draw.rect(screen, (200, 200, 200), blocks_slider)
            pygame.draw.rect(screen, (0, 0, 0), blocks_slider, 1)
            
            # Draw slider marker
            marker_x = blocks_slider.x + int((blocks_value - 2) * blocks_slider.width / 18)  # Max 20 blocks
            marker_rect = pygame.Rect(marker_x - 5, blocks_slider.y - 5, 10, blocks_slider.height + 10)
            pygame.draw.rect(screen, (0, 0, 255), marker_rect)
            
            # Draw min/max values
            min_text = small_font.render("2", True, (0, 0, 0))
            screen.blit(min_text, (blocks_slider.x - min_text.get_width()//2, blocks_slider.y + 25))
            
            max_text = small_font.render("20", True, (0, 0, 0))
            screen.blit(max_text, (blocks_slider.x + blocks_slider.width - max_text.get_width()//2, blocks_slider.y + 25))
            
            # Draw trials slider
            trials_text = font.render(f"Estímulos por bloco: {trials_value}", True, (0, 0, 0))
            screen.blit(trials_text, (SCREEN_WIDTH//2 - trials_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
            
            pygame.draw.rect(screen, (200, 200, 200), trials_slider)
            pygame.draw.rect(screen, (0, 0, 0), trials_slider, 1)
            
            # Draw slider marker
            marker_x = trials_slider.x + int((trials_value - 10) * trials_slider.width / 90)  # Range 10-100
            marker_rect = pygame.Rect(marker_x - 5, trials_slider.y - 5, 10, trials_slider.height + 10)
            pygame.draw.rect(screen, (0, 0, 255), marker_rect)
            
            # Draw min/max values
            min_text = small_font.render("10", True, (0, 0, 0))
            screen.blit(min_text, (trials_slider.x - min_text.get_width()//2, trials_slider.y + 25))
            
            max_text = small_font.render("100", True, (0, 0, 0))
            screen.blit(max_text, (trials_slider.x + trials_slider.width - max_text.get_width()//2, trials_slider.y + 25))
            
            # Draw continue button
            continue_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 40)
            pygame.draw.rect(screen, (100, 100, 250), continue_rect)
            pygame.draw.rect(screen, (0, 0, 0), continue_rect, 1)
            
            continue_text = font.render("Continuar", True, (0, 0, 0))
            screen.blit(continue_text, (continue_rect.x + continue_rect.width//2 - continue_text.get_width()//2, 
                                       continue_rect.y + continue_rect.height//2 - continue_text.get_height()//2))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if position_slider.collidepoint(event.pos):
                        position_slider_active = True
                    elif blocks_slider.collidepoint(event.pos):
                        blocks_slider_active = True
                    elif trials_slider.collidepoint(event.pos):
                        trials_slider_active = True
                    elif continue_rect.collidepoint(event.pos):
                        # Save settings and continue
                        self.positions = position_value
                        self.blocks = blocks_value
                        self.trials_per_block = trials_value
                        done = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    position_slider_active = False
                    blocks_slider_active = False
                    trials_slider_active = False
                
                if event.type == pygame.MOUSEMOTION:
                    # Update position slider
                    if position_slider_active:
                        rel_x = max(0, min(event.pos[0] - position_slider.x, position_slider.width))
                        position_value = int(2 + (rel_x / position_slider.width) * (MAX_POSITIONS - 2))
                        position_value = max(2, min(MAX_POSITIONS, position_value))
                    
                    # Update blocks slider
                    if blocks_slider_active:
                        rel_x = max(0, min(event.pos[0] - blocks_slider.x, blocks_slider.width))
                        blocks_value = int(2 + (rel_x / blocks_slider.width) * 18)
                        blocks_value = max(2, min(20, blocks_value))
                    
                    # Update trials slider
                    if trials_slider_active:
                        rel_x = max(0, min(event.pos[0] - trials_slider.x, trials_slider.width))
                        trials_value = int(10 + (rel_x / trials_slider.width) * 90)
                        trials_value = max(10, min(100, trials_value))
    
    def generate_block_sequence(self):
        """Generate the sequence for the current block"""
        if self.is_structured_block:
            # For structured blocks, repeat the predefined sequence as needed
            structured_sequence = self.generate_structured_sequence()
            repetitions = self.trials_per_block // SEQUENCE_LENGTH
            remainder = self.trials_per_block % SEQUENCE_LENGTH
            sequence = (structured_sequence * repetitions) + structured_sequence[:remainder]
            
            # Modify the sequence to ensure no immediate repetitions
            for i in range(1, len(sequence)):
                if sequence[i] == sequence[i-1]:
                    # Find a non-repeating value
                    options = list(range(self.positions))
                    options.remove(sequence[i-1])
                    sequence[i] = random.choice(options)
                    
            return sequence
        else:
            # For random blocks, generate a pseudo-random sequence
            random_sequence = []
            last_position = None
            
            for _ in range(self.trials_per_block):
                # Generate new positions ensuring no immediate repetitions
                available_positions = list(range(self.positions))
                if last_position is not None:
                    available_positions.remove(last_position)
                
                new_position = random.choice(available_positions)
                random_sequence.append(new_position)
                last_position = new_position
                
            return random_sequence
    
    def collect_participant_info(self):
        """Collect participant information using a simple input dialog"""
        pygame.display.set_caption("Enter Participant ID")
        input_box = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 20, 200, 40)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if text:
                                done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            
            screen.fill(BACKGROUND_COLOR)
            
            # Render instructions
            instructions = font.render('Digite o ID do participante e pressione Enter', True, (0, 0, 0))
            screen.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, SCREEN_HEIGHT//2 - 60))
            
            # Render input box
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))
            pygame.draw.rect(screen, color, input_box, 2)
            
            pygame.display.flip()
        
        self.participant_id = text
        
        # Move to settings screen
        self.get_experiment_settings()
    
    def show_instructions(self):
        """Display instructions for the experiment"""
        screen.fill(BACKGROUND_COLOR)
        
        instructions = [
            "Tarefa de Tempo de Reação em Série (SRTT)",
            "",
            f"Você verá círculos azuis em {self.positions} posições.",
            "Quando um círculo ficar vermelho, pressione a tecla correspondente",
            "o mais rápido e precisamente possível:",
            "",
        ]
        
        # Add key mapping instructions based on selected positions
        for i in range(self.positions):
            if i == 0:
                instructions.append(f"Posição {i + 1} (esquerda): tecla '{POSITION_KEYS[i]}'")
            elif i == self.positions - 1:
                instructions.append(f"Posição {i + 1} (direita): tecla '{POSITION_KEYS[i]}'")
            else:
                instructions.append(f"Posição {i + 1}: tecla '{POSITION_KEYS[i]}'")
        
        instructions += [
            "",
            "Mantenha seus dedos posicionados nas teclas durante todo o experimento.",
            f"O experimento consiste em {self.blocks} blocos de {self.trials_per_block} estímulos cada.",
            "",
            "Pressione ESPAÇO para iniciar o experimento."
        ]
        
        y_pos = SCREEN_HEIGHT // 4
        for line in instructions:
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 30
        
        pygame.display.flip()
        
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_input = False
    
    def show_break(self):
        """Display break screen between blocks"""
        screen.fill(BACKGROUND_COLOR)
        
        break_text = [
            f"Bloco {self.current_block} de {self.blocks} concluído!",
            "",
            "Você pode fazer uma pequena pausa agora.",
            "",
            "Pressione ESPAÇO quando estiver pronto para continuar."
        ]
        
        y_pos = SCREEN_HEIGHT // 3
        for line in break_text:
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 40
        
        pygame.display.flip()
        
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_input = False
    
    def draw_stimuli(self):
        """Draw all stimulus positions and highlight the active one"""
        # Calculate the starting position
        start_x = SCREEN_WIDTH // 2 - ((self.positions - 1) * STIMULUS_DISTANCE) // 2
        
        for i in range(self.positions):
            x = start_x + i * STIMULUS_DISTANCE
            y = SCREEN_HEIGHT // 2
            
            # Draw corresponding key above the circle
            key_text = font.render(POSITION_KEYS[i], True, (0, 0, 0))
            screen.blit(key_text, (x - key_text.get_width()//2, y - STIMULUS_SIZE - 15))
            
            color = STIMULUS_ACTIVE_COLOR if i == self.current_position and self.show_stimulus else STIMULUS_COLOR
            pygame.draw.circle(screen, color, (x, y), STIMULUS_SIZE // 2)
            
            # Draw position number underneath
            position_text = font.render(str(i + 1), True, (0, 0, 0))
            screen.blit(position_text, (x - position_text.get_width()//2, y + STIMULUS_SIZE))
    
    def validate_response(self, key_pressed):
        """Check if the key pressed corresponds to the current position"""
        if key_pressed in KEY_MAPPING and KEY_MAPPING[key_pressed] < self.positions and KEY_MAPPING[key_pressed] == self.current_position:
            return True
        return False
    
    def present_trial(self):
        """Present a single trial"""
        self.current_position = self.block_sequence[self.current_trial]
        self.show_stimulus = True
        self.start_time = time.time()
        
        # Reset for next trial
        self.reaction_time = 0
        waiting_for_response = True
        
        while waiting_for_response and self.running:
            screen.fill(BACKGROUND_COLOR)
            
            # Display block and trial info
            block_info = font.render(f"Bloco: {self.current_block + 1}/{self.blocks}  Trial: {self.current_trial + 1}/{self.trials_per_block}", 
                                     True, (0, 0, 0))
            screen.blit(block_info, (10, 10))
            
            self.draw_stimuli()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return
                    
                    # Check response keys
                    if event.key in KEY_MAPPING:
                        self.reaction_time = (time.time() - self.start_time) * 1000  # Convert to milliseconds
                        correct = self.validate_response(event.key)
                        
                        if correct:
                            self.correct_responses += 1
                        
                        # Record trial data
                        self.results.append({
                            "participant_id": self.participant_id,
                            "block": self.current_block + 1,
                            "block_type": "structured" if self.is_structured_block else "random",
                            "trial": self.current_trial + 1,
                            "position": self.current_position + 1,
                            "reaction_time": round(self.reaction_time, 2),
                            "correct": correct,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Show feedback briefly
                        self.show_stimulus = False
                        pygame.display.flip()
                        pygame.time.delay(100)  # Brief delay between trials
                        
                        waiting_for_response = False
            
            # If no response after 5 seconds, count as error and move on
            if time.time() - self.start_time > 5.0 and waiting_for_response:
                self.reaction_time = 5000  # Set to maximum RT
                
                # Record trial data (missed response)
                self.results.append({
                    "participant_id": self.participant_id,
                    "block": self.current_block + 1,
                    "block_type": "structured" if self.is_structured_block else "random",
                    "trial": self.current_trial + 1,
                    "position": self.current_position + 1,
                    "reaction_time": self.reaction_time,
                    "correct": False,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                waiting_for_response = False
    
    def save_results(self):
        """Save results to a CSV file"""
        # Create results directory if it doesn't exist
        if not os.path.exists('results'):
            os.makedirs('results')
        
        # Generate filename with participant ID and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/srtt_participant_{self.participant_id}_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ["participant_id", "block", "block_type", "trial", 
                          "position", "reaction_time", "correct", "timestamp"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
                
        print(f"Results saved to {filename}")
        return filename
    
    def show_completion_screen(self, filename):
        """Show experiment completion screen"""
        screen.fill(BACKGROUND_COLOR)
        
        # Calculate accuracy
        accuracy = (self.correct_responses / (self.current_block * self.trials_per_block + self.current_trial)) * 100
        
        completion_text = [
            "Experimento concluído!",
            "",
            f"Precisão geral: {accuracy:.1f}%",
            "",
            f"Os resultados foram salvos em:",
            filename,
            "",
            "Obrigado pela sua participação!",
            "",
            "Pressione ESC para sair."
        ]
        
        y_pos = SCREEN_HEIGHT // 4
        for line in completion_text:
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 40
        
        pygame.display.flip()
        
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting_for_input = False
    
    def calculate_block_statistics(self):
        """Calculate statistics for the current block"""
        if self.current_trial > 0:
            # Filter results for the current block
            block_results = [r for r in self.results if r["block"] == self.current_block + 1]
            
            # Calculate mean RT for correct responses only
            correct_rts = [r["reaction_time"] for r in block_results if r["correct"]]
            mean_rt = sum(correct_rts) / len(correct_rts) if correct_rts else 0
            
            # Calculate accuracy
            accuracy = (sum(1 for r in block_results if r["correct"]) / len(block_results)) * 100
            
            block_type = "structured" if self.is_structured_block else "random"
            
            self.blocks_data.append({
                "block": self.current_block + 1,
                "type": block_type,
                "mean_rt": mean_rt,
                "accuracy": accuracy
            })
    
    def run(self):
        """Run the entire experiment"""
        # Collect participant info
        self.collect_participant_info()
        
        # Show instructions
        self.show_instructions()
        
        while self.running and self.current_block < self.blocks:
            # Determine if this is a structured or random block (alternating)
            self.is_structured_block = (self.current_block % 2 == 0)
            
            # Generate block sequence
            self.block_sequence = self.generate_block_sequence()
            
            # Reset for new block
            self.current_trial = 0
            
            # Run trials for current block
            while self.current_trial < self.trials_per_block and self.running:
                # Present trial
                self.present_trial()
                
                # Move to next trial
                self.current_trial += 1
            
            # Calculate and store block statistics
            self.calculate_block_statistics()
            
            # Move to next block
            self.current_block += 1
            
            # Show break between blocks (if not the last block)
            if self.current_block < self.blocks and self.running:
                self.show_break()
        
        if self.running:
            # Save results to file
            filename = self.save_results()
            
            # Show completion screen
            self.show_completion_screen(filename)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    experiment = SRTTExperiment()
    experiment.run()
