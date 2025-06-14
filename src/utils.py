def draw_snake(surface, snake_body, block_size):
    for block in snake_body:
        pygame.draw.rect(surface, (0, 255, 0), (block[0], block[1], block_size, block_size))

def draw_food(surface, food_position, block_size):
    pygame.draw.rect(surface, (255, 0, 0), (food_position[0], food_position[1], block_size, block_size))

def display_score(surface, score, font, color, position):
    score_surface = font.render(f'Score: {score}', True, color)
    surface.blit(score_surface, position)