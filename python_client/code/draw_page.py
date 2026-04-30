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

class DrawGamePage:
    # Colors
    DARK_BG      = (10, 10, 26)
    PANEL_BG     = (17, 17, 42)
    BORDER       = (45, 45, 94)
    ROW_ALT      = (26, 26, 58)
    ROW_HL       = (49, 46, 129)      # highlight for current player
    HL_BORDER    = (99, 102, 241)
    PURP         = (167, 139, 250)
    BLUE         = (147, 197, 253)
    WHITE        = (255, 255, 255)
    MUTED        = (107, 114, 128)
    NAME_COL     = (209, 213, 219)
    MEDAL        = [(251, 191, 36), (156, 163, 175), (180, 83, 9)]
    BTN_BG       = (79, 70, 229)
    BTN_HOV      = (99, 102, 241)
    INPUT_BG     = (22, 22, 50)
    INPUT_ACTIVE = (30, 30, 70)
    ERR_COL      = (248, 113, 113)
    OK_COL       = (110, 231, 183)

    def __init__(self, screen, page_manager, username, game, handler):
        self.screen       = screen
        self.page_manager = page_manager
        self.username     = username
        self.game         = game
        self.handler      = handler

        self.run_button     = pygame.Rect(240, 190, 160, 42)
        self.back_button    = pygame.Rect(420, 190, 160, 42)
        self.refresh_button = pygame.Rect(WIDTH - 130, 190, 110, 42)

        # Leaderboard data
        self.score_leaderboard = []
        self.time_leaderboard  = []
        self.player_score      = None
        self.player_time       = None

        # Range query state — two input boxes per panel
        self.range_inputs = {
            'score_min': '', 'score_max': '',
            'time_min':  '', 'time_max':  '',
        }
        self.active_input    = None
        self.range_results   = None   # None = not searched yet
        self.range_error     = ''

        self.build_leaderboard()
        self.fetch_player_score()

    # ------------------------------------------------------------------ data
    def build_leaderboard(self):
        resp = self.handler.process_request({"type": "get_leaderboard", "game_name": self.game})
        if resp and resp.get("success"):
            self.score_leaderboard = resp.get("score_leaderboard", [])
            self.time_leaderboard  = resp.get("time_leaderboard",  [])
        else:
            self.score_leaderboard = []
            self.time_leaderboard  = []

    def fetch_player_score(self):
        resp = self.handler.process_request({
            "type": "get_player_score",
            "username": self.username,
            "game_name": self.game
        })
        if resp and resp.get("success"):
            self.player_score = resp.get("score")
            self.player_time  = resp.get("time")

    def do_refresh(self):
        self.range_results = None
        self.range_error   = ''
        self.build_leaderboard()
        self.fetch_player_score()

    def do_range_query(self):
        self.range_error = ''
        try:
            payload = {"type": "ranged_query", "game_name": self.game}
            si, sx = self.range_inputs['score_min'], self.range_inputs['score_max']
            ti, tx = self.range_inputs['time_min'],  self.range_inputs['time_max']
            if si or sx:
                payload['min_score'] = int(si or 0)
                payload['max_score'] = int(sx or 999999)
            if ti or tx:
                payload['min_time'] = int(ti or 0)
                payload['max_time'] = int(tx or 999999)
            resp = self.handler.process_request(payload)
            if resp and resp.get("success"):
                self.range_results = {
                    'scores': resp.get('score_results', []),
                    'times':  resp.get('time_results',  [])
                }
            else:
                self.range_error = resp.get('message', 'Query failed')
        except ValueError:
            self.range_error = 'Enter whole numbers only'

    # ---------------------------------------------------------------- helpers
    def format_time(self, seconds):
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        return f"{m}m {s:02d}s" if m else f"{s}s"

    def draw_text(self, text, font, color, x, y, align="center"):
        surf = font.render(str(text), True, color)
        rect = surf.get_rect(**{
            "center":   (x, y),
            "midleft":  (x, y),
            "midright": (x, y)
        }[align] if False else {})
        if align == "center":  rect = surf.get_rect(center=(x, y))
        elif align == "left":  rect = surf.get_rect(midleft=(x, y))
        elif align == "right": rect = surf.get_rect(midright=(x, y))
        self.screen.blit(surf, rect)

    def draw_button(self, rect, label, mouse_pos, color_override=None):
        bg = color_override or (self.BTN_HOV if rect.collidepoint(mouse_pos) else self.BTN_BG)
        pygame.draw.rect(self.screen, bg, rect, border_radius=8)
        pygame.draw.rect(self.screen, self.HL_BORDER, rect, 1, border_radius=8)
        self.draw_text(label, FONT, self.WHITE, rect.centerx, rect.centery)

    def draw_input(self, rect, key, placeholder):
        active = self.active_input == key
        bg = self.INPUT_ACTIVE if active else self.INPUT_BG
        pygame.draw.rect(self.screen, bg, rect, border_radius=6)
        pygame.draw.rect(self.screen, self.HL_BORDER if active else self.BORDER, rect, 1, border_radius=6)
        val = self.range_inputs[key]
        if val:
            self.draw_text(val, SMALL_FONT, self.WHITE, rect.x + 6, rect.centery, align="left")
        else:
            self.draw_text(placeholder, SMALL_FONT, self.MUTED, rect.x + 6, rect.centery, align="left")

    # --------------------------------------------------------------- panels
    def draw_panel(self, title, entries, player_val, x, y, w, h, value_key, format_fn=None):
        is_time  = value_key == "time"
        hdr_col  = self.BLUE if is_time else self.PURP
        val_col  = self.BLUE if is_time else self.PURP

        pygame.draw.rect(self.screen, self.PANEL_BG, (x, y, w, h), border_radius=10)
        pygame.draw.rect(self.screen, self.BORDER,   (x, y, w, h), 1, border_radius=10)

        # Header + player's own score
        self.draw_text(title, FONT, hdr_col, x + w // 2, y + 20)
        if player_val is not None:
            pv_str = format_fn(player_val) if format_fn else str(player_val)
            self.draw_text(f"Your best: {pv_str}", SMALL_FONT, self.OK_COL,
                           x + w // 2, y + 36)
            line_y = y + 48
        else:
            line_y = y + 34

        pygame.draw.line(self.screen, self.BORDER, (x + 12, line_y), (x + w - 12, line_y))

        row_y = line_y + 14
        row_h = 28

        if not entries:
            self.draw_text("No data yet", SMALL_FONT, self.MUTED, x + w // 2, row_y + 14)
            return

        for i, entry in enumerate(entries[:8]):
            is_player = entry.get("uuid") == self.username
            row_rect  = pygame.Rect(x + 8, row_y - 4, w - 16, row_h - 2)

            if is_player:
                pygame.draw.rect(self.screen, self.ROW_HL, row_rect, border_radius=4)
                pygame.draw.rect(self.screen, self.HL_BORDER, row_rect, 1, border_radius=4)
            elif i % 2 == 0:
                pygame.draw.rect(self.screen, self.ROW_ALT, row_rect, border_radius=4)

            rank_col = self.MEDAL[i] if i < 3 else self.MUTED
            self.draw_text(f"{i+1}", SMALL_FONT, rank_col, x + 22, row_y + 10)

            name_col = self.WHITE if is_player else self.NAME_COL
            self.draw_text(entry.get("uuid", "???"), SMALL_FONT, name_col,
                           x + 38, row_y + 10, align="left")

            raw = entry.get(value_key, 0)
            display = format_fn(raw) if format_fn else str(raw)
            self.draw_text(display, SMALL_FONT, val_col, x + w - 12, row_y + 10, align="right")

            row_y += row_h

    def draw_range_section(self, x, y, w):
        # Labels
        self.draw_text("Score range:", SMALL_FONT, self.MUTED, x, y, align="left")
        self.draw_text("Time range (s):", SMALL_FONT, self.MUTED, x + w // 2 + 8, y, align="left")

        box_w = (w // 2 - 20) // 2
        # Score inputs
        r_smin = pygame.Rect(x,              y + 18, box_w, 28)
        r_smax = pygame.Rect(x + box_w + 6,  y + 18, box_w, 28)
        # Time inputs
        r_tmin = pygame.Rect(x + w // 2 + 8,              y + 18, box_w, 28)
        r_tmax = pygame.Rect(x + w // 2 + 8 + box_w + 6,  y + 18, box_w, 28)

        self.draw_input(r_smin, 'score_min', 'min')
        self.draw_input(r_smax, 'score_max', 'max')
        self.draw_input(r_tmin, 'time_min',  'min')
        self.draw_input(r_tmax, 'time_max',  'max')

        # Store rects for hit-testing
        self._range_rects = {
            'score_min': r_smin, 'score_max': r_smax,
            'time_min':  r_tmin, 'time_max':  r_tmax,
        }

        # Search button
        search_rect = pygame.Rect(x + w - 90, y + 18, 90, 28)
        mouse_pos   = pygame.mouse.get_pos()
        self.draw_button(search_rect, "Search", mouse_pos)
        self._search_rect = search_rect

        # Error / results summary
        if self.range_error:
            self.draw_text(self.range_error, SMALL_FONT, self.ERR_COL,
                           x, y + 54, align="left")
        elif self.range_results is not None:
            ns = len(self.range_results['scores'])
            nt = len(self.range_results['times'])
            self.draw_text(f"{ns} score result(s)  |  {nt} time result(s)",
                           SMALL_FONT, self.OK_COL, x, y + 54, align="left")

    # ---------------------------------------------------------------- events
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if self.run_button.collidepoint(pos):
                RunInstance(self.username).run(self.game)

            elif self.back_button.collidepoint(pos):
                self.page_manager.set_page(
                    DrawMainPage(self.screen, self.page_manager, self.username, self.handler))

            elif self.refresh_button.collidepoint(pos):
                self.do_refresh()

            elif hasattr(self, '_search_rect') and self._search_rect.collidepoint(pos):
                self.do_range_query()

            elif hasattr(self, '_range_rects'):
                self.active_input = None
                for key, rect in self._range_rects.items():
                    if rect.collidepoint(pos):
                        self.active_input = key
                        break

            else:
                self.active_input = None

        elif event.type == pygame.KEYDOWN and self.active_input:
            key = self.active_input
            if event.key == pygame.K_BACKSPACE:
                self.range_inputs[key] = self.range_inputs[key][:-1]
            elif event.key == pygame.K_RETURN:
                self.do_range_query()
            elif event.unicode.isdigit():          # numbers only
                self.range_inputs[key] += event.unicode

    # ----------------------------------------------------------------- draw
    def draw(self):
        self.screen.fill(self.DARK_BG)
        draw_stars(self.screen)
        mouse_pos = pygame.mouse.get_pos()

        self.draw_text(self.game, BIG_FONT, self.PURP, WIDTH // 2, 90)

        self.draw_button(self.run_button,     "Play",    mouse_pos)
        self.draw_button(self.back_button,    "Back",    mouse_pos)
        self.draw_button(self.refresh_button, "Refresh", mouse_pos, 
                         color_override=(30, 58, 95) if not self.refresh_button.collidepoint(mouse_pos) else (37, 99, 235))

        panel_w = (WIDTH - 60) // 2
        panel_h = 300
        panel_y = 248

        self.draw_panel(
            "Top Scores", self.score_leaderboard, self.player_score,
            x=20, y=panel_y, w=panel_w, h=panel_h,
            value_key="score"
        )
        self.draw_panel(
            "Longest Survival", self.time_leaderboard, self.player_time,
            x=30 + panel_w, y=panel_y, w=panel_w, h=panel_h,
            value_key="time", format_fn=self.format_time
        )

        # Range query section below the panels
        self.draw_range_section(x=20, y=panel_y + panel_h + 16, w=WIDTH - 40)
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

        self.run_button = pygame.Rect(240, 190, 160, 42)
        self.back_button = pygame.Rect(420, 190, 160, 42)

        self.score_leaderboard = []
        self.time_leaderboard = []

        self.build_leaderboard()

    def build_leaderboard(self):
        request = {"type": "get_leaderboard", "game_name": self.game}
        response = self.handler.process_request(request)
        if response and response.get("success"):
            self.score_leaderboard = response.get("score_leaderboard", [])
            self.time_leaderboard = response.get("time_leaderboard", [])
        else:
            self.score_leaderboard = []
            self.time_leaderboard = []

    def format_time(self, seconds):
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        return f"{m}m {s:02d}s" if m else f"{s}s"

    def draw_text(self, text, font, color, x, y, align="center"):
        textobj = font.render(str(text), True, color)
        if align == "center":
            rect = textobj.get_rect(center=(x, y))
        elif align == "left":
            rect = textobj.get_rect(midleft=(x, y))
        elif align == "right":
            rect = textobj.get_rect(midright=(x, y))
        self.screen.blit(textobj, rect)

    def draw_panel(self, title, entries, x, y, w, h, value_key, format_fn=None):
        PANEL_BG   = (17, 17, 42)
        BORDER     = (45, 45, 94)
        HEADER_COL = (167, 139, 250)   # purple for score
        ROW_LINE   = (26, 26, 58)
        NAME_COL   = (209, 213, 219)
        VAL_COL    = (167, 139, 250)

        if value_key == "time":
            HEADER_COL = (147, 197, 253)   # blue for time
            VAL_COL    = (147, 197, 253)

        MEDAL = [(251, 191, 36), (156, 163, 175), (180, 83, 9)]

        pygame.draw.rect(self.screen, PANEL_BG, (x, y, w, h), border_radius=10)
        pygame.draw.rect(self.screen, BORDER, (x, y, w, h), 1, border_radius=10)

        # Header
        self.draw_text(title, FONT, HEADER_COL, x + w // 2, y + 22)
        pygame.draw.line(self.screen, BORDER, (x + 12, y + 38), (x + w - 12, y + 38))

        row_y = y + 56
        row_h = 30

        if not entries:
            self.draw_text("No data yet", FONT, (75, 85, 99), x + w // 2, row_y + 20)
            return

        for i, entry in enumerate(entries[:8]):
            # Alternating row bg
            if i % 2 == 0:
                pygame.draw.rect(self.screen, ROW_LINE,
                                 (x + 8, row_y - 6, w - 16, row_h - 2), border_radius=4)

            # Rank
            rank_col = MEDAL[i] if i < 3 else (75, 85, 99)
            self.draw_text(f"{i+1}", SMALL_FONT, rank_col, x + 24, row_y + 8)

            # Username
            username = entry.get("uuid", "???")
            self.draw_text(username, SMALL_FONT, NAME_COL, x + 42, row_y + 8, align="left")

            # Value
            raw = entry.get(value_key, 0)
            display = format_fn(raw) if format_fn else str(raw)
            self.draw_text(display, SMALL_FONT, VAL_COL, x + w - 14, row_y + 8, align="right")

            row_y += row_h

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
        DARK_BG    = (10, 10, 26)
        NEON_PURP  = (99, 102, 241)
        NEON_BLUE  = (167, 139, 250)
        BTN_BG     = (79, 70, 229)
        BTN_HOV    = (99, 102, 241)
        WHITE      = (255, 255, 255)

        self.screen.fill(DARK_BG)
        draw_stars(self.screen)

        # Title
        self.draw_text(self.game, BIG_FONT, NEON_BLUE, WIDTH // 2, 90)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn, label in [(self.run_button, "Play"), (self.back_button, "Back")]:
            color = BTN_HOV if btn.collidepoint(mouse_pos) else BTN_BG
            pygame.draw.rect(self.screen, color, btn, border_radius=8)
            pygame.draw.rect(self.screen, NEON_PURP, btn, 1, border_radius=8)
            self.draw_text(label, FONT, WHITE, btn.centerx, btn.centery)

        # Leaderboard panels — side by side
        panel_w = (WIDTH - 80) // 2
        panel_h = 310
        panel_y = 250

        self.draw_panel(
            "Top Scores",
            self.score_leaderboard,
            x=30, y=panel_y, w=panel_w, h=panel_h,
            value_key="score"
        )
        self.draw_panel(
            "Longest Survival",
            self.time_leaderboard,
            x=50 + panel_w, y=panel_y, w=panel_w, h=panel_h,
            value_key="time",
            format_fn=self.format_time
        )
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
            print(self.suggestions)
            return

        results = self.handler.search_usernames(self.text)
        print(results)

        if not isinstance(results, dict):
            self.suggestions = results
        else:
            self.suggestions = results.get('usernames', [])

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