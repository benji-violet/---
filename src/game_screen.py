import pygame
import map
import tanks
import spawner
import constant

class Game:
    def __init__(self, map_name):
        #初始化
        self.boxIsVisible = False    #是否显示碰撞箱
        self.screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
        #成员组
        self.obstacles = pygame.sprite.Group()  #障碍物
        self.forest = pygame.sprite.Group() #森林
        self.ground = pygame.sprite.Group() #地面
        self.river = pygame.sprite.Group()  #河流
        self.bullets = pygame.sprite.Group()    #子弹
        self.explosions = pygame.sprite.Group() #爆炸效果
        self.walls = pygame.sprite.Group()  #可破坏物
        self.players = pygame.sprite.Group()    #玩家组
        #地图设置
        self.game_map = map.Map(map_name)
        #图片初始化
        self.home = self.game_map.home    #司令部
        self.player = tanks.Hero(self.home)
        self.enemy_spawner = spawner.EnemySpawner(self.player, self.home)
        self.sprite_init()

    #图片初始化
    def sprite_init(self):
        for wall in self.game_map.create_map():
            if wall.tag == 0:
                # print('000000')
                self.ground.add(wall)
            if wall.tag == 1:
                # print('1111111111')
                self.obstacles.add(wall)
                self.walls.add(wall)
            if wall.tag == 2:
                # print('22222222222')
                self.obstacles.add(wall)
            if wall.tag == 3:
                # print('333333333')
                self.forest.add(wall)
            if wall.tag == 4:
                # print('44444444')
                self.river.add(wall)
            if wall.tag == 5:
                # print('okkkkk')
                self.walls.add(wall)
        self.player = tanks.Hero(self.game_map.home)
        self.players.add(self.player)
        self.enemy_spawner = spawner.EnemySpawner(self.player, self.home)

    #更新状态
    def update(self, current_time):
        if not constant.FAILURE:
            self.player.update(self.obstacles, self.bullets, self.explosions, self.river, self.walls, self.home, self.enemy_spawner.get_enemies())
        self.enemy_spawner.update(current_time, self.obstacles, self.river, self.bullets, self.explosions, self.forest)
        for enemy in self.enemy_spawner.get_enemies():
            enemy.update(self.obstacles, self.bullets, self.explosions, self.walls, self.player, self.players)

    #渲染画面
    def render(self):
        self.screen.fill('black')
        self.ground.draw(self.screen)
        self.walls.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.river.draw(self.screen)
        self.bullets.draw(self.screen)
        self.explosions.draw(self.screen)
        if not constant.FAILURE:
            self.screen.blit(self.player.image, self.player.rect)
        self.enemy_spawner.draw(self.screen)
        self.forest.draw(self.screen)
        self.draw_collision_box()
        self.display_player_info()

    #绘制碰撞箱
    def draw_collision_box(self):
        if self.boxIsVisible:
            pygame.draw.rect(self.screen, 'blue', self.player.rect, 2)
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, 'red', obstacle.rect, 2)
            for forest_ in self.forest:
                pygame.draw.rect(self.screen, 'yellow', forest_.rect, 2)
            for river_ in self.river:
                pygame.draw.rect(self.screen, 'green', river_.rect, 2)
            for bullet_ in self.bullets:
                if bullet_.tag == 0:
                    pygame.draw.rect(self.screen, 'blue', bullet_.rect, 1)
                if bullet_.tag == 1:
                    pygame.draw.rect(self.screen, 'gray', bullet_.rect, 2)
            for explosion_ in self.explosions:
                pygame.draw.rect(self.screen, 'purple', explosion_.rect, 2)
            for enemy_ in self.enemy_spawner.get_enemies():
                pygame.draw.rect(self.screen, 'gray', enemy_.rect, 2)

    def victory(self):
        pygame.font.init()
        text_content = '胜利'
        text_color = (255, 255, 255)
        text_font = pygame.font.SysFont('SimHei', 100)
        text = text_font.render(text_content, True, text_color, None)
        text_rect = text.get_rect()
        text_rect.center = (constant.SCREEN_WIDTH/2, constant.SCREEN_HEIGHT/2-25)
        self.screen.blit(text, text_rect)

        t = pygame.font.SysFont('SimHei', 50)
        tt = t.render('   按空格键继续...', True, text_color, None)
        ttt = tt.get_rect()
        ttt.center = (constant.SCREEN_WIDTH/2, constant.SCREEN_HEIGHT/2 + 50)
        self.screen.blit(tt, ttt)

    def lose(self):
        pygame.font.init()
        text_content = '失败'
        text_color = (255, 255, 255)
        text_font = pygame.font.SysFont('SimHei', 100)
        text = text_font.render(text_content, True, text_color, None)
        text_rect = text.get_rect()
        text_rect.center = (constant.SCREEN_WIDTH/2, constant.SCREEN_HEIGHT/2-25)
        self.screen.blit(text, text_rect)

        t = pygame.font.SysFont('SimHei', 50)
        tt = t.render('   按空格键继续...', True, text_color, None)
        ttt = tt.get_rect()
        ttt.center = (constant.SCREEN_WIDTH/2, constant.SCREEN_HEIGHT/2 + 50)
        self.screen.blit(tt, ttt)

    def display_player_info(self):
        pygame.font.init()
        text_color = (255, 255, 255)

        text_font = pygame.font.SysFont('SimHei', 20)
        text = text_font.render(f'坦克剩余耐久度：{self.player.health}', True, text_color, None)
        text_rect = text.get_rect()
        text_rect.topleft = (0, 0)
        self.screen.blit(text, text_rect)

        text2_font = pygame.font.SysFont('SimHei', 20)
        text2 = text2_font.render(f'剩余增援：{self.player.rest_tanks}', True, text_color, None)
        text2_rect = text2.get_rect()
        text2_rect.topleft = (200, 0)
        self.screen.blit(text2, text2_rect)

        text3_font = pygame.font.SysFont('SimHei', 20)
        text3 = text3_font.render(f'当前等级：{self.player.rank}', True, text_color, None)
        text3_rect = text3.get_rect()
        text3_rect.topleft = (340, 0)
        self.screen.blit(text3, text3_rect)

    def run(self):
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                constant.stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.boxIsVisible = not self.boxIsVisible   # 切换碰撞箱显示状态
        key = pygame.key.get_pressed()
        if key[pygame.K_CAPSLOCK] and key[pygame.K_ESCAPE]:
            constant.stop_game()
        self.update(current_time)
        self.render()
        if constant.SUCCESS:
            self.victory()
            pygame.display.flip()
            if key[pygame.K_SPACE]:
                constant.switch_to_settlement()
        elif constant.FAILURE:
            self.lose()
            pygame.display.flip()
            if key[pygame.K_SPACE]:
                constant.switch_to_settlement()