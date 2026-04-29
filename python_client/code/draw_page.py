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
                if not self.handler.connected:
                    self.handler.connect(self.username_text)
                user = UserData(self.handler)
                user.login(self.username_text, self.password_text)

                if user.logged_in:
                    print("Login successful")
                    self.page_manager.set_page(DrawMainPage(self.screen, self.page_manager, self.username_text, self.handler))
                else:
                    print("Login failed")

            if self.create_button.collidepoint(event.pos):
                self.page_manager.set_page(DrawCreateAccountPage(self.screen, self.page_manager, self.handler))

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
    def __init__(self, screen, page_manager, handler):
        self.screen = screen
        self.page_manager = page_manager
        self.handler = handler

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
                if not self.handler.connected:
                    self.handler.connect()
                user = UserData(self.handler)
                user.create_account(self.username_text, self.password_text)

                if user.user_id is not None:
                    print("Account created successfully")
                    self.page_manager.set_page(DrawMainPage(self.screen, self.page_manager, self.username_text, self.handler))
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
    def __init__(self, screen, page_manager, username, handler):
        self.screen = screen
        self.page_manager = page_manager
        self.username = username
        self.handler = handler
        self.profile_button = pygame.Rect(550, 120, 200, 50)
        self.search_button = pygame.Rect(300, 120, 200, 50)
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
            mouse_pos = event.pos

            if self.search_button.collidepoint(mouse_pos):
                self.page_manager.set_page(
                    DrawSearchUserPage(self.screen, self.page_manager, self.handler)
                )

            elif self.profile_button.collidepoint(mouse_pos):
                self.page_manager.set_page(
                    DrawUserPage(self.screen, self.page_manager, self.handler, self.username)
                )
            for game, rect in self.game_buttons:
                if rect.collidepoint(mouse_pos):
                    self.page_manager.set_page(
                        DrawGamePage(self.screen, self.page_manager, self.username, game, self.handler)
                    )
                    break
    def draw(self):
        self.screen.fill(DARK_BG)
        draw_stars(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        self.draw_text("Select a Game", BIG_FONT, NEON_BLUE, WIDTH // 2, 100, glow=True)
        draw_glow_rect(self.screen, self.search_button, PANEL,
                    NEON_BLUE if self.search_button.collidepoint(pygame.mouse.get_pos()) else NEON_PURPLE)

        draw_glow_rect(
            self.screen,
            self.profile_button,
            PANEL,
            NEON_BLUE if self.profile_button.collidepoint(mouse_pos) else NEON_PURPLE
        )

        self.draw_text(
            "My Profile",
            FONT,
            WHITE,
            self.profile_button.centerx,
            self.profile_button.centery
        )
        self.draw_text("Search Users", FONT, WHITE,
                    self.search_button.centerx, self.search_button.centery)
        

        for game, rect in self.game_buttons:
            draw_glow_rect(self.screen, rect, PANEL,
                           NEON_BLUE if rect.collidepoint(mouse_pos) else NEON_PURPLE)
            self.draw_text(game, FONT, WHITE, rect.centerx, rect.centery)       
class DrawUserPage:
    def __init__(self, screen, page_manager, handler, username):
        self.screen = screen
        self.page_manager = page_manager
        self.handler = handler
        self.username = username

        self.back_button = pygame.Rect(50, 50, 120, 40)

        self.user_data = None
        self.sessions = []

        self.load_user_data()

    def load_user_data(self):
        user = UserData(self.handler)
        response = user.get_user_data(self.username)

        if response and response.get('success'):
            data = response.get('user_data', {})
            self.sessions = data.get('sessions', [])
        else:
            self.sessions = []

    def draw_text(self, text, font, color, x, y, center=True):
        textobj = font.render(text, True, color)
        if center:
            textrect = textobj.get_rect(center=(x, y))
        else:
            textrect = textobj.get_rect(topleft=(x, y))
        self.screen.blit(textobj, textrect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.page_manager.set_page(
                    DrawMainPage(self.screen, self.page_manager, self.username, self.handler)
                )

    def draw(self):
        self.screen.fill(DARK_BG)
        draw_stars(self.screen)

        mouse_pos = pygame.mouse.get_pos()

        # Title
        self.draw_text(f"{self.username}'s Profile", BIG_FONT, NEON_BLUE, WIDTH // 2, 80)

        # Back button
        draw_glow_rect(
            self.screen,
            self.back_button,
            PANEL,
            NEON_BLUE if self.back_button.collidepoint(mouse_pos) else NEON_PURPLE
        )
        self.draw_text("Back", FONT, WHITE,
                       self.back_button.centerx, self.back_button.centery)

        # Sessions title
        self.draw_text("Recent Sessions", FONT, WHITE, WIDTH // 2, 150)

        # Sessions list
        y = 200

        if self.sessions:
            for session in self.sessions[:10]:  # limit display
                # session structure depends on your backend
                # assuming dict like {'game': ..., 'score': ..., 'date': ...}
                text = str(session)
                self.draw_text(text, FONT, WHITE, WIDTH // 2, y)
                y += 30
        else:
            self.draw_text("No session data available", FONT, WHITE, WIDTH // 2, 200)

class DrawGamePage:
    def __init__(self, screen, page_manager, username, game, handler):
        self.screen = screen
        self.page_manager = page_manager
        self.username = username
        self.game = game
        self.handler = handler

        self.run_button = pygame.Rect(300, 200, 200, 50)
        self.back_button = pygame.Rect(300, 270, 200, 50)

        self.leaderboard = []   # ALWAYS initialize

        self.build_leaderboard()

    def build_leaderboard(self):
        request = {
            "type": "get_leaderboard",
            "game_name": self.game
        }

        response = self.handler.process_request(request)

        if response and response.get("success"):
            self.leaderboard = response.get("score_leaderboard", [])
        else:
            self.leaderboard = []

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(str(text), True, color)
        textrect = textobj.get_rect(center=(x, y))
        self.screen.blit(textobj, textrect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.run_button.collidepoint(event.pos):
                instance = RunInstance(self.username)
                instance.run(self.game)

            elif self.back_button.collidepoint(event.pos):
                self.page_manager.set_page(
                    DrawMainPage(self.screen, self.page_manager, self.username, self.handler)
                )

    def draw(self):
        self.screen.fill(WHITE)

        self.draw_text(self.game, BIG_FONT, BLACK, WIDTH // 2, 100)

        pygame.draw.rect(self.screen, DARK_GRAY, self.run_button)
        pygame.draw.rect(self.screen, DARK_GRAY, self.back_button)

        self.draw_text("Play", FONT, WHITE, self.run_button.centerx, self.run_button.centery)
        self.draw_text("Back", FONT, WHITE, self.back_button.centerx, self.back_button.centery)

        self.draw_text("Leaderboard", FONT, BLACK, WIDTH // 2, 350)

        y = 400
        if self.leaderboard:
            for entry in self.leaderboard[:10]:
                self.draw_text(entry, FONT, BLACK, WIDTH // 2, y)
                y += 30
        else:
            self.draw_text("No scores yet", FONT, BLACK, WIDTH // 2, 400)
class DrawSearchUserPage:
    def __init__(self, screen, page_manager, handler):
        self.screen = screen
        self.page_manager = page_manager
        self.handler = handler

        self.input_rect = pygame.Rect(300, 150, 300, 50)
        self.text = ''
        self.active = False

        self.suggestions = []   # autocomplete results
        self.suggestion_rects = []

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        self.screen.blit(textobj, textrect)

    def update_suggestions(self):
        if self.text.strip() == '':
            self.suggestions = []
            self.create_suggestion_rects()
            return

        results = self.handler.search_usernames(self.text)

        if not isinstance(results, dict):
            self.suggestions = []
        else:
            self.suggestions = results.get('results') or []

        self.create_suggestion_rects()

    def create_suggestion_rects(self):
        self.suggestion_rects = []
        y = 220
        for name in self.suggestions[:5]:  # limit to 5 suggestions
            rect = pygame.Rect(300, y, 300, 40)
            self.suggestion_rects.append((name, rect))
            y += 45

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

            # Click suggestion -> autofill
            for name, rect in self.suggestion_rects:
                if rect.collidepoint(event.pos):
                    self.text = name
                    self.update_suggestions()

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                # ENTER -> go to user page if valid
                if self.text in self.suggestions:
                    self.page_manager.set_page(
                        DrawUserPage(self.screen, self.page_manager, self.handler, self.text)
                    )

            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.update_suggestions()
            else:
                self.text += event.unicode
                self.update_suggestions()

    def draw(self):
        self.screen.fill(DARK_BG)
        draw_stars(self.screen)

        # Title
        self.draw_text("Search Users", BIG_FONT, NEON_BLUE, WIDTH // 2, 80)

        # Input box
        draw_glow_rect(
            self.screen,
            self.input_rect,
            PANEL,
            NEON_BLUE if self.active else NEON_PURPLE
        )

        text_surface = FONT.render(self.text, True, WHITE)
        self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 10))

        # Suggestions
        mouse_pos = pygame.mouse.get_pos()

        for name, rect in self.suggestion_rects:
            draw_glow_rect(
                self.screen,
                rect,
                PANEL,
                NEON_BLUE if rect.collidepoint(mouse_pos) else NEON_PURPLE
            )
            self.draw_text(name, FONT, WHITE, rect.centerx, rect.centery)