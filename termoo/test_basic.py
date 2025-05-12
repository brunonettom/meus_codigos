import pygame
import asyncio
import sys

# Pygbag metadata as Python comments (for compatibility with both environments)
# The lines below are for Pygbag and are ignored by regular Python
# /// script
# # No dependencies needed for this test
# ///

# Simple colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

async def main():
    """Minimal Pygame test for Pygbag"""
    pygame.init()
    
    # Test with a fixed, smaller screen size
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pygbag Basic Test")
    
    # Initialize font safely
    try:
        font = pygame.font.SysFont(None, 36)
    except:
        print("Warning: Could not initialize font")
        font = None
    
    # Debug info
    platform_info = f"Platform: {sys.platform}"
    print(f"Debug: {platform_info}")
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear screen
        screen.fill(WHITE)
        
        # Draw test elements
        pygame.draw.rect(screen, RED, (50, 50, 100, 100))
        
        # Show platform info
        if font:
            text = font.render(platform_info, True, BLACK)
            screen.blit(text, (50, 200))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Required for Pygbag
        await asyncio.sleep(0)

asyncio.run(main())
