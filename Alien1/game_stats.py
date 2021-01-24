class GameStats():
    """外星入侵跟踪统计."""
    
    def __init__(self, ai_settings):
        """初始化统计信息."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # 在非活动状态下开始游戏.
        self.game_active = False
        
        # 在非活动状态下开始游戏高分不应重置.
        self.high_score = 0
        
    def reset_stats(self):
        """初始化可以在游戏中更改的统计信息."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
