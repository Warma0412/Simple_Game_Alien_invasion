import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):                               # 定义了一个名为Bullet的类，它继承自Sprite类
    def __init__(self, ai_settings, screen, ship):
        super().__init__()                          # 调用了父类Sprite的构造函数
        self.screen = screen                        # 将传入的screen参数赋值给实例变量self.screen

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx       # 将子弹的centerx设置为飞船的rect.centerx
        self.rect.top = ship.rect.top               # 表示子弹的rect的top属性设置为飞船的rect的top属性，即让子弹从飞船的顶部射出

        self.y = float(self.rect.y)                 # 存储用小数表示的子弹位置

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):                               # 向上移动子弹
        self.y -= self.speed_factor                 # 原点是屏幕的左上角----子弹在屏幕中向上移动，这意味着y坐标将不断减小
        self.rect.y = self.y                        # 更新表示子弹的rect的位置

    def draw_bullet(self):                          # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.color, self.rect)  # 调用draw_bullet()绘制子弹