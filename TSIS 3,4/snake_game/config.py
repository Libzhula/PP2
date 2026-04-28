import os

DB_NAME = os.getenv("SNAKE_DB_NAME", "snake_db")
DB_USER = os.getenv("SNAKE_DB_USER", "postgres")
DB_PASSWORD = os.getenv("SNAKE_DB_PASSWORD", "postgres")
DB_HOST = os.getenv("SNAKE_DB_HOST", "localhost")
DB_PORT = int(os.getenv("SNAKE_DB_PORT", "5432"))

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL = 20
GRID_W = WINDOW_WIDTH // CELL
GRID_H = WINDOW_HEIGHT // CELL
