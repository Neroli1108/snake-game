import pygame
import random

class Food:
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = self.generate_position()
        
    def generate_position(self):
        x = random.randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
        y = random.randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
        return (x, y)
        
    def respawn(self):
        self.position = self.generate_position()
        
    def draw(self, screen):
        rect = pygame.Rect(self.position[0], self.position[1], self.cell_size, self.cell_size)
        pygame.draw.rect(screen, (255, 0, 0), rect)  # Red food