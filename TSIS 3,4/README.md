# TSIS 3,4 Projects

## Install
```bash
pip install -r requirements.txt
```

## Snake (TSIS 4)
1. Create PostgreSQL database (default: `snake_db`).
2. Run schema from `snake_game/schema.sql`.
3. Optionally set env vars: `SNAKE_DB_NAME`, `SNAKE_DB_USER`, `SNAKE_DB_PASSWORD`, `SNAKE_DB_HOST`, `SNAKE_DB_PORT`.
4. Start: `python snake_game/main.py`

## Racer (TSIS 3)
Start: `python racer_game/main.py`

## Controls
- Menus: `UP/DOWN`, `ENTER`, `ESC` (on leaderboard)
- Snake: arrows
- Racer: left/right arrows
