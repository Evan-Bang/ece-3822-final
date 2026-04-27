"""
chat_ui.py - In-game chat overlay for the multiplayer pygame game.

Usage
-----
1. Drop this file next to level.py.
2. Follow the integration comments in level.py (search for CHAT INTEGRATION).

Controls
--------
  Enter       – open / send message
  Escape      – cancel / close without sending
  Backspace   – delete last character
"""

import pygame
import time
from datastructures.array import ArrayList
from datastructures.circular_buffer import CircularBuffer

# ── Visual constants ──────────────────────────────────────────────────────────
CHAT_WIDTH        = 420          # px, fixed width
CHAT_MAX_VISIBLE  = 10           # message rows shown in the log
CHAT_MSG_HEIGHT   = 22           # px per message row
CHAT_INPUT_HEIGHT = 30           # px for the text-input row
CHAT_PADDING      = 8            # inner padding
CHAT_ALPHA        = 210          # background opacity (0-255)
CHAT_FADE_SECS    = 6.0          # seconds before inactive log fades out
CHAT_MAX_HISTORY  = 200          # maximum messages kept in memory; CircularBuffer capacity
CHAT_MAX_CHARS    = 80           # character limit per message

# Colour palette – retro amber terminal on dark glass
COL_BG         = (10,  12,  20,  CHAT_ALPHA)  # near-black background
COL_BORDER     = (80, 140, 200, 180)           # cool-blue border
COL_INPUT_BG   = (20,  25,  40, 230)          # slightly lighter input row
COL_CURSOR     = (100, 200, 255, 255)          # blinking cursor bar
COL_SELF       = (120, 230, 120)               # your own messages: soft green
COL_OTHER      = (180, 200, 240)               # others: steel blue-white
COL_SYSTEM     = (160, 120, 220)               # system notices: lavender
COL_TIMESTAMP  = ( 80,  90, 110)               # dim timestamp text
COL_PROMPT     = ( 60, 160, 255)               # ">" prompt glyph


class ChatMessage:
    """One entry in the message history."""
    __slots__ = ('sender', 'text', 'color', 'timestamp', 'is_system')

    def __init__(self, sender: str, text: str, color, is_system: bool = False):
        self.sender    = sender
        self.text      = text
        self.color     = color
        self.timestamp = time.time()
        self.is_system = is_system


class ChatUI:
    """
    In-game chat overlay widget.

    Parameters
    ----------
    player_name : str
        Local player's display name.
    screen_w, screen_h : int
        Current display dimensions (used for positioning).
    font_path : str | None
        Optional path to a TTF font.  Falls back to pygame's built-in if None.
    """

    def __init__(self, player_name: str, screen_w: int, screen_h: int,
                 font_path: str | None = None):
        self.player_name = player_name
        self.screen_w    = screen_w
        self.screen_h    = screen_h

        # State
        self.active       = False   # is the input box open?
        self.input_text   = ""
        # CircularBuffer auto-evicts the oldest message once capacity is hit,
        # matching the old deque(maxlen=...) behaviour exactly.
        self.messages     = CircularBuffer(CHAT_MAX_HISTORY)
        self._last_activity = 0.0   # epoch time of last message received/sent

        # Cursor blink
        self._cursor_visible = True
        self._cursor_timer   = 0
        self.scroll_offset = 0

        # Fonts
        try:
            if font_path:
                self.font      = pygame.font.Font(font_path, 14)
                self.font_bold = pygame.font.Font(font_path, 14)
            else:
                raise FileNotFoundError
        except Exception:
            self.font      = pygame.font.SysFont('courier', 14)
            self.font_bold = pygame.font.SysFont('courier', 14, bold=True)

        # Pre-compute geometry
        self._log_height = CHAT_MAX_VISIBLE * CHAT_MSG_HEIGHT + CHAT_PADDING * 2
        self._total_h    = self._log_height + CHAT_INPUT_HEIGHT
        self._x          = CHAT_PADDING * 2
        self._y          = screen_h - self._total_h - CHAT_PADDING * 2

        # Surfaces (rebuilt each draw due to alpha; cached for perf)
        self._bg_surf  = pygame.Surface((CHAT_WIDTH, self._log_height), pygame.SRCALPHA)
        self._inp_surf = pygame.Surface((CHAT_WIDTH, CHAT_INPUT_HEIGHT), pygame.SRCALPHA)

        # System welcome message
        self._push(ChatMessage("System",
                               f"Welcome, {player_name}!  Press Enter to chat.",
                               COL_SYSTEM, is_system=True))

    # ── Public API ────────────────────────────────────────────────────────────

    def add_message(self, sender: str, text: str):
        """Add an incoming message from another player (or the server)."""
        is_self   = (sender == self.player_name)
        color     = COL_SELF if is_self else COL_OTHER
        self._push(ChatMessage(sender, text, color))

    def add_system_message(self, text: str):
        """Add a system / server notification."""
        self._push(ChatMessage("System", text, COL_SYSTEM, is_system=True))

    def handle_event(self, event: pygame.event.Event):
        """
        Feed pygame events here.

        Returns
        -------
        str | None
            The composed message string if the player pressed Enter to send,
            otherwise None.
        """
        if event.type == pygame.KEYDOWN:
            if not self.active:
                if event.key == pygame.K_RETURN:
                    self.active = True
                return None

            # ── Input is open ──
            if event.key == pygame.K_RETURN:
                return self._send()

            elif event.key == pygame.K_ESCAPE:
                self.active     = False
                self.input_text = ""
                return None

            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]

          
            else:
                char = event.unicode
                if char and char.isprintable() and len(self.input_text) < CHAT_MAX_CHARS:
                    self.input_text += char

        if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y   # wheel up = positive y
                max_scroll = max(0, self.messages.size() - CHAT_MAX_VISIBLE)
                self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        
        return None

    def draw(self, surface: pygame.Surface, dt: float = 1 / 60):
        """Render the chat overlay onto *surface*."""
        # Determine opacity: fade log out when idle and input is closed
        idle_secs = time.time() - self._last_activity
        if self.active or idle_secs < CHAT_FADE_SECS:
            log_alpha = 255
        elif idle_secs < CHAT_FADE_SECS + 2.0:
            log_alpha = int(255 * (1.0 - (idle_secs - CHAT_FADE_SECS) / 2.0))
        else:
            log_alpha = 0

        if log_alpha <= 0 and not self.active:
            return   # nothing to draw

        # ── Message log ──
        bg = self._bg_surf
        bg.fill(COL_BG)
        pygame.draw.rect(bg, COL_BORDER, bg.get_rect(), 1)

        # Build an ArrayList of the last CHAT_MAX_VISIBLE messages from the
        # CircularBuffer so we can iterate them in order without a plain list.
        count   = self.messages.size()
        start = max(0, count - CHAT_MAX_VISIBLE - self.scroll_offset)
        end   = start + CHAT_MAX_VISIBLE

        visible = ArrayList(initial_capacity=CHAT_MAX_VISIBLE)

        for i in range(start, min(end, count)):
            visible.append(self.messages[i])

        for i in range(len(visible)):
            msg = visible[i]
            y = CHAT_PADDING + i * CHAT_MSG_HEIGHT

            # Timestamp
            ts = time.strftime('%H:%M', time.localtime(msg.timestamp))
            ts_surf = self.font.render(ts, True, COL_TIMESTAMP)
            bg.blit(ts_surf, (CHAT_PADDING, y))

            # Sender (bold colour)
            sender_lbl = f"{msg.sender}: " if not msg.is_system else "• "
            s_surf = self.font_bold.render(sender_lbl, True, msg.color)
            sender_x  = CHAT_PADDING + ts_surf.get_width() + 6
            bg.blit(s_surf, (sender_x, y))

            # Message body
            body_x   = sender_x + s_surf.get_width()
            max_body = CHAT_WIDTH - body_x - CHAT_PADDING
            body_str = self._truncate(msg.text, max_body)
            b_surf   = self.font.render(body_str, True, msg.color)
            bg.blit(b_surf, (body_x, y))

        bg.set_alpha(log_alpha)
        surface.blit(bg, (self._x, self._y))

        # ── Input row (only when active) ──
        if self.active:
            inp = self._inp_surf
            inp.fill(COL_INPUT_BG)
            pygame.draw.rect(inp, COL_BORDER, inp.get_rect(), 1)

            # Prompt glyph
            p_surf = self.font_bold.render("> ", True, COL_PROMPT)
            inp.blit(p_surf, (CHAT_PADDING, (CHAT_INPUT_HEIGHT - p_surf.get_height()) // 2))
            text_x = CHAT_PADDING + p_surf.get_width()

            # Typed text
            max_inp = CHAT_WIDTH - text_x - CHAT_PADDING - 4
            display = self._truncate_left(self.input_text, max_inp)
            t_surf  = self.font.render(display, True, COL_SELF)
            ty = (CHAT_INPUT_HEIGHT - t_surf.get_height()) // 2
            inp.blit(t_surf, (text_x, ty))

            # Blinking cursor
            self._cursor_timer += dt
            if self._cursor_timer >= 0.5:
                self._cursor_timer   = 0
                self._cursor_visible = not self._cursor_visible
            if self._cursor_visible:
                cx = text_x + t_surf.get_width() + 2
                cy = ty
                pygame.draw.rect(inp, COL_CURSOR, (cx, cy, 2, t_surf.get_height()))

            inp.set_alpha(240)
            surface.blit(inp, (self._x, self._y + self._log_height))

    # ── Internals ─────────────────────────────────────────────────────────────

    def _push(self, msg: ChatMessage):
        self.messages.push(msg)   # CircularBuffer.push; evicts oldest when full
        self._last_activity = time.time()

    def _send(self) -> str | None:
        text = self.input_text.strip()
        self.input_text = ""
        self.active     = False
        if not text:
            return None
        # Echo locally so sender sees their own message immediately
        self._push(ChatMessage(self.player_name, text, COL_SELF))
        return text

    def _truncate(self, text: str, max_px: int) -> str:
        """Clip text to fit within max_px, appending '…' if cut."""
        if self.font.size(text)[0] <= max_px:
            return text
        while text and self.font.size(text + '…')[0] > max_px:
            text = text[:-1]
        return text + '…'

    def _truncate_left(self, text: str, max_px: int) -> str:
        """Show the *end* of a long string (like a text input box)."""
        if self.font.size(text)[0] <= max_px:
            return text
        while text and self.font.size('…' + text)[0] > max_px:
            text = text[1:]
        return '…' + text