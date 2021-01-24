import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船，并设置它的起始位置."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像，并获取其矩形.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 在屏幕底部中心开始每艘新船.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.rect.bottom = self.screen_rect.bottom

        # 存储船中心的十进制值.
        self.center = float(self.rect.centerx)

        # 移动标志.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.screen_top = self.rect.top

    def center_ship(self):
        """把船放在屏幕中央."""
        self.center = self.screen_rect.centerx

    def update(self):
        """根据移动标志更新船的位置."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.rect.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.top < self.screen_top:
            self.rect.centery += self.ai_settings.ship_speed_factor

        # 更新对象中心.
        self.rect.centerx = self.center


    def blitme(self):
        """把船拖到当前位置."""
        self.screen.blit(self.image, self.rect)
