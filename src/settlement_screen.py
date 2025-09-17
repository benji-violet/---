import sys
import pygame
import constant
from button import Button

class SettlementScreen:
    def __init__(self, background_image_path='../images/background/settlement_screen.png'):
        pygame.font.init()
        # 设置窗口和标题
        self.screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
        self.background = self._load_background(background_image_path)

        # 设置按钮
        self.next_level_button = Button(self.screen, '下一关', 0, 1.65)
        self.return_start_button = Button(self.screen, '回到主界面', 0.7, 1.65)
        self.exit_button = Button(self.screen, '退出游戏', 1.4, 1.65)

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
                if self.next_level_button.rect.collidepoint(mouse_x, mouse_y):
                    constant.next_level()
                    constant.game_start(constant.CURRENT_LEVEL)
                elif self.return_start_button.rect.collidepoint(mouse_x, mouse_y):
                    constant.switch_to_startscreen()
                elif self.exit_button.rect.collidepoint(mouse_x, mouse_y):
                    constant.stop_game()
        key = pygame.key.get_pressed()
        if key[pygame.K_CAPSLOCK] and key[pygame.K_ESCAPE]:
            constant.stop_game()
        # 绘制界面
        self.render()

    def congratulation(self):
        pygame.font.init()
        text_content = '恭喜你！'
        text_color = (255,215,0)
        text_font = pygame.font.SysFont('SimHei', 100)
        text = text_font.render(text_content, True, text_color, None)
        text_rect = text.get_rect()
        text_rect.center = (constant.SCREEN_WIDTH/2, constant.SCREEN_HEIGHT/2-185)
        self.screen.blit(text, text_rect)
        t = pygame.font.SysFont('SimHei', 80)
        tt = t.render('已经通过所有关卡！', True, text_color, None)
        ttt = tt.get_rect()
        ttt.center = (constant.SCREEN_WIDTH/2, constant.SCREEN_HEIGHT/2-100)
        self.screen.blit(tt, ttt)

    def render(self):
        # 绘制背景
        self.screen.blit(self.background, (0, 0))
        # 绘制按钮
        self.return_start_button.draw_button()
        self.exit_button.draw_button()
        if constant.CURRENT_LEVEL == constant.TOTAL_LEVEL:
            self.congratulation()
        if constant.CURRENT_LEVEL < constant.TOTAL_LEVEL and not constant.FAILURE:
            self.next_level_button.draw_button()
