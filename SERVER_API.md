# Server API Reference

The server communicates over TCP using newline-delimited JSON messages. Every request and response is a JSON object followed by `\n`.


---

## Request Format

Send a JSON object with a `type` field and any required parameters:

```json
{"type": "request_type", "param1": "value1", ...}
```

## Response Format

All responses include a `success` boolean:

```json
{"success": true, ...}
{"success": false, "message": "error description"}
```

---

## Messages

### `login`
Authenticate an existing user.

**Request:**
```json
{"type": "login", "username": "alice", "password": "secret"}
```

**Response:**
```json
{"success": true, "message": "..."}
```

---

### `create_account`
Register a new user account.

**Request:**
```json
{"type": "create_account", "username": "alice", "password": "secret"}
```

**Response:**
```json
{"success": true, "message": "..."}
```

---

### `get_user_data`
Get a user's profile and session history.

**Request:**
```json
{"type": "get_user_data", "username": "alice"}
```

**Response:**
```json
{
  "success": true,
  "user_data": {
    "username": "alice",
    "sessions": [...]
  }
}
```

---

### `get_sessions`
Get the session list for a user.

**Request:**
```json
{"type": "get_sessions", "username": "alice"}
```

**Response:**
```json
{"success": true, "sessions": [...]}
```

---

### `get_leaderboard`
Get the top 100 players for a game by score and playtime.

**Request:**
```json
{"type": "get_leaderboard", "game_name": "Surviving 1111"}
```

**Response:**
```json
{
  "success": true,
  "score_leaderboard": [{"uuid": "alice", "score": 9500}, ...],
  "time_leaderboard":  [{"uuid": "alice", "time": 3600}, ...]
}
```

---

### `get_player_score`
Get a specific player's score and playtime for a game.

**Request:**
```json
{"type": "get_player_score", "username": "alice", "game_name": "Surviving 1111"}
```

**Response:**
```json
{"success": true, "score": 9500, "time": 3600}
```

---

### `ranged_query`
Query leaderboard entries within a score or time range.

**Request:**
```json
{
  "type": "ranged_query",
  "game_name": "Surviving 1111",
  "min_score": 1000,
  "max_score": 5000,
  "min_time": 60,
  "max_time": 3600
}
```

All four range fields are optional — include only the ones you need.

**Response:**
```json
{
  "success": true,
  "score_results": [{"uuid": "alice", "score": 3200}, ...],
  "time_results":  [{"uuid": "alice", "time": 120}, ...]
}
```

---

### `prefix_search`
Search for usernames by prefix (used for autocomplete).

**Request:**
```json
{"type": "prefix_search", "prefix": "ali"}
```

**Response:**
```json
{"success": true, "results": ["alice", "ali_g", ...]}
```

---

### `game_summary` *(sent by C++ game server)*
Submit a game session result. This is called by the game server automatically when a session ends — not by the client.

**Request:**
```json
{
  "type": "game_summary",
  "username": "alice",
  "game_name": "Surviving 1111",
  "score": 9500,
  "playtime": 3600
}
```

**Response:**
```json
{"success": true, "message": "Summary processed"}
```


---

This file was formatted using AI.