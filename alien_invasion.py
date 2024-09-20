import pygame                                        # 模块pygame包含开发游戏所需的功能
from settings import Settings                        # 从 settings.py 中引入 Settings类
from ship import Ship                                # 从   ship.py   中引入   Ship类
import game_functions as gf                          # 导入 game_functions 模块并指定为别名gf
from pygame.sprite import Group                      # 从 pygame.sprite 中引入 Group类
from alien import Alien                              # 从  alien.py   中引入   Alien类
from game_stats import GameStats


def run_game():
    pygame.init()                                    # 初始化背景设置
    ai_settings = Settings()                         # 将ai_settings创建为Settings类的实例
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))   # 创建一个名为screen的显示窗口,尺寸来自于ai_settings实例中
    pygame.display.set_caption("Alien Invasion")     # 设置窗口标题为 "Alien Invasion"，玩家游玩时可在窗口的标题栏看到
    stats = GameStats(ai_settings)                   # 创建一个用于存储游戏统计信息的实例

    ship = Ship(ai_settings, screen)                 # 创建一个Ship类的实例，赋值给ship----在while后面，避免每次循环创建一个ship

    alien = Alien(ai_settings, screen)               # 在进入主while循环前创建了一个Alien实例 alien

    bullets = Group()                                # 创建一个用于存储子弹的编组，即一个Group实例，命名为bullets

    aliens = Group()                                 # 创建了一个空编组，用于存储所有的外星人

    gf.create_fleet(ai_settings, screen, ship, aliens)     # 创建外星人群

    while True:                                      # 开始游戏主循环
        gf.check_events(ai_settings, screen, ship, bullets)
        if stats.game_active:
            ship.update()                                # 引入ship.update()模块
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)  # 更新所有未消失的子弹的位置
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)  # 在更新子弹后再更新外星人的位置，因为要检查是否有子弹撞到了外星人
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)  # def后·刷新屏幕


run_game()