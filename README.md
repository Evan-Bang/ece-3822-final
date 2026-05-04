# Null Ptr Arcade
Owen Ringrose, Evan Bang, Emmanuel Morales-Negron
> ECE 3822 Spring 2026 Final Project

A multiplayer online arcade platform hosting a library of 25+ games, complete with user profiles, leaderboards, in-game chat, and a searchable game browser.

---

## Overview

Null Ptr Arcade is a client-server application that brings players together through a shared gaming platform. This project's primary purpose is to explore data structures such as BST's, Hashtables, Queues, and Tries. 

---

## Features

- **Ability to host many Games** — 5 games included but it is simple to add more.
- **Online Multiplayer** — Co-Op mulitplayer handled by our C++ game server
- **In-Game Text Chat** — Communicate with connected players in real time. Filters words from chats
- **User Profiles** — Track your stats and history across games
- **Leaderboards** — Individual leaderboards for every game
- **Search & Filter** — Easily browse and discover users on the platform
- **Automatic Backups and persistance** game and palyer data are store in json files backed up automatically.

---

## Game Library (Sample)

| # | Title | Genre | Multiplayer | Scoring |
|---|-------|-------|-------------|---------|
| 1 | Surviving 1111 | RPG | Shared World Co-op | Session duration, XP |
| 2 | Thellusoma | CRPG | Co-op |Session duration|
| 3 | Lizzy's Adventure | Adventure / RPG | Co-op | Session duration, EXP ||

---

## Architecture

The project is organized around a Python server and Python client, communicating over a network to support multiplayer sessions and real-time chat.

- **Server** — Manages user data and leaderboards
- **Client** — Provides the UI, game browser, and in-game interface
- **Game Server** - Handles game movement and chats
- **Data Structures** — Designed to efficiently support a large game library and concurrent users

---
## How to run

To run the server first make the game server
```
cd game_server
make clean
make
```
Then run the python server
```
cd platform_server/code
python server.py
```
Note this has to be ran on the ECE-000 server as this is hardcoded with our networking.

On the client:
```
cd python_client/code
python client.py
```
Enjoy!

Note if needed you can change what ports are used by editing ports.txt

---

## Course

ECE 3822 — Spring 2026