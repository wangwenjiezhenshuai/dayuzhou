import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """响应关键发布."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """响应按键和鼠标事件."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """当玩家单击“play”时开始新游戏."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置.
        ai_settings.initialize_dynamic_settings()

        # 隐藏鼠标光标.
        pygame.mouse.set_visible(False)

        # 重置游戏统计.
        stats.reset_stats()
        stats.game_active = True

        # 重置记分板图像.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人和子弹的名单.
        aliens.empty()
        bullets.empty()

        # 创建一个新舰队并将船置于中心.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # 创建新项目符号，添加到项目符号组.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """Update images on the screen, and flip to the new screen."""
    # 重新绘制屏幕，每次通过循环.
    screen.fill(ai_settings.bg_color)

    #background = pygame.image.load(r"E:\Alien1\Alien\images\2.bmp")
    #picture = pygame.transform.scale(background, (1200, 800))
    #screen.blit(picture, (0, 0))

    # 重画所有子弹，在飞船和外星人后面.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 绘制分数信息.
    sb.show_score()

    # 如果游戏处于非活动状态，请绘制“play”按钮.
    if not stats.game_active:
        play_button.draw_button()

    # 使最近绘制的屏幕可见.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置，清除旧子弹."""
    # 更新项目符号位置.
    bullets.update()

    # 扔掉已经消失的子弹.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_high_score(stats, sb):
    """看看有没有新的高分."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """检测子弹与外星人的碰撞."""
    # 移除所有的子弹和外星人.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            pygame.mixer.init()

            pygame.mixer.music.load(r"F:\python作业\Alien1\music\3.mp3")

            pygame.mixer.music.play()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 如果整个舰队被摧毁，开始一个新的等级.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """如果有外星人已经到了边缘，要做出适当的反应."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """放下整个舰队，改变舰队的方向."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """回应飞船被外星人击中."""
    if stats.ships_left > 0:
        # 左减.
        stats.ships_left -= 1

        # 更新记分板.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # 清空外星人和子弹的名单.
    aliens.empty()
    bullets.empty()

    # 创建一个新舰队，把船放在中心.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # 暂停.
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                        bullets):
    """检查屏幕底部是否有外星人."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 碰撞检测.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    检查舰队是否在边缘，

    然后更新舰队中所有外星人的位置。
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 寻找外星飞船碰撞.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 寻找撞击屏幕底部的外星人.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """确定排成一排的外星人的数量."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """确定适合屏幕的外星人行数."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人，并将其放置在行中."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创造一个完整的外星人舰队."""
    # 创建一个外星人，并在一行中查找外星人的数量.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创造外星人舰队.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)
