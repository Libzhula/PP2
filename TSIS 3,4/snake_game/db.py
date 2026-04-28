import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


def init_db():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
            """
        )


def get_or_create_player(username: str) -> int:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id FROM players WHERE username=%s", (username,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
        return cur.fetchone()[0]


def save_session(username: str, score: int, level: int):
    player_id = get_or_create_player(username)
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO game_sessions(player_id, score, level_reached) VALUES(%s, %s, %s)",
            (player_id, score, level),
        )


def top10():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.username, g.score, g.level_reached, g.played_at
            FROM game_sessions g
            JOIN players p ON p.id = g.player_id
            ORDER BY g.score DESC, g.played_at ASC
            LIMIT 10
            """
        )
        return cur.fetchall()


def personal_best(username: str) -> int:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT COALESCE(MAX(g.score), 0)
            FROM game_sessions g
            JOIN players p ON p.id = g.player_id
            WHERE p.username = %s
            """,
            (username,),
        )
        return cur.fetchone()[0]
