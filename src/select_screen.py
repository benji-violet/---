import sys
import pygame
import constant
from button import Button

class SelectScreen:
    def __init__(self, background_image_path='../images/background/select_screen.png'):
        pygame.font.init()
        # 设置窗口和标题
        self.screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
        self.background = self._load_background(background_image_path)

        # 设置按钮
        self.level1 = Button(self.screen, '1', 0,0.55,(0, 191, 255))
        self.level2 = Button(self.screen, '2', 0,1.65,(0, 191, 255))
        self.level3 = Button(self.screen, '3', 0,2.75,(0, 191, 255))
        self.level4 = Button(self.screen, '4', 1,0.55,(0, 191, 255))
        self.level5 = Button(self.screen, '5', 1,1.65,(0, 191, 255))
        self.level6 = Button(self.screen, '6', 1,2.75,(0, 191, 255))
        self.return_start_button = Button(self.screen, '返回主界面', 2, 1.65,(0, 191, 255))

    """加载并调整背景图片大小"""
    @staticmethod
    def _load_background(image_path):
        if image_path:
            background = pygame.image.load(image_path)
            background = pygame.transform.scale(background, (constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
            return background
        # 如果无法加载图片或没有提供图片路径，则使用纯黑色背景
        return pygame.Surface((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                constant.stop_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 检测鼠标点击事件
                mouse_x, mouse_y = pygame.mouse.get_pos()  # get_pos()返回一个单击时鼠标的xy坐标
                if self.level1.rect.collidepoint(mouse_x, mouse_y):
                    constant.games_init()
                    constant.game_start(1)
                elif self.level2.rect.collidepoint(mouse_x, mouse_y):
                    constant.games_init()
                    constant.game_start(2)
                elif self.level3.rect.collidepoint(mouse_x, mouse_y):
                    constant.games_init()
                    constant.game_start(3)
                elif self.level4.rect.collidepoint(mouse_x, mouse_y):
                    constant.games_init()
                    constant.game_start(4)
                elif self.level5.rect.collidepoint(mouse_x, mouse_y):
                    constant.games_init()
                    constant.game_start(5)
                elif self.level6.rect.collidepoint(mouse_x, mouse_y):
                    constant.games_init()
                    constant.game_start(6)
                elif self.return_start_button.rect.collidepoint(mouse_x, mouse_y):
                    constant.switch_to_startscreen()
        key = pygame.key.get_pressed()
        if key[pygame.K_CAPSLOCK] and key[pygame.K_ESCAPE]:
            constant.stop_game()
        # 绘制界面
        self.render()

    def render(self):
        # 绘制背景
        self.screen.blit(self.background, (0, 0))
        # 绘制按钮
        self.level1.draw_button()
        self.level2.draw_button()
        self.level3.draw_button()
        self.level4.draw_button()
        self.level5.draw_button()
        self.level6.draw_button()
        self.return_start_button.draw_button()
