import pygame
import sys
import os
from game import Game
from dual_game import DualGame
from battle_royale import BattleRoyaleGame

class LanguageManager:
    def __init__(self):
        self.current_language = "en"  # 默认英文
        self.texts = {
            "en": {
                "title": "Snake Game",
                "single_ai": "1 - Single Player (AI)",
                "single_manual": "2 - Single Player (Manual)",
                "dual_mode": "3 - Dual Mode (AI vs Human)",
                "battle_royale": "4 - Battle Royale (25 Snakes)",
                "quit": "Q - Quit",
                "click_flag": "Click flag to change language"
            },
            "zh": {
                "title": "贪吃蛇游戏",
                "single_ai": "1 - 单人模式 (AI)",
                "single_manual": "2 - 单人模式 (手动)",
                "dual_mode": "3 - 双人模式 (AI vs 人类)",
                "battle_royale": "4 - 大逃杀模式 (25条蛇)",
                "quit": "Q - 退出",
                "click_flag": "点击国旗切换语言"
            }
        }
        
        # 国旗位置和大小
        self.flag_rect = pygame.Rect(20, 20, 60, 40)
        
    def get_text(self, key):
        return self.texts[self.current_language].get(key, key)
    
    def toggle_language(self):
        self.current_language = "zh" if self.current_language == "en" else "en"
    
    def get_font(self, size):
        """根据当前语言获取合适的字体"""
        if self.current_language == "zh":
            # 中文字体
            font_paths = [
                "C:/Windows/Fonts/simhei.ttf",      # 黑体
                "C:/Windows/Fonts/msyh.ttc",        # 微软雅黑
                "C:/Windows/Fonts/simsun.ttc",      # 宋体
            ]
            
            for font_path in font_paths:
                try:
                    if os.path.exists(font_path):
                        return pygame.font.Font(font_path, size)
                except:
                    continue
        
        # 英文字体或中文字体加载失败时使用默认字体
        return pygame.font.Font(None, size)
    
    def draw_flag(self, screen):
        """绘制国旗"""
        # 绘制国旗背景
        pygame.draw.rect(screen, (255, 255, 255), self.flag_rect)
        pygame.draw.rect(screen, (100, 100, 100), self.flag_rect, 2)
        
        if self.current_language == "en":
            # 绘制英国国旗 (简化版)
            # 蓝色背景
            pygame.draw.rect(screen, (0, 0, 150), self.flag_rect)
            
            # 白色十字
            pygame.draw.line(screen, (255, 255, 255), 
                           (self.flag_rect.left, self.flag_rect.centery),
                           (self.flag_rect.right, self.flag_rect.centery), 8)
            pygame.draw.line(screen, (255, 255, 255),
                           (self.flag_rect.centerx, self.flag_rect.top),
                           (self.flag_rect.centerx, self.flag_rect.bottom), 8)
            
            # 红色十字
            pygame.draw.line(screen, (200, 0, 0),
                           (self.flag_rect.left, self.flag_rect.centery),
                           (self.flag_rect.right, self.flag_rect.centery), 4)
            pygame.draw.line(screen, (200, 0, 0),
                           (self.flag_rect.centerx, self.flag_rect.top),
                           (self.flag_rect.centerx, self.flag_rect.bottom), 4)
        else:
            # 绘制中国国旗 (简化版)
            # 红色背景
            pygame.draw.rect(screen, (200, 0, 0), self.flag_rect)
            
            # 大星星
            star_center = (self.flag_rect.left + 15, self.flag_rect.top + 12)
            self.draw_star(screen, star_center, 6, (255, 255, 0))
            
            # 小星星
            small_stars = [
                (self.flag_rect.left + 25, self.flag_rect.top + 8),
                (self.flag_rect.left + 30, self.flag_rect.top + 12),
                (self.flag_rect.left + 30, self.flag_rect.top + 18),
                (self.flag_rect.left + 25, self.flag_rect.top + 22)
            ]
            for star_pos in small_stars:
                self.draw_star(screen, star_pos, 3, (255, 255, 0))
        
        # 绘制边框
        pygame.draw.rect(screen, (0, 0, 0), self.flag_rect, 2)
    
    def draw_star(self, screen, center, size, color):
        """绘制五角星"""
        # 简化的星星绘制
        points = []
        for i in range(5):
            angle = i * 72 - 90  # 从顶部开始
            x = center[0] + size * pygame.math.Vector2(1, 0).rotate(angle).x
            y = center[1] + size * pygame.math.Vector2(1, 0).rotate(angle).y
            points.append((x, y))
        
        if len(points) >= 3:
            pygame.draw.polygon(screen, color, points)
    
    def handle_click(self, pos):
        """处理点击事件"""
        if self.flag_rect.collidepoint(pos):
            self.toggle_language()
            return True
        return False

def show_menu(screen, lang_manager):
    """显示游戏模式选择菜单"""
    
    while True:
        screen.fill((0, 0, 0))
        
        # 绘制国旗
        lang_manager.draw_flag(screen)
        
        # 绘制语言提示
        hint_font = lang_manager.get_font(18)
        hint_text = hint_font.render(lang_manager.get_text("click_flag"), True, (150, 150, 150))
        screen.blit(hint_text, (100, 30))
        
        # 标题
        title_font = lang_manager.get_font(48)
        title = title_font.render(lang_manager.get_text("title"), True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 120))
        screen.blit(title, title_rect)
        
        # 模式选项
        option_font = lang_manager.get_font(28)
        options = [
            lang_manager.get_text("single_ai"),
            lang_manager.get_text("single_manual"),
            lang_manager.get_text("dual_mode"),
            lang_manager.get_text("battle_royale"),
            lang_manager.get_text("quit")
        ]
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == 3 else (200, 200, 200)  # 大逃杀模式高亮
            option_text = option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(screen.get_width() // 2, 200 + i * 45))
            screen.blit(option_text, option_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    if lang_manager.handle_click(event.pos):
                        # 语言切换后重新绘制
                        continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "single_ai"
                elif event.key == pygame.K_2:
                    return "single_manual"
                elif event.key == pygame.K_3:
                    return "dual"
                elif event.key == pygame.K_4:
                    return "battle_royale"
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return None

def main():
    pygame.init()
    
    # 创建游戏屏幕
    screen = pygame.display.set_mode((1200, 700))  # 加大屏幕以适应大逃杀模式
    pygame.display.set_caption("Snake Game - Multi Mode")
    
    # 创建语言管理器
    lang_manager = LanguageManager()
    
    while True:
        mode = show_menu(screen, lang_manager)
        
        if mode is None:
            break
        elif mode == "single_ai":
            game = Game(screen, ai_mode=True)
            game.run()
        elif mode == "single_manual":
            game = Game(screen, ai_mode=False)
            game.run()
        elif mode == "dual":
            dual_game = DualGame(screen)
            dual_game.run()
        elif mode == "battle_royale":
            battle_royale = BattleRoyaleGame(screen)
            battle_royale.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()