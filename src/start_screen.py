import sys
import pygame
import constant
from button import Button

class StartScreen:
    # background_image_path: 背景图片路径，如果为None则使用纯黑色背景
    def __init__(self, background_image_path='../images/background/start_screen.png'):
        pygame.font.init()
        # 设置窗口和标题
        self.screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))

        # 设置背景
        self.background = self._load_background(background_image_path)

        # 设置按钮
        self.start_button = Button(self.screen, '开始游戏', 1.2, 1.65)
        self.exit_button = Button(self.screen, '退出游戏', 2, 1.65)
        self.select_map = Button(self.screen, '选择关卡', 2.8, 1.65)

    """加载并调整背景图片大小"""
    @staticmethod
    def _load_background(image_path):
        if image_path:
            background = pygame.image.load(image_path)
            background = pygame.transform.scale(background, (constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
            return background
        # 如果无法加载图片或没有提供图片路径，则使用纯黑色背景
        return pygame.Surface((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))

    def game_guide(self):
        pygame.font.init()
        text_content = 'WASD键移动，J键射击'
        text_color = (0,191,255)
        text_font = pygame.font.SysFont('SimHei', 50)
        text = text_font.render(text_content, True, text_color, None)
        text_rect = text.get_rect()
        text_rect.center = (constant.SCREEN_WIDTH/2, constant.SCREEN_HEIGHT/2 + 325)
        self.screen.blit(text, text_rect)

    """运行菜单循环，直到用户选择开始游戏或关闭窗口"""
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                constant.stop_game()
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:#检测鼠标点击事件
                mouse_x,mouse_y=pygame.mouse.get_pos() #get_pos()返回一个单击时鼠标的xy坐标
                if self.start_button.rect.collidepoint(mouse_x, mouse_y):
                    constant.games_init()
                    constant.game_start(1)
                elif self.exit_button.rect.collidepoint(mouse_x,mouse_y):
                    constant.stop_game()
                elif self.select_map.rect.collidepoint(mouse_x,mouse_y):
                    constant.switch_to_selectscreen()
        key = pygame.key.get_pressed()
        if key[pygame.K_CAPSLOCK] and key[pygame.K_ESCAPE]:
            constant.stop_game()
        # 绘制界面
        self.render()

    """绘制菜单界面"""
    def render(self):
        # 绘制背景
        self.screen.blit(self.background, (0, 0))
        self.game_guide()
        # 绘制按钮
        self.start_button.draw_button()
        self.exit_button.draw_button()
        self.select_map.draw_button()
