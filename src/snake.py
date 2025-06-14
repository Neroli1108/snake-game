import pygame

class Snake:
    def __init__(self, x, y, cell_size):
        self.body = [(x, y)]
        self.direction = (1, 0)
        self.cell_size = cell_size
        self.color = (0, 255, 0)
        self.alive = True
        
    def move(self):
        if not self.alive:
            return
            
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0] * self.cell_size, 
                   head_y + self.direction[1] * self.cell_size)
        self.body.insert(0, new_head)
        self.body.pop()
        
    def grow(self):
        if not self.alive:
            return
            
        tail = self.body[-1]
        self.body.append(tail)
        
    def change_direction(self, dx, dy):
        if not self.alive:
            return
            
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)
            
    def get_head(self):
        return self.body[0]
        
    def check_collision(self):
        head = self.get_head()
        return head in self.body[1:]
        
    def draw(self, screen):
        if not self.alive:
            return
            
        for segment in self.body:
            rect = pygame.Rect(segment[0], segment[1], self.cell_size, self.cell_size)
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)