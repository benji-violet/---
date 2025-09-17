import sys
import pygame
import game_screen
import select_screen
import start_screen
import settlement_screen
import constant

class MainWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
        #游戏界面
        self.game_screen = constant.GAME_SCREEN
        #开始界面
        self.start_screen = constant.START_SCREEN
        self.start = start_screen.StartScreen()
        #结算界面
        self.settlement_screen = constant.SETTLEMENT_SCREEN
        self.settlement = settlement_screen.SettlementScreen()
        #关卡选择界面
        self.select_screen = constant
        self.select = select_screen.SelectScreen()
        #胜负状态
        self.success = constant.SUCCESS
        self.failure = constant.FAILURE
        #游戏运行状态
        self.running = constant.RUNNING
        #设置帧数
        self.clock = pygame.time.Clock()

    def update(self):
        self.running = constant.RUNNING
        self.game_screen = constant.GAME_SCREEN
        self.start_screen = constant.START_SCREEN
        self.settlement_screen = constant.SETTLEMENT_SCREEN
        self.select_screen = constant.SELECT_SCREEN

    def run(self):
        while self.running:
            pygame.init()
            pygame.display.set_caption('坦克大战')
            if self.start_screen:
                self.start.run()
            elif self.select_screen:
                self.select.run()
            elif self.game_screen:
                constant.GAMES[f'level{constant.CURRENT_LEVEL}'].run()
            elif self.settlement_screen:
                self.settlement.run()
            self.update()
            pygame.display.flip()
            self.clock.tick(30)

if __name__ == '__main__':
    mainwindow = MainWindow()
    mainwindow.run()
    pygame.quit()
    sys.exit()

