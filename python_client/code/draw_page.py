import pygame
import sys
pygame.init()
from settings import *
from python_server_handler import *
import os
from game_instance_manager import *
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
    def __init__(self, screen, page_manager):
        self.screen = screen
        self.page_manager = page_manager
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

            # LOGIN BUTTON
            if self.login_button.collidepoint(event.pos):
                user = UserData(self.username_text)
                user.login(self.username_text, self.password_text)

                if user.logged_in:
                    print("Login successful")
                    self.page_manager.set_page(DrawMainPage(self.screen, self.page_manager, self.username_text))
                else:
                    print("Login failed")

            # GO TO CREATE ACCOUNT PAGE
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
    def __init__(self, screen, page_manager):
        self.screen = screen
        self.username_rect = pygame.Rect(300, 200, 200, 40)
        self.password_rect = pygame.Rect(300, 260, 200, 40)
        self.page_manager = page_manager
        self.active_box = None
        self.username_text = ''
        self.password_text = ''

        # Buttons
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

            # CREATE ACCOUNT BUTTON
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
        pygame.draw.rect(self.screen, DARK_GRAY, self.create_button)
        self.draw_text("Create Account", FONT, WHITE, self.create_button.centerx, self.create_button.centery)

        
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

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        self.screen.blit(textobj, textrect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for game, rect in self.game_buttons:
                if rect.collidepoint(event.pos):
                    self.page_manager.set_page(
                        DrawGamePage(self.screen, self.page_manager, self.username, game)
                    )

    def draw(self):
        self.screen.fill(WHITE)

        self.draw_text("Select a Game", BIG_FONT, BLACK, WIDTH // 2, 100)

        for game, rect in self.game_buttons:
            pygame.draw.rect(self.screen, DARK_GRAY, rect)
            self.draw_text(game, FONT, WHITE, rect.centerx, rect.centery)
    

