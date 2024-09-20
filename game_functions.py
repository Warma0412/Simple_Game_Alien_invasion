import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

# (1)首先把管理事件的代码移到一个名为check_events()的函数中，以简化run_game()并隔离事件管理循环
# (3)修改check_events()，每次按键都被注册为一个KEYDOWN事件，我们指定要检查哪些类型的事件
# (4)修改check_events()，使其在玩家按下右箭头键时将moving_right设置为True，并在玩家松开时将moving_right设置为False
# (5)修改check_events()，飞船能够不断地向右移动后，添加向左移动的逻辑很容易。我们将再次修改Ship类和函数check_events()
# (6)需要修改check_keydown_events()，以便在玩家按空格键时发射一颗子弹。无需修改check_keyup_events()，因为玩家松开空格键时什么都不会发生
# (7)要绘制一群外星人，需要确定一行能容纳多少个外星人以及要绘制多少行外星人。我们将首先计算外星人之间的水平间距，并创建一行外星人，再确定可用的垂直空间，并创建整群外星人


def check_keydown_events(event, ai_settings, screen, ship, bullets):  # 响应按键
    if event.key == pygame.K_RIGHT:                # 读取属性event.key，以检查按下的是否是右箭头键pygame.K_RIGHT
        ship.moving_right = True                   # 当按下右箭头键时，将右移标志改为True
    elif event.key == pygame.K_LEFT:               # 读取属性event.key，以检查按下的是否是左箭头键pygame.K_LEFT
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:              # 当按下空格键时，开火
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:                  # 当按下q键时，退出游戏
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):    # 将发射子弹的代码移到一个独立的函数fire_bullet()中
    if len(bullets) < ai_settings.bullets_allowed:      # 玩家按空格键时，我们检查bullets的长度,使子弹存在的数量不超过上限
        new_bullet = Bullet(ai_settings, screen, ship)  # 玩家按空格键时，创建一颗新子弹
        bullets.add(new_bullet)                         # 使用方法add()将其加入到编组bullets中


def check_keyup_events(event, ship):               # 响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:               # 玩家松开K_LEFT而触发了KEYUP事件，我们就将moving_left设置为False
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):  # 响应按键和鼠标事件
    for event in pygame.event.get():                # for循环就是一个事件循环----通过隔离事件循环，可将事件管理与游戏的其他方面分离
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:          # 每当玩家按键时，都将在Pygame中注册为一个KEYDOWN事件
            check_keydown_events(event, ai_settings, screen, ship, bullets)  # 这里之所以可以使用两个elif代码块，是因为每个事件都只与一个键相关联

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


# (2)为进一步简化run_game()，下面将更新屏幕的代码移到一个名为update_screen()的函数中
def update_screen(ai_settings, screen, ship, aliens, bullets):  # 更新屏幕上的图像，并切换到新屏幕
    screen.fill(ai_settings.bg_color)               # 重绘屏幕背景色

    for bullet in bullets.sprites():                # 方法bullets.sprites()返回一个列表，其中包含编组bullets中的所有精灵
        bullet.draw_bullet()                        # 为在屏幕上绘制发射的所有子弹，我们遍历编组bullets中的精灵，并对每个精灵都调用draw_bullet()

    ship.blitme()                                   # 利用方法blitme()将ship放在屏幕指定初始位置
    aliens.draw(screen)                             # 在屏幕上绘制编组中的每个外星人

    pygame.display.flip()                           # 让最近绘制的屏幕可见


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()  # 当你对编组调用update()时，编组将自动对其中的每个精灵调用update()
    # 检查是否有子弹击中了外星人，如果是这样，就删除相应的子弹

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):  # 响应子弹和外星人的碰撞
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:                             # 删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

    print(len(bullets))  # 用于在终端窗口检查子弹是否会消失
    # 在Python中，直接在for循环中遍历并修改列表可能会导致错误或意外的行为，因为迭代器可能会因为列表长度的变化而变得混乱。
    #           使用bullets.copy()创建了一个列表的副本，这样在循环中修改原始列表时不会影响循环的进行


def get_number_aliens_x(ai_settings, alien_width):   # 计算每行可容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # 需要在屏幕两边都留下一定的边距，把它设置为外星人的宽度
    number_aliens_x = int(available_space_x / (2 * alien_width))
    # 为确定一行可容纳多少个外星人，我们将可用空间除以外星人宽度的两倍----使用了int()来确保计算得到的外星人数量为整数
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):  # 计算屏幕可容纳多少行外星人
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):  # 创建一个外星人并将其放在当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number  # 将每个外星人都往右推一个外星人的宽度
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):  # 创建外星人群
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)  # 创建一个外星人，并计算每行可容纳多少个外星人
    number_rows = get_number_rows(ai_settings, ship.rect.height,alien.rect.height)

    for row_number in range(number_rows):  # 创建外星人群
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)


def check_fleet_edges(ai_settings, aliens):          # 有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):  # 响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1                            # 将ships_left减1
        aliens.empty()                                   # 清空外星人列表和子弹列表
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)  # 创建一群新的外星人，并将飞船放到屏幕底端中央
        ship.center_ship()
        sleep(0.5)                                       # 暂停
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):   # 检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:  # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):   # 检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):  # 检测外星人和飞船之间的碰撞
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)  # 检查是否有外星人到达屏幕底端