import pygame
from numpy.testing.overrides import allows_array_ufunc_override

import audio_player
import bullet
from pygame import sprite
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, success_or_fail

last_time = pygame.time.get_ticks()

class Hero(sprite.Sprite):
    def __init__(self, home):
        super().__init__()

        self.rank = 1   #等级
        self.last_bullet = pygame.time.get_ticks()
        self.face_direction = 'U'   #朝向：'U','D','L','R'
        self.fire_rate = 500  #攻击频率
        self.health = 1    #生命值
        self.bullet_speed = 4 * self.rank + 1
        self.kill_num = 0   #击杀数

        self.audio_fire = audio_player.AudioPlayer() #音频播放
        self.audio_boom = audio_player.AudioPlayer() #音频播放

        self.image = pygame.image.load(f'../images/hero/hero1{self.face_direction}.gif')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.home= pygame.Rect(home[0], home[1], 50, 50)
        self.rect.center = self.home.center
        self.rest_tanks = 3 #剩余支援坦克数

    #移动
    def move(self, obstacles, river, face_d, v_x, v_y, enemys):
        old_x = self.rect.x
        old_y = self.rect.y
        self.face_direction = face_d
        self.reload_image()
        self.rect.move_ip(v_x, v_y)
        if (sprite.spritecollideany(self, obstacles) or
                sprite.spritecollideany(self, river) or
                sprite.spritecollideany(self, enemys)):
            self.rect.x = old_x - (v_x/abs(v_x))*0.01 if v_x != 0 else old_x
            self.rect.y = old_y - (v_y/abs(v_y))*0.01 if v_y != 0 else old_y
            # print('发生碰撞')
        elif (self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or
                self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT):
            self.rect.x, self.rect.y = old_x, old_y
            # print('遇到边界')

    #处理输入
    def handle_input(self, obstacles, river, enemys):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(obstacles=obstacles, river=river, face_d='U', v_x=0, v_y=-5, enemys=enemys)
        if keys[pygame.K_s]:
            self.move(obstacles=obstacles, river=river, face_d='D', v_x=0, v_y=5, enemys=enemys)
        if keys[pygame.K_a]:
            self.move(obstacles=obstacles, river=river, face_d='L', v_x=-5, v_y=0, enemys=enemys)
        if keys[pygame.K_d]:
            self.move(obstacles=obstacles, river=river, face_d='R', v_x=5, v_y=0, enemys=enemys)

    #射击
    def shoot(self, obstacles, bullets, explosions, walls):
        key = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        for explosion_ in explosions:
            explosion_.explode()
        for bullet_ in bullets:
            bullet_.flight(obstacles, walls)
            if bullet_.isCollide(group=obstacles):
                new_explosion = bullet.BulletBoom(bullet_.rect.center)
                explosions.add(new_explosion)
        if current_time - self.last_bullet >= self.fire_rate:
            if key[pygame.K_j]:
                self.last_bullet = current_time
                new_bullet = bullet.Bullet(self.rect.center, 0, self.face_direction, self.bullet_speed)
                bullets.add(new_bullet)
                self.audio_fire.play('../musics/fire.wav')

    #复活
    def revive(self):
        self.rect.center = self.home.center
        print('复活')
        self.reload_image()

    #重载图片
    def reload_image(self):
        self.image = pygame.image.load(f'../images/hero/hero1{self.face_direction}.gif')
        self.image = pygame.transform.scale(self.image, (50, 50))

    #受伤
    def damage(self, bullets):
        if self.rest_tanks <= 0:
            success_or_fail('failure')
        elif self.health <= 0 < self.rest_tanks:
            self.rest_tanks -= 1
            self.health = self.rank
            self.rank = 1
            self.kill_num = 0
            self.rect.center = self.home.center
            self.reload_image()
            # print('复活 ')
        else:
            for bullet_ in bullets:
                if self.rect.colliderect(bullet_.rect) and bullet_.tag == 1 and self.health > 0:
                    # print('受到伤害')
                    self.audio_boom.play('../musics/boom.wav')
                    self.health -= 1
                    bullet_.kill()
    #升级
    def upgrade(self):
        # print(f'连续击杀{self.kill_num}个')
        if self.kill_num >= 2 and self.rank < 3:
            self.kill_num = 0
            self.rank += 1
            self.health = self.rank
            self.bullet_speed = 4 * self.rank + 1
            print(f'升级,当前{self.rank}级,{self.health}点生命值')
        elif self.kill_num >= 2 and self.rank >= 3:
            pass
            # print('已经满级了')

    #更新状态
    def update(self, obstacles, bullets, explosions, river, walls, home, enemys):
        self.upgrade()
        self.damage(bullets)
        self.handle_input(obstacles, river, enemys)
        self.shoot(obstacles, bullets, explosions, walls)
