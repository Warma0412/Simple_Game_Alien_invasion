import pygame


class Ship:

    def __init__(self, ai_settings, screen):               # Ship的方法__init__()接受三个参数
        self.screen = screen                               # 初始化飞船并设置其初始位置
        self.ai_settings = ai_settings                     # 在形参列表中增加 ai_settings

        self.image = pygame.image.load("images/ship.bmp")  # pygame.image.load()加载图像，该函数返回一个表示飞船的surface
        self.rect = self.image.get_rect()                  # 用get_rect()获取相应surface的属性rect，返回一个表示图像矩形区域的对象
        self.screen_rect = screen.get_rect()               # 将表示屏幕的矩形存储在self.screen_rect中

        self.rect.centerx = self.screen_rect.centerx       # 将初始飞船放在屏幕的中间
        self.rect.bottom = self.screen_rect.bottom         # 将初始飞船放在屏幕的底部

        self.center = float(self.rect.centerx)             # 在飞船的属性center中存储小数值

        self.moving_right = False                          # 添加了属性self.moving_right，并将其初始值设置为False
        self.moving_left = False

    def update(self):                                      # 添加了方法update()，它在前述标志为True时向右移动飞船
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # 如果按下的是右箭头键，且飞船外接矩形的右边缘的x坐标小于屏幕右边缘时，则增加ship.rect.centerx，从而将飞船向右移动
            self.center += self.ai_settings.ship_speed_factor  # 更新飞船的center值，而不是rect

        if self.moving_left and self.rect.left > 0:
            # 这里我们用的是if而不是elif，才能使得左右键一起按时飞船位置不变（飞船外接矩形的左边未触及屏幕边缘时）
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center                    # 根据self.center更新rect对象

    def blitme(self):
        self.screen.blit(self.image, self.rect)            # 定义了方法blitme()，利用.blit()将图像image绘制到屏幕上的指定位置self.rect


    def center_ship(self):                                 # 让飞船在屏幕上居中
        self.center = self.screen_rect.centerx