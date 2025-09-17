import pygame
import random
import audio_player
import bullet
from pygame import sprite
from constant import SCREEN_WIDTH, SCREEN_HEIGHT


class EnemyTank(sprite.Sprite):
    def __init__(self, x, y, player, home):
        super().__init__()
        self.image = pygame.image.load('../images/enemy/enemy1U.gif')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

        # 基本属性
        self.speed = {
            'U':(0,-5),
            'D':(0,5),
            'L':(-5,0),
            'R':(5,0)
        }
        self.rank = random.choice([1, 2])  # 随机坦克类型
        self.health = 1 if self.rank == 1 else 2
        self.direction = random.choice(['U', 'D', 'L', 'R'])  # 初始方向

        # 武器属性
        self.fire_rate = 1000 if self.rank == 1 else 800  # 射击间隔(毫秒)
        self.last_bullet = pygame.time.get_ticks()
        self.bullet_speed = 5 if self.rank == 1 else 10  # 子弹速度

        # 碰撞检测相关
        self.obstacle_group = None
        self.river_group = None
        self.bullet_group = None
        self.explosion_group = None
        self.forest_group = None
        self.step = 50
        self.stop_times = 10

        self.audio_fire = audio_player.AudioPlayer()
        self.audio_boom = audio_player.AudioPlayer()

    # 设置碰撞检测所需的精灵组"""
    def set_groups(self, obstacle_group, river_group, bullet_group, explosion_group, forest_group):
        self.obstacle_group = obstacle_group
        self.river_group = river_group
        self.bullet_group = bullet_group
        self.explosion_group = explosion_group
        self.forest_group = forest_group

    def move(self, players):
        old_x = self.rect.x
        old_y = self.rect.y
        v_x = self.speed[self.direction][0]
        v_y = self.speed[self.direction][1]
        self.reload_img()
        self.rect.move_ip(v_x, v_y)
        if (sprite.spritecollideany(self, self.obstacle_group) or
            sprite.spritecollideany(self, self.river_group) or
            sprite.spritecollideany(self, players)):
            self.rect.x = old_x-(v_x/abs(v_x))*0.01 if v_x!=0 else old_x
            self.rect.y = old_y-(v_y/abs(v_y))*0.01 if v_y!=0 else old_y
            self.stop_times += 1
            # print(self.stop_times)
        elif (self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or
            self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT):
            self.rect.x, self.rect.y = old_x, old_y
            self.stop_times += 5

    def isCease(self):
        if self.stop_times >= 10:
            self.stop_times = 0
            return True
        else:
            return False

    def reload_img(self):
        self.image = pygame.image.load(f'../images/enemy/enemy{self.rank}{self.direction}.gif')
        self.image = pygame.transform.scale(self.image, (50, 50))

    # 发射
    def shoot(self, obstacles, bullets, explosions, walls):
        current_time = pygame.time.get_ticks()
        for explosion_ in explosions:
            explosion_.explode()
        for bullet_ in bullets:
            bullet_.flight(obstacles, walls)
            if bullet_.isCollide(group=obstacles):
                new_explosion = bullet.BulletBoom(bullet_.rect.center)
                explosions.add(new_explosion)
        if current_time - self.last_bullet >= self.fire_rate:
            self.last_bullet = current_time
            new_bullet = bullet.Bullet(self.rect.center, 1, self.direction, self.bullet_speed)
            bullets.add(new_bullet)
            self.audio_fire.play('../musics/fire.wav')

    def damage(self, bullets, player):
        if self.health <= 0:
            self.kill()
            player.kill_num += 1
            return True
        for bullet_ in bullets:
            if self.rect.colliderect(bullet_.rect) and bullet_.tag == 0 and self.health > 0:
                print('攻击敌人')
                self.audio_boom.play('../musics/boom.wav')
                self.health -= 1
                bullet_.kill()
        return False

    def update(self, obstacles, bullets, explosions, walls, player, players):
        self.damage(bullets, player)
        if self.step <= 0:
            self.direction = random.choice(['U', 'D', 'L', 'R'])
            self.step = 50
        elif self.isCease():
            self.direction = random.choice(['U', 'D', 'L', 'R'])
            self.stop_times = 0
        else:
            self.move(players)
            self.step -= 1
        self.shoot(obstacles, bullets, explosions, walls)