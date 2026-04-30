"""
session_handler.py
Author: Owen Ringrose
Date: 4/30/2026
Helper class to manage sessions. Used for sorting and filtering.
**** Revision History ****
- 4/30/2026: file created
"""
import sys
from python_server_handler import UserData
sys.path.append('../..')
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable


class SessionHandler:
    """
    Helper class that fetches and parses user session data from the server.
    Owns all session logic so UI pages don't need to know about raw response shapes.
    """
    def __init__(self, handler):
        self.handler = handler

        self.sessions       = ArrayList()   # ArrayList of HashTable, one per session
        self.loaded         = False
        self.error          = None

        # Computed stats
        self.total_sessions = 0
        self.best_score     = 0
        self.best_time      = 0
        self.games_played   = ArrayList()   # unique game names

    # ------------------------------------------------------------------ load
    def load(self, username):
        """Fetch and parse session data for the given username. Returns True on success."""
        self.sessions = ArrayList()
        self.loaded   = False
        self.error    = None

        try:
            user     = UserData(self.handler)
            response = user.get_user_data(username)

            # response itself is a JSON dict
            if not response or not response.get("success"):
                self.error = (
                    response.get("message", "Failed to load user data")
                    if response else "No response from server"
                )
                return False

            # Get sessions from server response
            raw_sessions = response.get("user_data", {}).get("sessions", [])

            # Convert into hashtable data struct
            for s in raw_sessions:
                # Parse each raw JSON dict into a HashTable
                session = HashTable()
                session.set("game",  s.get("GAME","Unknown"))
                session.set("score", s.get("SCORE",0))
                session.set("time",  s.get("PLAYTIME",0))
                session.set("date",  s.get("DATE","--"))
                self.sessions.append(session)

            self._compute_stats()
            self.loaded = True
            return True

        except Exception as e:
            self.error = str(e)
            return False

    def _compute_stats(self):
        self.total_sessions = len(self.sessions)

        if self.total_sessions > 0:
            self.best_score = 0
            self.best_time  = 0
            self.games_played = ArrayList()

            for i in range(len(self.sessions)):
                s = self.sessions[i]
                score = s.get("score")
                time  = s.get("time")
                game  = s.get("game")

                if score > self.best_score:
                    self.best_score = score
                if time > self.best_time:
                    self.best_time = time

                # Track unique games
                found = False
                for j in range(len(self.games_played)):
                    if self.games_played[j] == game:
                        found = True
                        break
                if not found:
                    self.games_played.append(game)
        else:
            self.best_score   = 0
            self.best_time    = 0
            self.games_played = ArrayList()

    # ---------------------------------------------------------------- queries
    def get_sessions(self, game=None, limit=None):
        """Return an ArrayList of sessions, optionally filtered by game and/or capped."""
        result = ArrayList()

        for i in range(len(self.sessions)):
            s = self.sessions[i]
            if game is None or s.get("game") == game:
                result.append(s)

        if limit is not None:
            capped = ArrayList()
            for i in range(min(limit, len(result))):
                capped.append(result[i])
            return capped

        return result

    def get_best_score_for(self, game):
        """Best score the user achieved in a specific game. Returns None if no data."""
        best  = None
        for i in range(len(self.sessions)):
            s = self.sessions[i]
            if s.get("game") == game:
                score = s.get("score")
                if best is None or score > best:
                    best = score
        return best

    def get_best_time_for(self, game):
        """Best (longest) survival time in a specific game. Returns None if no data."""
        best = None
        for i in range(len(self.sessions)):
            s = self.sessions[i]
            if s.get("game") == game:
                t = s.get("time")
                if best is None or t > best:
                    best = t
        return best
    def sort_sessions(self, key="score", descending=True):
        """Return a sorted ArrayList of sessions using merge sort."""
        return self._merge_sort(self.sessions, key, descending)

    def _merge_sort(self, arr, key, descending):
        """Merge sort algorighm,https://www.geeksforgeeks.org/dsa/merge-sort/"""
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = ArrayList()
        right = ArrayList()

        for i in range(mid):
            left.append(arr[i])
        for i in range(mid, len(arr)):
            right.append(arr[i])

        left  = self._merge_sort(left, key, descending)
        right = self._merge_sort(right, key, descending)
        return self._merge(left, right, key, descending)

    def _merge(self, left, right, key, descending):
        """Merges two arrays for merge sort"""
        result = ArrayList()
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            lv = left[i].get(key)
            rv = right[j].get(key)
            if (lv >= rv) if descending else (lv <= rv):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            i += 1
        while j < len(right):
            result.append(right[j])
            j += 1

        return result
    # --------------------------------------------------------------- helpers
    @staticmethod
    def format_time(seconds):
        seconds = int(float(seconds))
        m, s = divmod(seconds, 60)
        return f"{m}m {s:02d}s" if m else f"{s}s"

    @staticmethod
    def format_score(score):
        return f"{int(score):,}"