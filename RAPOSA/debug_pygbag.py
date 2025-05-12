import asyncio
import pygame
import sys
import os
import math  # Use standard math module instead of pygame.math

# Print working directory for debugging
print(f"Current working directory: {os.getcwd()}")

# Initialize pygame
pygame.init()
pygame.display.init()

# Create a window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debug Pygbag")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)

# For tracking frame rate
clock = pygame.time.Clock()
fps_counter = 0
fps_timer = 0
current_fps = 0

# Test image loading to see if that works
def try_load_image():
    try:
        # Try to load a simple shape - this always works
        surf = pygame.Surface((100, 100))
        surf.fill(RED)
        return surf, "Created red square surface"
    except Exception as e:
        return None, f"Error creating surface: {str(e)}"

async def main():
    global fps_counter, fps_timer, current_fps
    
    print("Debug script started")
    
    # Platform check
    if sys.platform == "emscripten":
        print("Running in browser with Emscripten")
    else:
        print("Running natively")
    
    # Print pygame info
    print(f"Pygame version: {pygame.version.ver}")
    print(f"SDL version: {pygame.version.SDL}")
    
    # Try to load an image
    test_surf, message = try_load_image()
    
    print(f"Image test result: {message}")
    
    # Main game loop
    running = True
    frame_count = 0
    
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Clear screen
        screen.fill(BLACK)
        
        # Draw test content
        if test_surf:
            screen.blit(test_surf, (WIDTH//2 - 50, HEIGHT//2 - 50))
            
        # Draw debug text
        frame_count += 1
        fps_counter += 1
        current_time = pygame.time.get_ticks()
        
        if current_time - fps_timer > 1000:  # Update FPS every second
            current_fps = fps_counter
            fps_counter = 0
            fps_timer = current_time
            
        # Draw platform info
        platform_text = f"Platform: {'Browser' if sys.platform == 'emscripten' else 'Native'}"
        text_surf = font.render(platform_text, True, WHITE)
        screen.blit(text_surf, (20, 20))
        
        # Draw FPS
        fps_text = f"FPS: {current_fps}"
        text_surf = font.render(fps_text, True, WHITE)
        screen.blit(text_surf, (20, 60))
        
        # Draw frame count
        frame_text = f"Frames: {frame_count}"
        text_surf = font.render(frame_text, True, WHITE)
        screen.blit(text_surf, (20, 100))
        
        # Draw animation test (moving circle) - use standard math module instead of pygame.math
        pygame.draw.circle(
            screen, 
            BLUE, 
            (int(WIDTH//2 + 150 * math.sin(frame_count/30)), HEIGHT//2), 
            30
        )
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(60)
        
        # Required for Pygbag
        await asyncio.sleep(0)
        
    pygame.quit()

# Run the async function
print("Starting debug script...")
asyncio.run(main())
