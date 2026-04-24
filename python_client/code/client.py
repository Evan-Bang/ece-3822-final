from draw_page import *
from game_instance_manager import *
from python_server_handler import *
import pygame
from settings import *
class Client:
    def __init__(self, screen):
        self.screen = screen
        self.page_manager = PageManager()
        self.server_handler = ServerHandler()
        self.game_manager = GameInstanceManager()
        self.page_manager.set_page(DrawLoginPage(screen, self.page_manager, self.server_handler))
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    client = Client(screen)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                client.server_handler.disconnect()
            client.page_manager.current_page.handle_event(event)
        client.page_manager.current_page.draw()
        pygame.display.flip()
    pygame.quit()