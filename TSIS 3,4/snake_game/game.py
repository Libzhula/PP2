import json
import random
import pygame
from dataclasses import dataclass

from config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL, GRID_W, GRID_H
import db

SETTINGS_PATH = "settings.json"


@dataclass
class PowerUp:
    kind: str
    pos: tuple[int, int]
    spawn_time: int


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("TSIS 4 Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.small = pygame.font.SysFont("arial", 18)
        self.settings = self.load_settings()
        self.state = "menu"
        self.username = ""
        self.personal_best = 0
        self.menu_index = 0
        self.settings_index = 0
        self.level_rows = []
        try:
            db.init_db()
            self.db_ok = True
        except Exception:
            self.db_ok = False
        self.reset_game()

    def load_settings(self):
        default = {"snake_color": [0, 200, 0], "grid_overlay": True, "sound": False}
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                default.update(loaded)
                return default
        except Exception:
            return default

    def save_settings(self):
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)

    def reset_game(self):
        self.snake = [(GRID_W // 2, GRID_H // 2), (GRID_W // 2 - 1, GRID_H // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.base_speed = 8
        self.normal_food = self.spawn_item()
        self.normal_food_weight = random.choice([1, 2, 3])
        self.food_spawn_tick = pygame.time.get_ticks()
        self.poison_food = self.spawn_item(blocked={self.normal_food})
        self.powerup = None
        self.active_power = None
        self.active_until = 0
        self.shield_hits = 0
        self.obstacles = set()
        self.game_over_reason = ""

    def spawn_item(self, blocked=None):
        if blocked is None:
            blocked = set()
        occupied = set(self.snake) | self.obstacles | set(blocked)
        while True:
            p = (random.randint(1, GRID_W - 2), random.randint(1, GRID_H - 2))
            if p not in occupied:
                return p

    def generate_obstacles_for_level(self):
        if self.level < 3:
            self.obstacles = set()
            return
        self.obstacles = set()
        need = min(8 + self.level * 2, 30)
        safe_zone = set((self.snake[0][0] + dx, self.snake[0][1] + dy) for dx in range(-2, 3) for dy in range(-2, 3))
        attempts = 0
        while len(self.obstacles) < need and attempts < 2000:
            attempts += 1
            p = (random.randint(1, GRID_W - 2), random.randint(1, GRID_H - 2))
            if p in safe_zone or p in self.snake:
                continue
            self.obstacles.add(p)

    def maybe_spawn_powerup(self, now):
        if self.powerup is None and random.random() < 0.01:
            kind = random.choice(["speed", "slow", "shield"])
            self.powerup = PowerUp(kind, self.spawn_item(blocked={self.normal_food, self.poison_food}), now)

    def update_food_timer(self, now):
        if now - self.food_spawn_tick > 6000:
            self.normal_food = self.spawn_item(blocked={self.poison_food})
            self.normal_food_weight = random.choice([1, 2, 3])
            self.food_spawn_tick = now

    def start_for_user(self):
        if self.db_ok and self.username.strip():
            try:
                self.personal_best = db.personal_best(self.username.strip())
            except Exception:
                self.personal_best = 0
        else:
            self.personal_best = 0
        self.reset_game()
        self.state = "game"

    def eat_food(self):
        self.score += self.normal_food_weight
        self.food_eaten += 1
        self.normal_food = self.spawn_item(blocked={self.poison_food})
        self.normal_food_weight = random.choice([1, 2, 3])
        self.food_spawn_tick = pygame.time.get_ticks()
        if self.food_eaten % 4 == 0:
            self.level += 1
            self.generate_obstacles_for_level()

    def eat_poison(self):
        if len(self.snake) <= 3:
            self.game_over_reason = "Poison food ended the run"
            self.state = "game_over"
            return
        self.snake = self.snake[:-2]
        self.poison_food = self.spawn_item(blocked={self.normal_food})

    def apply_power(self, kind, now):
        if kind == "shield":
            self.shield_hits = 1
            self.active_power = "shield"
            self.active_until = 0
        else:
            self.active_power = kind
            self.active_until = now + 5000

    def save_result(self):
        if self.db_ok and self.username.strip():
            try:
                db.save_session(self.username.strip(), self.score, self.level)
            except Exception:
                pass

    def draw_grid(self):
        if not self.settings.get("grid_overlay", True):
            return
        for x in range(0, WINDOW_WIDTH, CELL):
            pygame.draw.line(self.screen, (45, 45, 45), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL):
            pygame.draw.line(self.screen, (45, 45, 45), (0, y), (WINDOW_WIDTH, y))

    def draw_game(self):
        self.screen.fill((20, 20, 20))
        self.draw_grid()
        pygame.draw.rect(self.screen, (200, 50, 50), (*[v * CELL for v in self.normal_food], CELL, CELL))
        pygame.draw.rect(self.screen, (120, 0, 0), (*[v * CELL for v in self.poison_food], CELL, CELL))
        for o in self.obstacles:
            pygame.draw.rect(self.screen, (120, 120, 120), (o[0] * CELL, o[1] * CELL, CELL, CELL))
        if self.powerup:
            c = {"speed": (255, 180, 0), "slow": (0, 180, 255), "shield": (180, 0, 255)}[self.powerup.kind]
            pygame.draw.rect(self.screen, c, (self.powerup.pos[0] * CELL, self.powerup.pos[1] * CELL, CELL, CELL))
        snake_color = tuple(self.settings.get("snake_color", [0, 200, 0]))
        for s in self.snake:
            pygame.draw.rect(self.screen, snake_color, (s[0] * CELL, s[1] * CELL, CELL, CELL))
        info = f"Score:{self.score} Level:{self.level} Best:{self.personal_best}"
        self.screen.blit(self.small.render(info, True, (240, 240, 240)), (10, 10))
        if self.active_power:
            txt = self.active_power
            if self.active_until:
                left = max(0, (self.active_until - pygame.time.get_ticks()) // 1000)
                txt += f" {left}s"
            self.screen.blit(self.small.render(f"Power:{txt}", True, (240, 240, 120)), (10, 32))

    def update_game(self):
        now = pygame.time.get_ticks()
        self.update_food_timer(now)
        self.maybe_spawn_powerup(now)
        if self.powerup and now - self.powerup.spawn_time > 8000:
            self.powerup = None

        speed = self.base_speed + self.level
        if self.active_power == "speed" and now <= self.active_until:
            speed += 4
        elif self.active_power == "slow" and now <= self.active_until:
            speed = max(4, speed - 3)
        elif self.active_until and now > self.active_until:
            self.active_power = None
            self.active_until = 0

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        hit_wall = not (0 < new_head[0] < GRID_W - 1 and 0 < new_head[1] < GRID_H - 1)
        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles
        if hit_wall or hit_self or hit_obstacle:
            if self.shield_hits > 0:
                self.shield_hits = 0
                self.active_power = None
                return speed
            self.game_over_reason = "Collision"
            self.state = "game_over"
            self.save_result()
            return speed

        self.snake.insert(0, new_head)

        if new_head == self.normal_food:
            self.eat_food()
        elif new_head == self.poison_food:
            self.eat_poison()
            if self.state == "game_over":
                self.save_result()
                return speed
        else:
            self.snake.pop()

        if self.powerup and new_head == self.powerup.pos:
            self.apply_power(self.powerup.kind, now)
            self.powerup = None

        return speed

    def draw_menu(self):
        self.screen.fill((15, 30, 45))
        title = self.font.render("Snake TSIS4", True, (255, 255, 255))
        self.screen.blit(title, (320, 80))
        self.screen.blit(self.small.render("Username: " + self.username, True, (230, 230, 230)), (250, 150))
        items = ["Play", "Leaderboard", "Settings", "Quit"]
        for i, item in enumerate(items):
            c = (255, 220, 120) if i == self.menu_index else (220, 220, 220)
            self.screen.blit(self.font.render(item, True, c), (350, 220 + i * 50))

    def draw_leaderboard(self):
        self.screen.fill((10, 10, 20))
        self.screen.blit(self.font.render("Top 10", True, (255, 255, 255)), (360, 50))
        if self.db_ok:
            try:
                rows = db.top10()
            except Exception:
                rows = []
        else:
            rows = []
        y = 110
        for i, r in enumerate(rows, 1):
            line = f"{i}. {r[0]}  S:{r[1]}  L:{r[2]}  {r[3].strftime('%Y-%m-%d')}"
            self.screen.blit(self.small.render(line, True, (220, 220, 220)), (140, y))
            y += 36
        self.screen.blit(self.small.render("Press ESC to back", True, (180, 180, 180)), (20, 560))

    def draw_settings(self):
        self.screen.fill((30, 15, 30))
        self.screen.blit(self.font.render("Settings", True, (255, 255, 255)), (330, 60))
        opts = [
            f"Grid: {'ON' if self.settings['grid_overlay'] else 'OFF'}",
            f"Sound: {'ON' if self.settings['sound'] else 'OFF'}",
            f"Snake Color: {self.settings['snake_color']}",
            "Save & Back",
        ]
        for i, opt in enumerate(opts):
            c = (255, 220, 120) if i == self.settings_index else (220, 220, 220)
            self.screen.blit(self.font.render(opt, True, c), (230, 170 + i * 60))

    def draw_game_over(self):
        self.screen.fill((40, 0, 0))
        self.screen.blit(self.font.render("Game Over", True, (255, 255, 255)), (320, 120))
        self.screen.blit(self.small.render(f"Score: {self.score}", True, (255, 255, 255)), (340, 200))
        self.screen.blit(self.small.render(f"Level: {self.level}", True, (255, 255, 255)), (340, 230))
        best = max(self.personal_best, self.score)
        self.screen.blit(self.small.render(f"Best: {best}", True, (255, 255, 255)), (340, 260))
        self.screen.blit(self.small.render("R: Retry  M: Main Menu", True, (255, 220, 120)), (280, 320))

    def run(self):
        running = True
        fps = 10
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    if self.state == "menu":
                        if e.key == pygame.K_UP:
                            self.menu_index = (self.menu_index - 1) % 4
                        elif e.key == pygame.K_DOWN:
                            self.menu_index = (self.menu_index + 1) % 4
                        elif e.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        elif e.key == pygame.K_RETURN:
                            if self.menu_index == 0:
                                self.start_for_user()
                            elif self.menu_index == 1:
                                self.state = "leaderboard"
                            elif self.menu_index == 2:
                                self.state = "settings"
                            else:
                                running = False
                        elif e.unicode.isalnum() or e.unicode in "_-":
                            if len(self.username) < 16:
                                self.username += e.unicode
                    elif self.state == "game":
                        if e.key == pygame.K_UP and self.direction != (0, 1):
                            self.direction = (0, -1)
                        elif e.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.direction = (0, 1)
                        elif e.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.direction = (-1, 0)
                        elif e.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.direction = (1, 0)
                    elif self.state == "leaderboard" and e.key == pygame.K_ESCAPE:
                        self.state = "menu"
                    elif self.state == "settings":
                        if e.key == pygame.K_UP:
                            self.settings_index = (self.settings_index - 1) % 4
                        elif e.key == pygame.K_DOWN:
                            self.settings_index = (self.settings_index + 1) % 4
                        elif e.key == pygame.K_RETURN:
                            if self.settings_index == 0:
                                self.settings["grid_overlay"] = not self.settings["grid_overlay"]
                            elif self.settings_index == 1:
                                self.settings["sound"] = not self.settings["sound"]
                            elif self.settings_index == 2:
                                colors = [[0, 200, 0], [0, 180, 255], [255, 160, 0], [240, 240, 240]]
                                idx = colors.index(self.settings["snake_color"]) if self.settings["snake_color"] in colors else 0
                                self.settings["snake_color"] = colors[(idx + 1) % len(colors)]
                            else:
                                self.save_settings()
                                self.state = "menu"
                    elif self.state == "game_over":
                        if e.key == pygame.K_r:
                            self.start_for_user()
                        elif e.key == pygame.K_m:
                            self.state = "menu"

            if self.state == "menu":
                self.draw_menu()
                fps = 30
            elif self.state == "game":
                fps = self.update_game()
                self.draw_game()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
                fps = 30
            elif self.state == "settings":
                self.draw_settings()
                fps = 30
            elif self.state == "game_over":
                self.draw_game_over()
                fps = 30

            pygame.display.flip()
            self.clock.tick(fps)

        pygame.quit()
