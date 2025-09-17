import pygame


class AudioPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # 初始化混音器
        self.is_playing = False

    def play(self, file_path, loops=0):
        """非阻塞播放音频"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(loops=loops)
            self.is_playing = True
            return True
        except pygame.error as e:
            print(f"音频加载失败: {e}")
            return False

    def stop(self):
        """停止播放"""
        pygame.mixer.music.stop()
        self.is_playing = False

    def is_busy(self):
        """检查是否在播放"""
        return pygame.mixer.music.get_busy() and self.is_playing