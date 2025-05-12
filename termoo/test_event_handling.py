import pygame
import asyncio
import sys

# Pygbag metadata - using Python comments for compatibility
# /// script
# # No dependencies needed for this test
# ///

# Simple colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

async def main():
    """Test for event handling with Pygbag"""
    pygame.init()
    pygame.font.init()
    
    # Test with browser-friendly screen size
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Pygbag Event Test")
    
    font = pygame.font.SysFont("Arial", 24)
    
    # Debug variables
    mouse_pos = (0, 0)
    last_key = "None"
    click_count = 0
    
    clock = pygame.time.Clock()
    running = True
    
    # Create a button
    button_rect = pygame.Rect(300, 250, 200, 100)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_count += 1
                if button_rect.collidepoint(event.pos):
                    print("Button clicked!")
                    
            elif event.type == pygame.KEYDOWN:
                last_key = pygame.key.name(event.key)
                
        # Clear screen
        screen.fill(WHITE)
        
        # Draw button
        color = GREEN if button_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(screen, color, button_rect)
        
        button_text = font.render("Click Me!", True, BLACK)
        screen.blit(button_text, 
                    (button_rect.centerx - button_text.get_width()//2, 
                     button_rect.centery - button_text.get_height()//2))
        
        # Draw debug info
        info_texts = [
            f"Platform: {sys.platform}",
            f"Mouse: {mouse_pos}",
            f"Last key: {last_key}",
            f"Clicks: {click_count}"
        ]
        
        for i, text in enumerate(info_texts):
            text_surf = font.render(text, True, BLACK)
            screen.blit(text_surf, (20, 20 + i*30))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Required for Pygbag
        await asyncio.sleep(0)

asyncio.run(main())
