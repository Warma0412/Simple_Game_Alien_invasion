class Settings:                            # 存储《外星人入侵》的所有设置的类

    def __init__(self):                    # 初始化游戏的设置
        self.screen_width = 1500           # 设置屏幕宽度
        self.screen_height = 800           # 设置屏幕高度
        self.bg_color = (230, 230, 230)    # 设置背景颜色

        self.ship_speed_factor = 3         # 初始速度为3（但rect的centerx属性只能储存整数值，因此还得对ship.py进行修改）
        self.ship_limit = 3

        self.bullet_speed_factor = 3       # 创建子弹bullet的设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 0, 0, 255
        self.bullets_allowed = 30          # 这将未消失的子弹数限制为3颗

        self.alien_speed_factor = 1

        self.fleet_drop_speed = 10
        self.fleet_direction = 1           # fleet_direction为1表示向右移，为-1表示向左移