import pygame
import sys
pygame.init()
from settings import *
# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Arcade Login")

FONT = pygame.font.Font(None, 32)
BIG_FONT = pygame.font.Font(None, 48)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
class PageManager:
    def __init__(self):
        self.current_page = None
    def set_page(self, page):
        self.current_page = page
    def draw(self, screen):
        if self.current_page:
            self.current_page.draw(screen)
class DrawLoginPage:
    def __init__(self, screen):
        self.screen = screen

        # Input boxes
        self.username_rect = pygame.Rect(300, 200, 200, 40)
        self.password_rect = pygame.Rect(300, 260, 200, 40)

        self.active_box = None
        self.username_text = ''
        self.password_text = ''

        # Buttons
        self.login_button = pygame.Rect(300, 330, 200, 40)
        self.create_button = pygame.Rect(300, 380, 200, 40)

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        self.screen.blit(textobj, textrect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_rect.collidepoint(event.pos):
                self.active_box = 'username'
            elif self.password_rect.collidepoint(event.pos):
                self.active_box = 'password'
            else:
                self.active_box = None

            if self.login_button.collidepoint(event.pos):
                print("Login clicked")
                print("Username:", self.username_text)
                print("Password:", self.password_text)

            if self.create_button.collidepoint(event.pos):
                print("Go to create account page")

        if event.type == pygame.KEYDOWN:
            if self.active_box == 'username':
                if event.key == pygame.K_BACKSPACE:
                    self.username_text = self.username_text[:-1]
                else:
                    self.username_text += event.unicode

            elif self.active_box == 'password':
                if event.key == pygame.K_BACKSPACE:
                    self.password_text = self.password_text[:-1]
                else:
                    self.password_text += event.unicode

    def draw(self):
        self.screen.fill(WHITE)

        # Title
        self.draw_text("Virtual Arcade", BIG_FONT, BLACK, WIDTH // 2, 100)

        # Labels
        self.draw_text("Username:", FONT, BLACK, 200, 220)
        self.draw_text("Password:", FONT, BLACK, 200, 280)

        # Draw input boxes
        pygame.draw.rect(self.screen, BLUE if self.active_box == 'username' else GRAY, self.username_rect, 2)
        pygame.draw.rect(self.screen, BLUE if self.active_box == 'password' else GRAY, self.password_rect, 2)

        # Render text
        username_surface = FONT.render(self.username_text, True, BLACK)
        password_surface = FONT.render('*' * len(self.password_text), True, BLACK)

        self.screen.blit(username_surface, (self.username_rect.x + 5, self.username_rect.y + 5))
        self.screen.blit(password_surface, (self.password_rect.x + 5, self.password_rect.y + 5))

        # Draw buttons
        pygame.draw.rect(self.screen, DARK_GRAY, self.login_button)
        pygame.draw.rect(self.screen, DARK_GRAY, self.create_button)

        self.draw_text("Login", FONT, WHITE, self.login_button.centerx, self.login_button.centery)
        self.draw_text("Create Account", FONT, WHITE, self.create_button.centerx, self.create_button.centery)

class DrawCreateAccountPage:
    def __init__(self, screen):
        self.screen = screen
class DrawUserPage:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.logged_in = True
        self.user_data = UserData(username)

class DrawGamePage:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
class DrawMainPage:
    def __init__(self, screen):
        self.screen = screen

