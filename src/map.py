import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, tag, x, y, durability = -1):
        super().__init__()
        self.image = pygame.image.load(f'../images/walls/{tag}.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.tag = tag
        self.durability = 1 if self.tag == 1 or self.tag == 5 else -1

class Map:
    def __init__(self, map_name):
        self.map_name = map_name
        self.home = ()
        self.create_map()

    @staticmethod
    def get_map_file(map_name):
        map_file_name = f"../maps/{map_name}.txt"
        map_info = []
        row = []
        with open(map_file_name, 'r') as file:
            for line in file.readlines():
                for tag in line:
                    if tag != '[' and tag != ']' and tag != ' ' and tag != '\n' and tag != ',':
                        row.append(int(tag))
                map_info.append(row)
                row = []
        return map_info

    def create_map(self):
        walls = []
        map_info = self.get_map_file(self.map_name)
        for i in range(len(map_info) - 1):
            for j in range(len(map_info[0])):
                index = map_info[i][j]
                wall = Wall(tag=index, x=j * 50, y=i * 50)
                walls.append(wall)
                if map_info[i][j] == 5:
                    self.home = (j * 50, i * 50)
        return walls







