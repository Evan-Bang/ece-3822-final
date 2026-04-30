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
        self.username = ""
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
        self.error_message = ''

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
                self.error_message = ''  # clear previous error
                try:
                    if not self.handler.connected:
                        self.handler.connect(self.username_text)
                    user = UserData(self.handler)
                    user.login(self.username_text, self.password_text)

                    if getattr(user, 'logged_in', False):
                        self.page_manager.username = self.username_text
                        self.page_manager.set_page(
                            DrawMainPage(self.screen, self.page_manager, self.username_text, self.handler)
                        )
                    else:
                        self.error_message = "Invalid username or password."
                except Exception as e:
                    print(f"Login error: {e}")
                    self.error_message = "Could not connect to server."

            if self.create_button.collidepoint(event.pos):
                self.page_manager.set_page(
                    DrawCreateAccountPage(self.screen, self.page_manager, self.handler)
                )

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
        if self.error_message:
            self.draw_text(self.error_message, FONT, (255, 80, 80), WIDTH // 2, 440)

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
                
                user = UserData(self.handler)
                user.create_account(self.username_text, self.password_text)
                if not self.handler.connected:
                    self.handler.connect(self.username_text)
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
                    DrawUserPage(self.screen, self.page_manager, self.handler, self.page_manager.username)
                )
            for game, rect in self.game_buttons:
                if rect.collidepoint(mouse_pos):
                    self.page_manager.set_page(
                        DrawGamePage(self.screen, self.page_manager, self.page_manager.username, game, self.handler)
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
class DrawGamePage:
    def __init__(self, screen, page_manager, username, game, handler):
        self.screen       = screen
        self.page_manager = page_manager
        self.username     = username
        self.game         = game
        self.handler      = handler
        self.score_scroll = 0
        self.time_scroll  = 0

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
        seconds = int(float(seconds))
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
        bg = color_override or (BTN_HOV if rect.collidepoint(mouse_pos) else BTN_BG)
        pygame.draw.rect(self.screen, bg, rect, border_radius=8)
        pygame.draw.rect(self.screen, HL_BORDER, rect, 1, border_radius=8)
        self.draw_text(label, FONT, WHITE, rect.centerx, rect.centery)

    def draw_input(self, rect, key, placeholder):
        active = self.active_input == key
        bg = INPUT_ACTIVE if active else INPUT_BG
        pygame.draw.rect(self.screen, bg, rect, border_radius=6)
        pygame.draw.rect(self.screen, HL_BORDER if active else BORDER, rect, 1, border_radius=6)
        val = self.range_inputs[key]
        if val:
            self.draw_text(val, SMALL_FONT, WHITE, rect.x + 6, rect.centery, align="left")
        else:
            self.draw_text(placeholder, SMALL_FONT, MUTED, rect.x + 6, rect.centery, align="left")

    # --------------------------------------------------------------- panels
    def draw_panel(self, title, entries, player_val, x, y, w, h, value_key, format_fn=None, scroll_offset=0):
        is_time = value_key == "time"
        hdr_col = BLUE if is_time else PURP
        val_col = BLUE if is_time else PURP

        pygame.draw.rect(self.screen, PANEL_BG, (x, y, w, h), border_radius=10)
        pygame.draw.rect(self.screen, BORDER,   (x, y, w, h), 1, border_radius=10)

        # Header + player's own score
        self.draw_text(title, FONT, hdr_col, x + w // 2, y + 20)
        if player_val is not None:
            pv_str = format_fn(player_val) if format_fn else str(player_val)
            self.draw_text(f"Your best: {pv_str}", SMALL_FONT, OK_COL, x + w // 2, y + 36)
            line_y = y + 48
        else:
            line_y = y + 34

        pygame.draw.line(self.screen, BORDER, (x + 12, line_y), (x + w - 12, line_y))

        if not entries:
            self.draw_text("No data yet", SMALL_FONT, MUTED, x + w // 2, line_y + 20)
            return

        row_h        = 28
        content_top  = line_y + 8          # where rows start inside the panel
        visible_h    = y + h - content_top - 8
        total_h      = len(entries) * row_h

        # Clamp scroll
        max_scroll = max(0, total_h - visible_h)
        scroll_offset = max(0, min(scroll_offset, max_scroll))

        # --- Draw rows onto a temporary surface, then blit clipped ---
        row_surf = pygame.Surface((w, total_h), pygame.SRCALPHA)

        for i, entry in enumerate(entries):
            is_player = entry.get("uuid") == self.username
            ry        = i * row_h
            row_rect  = pygame.Rect(8, ry, w - 16, row_h - 2)

            if is_player:
                pygame.draw.rect(row_surf, ROW_HL,    row_rect, border_radius=4)
                pygame.draw.rect(row_surf, HL_BORDER, row_rect, 1, border_radius=4)
            elif i % 2 == 0:
                pygame.draw.rect(row_surf, ROW_ALT, row_rect, border_radius=4)

            rank_col = MEDAL[i] if i < 3 else MUTED
            cy = ry + row_h // 2

            rank_surf = SMALL_FONT.render(f"{i+1}", True, rank_col)
            row_surf.blit(rank_surf, rank_surf.get_rect(midleft=(14, cy)))

            name_col  = WHITE if is_player else NAME_COL
            name_surf = SMALL_FONT.render(entry.get("uuid", "???"), True, name_col)
            row_surf.blit(name_surf, name_surf.get_rect(midleft=(32, cy)))

            raw     = entry.get(value_key, 0)
            display = format_fn(raw) if format_fn else str(raw)
            val_surf = SMALL_FONT.render(display, True, val_col)
            row_surf.blit(val_surf, val_surf.get_rect(midright=(w - 10, cy)))

        # Clip and blit
        clip_area = pygame.Rect(0, scroll_offset, w, visible_h)
        self.screen.blit(row_surf, (x, content_top), area=clip_area)

        # --- Scrollbar ---
        if total_h > visible_h:
            bar_x     = x + w - 6
            bar_track = pygame.Rect(bar_x, content_top, 4, visible_h)
            pygame.draw.rect(self.screen, BORDER, bar_track, border_radius=2)

            thumb_h   = max(20, int(visible_h * visible_h / total_h))
            thumb_pct = scroll_offset / max_scroll if max_scroll else 0
            thumb_y   = content_top + int(thumb_pct * (visible_h - thumb_h))
            thumb     = pygame.Rect(bar_x, thumb_y, 4, thumb_h)
            pygame.draw.rect(self.screen, NEON_BLUE, thumb, border_radius=2)

    def draw_range_section(self, x, y, w):
        # Labels
        self.draw_text("Score range:", SMALL_FONT, MUTED, x, y, align="left")
        self.draw_text("Time range (s):", SMALL_FONT, MUTED, x + w // 2 + 8, y, align="left")

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
            self.draw_text(self.range_error, SMALL_FONT, ERR_COL, x, y + 54, align="left")
        elif self.range_results is not None:
            ns = len(self.range_results['scores'])
            nt = len(self.range_results['times'])
            summary = f"Found {ns} scores, {nt} times. (Click Refresh to clear)"
            self.draw_text(summary, SMALL_FONT, OK_COL, x, y + 54, align="left")

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
        elif event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            panel_w = (WIDTH - 60) // 2
            panel_y = 248
            panel_h = 300

            left_panel  = pygame.Rect(20,          panel_y, panel_w, panel_h)
            right_panel = pygame.Rect(30 + panel_w, panel_y, panel_w, panel_h)

            if left_panel.collidepoint(mouse_pos):
                self.score_scroll = max(0, self.score_scroll - event.y * 20)
            elif right_panel.collidepoint(mouse_pos):
                self.time_scroll  = max(0, self.time_scroll  - event.y * 20)

    # ----------------------------------------------------------------- draw
    def draw(self):
        # 1. Background and Stars
        self.screen.fill(DARK_BG)
        draw_stars(self.screen)
        mouse_pos = pygame.mouse.get_pos()

        # 2. Header Title
        self.draw_text(self.game, BIG_FONT, PURP, WIDTH // 2, 90)

        # 3. Action Buttons (Play, Back, Refresh)
        self.draw_button(self.run_button, "Play", mouse_pos)
        self.draw_button(self.back_button, "Back", mouse_pos)
        
        # Highlight Refresh button differently if a search is active (acts as a 'Clear')
        refresh_label = "Clear" if self.range_results is not None else "Refresh"
        refresh_idle_col = (30, 58, 95) if self.range_results is None else (70, 30, 30)
        
        self.draw_button(
            self.refresh_button, 
            refresh_label, 
            mouse_pos, 
            color_override=refresh_idle_col if not self.refresh_button.collidepoint(mouse_pos) else (37, 99, 235)
        )

        # 4. Panel Configuration
        panel_w = (WIDTH - 60) // 2
        panel_h = 300
        panel_y = 248

        # --- Data Selection Logic ---
        # If the user has performed a range query, show those results.
        # Otherwise, show the default global leaderboards.
        if self.range_results is not None:
            score_data  = self.range_results.get('scores', [])
            time_data   = self.range_results.get('times', [])
            score_title = "Filtered Scores"
            time_title  = "Filtered Times"
        else:
            score_data  = self.score_leaderboard
            time_data   = self.time_leaderboard
            score_title = "Top Scores"
            time_title  = "Longest Survival"

        # 5. Draw the Two Main Panels
        # Left Panel: Scores
        self.draw_panel(
            score_title, 
            score_data, 
            self.player_score,
            x=20, 
            y=panel_y, 
            w=panel_w, 
            h=panel_h,
            value_key="score",
            scroll_offset=self.score_scroll
        )
        
        # Right Panel: Survival Time
        self.draw_panel(
            time_title, 
            time_data, 
            self.player_time,
            x=30 + panel_w, 
            y=panel_y, 
            w=panel_w, 
            h=panel_h,
            value_key="time", 
            format_fn=self.format_time,
            scroll_offset=self.time_scroll      
        )

        # 6. Draw Range Query Input Section (Bottom)
        self.draw_range_section(x=20, y=panel_y + panel_h + 16, w=WIDTH - 40)

class DrawUserPage:
    def __init__(self, screen, page_manager, handler, username):
        self.screen = screen
        self.page_manager = page_manager
        self.handler = handler
        self.username = username

        self.back_button = pygame.Rect(40, 40, 120, 42)

        self.sessions = []
        self.stats = {
            "total_sessions": 0,
            "best_score": 0,
            "best_time": 0
        }

        self.load_user_data()

    # ----------------------------------------------------- data
    def load_user_data(self):
        user = UserData(self.handler)
        response = user.get_user_data(self.username)

        if response and response.get("success"):
            data = response.get("user_data", {})
            raw_sessions = data.get("sessions", [])

            self.sessions = []

            for s in raw_sessions:
                self.sessions.append({
                    "game": s.get("GAME", "Unknown"),
                    "score": s.get("SCORE", 0),
                    "time": s.get("PLAYTIME", 0),
                    "date": s.get("DATE", "--")
                })

            self.stats["total_sessions"] = len(self.sessions)

            if self.sessions:
                self.stats["best_score"] = max(
                    session["score"] for session in self.sessions
                )
                self.stats["best_time"] = max(
                    session["time"] for session in self.sessions
                )
            else:
                self.stats["best_score"] = 0
                self.stats["best_time"] = 0

        else:
            self.sessions = []
            self.stats["total_sessions"] = 0
            self.stats["best_score"] = 0
            self.stats["best_time"] = 0

    # ----------------------------------------------------- helpers
    def format_time(self, seconds):
        seconds = int(float(seconds))
        m, s = divmod(seconds, 60)
        return f"{m}m {s:02d}s" if m else f"{s}s"

    def draw_text(self, text, font, color, x, y, align="center"):
        surf = font.render(str(text), True, color)

        if align == "center":
            rect = surf.get_rect(center=(x, y))
        elif align == "left":
            rect = surf.get_rect(midleft=(x, y))
        elif align == "right":
            rect = surf.get_rect(midright=(x, y))

        self.screen.blit(surf, rect)

    def draw_button(self, rect, label, mouse_pos):
        bg = (45, 45, 85) if rect.collidepoint(mouse_pos) else PANEL
        pygame.draw.rect(self.screen, bg, rect, border_radius=8)
        pygame.draw.rect(self.screen, NEON_BLUE, rect, 1, border_radius=8)
        self.draw_text(label, FONT, WHITE, rect.centerx, rect.centery)

    def draw_stat_card(self, label, value, x, y, w, h, accent):
        pygame.draw.rect(self.screen, PANEL, (x, y, w, h), border_radius=10)
        pygame.draw.rect(self.screen, accent, (x, y, w, h), 2, border_radius=10)

        self.draw_text(label, SMALL_FONT, WHITE, x + w // 2, y + 18)
        self.draw_text(value, FONT, accent, x + w // 2, y + h // 2 + 10)

    def draw_sessions_panel(self, x, y, w, h):
        pygame.draw.rect(self.screen, PANEL, (x, y, w, h), border_radius=12)
        pygame.draw.rect(self.screen, NEON_PURPLE, (x, y, w, h), 2, border_radius=12)

        # Title
        self.draw_text("Session History", FONT, NEON_BLUE, x + w // 2, y + 20)

        # Header row
        header_y = y + 55
        pygame.draw.line(self.screen, WHITE, (x + 15, header_y), (x + w - 15, header_y), 1)

        self.draw_text("Game", SMALL_FONT, NEON_BLUE, x + 35, header_y + 16, align="left")
        self.draw_text("Score", SMALL_FONT, NEON_BLUE, x + 260, header_y + 16, align="right")
        self.draw_text("Time", SMALL_FONT, NEON_BLUE, x + 390, header_y + 16, align="right")
        self.draw_text("Date", SMALL_FONT, NEON_BLUE, x + w - 25, header_y + 16, align="right")

        # Rows
        row_y = header_y + 38
        row_h = 32

        if not self.sessions:
            self.draw_text("No session data available", FONT, WHITE,
                           x + w // 2, y + h // 2)
            return

        for i, session in enumerate(self.sessions[:8]):
            row_rect = pygame.Rect(x + 10, row_y - 10, w - 20, row_h)

            if i % 2 == 0:
                pygame.draw.rect(self.screen, (35, 35, 60), row_rect, border_radius=6)

            game = session.get("game", "Unknown")
            score = session.get("score", 0)
            time_val = self.format_time(session.get("time", 0))
            date = session.get("date", "--")

            self.draw_text(game, SMALL_FONT, WHITE, x + 35, row_y + 5, align="left")
            self.draw_text(score, SMALL_FONT, NEON_PURPLE, x + 260, row_y + 5, align="right")
            self.draw_text(time_val, SMALL_FONT, NEON_BLUE, x + 390, row_y + 5, align="right")
            self.draw_text(date, SMALL_FONT, WHITE, x + w - 25, row_y + 5, align="right")

            row_y += row_h

    # ----------------------------------------------------- events
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.page_manager.set_page(
                    DrawMainPage(
                        self.screen,
                        self.page_manager,
                        self.username,
                        self.handler
                    )
                )

    # ----------------------------------------------------- draw
    def draw(self):
        self.screen.fill(DARK_BG)
        draw_stars(self.screen)

        mouse_pos = pygame.mouse.get_pos()

        # Title
        self.draw_text(
            f"{self.username}'s Profile",
            BIG_FONT,
            NEON_BLUE,
            WIDTH // 2,
            70
        )

        # Back button
        self.draw_button(self.back_button, "Back", mouse_pos)

        # Stats row
        card_w = 180
        card_h = 80
        gap = 20
        start_x = (WIDTH - (card_w * 3 + gap * 2)) // 2
        y = 120

        self.draw_stat_card(
            "Sessions",
            self.stats["total_sessions"],
            start_x,
            y,
            card_w,
            card_h,
            NEON_BLUE
        )

        self.draw_stat_card(
            "Best Score",
            self.stats["best_score"],
            start_x + card_w + gap,
            y,
            card_w,
            card_h,
            NEON_PURPLE
        )

        self.draw_stat_card(
            "Best Time",
            self.format_time(self.stats["best_time"]),
            start_x + (card_w + gap) * 2,
            y,
            card_w,
            card_h,
            NEON_BLUE
        )

        # Sessions table
        self.draw_sessions_panel(90, 240, WIDTH - 180, 320)

class DrawSearchUserPage:
    def __init__(self, screen, page_manager, handler):
        self.screen = screen
        self.page_manager = page_manager
        self.handler = handler
        self.back_button = pygame.Rect(40, 40, 120, 42)
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
            if self.back_button.collidepoint(event.pos):
                self.page_manager.set_page(
                    DrawMainPage(self.screen, self.page_manager, self.page_manager.username, self.handler)
                )
                return

            if self.input_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

            # Click suggestion -> autofill
            for name, rect in self.suggestion_rects:
                if rect.collidepoint(event.pos):
                    self.text = name
                    self.update_suggestions()

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
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

        draw_glow_rect(
            self.screen,
            self.back_button,
            PANEL,
            NEON_BLUE if self.back_button.collidepoint(mouse_pos) else NEON_PURPLE
        )

        self.draw_text(
            "Back",
            FONT,
            WHITE,
            self.back_button.centerx,
            self.back_button.centery
        )
        for name, rect in self.suggestion_rects:
            pygame.draw.rect(self.screen, PANEL, rect, border_radius=6)
            pygame.draw.rect(self.screen, NEON_PURPLE, rect, 1, border_radius=6)

            text_surface = SMALL_FONT.render(name, True, WHITE)
            self.screen.blit(text_surface, (rect.x + 10, rect.y + 10))