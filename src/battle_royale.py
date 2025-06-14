import pygame
import random
import math
from snake import Snake
from ai_controller import AIController

class BattleRoyaleGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.human_eliminated = False
        
        # Game settings
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.cell_size = 20
        
        # Boundary shrinking system
        self.original_width = self.width
        self.original_height = self.height
        self.safe_zone_width = self.width
        self.safe_zone_height = self.height
        self.safe_zone_x = 0
        self.safe_zone_y = 0
        self.shrink_timer = 0
        self.shrink_interval = 60000  # 60 seconds = 60000ms
        self.shrink_amount = 40  # Shrink by 40 pixels each time
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 72)
        
        # Game state
        self.snakes = []
        self.ai_controllers = []
        self.foods = []
        self.human_snake_index = 0
        self.winner = None
        self.game_start_time = pygame.time.get_ticks()
        
        # Initialize game
        self.init_game()
        
    def init_game(self):
        """Initialize 25 snakes and AI controllers"""
        self.snakes = []
        self.ai_controllers = []
        self.human_eliminated = False
        
        # Create 25 snakes
        for i in range(25):
            # Random position, ensure within boundaries
            x = random.randint(2, (self.width // self.cell_size) - 3) * self.cell_size
            y = random.randint(2, (self.height // self.cell_size) - 3) * self.cell_size
            
            snake = Snake(x, y, self.cell_size)
            # Ensure snake has alive attribute
            if not hasattr(snake, 'alive'):
                snake.alive = True
            
            # Random color
            snake.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.snakes.append(snake)
            
            # Create AI controller for each snake (including human-controlled snake as backup)
            ai_controller = AIController(snake, None, self.width, self.height, self.cell_size)
            self.ai_controllers.append(ai_controller)
        
        # First snake controlled by human
        self.human_snake_index = 0
        self.snakes[0].color = (0, 255, 255)  # Cyan to identify human snake
        
        # Generate initial food
        self.generate_foods()
        
        print(f"Battle Royale initialized with {len(self.snakes)} snakes")
        
    def generate_foods(self):
        """Generate random number of foods"""
        self.foods = []
        food_count = random.randint(3, 8)  # 3-8 foods
        
        for _ in range(food_count):
            # Ensure food is within safe zone
            attempts = 0
            while attempts < 100:
                x = random.randint(
                    max(0, self.safe_zone_x // self.cell_size),
                    min((self.width // self.cell_size) - 1, (self.safe_zone_x + self.safe_zone_width) // self.cell_size - 1)
                ) * self.cell_size
                y = random.randint(
                    max(0, self.safe_zone_y // self.cell_size),
                    min((self.height // self.cell_size) - 1, (self.safe_zone_y + self.safe_zone_height) // self.cell_size - 1)
                ) * self.cell_size
                
                food_pos = (x, y)
                
                # Check if food overlaps with snakes
                occupied = False
                for snake in self.snakes:
                    if hasattr(snake, 'alive') and snake.alive and food_pos in snake.body:
                        occupied = True
                        break
                
                if not occupied:
                    self.foods.append(food_pos)
                    break
                
                attempts += 1
        
        print(f"Generated {len(self.foods)} foods")
        
    def get_snake_speed(self, snake_length):
        """Calculate speed based on snake length (longer snakes are slower)"""
        # Length 1-5: Speed 25-21
        # Length 6-10: Speed 20-16
        # Length 11+: Speed 15-5 (minimum 5)
        base_speed = max(5, 30 - snake_length)
        return min(25, base_speed)
        
    def run(self):
        print("Battle Royale started!")
        frame_count = 0
        
        while self.running:
            current_time = pygame.time.get_ticks()
            
            self.handle_events()
            
            if not self.game_over:
                # Check if human player died
                human_snake = self.snakes[self.human_snake_index]
                if not hasattr(human_snake, 'alive'):
                    human_snake.alive = True
                    
                if not human_snake.alive and not self.human_eliminated:
                    self.human_eliminated = True
                    print("Human player eliminated! Game Over!")
                    self.end_game_human_eliminated()
                
                # Check boundary shrinking
                if current_time - self.shrink_timer >= self.shrink_interval:
                    self.shrink_safe_zone()
                    self.shrink_timer = current_time
                
                # Update snakes at different speeds based on their length
                for i, snake in enumerate(self.snakes):
                    # Check if snake has alive attribute, add if missing
                    if not hasattr(snake, 'alive'):
                        snake.alive = True
                        
                    if not snake.alive:
                        continue
                        
                    speed = self.get_snake_speed(len(snake.body))
                    # Determine update frequency based on speed
                    update_frequency = max(1, 30 - speed)
                    if frame_count % update_frequency == 0:
                        self.update_snake(i)
                
                # Periodically regenerate food
                if len(self.foods) < 2:
                    self.generate_foods()
                
                # Check game end conditions
                if not self.human_eliminated:
                    alive_ai_snakes = [s for i, s in enumerate(self.snakes) 
                                     if i != self.human_snake_index and hasattr(s, 'alive') and s.alive]
                    if len(alive_ai_snakes) == 0 and human_snake.alive:
                        # Human wins
                        self.end_game_human_win()
                    elif len(alive_ai_snakes) <= 1 and not human_snake.alive:
                        # AI wins or no winner
                        self.end_game()
                    
            self.draw()
            self.clock.tick(30)  # Fixed 30 FPS
            frame_count += 1
            
    def update_snake(self, snake_index):
        """Update single snake"""
        snake = self.snakes[snake_index]
        if not hasattr(snake, 'alive'):
            snake.alive = True
            
        if not snake.alive:
            return
            
        # Human control vs AI control
        if snake_index == self.human_snake_index:
            # Human snake controlled by keyboard (handled in handle_events)
            pass
        else:
            # AI control
            ai_controller = self.ai_controllers[snake_index]
            # Update AI target (nearest food or smaller snake)
            self.update_ai_target(ai_controller, snake)
            direction = ai_controller.get_next_direction()
            snake.change_direction(direction[0], direction[1])
        
        # Move snake
        snake.move()
        
        # Check food collision
        head = snake.get_head()
        eaten_food = None
        for food_pos in self.foods:
            if head == food_pos:
                snake.grow()
                eaten_food = food_pos
                print(f"Snake {snake_index} ate food! New length: {len(snake.body)}")
                break
        
        if eaten_food:
            self.foods.remove(eaten_food)
            
        # Check snake-to-snake collision (big snake eats small snake)
        for i, other_snake in enumerate(self.snakes):
            if i == snake_index:
                continue
            if not hasattr(other_snake, 'alive'):
                other_snake.alive = True
            if not other_snake.alive:
                continue
                
            if head in other_snake.body:
                if len(snake.body) > len(other_snake.body):
                    # Big snake eats small snake
                    snake.grow()
                    other_snake.alive = False
                    
                    if i == self.human_snake_index:
                        print(f"Human player was eaten by snake {snake_index}!
")
                    else:
                        print(f"Snake {snake_index} ate snake {i}! Size: {len(snake.body)} vs {len(other_snake.body)}")
                else:
                    # Small snake dies hitting big snake
                    snake.alive = False
                    
                    if snake_index == self.human_snake_index:
                        print(f"Human player died by hitting larger snake {i}")
                    else:
                        print(f"Snake {snake_index} died by hitting larger snake {i}")
                    return
        
        # Check boundary and self collision
        if (head[0] < self.safe_zone_x or 
            head[0] >= self.safe_zone_x + self.safe_zone_width or
            head[1] < self.safe_zone_y or 
            head[1] >= self.safe_zone_y + self.safe_zone_height or
            snake.check_collision()):
            snake.alive = False
            
            if snake_index == self.human_snake_index:
                print(f"Human player died by boundary/self collision")
            else:
                print(f"Snake {snake_index} died by boundary/self collision")
            
    def update_ai_target(self, ai_controller, snake):
        """Update AI target"""
        # Create temporary food object
        if self.foods:
            closest_food = min(self.foods, key=lambda f: abs(f[0] - snake.get_head()[0]) + abs(f[1] - snake.get_head()[1]))
            temp_food = type('Food', (), {'position': closest_food})()
            ai_controller.food = temp_food
        
        # Update safe zone info
        ai_controller.screen_width = self.safe_zone_width
        ai_controller.screen_height = self.safe_zone_height
        
    def shrink_safe_zone(self):
        """Shrink safe zone"""
        if self.safe_zone_width > 200 and self.safe_zone_height > 200:
            self.safe_zone_width -= self.shrink_amount
            self.safe_zone_height -= self.shrink_amount
            self.safe_zone_x += self.shrink_amount // 2
            self.safe_zone_y += self.shrink_amount // 2
            
            print(f"Safe zone shrunk! New size: {self.safe_zone_width}x{self.safe_zone_height}")
            
            # Regenerate food
            self.generate_foods()
        
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
                    # Human player control
                    if (self.human_snake_index < len(self.snakes) and not self.human_eliminated):
                        human_snake = self.snakes[self.human_snake_index]
                        if not hasattr(human_snake, 'alive'):
                            human_snake.alive = True
                            
                        if human_snake.alive:
                            current_dir = human_snake.direction
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
                                human_snake.change_direction(new_dir[0], new_dir[1])
    
    def end_game_human_eliminated(self):
        """Human eliminated, game over"""
        self.game_over = True
        self.winner = "You were eliminated!"
        print("Human eliminated - Game Over!")
        
    def end_game_human_win(self):
        """Human wins"""
        self.game_over = True
        self.winner = "Human"
        print("Human wins the Battle Royale!")
        
    def end_game(self):
        """Regular game end"""
        self.game_over = True
        alive_snakes = [(i, s) for i, s in enumerate(self.snakes) 
                       if hasattr(s, 'alive') and s.alive and i != self.human_snake_index]
        
        if alive_snakes:
            winner_index, winner_snake = alive_snakes[0]
            self.winner = f"AI Snake {winner_index}"
        else:
            self.winner = "No Winner"
            
        print(f"Battle Royale ended! Winner: {self.winner}")
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if not self.game_over:
            self.draw_game()
        else:
            self.draw_result_screen()
            
        pygame.display.flip()
        
    def draw_game(self):
        """Draw game screen"""
        # Draw danger zone (red)
        if (self.safe_zone_x > 0 or self.safe_zone_y > 0 or 
            self.safe_zone_width < self.width or self.safe_zone_height < self.height):
            
            # Draw entire screen as danger zone
            self.screen.fill((100, 0, 0))
            
            # Draw safe zone (black)
            pygame.draw.rect(self.screen, (0, 0, 0), 
                           (self.safe_zone_x, self.safe_zone_y, self.safe_zone_width, self.safe_zone_height))
        
        # Draw safe zone boundary
        if self.safe_zone_width < self.width or self.safe_zone_height < self.height:
            pygame.draw.rect(self.screen, (255, 255, 255), 
                            (self.safe_zone_x, self.safe_zone_y, self.safe_zone_width, self.safe_zone_height), 2)
        
        # Draw all alive snakes only
        for i, snake in enumerate(self.snakes):
            if not hasattr(snake, 'alive'):
                snake.alive = True
                
            # Only draw alive snakes
            if snake.alive:
                # Special identifier for human snake
                if i == self.human_snake_index:
                    # Draw halo effect
                    head = snake.get_head()
                    pygame.draw.circle(self.screen, (255, 255, 255), 
                                     (head[0] + self.cell_size//2, head[1] + self.cell_size//2), 
                                     self.cell_size, 2)
                
                snake.draw(self.screen)
        
        # Draw food
        for food_pos in self.foods:
            rect = pygame.Rect(food_pos[0], food_pos[1], self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (255, 0, 0), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
        
        # Draw game info
        self.draw_game_info()
        
    def draw_game_info(self):
        """Draw game information"""
        # Number of alive snakes (including human)
        alive_count = sum(1 for s in self.snakes if hasattr(s, 'alive') and s.alive)
        alive_text = self.font.render(f"Alive: {alive_count}/25", True, (255, 255, 255))
        self.screen.blit(alive_text, (10, 10))
        
        # Number of alive AI snakes
        alive_ai_count = sum(1 for i, s in enumerate(self.snakes) 
                           if i != self.human_snake_index and hasattr(s, 'alive') and s.alive)
        ai_text = self.small_font.render(f"AI Snakes: {alive_ai_count}/24", True, (255, 255, 255))
        self.screen.blit(ai_text, (10, 40))
        
        # Human snake info
        if (self.human_snake_index < len(self.snakes)):
            human_snake = self.snakes[self.human_snake_index]
            if not hasattr(human_snake, 'alive'):
                human_snake.alive = True
                
            if human_snake.alive and not self.human_eliminated:
                length = len(human_snake.body)
                speed = self.get_snake_speed(length)
                
                player_text = self.small_font.render(f"You: Length {length}, Speed {speed}", True, (0, 255, 255))
                self.screen.blit(player_text, (10, 65))
            else:
                dead_text = self.small_font.render("You are eliminated!", True, (255, 0, 0))
                self.screen.blit(dead_text, (10, 65))
        
        # Game time and next shrink countdown
        current_time = pygame.time.get_ticks()
        game_time = (current_time - self.game_start_time) // 1000
        next_shrink = max(0, (self.shrink_interval - (current_time - self.shrink_timer)) // 1000)
        
        time_text = self.small_font.render(f"Time: {game_time//60:02d}:{game_time%60:02d}", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 90))
        
        shrink_text = self.small_font.render(f"Next shrink: {next_shrink}s", True, (255, 255, 0))
        self.screen.blit(shrink_text, (10, 115))
        
        # Control instructions
        if not self.human_eliminated:
            controls = self.small_font.render("WASD/Arrow Keys to move", True, (150, 150, 150))
            self.screen.blit(controls, (10, 140))
        
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
        title_text = self.large_font.render("BATTLE ROYALE ENDED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Winner info
        if self.winner == "Human":
            winner_text = self.font.render("🎉 YOU WON! 🎉", True, (255, 255, 0))
        elif "eliminated" in self.winner:
            winner_text = self.font.render("💀 YOU WERE ELIMINATED! 💀", True, (255, 0, 0))
        else:
            winner_text = self.font.render(f"Winner: {self.winner}", True, (255, 100, 100))
            
        winner_rect = winner_text.get_rect(center=(self.width // 2, 220))
        self.screen.blit(winner_text, winner_rect)
        
        # Statistics
        stats_y = 290
        stats = [
            f"Survival Time: {minutes:02d}:{seconds:02d}",
            f"Final Survivors: {sum(1 for s in self.snakes if hasattr(s, 'alive') and s.alive)}/25"
        ]
        
        if (self.human_snake_index < len(self.snakes)):
            human_snake = self.snakes[self.human_snake_index]
            if not hasattr(human_snake, 'alive'):
                human_snake.alive = True
                
            if human_snake.alive:
                stats.append(f"Your Final Length: {len(human_snake.body)}")
                stats.append("Status: WINNER!")
            else:
                stats.append("Status: ELIMINATED")
        
        for i, stat in enumerate(stats):
            color = (0, 255, 0) if "WINNER" in stat else (255, 0, 0) if "ELIMINATED" in stat else (255, 255, 255)
            stat_text = self.font.render(stat, True, color)
            stat_rect = stat_text.get_rect(center=(self.width // 2, stats_y + i * 40))
            self.screen.blit(stat_text, stat_rect)
        
        # Control instructions
        controls = [
            "Press R to Play Again",
            "Press Q or ESC to Quit"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, (150, 150, 150))
            control_rect = control_text.get_rect(center=(self.width // 2, stats_y + len(stats) * 40 + 60 + i * 25))
            self.screen.blit(control_text, control_rect)
        
    def restart_game(self):
        """Restart the game"""
        self.game_over = False
        self.winner = None
        self.human_eliminated = False
        self.safe_zone_width = self.width
        self.safe_zone_height = self.height
        self.safe_zone_x = 0
        self.safe_zone_y = 0
        self.shrink_timer = pygame.time.get_ticks()
        self.game_start_time = pygame.time.get_ticks()
        self.init_game()