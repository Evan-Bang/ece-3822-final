from draw_page import *
from game_instance_manager import *
from python_server_handler import *
import pygame
from settings import *
class Client:
    def __init__(self, screen, port):
        self.screen = screen
        self.server_handler = ServerHandler(port)
        self.game_manager = GameInstanceManager()
        self.current_page = DrawLoginPage(screen) 

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    client = Client(screen, SERVER_PORT)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            client.current_page.handle_event(event)
        client.current_page.draw(screen)
        pygame.display.flip()
    pygame.quit()