import pygame
import sys
pygame.init()
from settings import *
from python_server_handler import *
import os
from game_instance_manager import *
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from datastructures.array import ArrayList
def draw_glow_rect(surface, rect, color, glow_color):
    for i in range(8, 0, -2):
        glow_rect = rect.inflate(i*2, i*2)
        pygame.draw.rect(surface, glow_color, glow_rect, border_radius=8)
    pygame.draw.rect(surface, color, rect, border_radius=8)

def draw_stars(screen):
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, (100, 100, 255), (x, y), 1)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Arcade Login")

class PageManager:
    def __init__(self):
        self.current_page = None
    def set_page(self, page):
        self.current_page = page
    def draw(self, screen):
        if self.current_page:
            self.current_page.draw(screen)

class DrawLoginPage:
    def __init__(self, screen, page_manager, handler):
        self.screen = screen
        self.page_manager = page_manager
        self.handler = handler
        self.username_rect = pygame.Rect(300, 200, 200, 40)
        self.password_rect = pygame.Rect(300, 260, 200, 40)

        self.active_box = None
        self.username_text = ''
        self.password_text = ''

        self.login_button = pygame.Rect(300, 330, 200, 40)
        self.create_button = pygame.Rect(300, 380, 200, 40)

    def draw_text(self, text, font, color, x, y, glow=False):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))

        if glow:
            glow_surf = font.render(text, True, NEON_BLUE)
            for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                self.screen.blit(glow_surf, textrect.move(dx, dy))

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
                user = UserData(self.handler)
                user.login(self.username_text, self.password_text)

                if user.logged_in:
                    print("Login successful")
                    self.page_manager.set_page(DrawMainPage(self.screen, self.page_manager, self.username_text))
                else:
                    print("Login failed")

            if self.create_button.collidepoint(event.pos):
                self.page_manager.set_page(DrawCreateAccountPage(self.screen, self.page_manager))

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
        self.screen.fill(DARK_BG)
        draw_stars(self.screen)

        self.draw_text("Virtual Arcade", BIG_FONT, NEON_BLUE, WIDTH // 2, 100, glow=True)

        self.draw_text("Username:", FONT, WHITE, 200, 220)
        self.draw_text("Password:", FONT, WHITE, 200, 280)

        draw_glow_rect(self.screen, self.username_rect, PANEL,
                       NEON_BLUE if self.active_box == 'username' else NEON_PURPLE)
        draw_glow_rect(self.screen, self.password_rect, PANEL,
                       NEON_BLUE if self.active_box == 'password' else NEON_PURPLE)

        username_surface = FONT.render(self.username_text, True, WHITE)
        password_surface = FONT.render('*' * len(self.password_text), True, WHITE)

        self.screen.blit(username_surface, (self.username_rect.x + 5, self.username_rect.y + 5))
        self.screen.blit(password_surface, (self.password_rect.x + 5, self.password_rect.y + 5))

        mouse_pos = pygame.mouse.get_pos()

        draw_glow_rect(self.screen, self.login_button, PANEL,
                       NEON_BLUE if self.login_button.collidepoint(mouse_pos) else NEON_PURPLE)
        draw_glow_rect(self.screen, self.create_button, PANEL,
                       NEON_BLUE if self.create_button.collidepoint(mouse_pos) else NEON_PURPLE)

        self.draw_text("Login", FONT, WHITE, self.login_button.centerx, self.login_button.centery)
        self.draw_text("Create Account", FONT, WHITE, self.create_button.centerx, self.create_button.centery)

class DrawCreateAccountPage:
    def __init__(self, screen, page_manager):
        self.screen = screen
        self.page_manager = page_manager

        self.username_rect = pygame.Rect(300, 200, 200, 40)
        self.password_rect = pygame.Rect(300, 260, 200, 40)

        self.active_box = None
        self.username_text = ''
        self.password_text = ''

        self.create_button = pygame.Rect(300, 380, 200, 40)

    def draw_text(self, text, font, color, x, y, glow=False):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))

        if glow:
            glow_surf = font.render(text, True, NEON_BLUE)
            for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                self.screen.blit(glow_surf, textrect.move(dx, dy))

        self.screen.blit(textobj, textrect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_rect.collidepoint(event.pos):
                self.active_box = 'username'
            elif self.password_rect.collidepoint(event.pos):
                self.active_box = 'password'
            else:
                self.active_box = None

            if self.create_button.collidepoint(event.pos):
                user = UserData(self.username_text)
                user.create_account(self.username_text, self.password_text)

                if user.user_id is not None:
                    print("Account created successfully")
                    self.page_manager.set_page(DrawMainPage(self.screen, self.page_manager, self.username_text))
                else:
                    print("Account creation failed")

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
        self.screen.fill(DARK_BG)
        draw_stars(self.screen)

        self.draw_text("Create Account", BIG_FONT, NEON_BLUE, WIDTH // 2, 100, glow=True)

        draw_glow_rect(self.screen, self.username_rect, PANEL,
                       NEON_BLUE if self.active_box == 'username' else NEON_PURPLE)
        draw_glow_rect(self.screen, self.password_rect, PANEL,
                       NEON_BLUE if self.active_box == 'password' else NEON_PURPLE)

        username_surface = FONT.render(self.username_text, True, WHITE)
        password_surface = FONT.render('*' * len(self.password_text), True, WHITE)

        self.screen.blit(username_surface, (self.username_rect.x + 5, self.username_rect.y + 5))
        self.screen.blit(password_surface, (self.password_rect.x + 5, self.password_rect.y + 5))

        mouse_pos = pygame.mouse.get_pos()

        draw_glow_rect(self.screen, self.create_button, PANEL,
                       NEON_BLUE if self.create_button.collidepoint(mouse_pos) else NEON_PURPLE)

        self.draw_text("Create Account", FONT, WHITE, self.create_button.centerx, self.create_button.centery)

class DrawMainPage:
    def __init__(self, screen, page_manager, username):
        self.screen = screen
        self.page_manager = page_manager
        self.username = username

        self.games = self.get_games()
        self.game_buttons = []

        self.create_buttons()

    def get_games(self):
        games = ArrayList()
        for name in os.listdir(GAME_PATH):
            games.append(name)
        return games

    def create_buttons(self):
        y = 200
        for game in self.games:
            rect = pygame.Rect(300, y, 200, 50)
            self.game_buttons.append((game, rect))
            y += 70

    def draw_text(self, text, font, color, x, y, glow=False):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))

        if glow:
            glow_surf = font.render(text, True, NEON_BLUE)
            for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                self.screen.blit(glow_surf, textrect.move(dx, dy))

        self.screen.blit(textobj, textrect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for game, rect in self.game_buttons:
                if rect.collidepoint(event.pos):
                    self.page_manager.set_page(
                        DrawGamePage(self.screen, self.page_manager, self.username, game)
                    )

    def draw(self):
        self.screen.fill(DARK_BG)
        draw_stars(self.screen)

        self.draw_text("Select a Game", BIG_FONT, NEON_BLUE, WIDTH // 2, 100, glow=True)

        mouse_pos = pygame.mouse.get_pos()

        for game, rect in self.game_buttons:
            draw_glow_rect(self.screen, rect, PANEL,
                           NEON_BLUE if rect.collidepoint(mouse_pos) else NEON_PURPLE)
            self.draw_text(game, FONT, WHITE, rect.centerx, rect.centery)       
class DrawUserPage:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.logged_in = True
        self.user_data = UserData(username)

class DrawGamePage:
    def __init__(self, screen, page_manager, username, game):
        self.screen = screen
        self.page_manager = page_manager
        self.username = username
        self.game = game

        self.data = GameData(game)
        self.leaderboard = self.data.get_leaderboard()

        self.run_button = pygame.Rect(300, 200, 200, 50)
        self.back_button = pygame.Rect(300, 270, 200, 50)

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        self.screen.blit(textobj, textrect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.run_button.collidepoint(event.pos):
                instance = RunInstance()
                instance.run(self.username, self.game)

            if self.back_button.collidepoint(event.pos):
                self.page_manager.set_page(
                    DrawMainPage(self.screen, self.page_manager, self.username)
                )

    def draw(self):
        self.screen.fill(WHITE)

        # Title
        self.draw_text(self.game, BIG_FONT, BLACK, WIDTH // 2, 100)

        # Buttons
        pygame.draw.rect(self.screen, DARK_GRAY, self.run_button)
        pygame.draw.rect(self.screen, DARK_GRAY, self.back_button)

        self.draw_text("Play", FONT, WHITE, self.run_button.centerx, self.run_button.centery)
        self.draw_text("Back", FONT, WHITE, self.back_button.centerx, self.back_button.centery)

        # Leaderboard title
        self.draw_text("Leaderboard", FONT, BLACK, WIDTH // 2, 350)

        # Leaderboard entries
        y = 400
        if self.leaderboard:
            for entry in self.leaderboard:
                text = str(entry)
                self.draw_text(text, FONT, BLACK, WIDTH // 2, y)
                y += 30
        else:
            self.draw_text("No scores yet", FONT, BLACK, WIDTH // 2, 400)
