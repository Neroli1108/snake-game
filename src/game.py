import pygame
import random
from snake import Snake
from ai_controller import AIController

class Game:
    def __init__(self, screen, ai_mode=False):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.ai_mode = ai_mode
        
        # Game settings
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.cell_size = 20
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 72)
        
        # Initialize game objects
        start_x = (self.width // 2 // self.cell_size) * self.cell_size
        start_y = (self.height // 2 // self.cell_size) * self.cell_size
        self.snake = Snake(start_x, start_y, self.cell_size)
        
        self.score = 0
        self.game_start_time = pygame.time.get_ticks()
        
        # Generate food
        self.food_pos = self.generate_food()
        
        # AI controller
        if self.ai_mode:
            # Create temporary food object for AI use
            self.temp_food = type('Food', (), {'position': self.food_pos})()
            self.ai_controller = AIController(self.snake, self.temp_food, self.width, self.height, self.cell_size)
        
        print(f"Game initialized - Snake at: {(start_x, start_y)}, Food at: {self.food_pos}")
        
    def generate_food(self):
        """Generate food position, ensuring it's not on the snake body"""
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            food_pos = (x, y)
            
            # Ensure food is not on snake body
            if food_pos not in self.snake.body:
                print(f"Food generated at: {food_pos}")
                return food_pos
                
            attempts += 1
        
        # If no suitable position found, return a safe position
        return (self.cell_size, self.cell_size)
            
    def run(self):
        print(f"Starting {'AI' if self.ai_mode else 'Manual'} game...")
        
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    # Only respond to keyboard control in manual mode
                    if not self.ai_mode:
                        current_dir = self.snake.direction
                        new_dir = None
                        
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            new_dir = (0, -1)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            new_dir = (0, 1)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            new_dir = (-1, 0)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            new_dir = (1, 0)
                        
                        # Prevent reverse movement
                        if new_dir and new_dir != (-current_dir[0], -current_dir[1]):
                            self.snake.change_direction(new_dir[0], new_dir[1])
                            print(f"Direction changed to: {new_dir}")
                            
    def update(self):
        # AI control
        if self.ai_mode:
            # Update AI food target
            self.temp_food.position = self.food_pos
            direction = self.ai_controller.get_next_direction()
            self.snake.change_direction(direction[0], direction[1])
        
        # Move snake
        self.snake.move()
        
        # Check food collision
        head = self.snake.get_head()
        if head == self.food_pos:
            print(f"Food eaten! Snake head: {head}, Food position: {self.food_pos}")
            self.snake.grow()
            self.score += 10
            self.food_pos = self.generate_food()
            print(f"Score: {self.score}, Snake length: {len(self.snake.body)}")
        
        # Check boundary collision
        if (head[0] < 0 or head[0] >= self.width or 
            head[1] < 0 or head[1] >= self.height):
            print("Snake hit boundary!")
            self.end_game()
            
        # Check self collision
        if self.snake.check_collision():
            print("Snake hit itself!")
            self.end_game()
            
    def end_game(self):
        """End the game"""
        self.game_over = True
        print(f"Game Over! Final score: {self.score}")
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if not self.game_over:
            self.draw_game()
        else:
            self.draw_result_screen()
            
        pygame.display.flip()
        
    def draw_game(self):
        """Draw game screen"""
        # Draw snake
        self.snake.draw(self.screen)
        
        # Draw food
        self.draw_food(self.food_pos)
        
        # Draw score and info
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        length_text = self.small_font.render(f"Length: {len(self.snake.body)}", True, (255, 255, 255))
        self.screen.blit(length_text, (10, 50))
        
        # Show mode
        mode_text = self.small_font.render(f"Mode: {'AI' if self.ai_mode else 'Manual'}", True, (150, 150, 150))
        self.screen.blit(mode_text, (10, 75))
        
        # Control instructions (manual mode only)
        if not self.ai_mode:
            controls = self.small_font.render("WASD/Arrow Keys to move", True, (100, 100, 100))
            self.screen.blit(controls, (10, 100))
            
    def draw_food(self, food_pos):
        """Draw food"""
        rect = pygame.Rect(food_pos[0], food_pos[1], self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (255, 0, 0), rect)  # Red food
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # White border
        
    def draw_result_screen(self):
        """Draw result screen"""
        # Semi-transparent background
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game time
        game_time = (pygame.time.get_ticks() - self.game_start_time) // 1000
        minutes = game_time // 60
        seconds = game_time % 60
        
        # Title
        title_text = self.large_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Statistics
        stats = [
            f"Final Score: {self.score}",
            f"Snake Length: {len(self.snake.body)}",
            f"Survival Time: {minutes:02d}:{seconds:02d}",
            f"Mode: {'AI' if self.ai_mode else 'Manual'}"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.font.render(stat, True, (255, 255, 255))
            stat_rect = stat_text.get_rect(center=(self.width // 2, self.height // 2 - 20 + i * 40))
            self.screen.blit(stat_text, stat_rect)
        
        # Control instructions
        controls = [
            "Press R to Play Again",
            "Press Q or ESC to Return to Menu"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, (150, 150, 150))
            control_rect = control_text.get_rect(center=(self.width // 2, self.height // 2 + 120 + i * 25))
            self.screen.blit(control_text, control_rect)
        
    def restart_game(self):
        """Restart the game"""
        print("Restarting game...")
        self.game_over = False
        self.score = 0
        self.game_start_time = pygame.time.get_ticks()
        
        # Reset snake position
        start_x = (self.width // 2 // self.cell_size) * self.cell_size
        start_y = (self.height // 2 // self.cell_size) * self.cell_size
        self.snake = Snake(start_x, start_y, self.cell_size)
        
        # Regenerate food
        self.food_pos = self.generate_food()
        
        # Reinitialize AI controller
        if self.ai_mode:
            self.temp_food = type('Food', (), {'position': self.food_pos})()
            self.ai_controller = AIController(self.snake, self.temp_food, self.width, self.height, self.cell_size)
        
        print("Game restarted!")