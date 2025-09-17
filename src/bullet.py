import pygame
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, success_or_fail
import audio_player


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, tag, direction, speed):
        super().__init__()

        self.damage = 1
        self.direction = direction
        self.images = self.images_init()
        self.image = self.images[self.direction]
        self.rect = self.images[self.direction].get_rect()
        self.rect.center = position
        self.tag = tag    #0为友方子弹 1为敌方子弹
        self.speed = {
            'U':(0, -speed),
            'D':(0, speed),
            'L':(-speed,0),
            'R':(speed,0)
        }
        self.audio = audio_player.AudioPlayer()

    def isCollide(self, group):
        if (self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or
            self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT or
            pygame.sprite.spritecollideany(self, group)):
            return True
        else:
            return False

    def flight(self, obstacles, walls):
        self.rect.move_ip(self.speed[self.direction][0], self.speed[self.direction][1])
        if self.isCollide(obstacles):
            # print('击中墙壁')
            self.kill()
        for wall in walls:
            if self.rect.colliderect(wall) and wall.tag == 5 and self.tag == 1:
                wall.kill()
                self.audio.play('../musics/boom.wav')
                success_or_fail('failure')
            elif self.rect.colliderect(wall) and wall.tag == 1:
                wall.kill()
                self.audio.play('../musics/boom.wav')


    @staticmethod
    def images_init():
        image = pygame.image.load('../images/bullet/bullet.png')
        image = pygame.transform.scale(image, (7, 7))
        images = {'U': image,
                  'D': pygame.transform.rotate(image, angle=180),
                  'L': pygame.transform.rotate(image, angle=90),
                  'R': pygame.transform.rotate(image, angle=-90)}
        return images


class BulletBoom(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('../images/bullet_boom/bomb_3.gif')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.interval = 50
        self.last_explosion = pygame.time.get_ticks()  # 实例属性
        self.frame = 0  # 当前帧
        self.frames = 3  # 总帧数

    def explode(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_explosion >= self.interval:
            if self.frame < self.frames:
                self.image = pygame.image.load(f'../images/bullet_boom/bomb_{self.frames-self.frame}.gif')
                self.image = pygame.transform.scale(self.image, (20,20))
                self.last_explosion = current_time
                self.frame += 1
                # print(f"BOMB BOMB {self.frame}")
            else:
                self.kill()
