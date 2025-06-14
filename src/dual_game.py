import pygame
from snake import Snake
from food import Food
from ai_controller import AIController
import random

class DualGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # Game settings
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.cell_size = 20
        self.divider_width = 4
        
        # Left and right game areas
        self.left_width = (self.width - self.divider_width) // 2
        self.right_width = self.width - self.left_width - self.divider_width
        self.right_area_start = self.left_width + self.divider_width
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 72)
        
        # Initialize both game areas
        self.init_games()
        
    def init_games(self):
        """Initialize AI and human player games"""
        # AI player (left side)
        self.ai_score = 0
        ai_start_x = (self.left_width // 2 // self.cell_size) * self.cell_size
        ai_start_y = (self.height // 2 // self.cell_size) * self.cell_size
        self.ai_snake = Snake(ai_start_x, ai_start_y, self.cell_size)
        self.ai_food_pos = self.generate_ai_food()
        
        # Create temporary food object for AI use
        self.temp_ai_food = type('Food', (), {'position': self.ai_food_pos})()
        self.ai_controller = AIController(self.ai_snake, self.temp_ai_food, self.left_width, self.height, self.cell_size)
        self.ai_alive = True
        
        # Human player (right side)
        self.human_score = 0
        human_start_x = self.right_area_start + (self.right_width // 2 // self.cell_size) * self.cell_size
        human_start_y = (self.height // 2 // self.cell_size) * self.cell_size
        self.human_snake = Snake(human_start_x, human_start_y, self.cell_size)
        self.human_food_pos = self.generate_human_food()
        self.human_alive = True
        
        # Game state
        self.winner = None
        self.game_start_time = pygame.time.get_ticks()
        
        print(f"Game initialized - AI start: ({ai_start_x}, {ai_start_y}), Human start: ({human_start_x}, {human_start_y})")
        
    def generate_ai_food(self):
        """Generate food for AI (in left area)"""
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            x = random.randint(0, (self.left_width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            food_pos = (x, y)
            
            # Ensure food is not on snake body
            if hasattr(self, 'ai_snake') and food_pos not in self.ai_snake.body:
                return food_pos
            elif not hasattr(self, 'ai_snake'):
                return food_pos
            
            attempts += 1
        
        # If no suitable position found, return a safe position
        return (self.cell_size, self.cell_size)
                
    def generate_human_food(self):
        """Generate food for human (in right area)"""
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            x = random.randint(0, (self.right_width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            # Convert to actual coordinates in right area
            food_pos = (x + self.right_area_start, y)
            
            # Ensure food is not on snake body
            if hasattr(self, 'human_snake') and food_pos not in self.human_snake.body:
                return food_pos
            elif not hasattr(self, 'human_snake'):
                return food_pos
            
            attempts += 1
        
        # If no suitable position found, return a safe position
        return (self.right_area_start + self.cell_size, self.cell_size)
        
    def run(self):
        print("Dual game started!")
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(8)
            
    def handle_events(self):
        keys = pygame.key.get_pressed()  # Get current key states
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)}")  # Debug info
                
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    # Human player control (right side)
                    if self.human_alive:
                        current_dir = self.human_snake.direction
                        new_dir = None
                        
                        # Arrow key control
                        if event.key == pygame.K_UP:
                            new_dir = (0, -1)
                            print("UP pressed")
                        elif event.key == pygame.K_DOWN:
                            new_dir = (0, 1)
                            print("DOWN pressed")
                        elif event.key == pygame.K_LEFT:
                            new_dir = (-1, 0)
                            print("LEFT pressed")
                        elif event.key == pygame.K_RIGHT:
                            new_dir = (1, 0)
                            print("RIGHT pressed")
                        
                        # WASD control
                        elif event.key == pygame.K_w:
                            new_dir = (0, -1)
                            print("W pressed")
                        elif event.key == pygame.K_s:
                            new_dir = (0, 1)
                            print("S pressed")
                        elif event.key == pygame.K_a:
                            new_dir = (-1, 0)
                            print("A pressed")
                        elif event.key == pygame.K_d:
                            new_dir = (1, 0)
                            print("D pressed")
                        
                        # Prevent reverse movement and apply new direction
                        if new_dir and new_dir != (-current_dir[0], -current_dir[1]):
                            self.human_snake.change_direction(new_dir[0], new_dir[1])
                            print(f"Direction changed to: {new_dir}")
                    
    def update(self):
        # Update AI player
        if self.ai_alive:
            # Update AI controller food position
            self.temp_ai_food.position = self.ai_food_pos
            
            direction = self.ai_controller.get_next_direction()
            self.ai_snake.change_direction(direction[0], direction[1])
            self.ai_snake.move()
            
            # Check if AI ate food
            ai_head = self.ai_snake.get_head()
            if ai_head == self.ai_food_pos:
                self.ai_snake.grow()
                self.ai_food_pos = self.generate_ai_food()
                self.ai_score += 10
                print(f"AI ate food! Score: {self.ai_score}")
                
            # Check if AI died
            if (ai_head[0] < 0 or ai_head[0] >= self.left_width or 
                ai_head[1] < 0 or ai_head[1] >= self.height or
                self.ai_snake.check_collision()):
                self.ai_alive = False
                print("AI died!")
        
        # Update human player
        if self.human_alive:
            self.human_snake.move()
            
            # Check if human ate food
            human_head = self.human_snake.get_head()
            if human_head == self.human_food_pos:
                self.human_snake.grow()
                self.human_food_pos = self.generate_human_food()
                self.human_score += 10
                print(f"Human ate food! Score: {self.human_score}")
                
            # Check if human died
            if (human_head[0] < self.right_area_start or human_head[0] >= self.width or 
                human_head[1] < 0 or human_head[1] >= self.height or
                self.human_snake.check_collision()):
                self.human_alive = False
                print("Human died!")
        
        # Check if game is over
        if not self.ai_alive or not self.human_alive:
            self.end_game()
            
    def end_game(self):
        """End game and determine winner"""
        self.game_over = True
        
        if not self.ai_alive and not self.human_alive:
            # Tie, compare scores
            if self.ai_score > self.human_score:
                self.winner = "AI"
            elif self.human_score > self.ai_score:
                self.winner = "Human"
            else:
                self.winner = "Tie"
        elif not self.ai_alive:
            self.winner = "Human"
        elif not self.human_alive:
            self.winner = "AI"
        
        print(f"Game Over! Winner: {self.winner}")
            
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if not self.game_over:
            self.draw_game()
        else:
            self.draw_result_screen()
            
        pygame.display.flip()
        
    def draw_game(self):
        """Draw game screen"""
        # Draw divider line
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (self.left_width, 0, self.divider_width, self.height))
        
        # Draw AI area (left side)
        if self.ai_alive:
            self.ai_snake.draw(self.screen)
            self.draw_food(self.ai_food_pos, (255, 0, 0))
        else:
            # AI died, show semi-transparent overlay
            overlay = pygame.Surface((self.left_width, self.height))
            overlay.set_alpha(100)
            overlay.fill((255, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
        # Draw human area (right side)
        if self.human_alive:
            self.human_snake.draw(self.screen)
            self.draw_food(self.human_food_pos, (255, 0, 0))
        else:
            # Human died, show semi-transparent overlay
            overlay = pygame.Surface((self.right_width, self.height))
            overlay.set_alpha(100)
            overlay.fill((255, 0, 0))
            self.screen.blit(overlay, (self.right_area_start, 0))
        
        # Draw scores and labels
        self.draw_scores()
        
        # Debug info
        debug_info = [
            f"AI: Head={self.ai_snake.get_head()}, Food={self.ai_food_pos}, Alive={self.ai_alive}",
            f"Human: Head={self.human_snake.get_head()}, Food={self.human_food_pos}, Alive={self.human_alive}",
            f"Human Direction: {self.human_snake.direction}"
        ]
        
        for i, debug_text in enumerate(debug_info):
            debug_surface = pygame.font.Font(None, 20).render(debug_text, True, (100, 100, 100))
            self.screen.blit(debug_surface, (10, self.height - 60 + i * 20))
        
    def draw_food(self, food_pos, color):
        """Draw food"""
        rect = pygame.Rect(food_pos[0], food_pos[1], self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect)
        # Draw food border
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
        
    def draw_scores(self):
        """Draw scores and labels"""
        # AI area label and score
        ai_label = self.font.render("AI Player", True, (0, 255, 0))
        ai_label_rect = ai_label.get_rect(center=(self.left_width // 2, 30))
        self.screen.blit(ai_label, ai_label_rect)
        
        ai_score_text = self.small_font.render(f"Score: {self.ai_score}", True, (255, 255, 255))
        ai_score_rect = ai_score_text.get_rect(center=(self.left_width // 2, 60))
        self.screen.blit(ai_score_text, ai_score_rect)
        
        # Human area label and score
        human_center_x = self.right_area_start + self.right_width // 2
        human_label = self.font.render("Human Player", True, (0, 255, 255))
        human_label_rect = human_label.get_rect(center=(human_center_x, 30))
        self.screen.blit(human_label, human_label_rect)
        
        human_score_text = self.small_font.render(f"Score: {self.human_score}", True, (255, 255, 255))
        human_score_rect = human_score_text.get_rect(center=(human_center_x, 60))
        self.screen.blit(human_score_text, human_score_rect)
        
        # Control instructions
        controls = self.small_font.render("Controls: WASD or Arrow Keys", True, (150, 150, 150))
        controls_rect = controls.get_rect(center=(human_center_x, 90))
        self.screen.blit(controls, controls_rect)
        
    def draw_result_screen(self):
        """Draw result screen"""
        # Semi-transparent background
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game time
        game_time = (pygame.time.get_ticks() - self.game_start_time) // 1000
        minutes = game_time // 60
        seconds = game_time % 60
        
        # Title
        title_text = self.large_font.render("GAME OVER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Winner info
        if self.winner == "Tie":
            winner_text = self.font.render("IT'S A TIE!", True, (255, 255, 0))
        elif self.winner == "AI":
            winner_text = self.font.render("AI WINS!", True, (0, 255, 0))
        else:
            winner_text = self.font.render("HUMAN WINS!", True, (0, 255, 255))
            
        winner_rect = winner_text.get_rect(center=(self.width // 2, 170))
        self.screen.blit(winner_text, winner_rect)
        
        # Detailed statistics
        stats_y = 240
        stats = [
            f"Game Time: {minutes:02d}:{seconds:02d}",
            f"AI Score: {self.ai_score}",
            f"Human Score: {self.human_score}",
            f"Score Difference: {abs(self.ai_score - self.human_score)}"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.font.render(stat, True, (255, 255, 255))
            stat_rect = stat_text.get_rect(center=(self.width // 2, stats_y + i * 35))
            self.screen.blit(stat_text, stat_rect)
        
        # Survival status
        survival_y = stats_y + len(stats) * 35 + 30
        ai_status = "Alive" if self.ai_alive else "Dead"
        human_status = "Alive" if self.human_alive else "Dead"
        
        ai_status_text = self.small_font.render(f"AI Status: {ai_status}", True, 
                                               (0, 255, 0) if self.ai_alive else (255, 100, 100))
        ai_status_rect = ai_status_text.get_rect(center=(self.width // 2, survival_y))
        self.screen.blit(ai_status_text, ai_status_rect)
        
        human_status_text = self.small_font.render(f"Human Status: {human_status}", True, 
                                                  (0, 255, 255) if self.human_alive else (255, 100, 100))
        human_status_rect = human_status_text.get_rect(center=(self.width // 2, survival_y + 25))
        self.screen.blit(human_status_text, human_status_rect)
        
        # Control instructions
        controls = [
            "Press R to Play Again",
            "Press Q or ESC to Quit"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, (150, 150, 150))
            control_rect = control_text.get_rect(center=(self.width // 2, survival_y + 80 + i * 25))
            self.screen.blit(control_text, control_rect)
        
    def restart_game(self):
        """Restart the match"""
        self.game_over = False
        self.winner = None
        self.init_games()