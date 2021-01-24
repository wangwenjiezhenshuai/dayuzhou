import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理从船上发射的子弹的类."""

    def __init__(self, ai_settings, screen, ship):
        """在船的当前位置创建一个项目符号对象."""
        super(Bullet, self).__init__()
        self.screen = screen

        # 在（0，0）处创建项目符号矩形，然后设置正确的位置.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # 存储项目符号位置的十进制值.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """把子弹移到屏幕上."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """把子弹拉到屏幕上."""
        pygame.draw.rect(self.screen, self.color, self.rect)
