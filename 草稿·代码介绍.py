import sys       # 模块sys包含玩家退出游戏的功能
import pygame    # 模块pygame包含开发游戏所需的功能

'''
p226-p228
在不引入Settings类时的代码，更容易理解
'''


def run_game():
    pygame.init()                                    # 初始化背景设置
    screen = pygame.display.set_mode((1200, 800))    # 创建一个名为screen的显示窗口：实参(1200, 800)是元组，也是游戏窗口的尺寸
    # 对象screen是一个surface：在Pygame中，surface是屏幕的一部分，用于显示游戏元素
    # 在这个游戏中，每个元素（如外星人或飞船）都是一个surface
    pygame.display.set_caption("Alien Invasion")     # 设置窗口标题为 "Alien Invasion"，玩家游玩时可在窗口的标题栏看到

    bg_color = (200, 230, 255)                       # 以RGB值指定颜色，此时(200, 230, 255)为浅蓝色，(230, 230, 230)为浅灰色

    while True:                                      # 开始游戏主循环
        for event in pygame.event.get():             # 监视键盘和鼠标事件：让程序响应事件
            if event.type == pygame.QUIT:            # 当玩家单击窗口的关闭按钮时，即检测到pygame.QUIT事件
                sys.exit()                           # 此时调用sys.exit()退出游戏，此处的for循环就是一个事件循环

            screen.fill(bg_color)                    # 每次循环时都重绘屏幕背景色，screen.fill()仅接受一个实参

        pygame.display.flip()                        # 不断更新屏幕，展示最新绘制的屏幕，显示元素新位置，隐藏元素老位置，实现平滑效果


run_game()




# 在ship.py更新 （12.6.5 限制飞船的活动范围） 补丁前
def update(self):  # 添加了方法update()，它在前述标志为True时向右移动飞船
    if self.moving_right:  # 如果按下的是右箭头键，就将ship.rect.centerx的值加1，从而将飞船向右移动
        self.center += self.ai_settings.ship_speed_factor  # 更新飞船的center值，而不是rect

    if self.moving_left:  # 这里我们用的是if而不是elif，才能使得左右键一起按时飞船位置不变
        self.center -= self.ai_settings.ship_speed_factor

    self.rect.centerx = self.center  # 根据self.center更新rect对象


# 在game_functions.py更新 （12.6.6 重构 check_events()） 补丁前
def check_events(ship):                             # 响应按键和鼠标事件
    for event in pygame.event.get():                # for循环就是一个事件循环----通过隔离事件循环，可将事件管理与游戏的其他方面分离
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:          # 每当玩家按键时，都将在Pygame中注册为一个KEYDOWN事件
            if event.key == pygame.K_RIGHT:         # 读取属性event.key，以检查按下的是否是右箭头键pygame.K_RIGHT
                ship.moving_right = True            # 当按下右箭头键时，将右移标志改为True
            elif event.key == pygame.K_LEFT:        # 读取属性event.key，以检查按下的是否是左箭头键pygame.K_LEFT
                ship.moving_left = True             # 这里之所以可以使用两个elif代码块，是因为每个事件都只与一个键相关联

        elif event.type == pygame.KEYUP:            # 每当玩家松开按键时，都将在Pygame中注册为一个KEYUP事件
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:        # 玩家松开K_LEFT而触发了KEYUP事件，我们就将moving_left设置为False
                ship.moving_left = False