import pygame
import asyncio
import sys

# Pygbag metadata with proper format
### script
# No dependencies for this minimal test
###

async def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Minimal Test")
    
    # Debug info
    print(f"Running on platform: {sys.platform}")
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # White background
        
        # Draw a simple red square
        pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 200))
        
        # Draw platform info
        if pygame.font.get_init():
            font = pygame.font.SysFont(None, 24)
            text = font.render(f"Platform: {sys.platform}", True, (0, 0, 0))
            screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
