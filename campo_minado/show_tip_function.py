def show_tip(text):
    """Show a gameplay tip to the user if tips are enabled."""
    if not show_tips:
        return
        
    # Create a semi-transparent overlay for the tip
    tip_overlay = pygame.Surface((WINDOWWIDTH, 80), pygame.SRCALPHA)
    tip_overlay.fill((0, 0, 128, 180))  # Semi-transparent blue
    
    # Draw the tip text
    tip_font = pygame.font.Font(None, 24)
    tip_text = tip_font.render(text, True, WHITE)
    tip_rect = tip_text.get_rect(center=(WINDOWWIDTH // 2, 40))
    
    # Display the tip at the bottom of the screen
    DISPLAYSURF.blit(tip_overlay, (0, WINDOWHEIGHT - 80))
    DISPLAYSURF.blit(tip_text, (tip_rect.x, WINDOWHEIGHT - 50))
    
    # Update only the tip area
    pygame.display.update(pygame.Rect(0, WINDOWHEIGHT - 80, WINDOWWIDTH, 80))
    
    # Show the tip for a short time
    pygame.time.delay(3000)  # Show for 3 seconds
