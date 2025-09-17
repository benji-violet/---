import pygame
import random
import constant
from enemy import EnemyTank
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, success_or_fail

class EnemySpawner:
    # 敌方坦克生成器初始化
    def __init__(self, player, home):

        self.last_spawn_time = None
        self.player = player
        self.home = home

        self.enemies = pygame.sprite.Group()  # 存储所有敌方坦克
        self.max_enemies = 3  # 最大同时存在的敌方数量
        self.min_enemies = 1  # 最小敌方数量
        self.spawn_cooldown = 0  # 生成冷却时间
        self.spawn_interval = 2000  # 生成间隔(毫秒)
        self.spawn_positions = []  # 预设生成位置
        self.total_spawned_enemies = 0  # 已经生成的敌人总数
        self.total_allowed_enemies = 6  # 总共允许生成的敌人数量

        # 初始化生成位置（屏幕边缘随机位置）
        self._init_spawn_positions()

    # 初始化可能的生成位置
    def _init_spawn_positions(self):
        # 屏幕四个边缘的随机位置
        for _ in range(20):  # 预设20个生成位置
            edge = random.choice(['top', 'left', 'right'])
            if edge == 'top':
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = 0  # 顶部
            elif edge == 'left':
                x = 0  # 左侧
                y = random.randint(50, int(SCREEN_HEIGHT / 2))
            elif edge == 'right':
                x = SCREEN_WIDTH - 50  # 右侧
                y = random.randint(50, int(SCREEN_HEIGHT / 2))
            self.spawn_positions.append((x, y))

    # 更新生成器状态，检查是否需要生成新敌人
    def update(self, current_time, obstacles, river, bullets, explosions, forest):
        # 减少生成冷却
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -= current_time - self.last_spawn_time
        # 检查是否需要生成新敌人
        if len(self.enemies) <= self.min_enemies and self.spawn_cooldown <= 0 and self.total_spawned_enemies < self.total_allowed_enemies:
            if self.spawn_enemy(obstacles, river, bullets, explosions, forest):
                self.spawn_cooldown = self.spawn_interval
                self.last_spawn_time = current_time
        elif len(self.enemies) < self.max_enemies and self.total_spawned_enemies < self.total_allowed_enemies:
            # 当敌人数量在最小和最大之间时，随机生成
            if random.random() < 0.01 and self.spawn_cooldown <= 0:
                if self.spawn_enemy(obstacles, river, bullets, explosions, forest):
                    self.spawn_cooldown = self.spawn_interval
                    self.last_spawn_time = current_time
        if len(self.enemies) <= 0:
            success_or_fail('success')
            # print('敌人消灭完毕')

    # 生成新的敌方坦克
    def spawn_enemy(self, obstacles, river, bullets, explosions, forest):
        if len(self.enemies) >= self.max_enemies or self.total_spawned_enemies >= self.total_allowed_enemies:
            return False
        # 随机选择生成位置
        if not self.spawn_positions:
            self._init_spawn_positions()  # 重新初始化生成位置
        spawn_pos = random.choice(self.spawn_positions)
        x, y = spawn_pos
        # 创建敌方坦克
        enemy = EnemyTank(x, y, self.player, self.home)
        enemy.set_groups(obstacles, river, bullets, explosions, forest)
        # 检查生成位置是否与障碍物碰撞
        if not pygame.sprite.spritecollideany(enemy, obstacles):
            self.enemies.add(enemy)
            self.total_spawned_enemies += 1
            return True
        if not pygame.sprite.spritecollideany(enemy, river):
            self.enemies.add(enemy)
            self.total_spawned_enemies += 1
            return True
        return False  # 生成位置无效，放弃生成

    # 绘制所有敌方坦克
    def draw(self, screen):
        self.enemies.draw(screen)

    # 获取所有敌方坦克
    def get_enemies(self):
        return self.enemies