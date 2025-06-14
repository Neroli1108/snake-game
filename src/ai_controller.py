import random
from collections import deque

class AIController:
    def __init__(self, snake, food, screen_width, screen_height, cell_size):
        self.snake = snake
        self.food = food
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        
    def get_next_direction(self):
        """Smart AI strategy"""
        head = self.snake.get_head()
        
        # First check all safe moves
        safe_moves = self.get_safe_moves()
        
        if not safe_moves:
            # If no safe moves, try to find least dangerous move
            return self.get_least_dangerous_move()
        
        # Choose best among safe moves
        best_move = self.choose_best_safe_move(safe_moves)
        return best_move
    
    def get_safe_moves(self):
        """Get all safe movement directions"""
        head = self.snake.get_head()
        safe_moves = []
        
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Up, down, left, right
            if self.is_move_safe(direction):
                safe_moves.append(direction)
        
        return safe_moves
    
    def is_move_safe(self, direction):
        """Check if move is safe (won't die immediately and has enough space)"""
        head = self.snake.get_head()
        new_x = head[0] + direction[0] * self.cell_size
        new_y = head[1] + direction[1] * self.cell_size
        
        # Check boundaries
        if (new_x < 0 or new_x >= self.screen_width or 
            new_y < 0 or new_y >= self.screen_height):
            return False
        
        # Check collision with body
        if (new_x, new_y) in self.snake.body:
            return False
        
        # Check if opposite to current direction
        current_dir = self.snake.direction
        if direction == (-current_dir[0], -current_dir[1]):
            return False
        
        # Check if this move leads to dead end
        return self.has_escape_route((new_x, new_y), direction)
    
    def has_escape_route(self, position, direction):
        """Check if there's an escape route from this position"""
        # Use BFS to check if there's enough space
        visited = set()
        queue = deque([position])
        visited.add(position)
        space_count = 0
        
        while queue and space_count < len(self.snake.body) + 5:  # Need at least snake length + 5 space
            current = queue.popleft()
            space_count += 1
            
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                next_x = current[0] + dx * self.cell_size
                next_y = current[1] + dy * self.cell_size
                next_pos = (next_x, next_y)
                
                if (0 <= next_x < self.screen_width and 
                    0 <= next_y < self.screen_height and
                    next_pos not in self.snake.body and
                    next_pos not in visited):
                    visited.add(next_pos)
                    queue.append(next_pos)
        
        return space_count >= len(self.snake.body) + 3
    
    def choose_best_safe_move(self, safe_moves):
        """Choose best among safe moves"""
        head = self.snake.get_head()
        food_pos = self.food.position
        
        # Calculate score for each safe move
        move_scores = []
        
        for direction in safe_moves:
            new_x = head[0] + direction[0] * self.cell_size
            new_y = head[1] + direction[1] * self.cell_size
            
            # Calculate distance to food (negative because we want minimum distance)
            food_distance = -(abs(new_x - food_pos[0]) + abs(new_y - food_pos[1]))
            
            # Calculate distance to borders (positive because we want to stay away from borders)
            border_distance = min(new_x, new_y, 
                                self.screen_width - new_x - self.cell_size,
                                self.screen_height - new_y - self.cell_size)
            
            # Calculate nearest distance to snake body
            min_body_distance = float('inf')
            for body_part in self.snake.body:
                dist = abs(new_x - body_part[0]) + abs(new_y - body_part[1])
                min_body_distance = min(min_body_distance, dist)
            
            # Combined score
            score = food_distance * 0.7 + border_distance * 0.2 + min_body_distance * 0.1
            move_scores.append((direction, score))
        
        # Choose move with highest score
        best_move = max(move_scores, key=lambda x: x[1])[0]
        return best_move
    
    def get_least_dangerous_move(self):
        """When no safe moves, choose least dangerous move"""
        head = self.snake.get_head()
        current_dir = self.snake.direction
        
        # At least don't reverse
        possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        reverse_dir = (-current_dir[0], -current_dir[1])
        
        if reverse_dir in possible_moves:
            possible_moves.remove(reverse_dir)
        
        # Among remaining moves, choose one that won't immediately hit wall
        for direction in possible_moves:
            new_x = head[0] + direction[0] * self.cell_size
            new_y = head[1] + direction[1] * self.cell_size
            
            if (0 <= new_x < self.screen_width and 
                0 <= new_y < self.screen_height):
                return direction
        
        # If all will hit wall, randomly choose one
        return random.choice(possible_moves) if possible_moves else (1, 0)