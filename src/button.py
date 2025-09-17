import pygame.font

class Button:
    def __init__(self, screen, msg, order, www = 0, color = (128,128,128)): #msg为要在按钮中显示的文本
        # 初始化按钮的属性
        self.msg_img_rect = None
        self.msg_img = None
        self.screen=screen
        self.screen_rect = screen.get_rect()
        self.msg = msg
        self.width, self.height= 200, 80  # 这种赋值方式很不错
        self.button_color = color  # 设置按钮的rect对象颜色为深蓝
        self.text_color = (0,0,0)  # 设置文本的颜色为白色
        self.font = pygame.font.SysFont('SimHei',40)     #设置文本为黑体，字号为40

        self.rect=pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center   #创建按钮的rect对象，并使其居中
        self.rect.topleft=(20 + 210 * www, 250 + 120 * order)

        self.deal_msg(msg)  #渲染图像

    # 将msg渲染为图像，并将其在按钮上居中
    def deal_msg(self, msg):
        self.msg_img = self.font.render(msg,True, self.text_color, self.button_color) #render将存储在msg的文本转换为图像
        self.msg_img_rect = self.msg_img.get_rect()  #根据文本图像创建一个rect
        self.msg_img_rect.center = self.rect.center  #将该rect的center属性设置为按钮的center属性

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)  #填充颜色
        self.screen.blit(self.msg_img, self.msg_img_rect) #将该图像绘制到屏幕
        pygame.draw.rect(self.screen, (0,0,0), self.rect, 3)
