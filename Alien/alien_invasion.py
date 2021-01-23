import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 设置play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一个实例来存储游戏统计数据和记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 设置背景颜色
    bg_color = (230, 230, 230)

    background = pygame.image.load(r"F:\python学习\Alien\images\beijing.bmp").convert()

    # 设置一艘船，一组子弹，还有一群外星人
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    pygame.mixer.init()

    pygame.mixer.music.load(r"F:\python学习\Alien\sound\game_music.ogg")

    pygame.mixer.music.play()

    # 创造外星人舰队
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, play_button)



run_game()
