import random
import pygame

from persistence import load_settings, save_settings, load_leaderboard, save_result

W, H = 500, 700
LANES_X = [100, 200, 300]


class RacerGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("TSIS 3 Racer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 28)
        self.small = pygame.font.SysFont("arial", 20)
        self.settings = load_settings()
        self.state = "menu"
        self.menu_index = 0
        self.settings_index = 0
        self.username = ""
        self.reset_run()

    def reset_run(self):
        self.player = pygame.Rect(200, 600, 60, 90)
        self.speed = 7
        self.road_scroll = 0
        self.coins = []
        self.traffic = []
        self.hazards = []
        self.events = []
        self.powerups = []
        self.active_power = None
        self.power_until = 0
        self.shield_hits = 0
        self.repair_count = 0
        self.score = 0
        self.coin_score = 0
        self.distance = 0
        self.finish_distance = 4000
        self.spawn_tick = 0

    def spawn_objects(self):
        lane = random.choice(LANES_X)
        if random.random() < 0.08 and abs(lane - self.player.x) > 40:
            self.traffic.append(pygame.Rect(lane, -100, 60, 90))
        if random.random() < 0.08 and abs(lane - self.player.x) > 40:
            kind = random.choice(["barrier", "oil", "pothole", "slow"])
            self.hazards.append({"rect": pygame.Rect(lane + 5, -60, 50, 50), "kind": kind})
        if random.random() < 0.03:
            self.coins.append({"rect": pygame.Rect(lane + 20, -30, 20, 20), "value": random.choice([1, 2, 3])})
        if random.random() < 0.015 and not self.powerups:
            k = random.choice(["nitro", "shield", "repair"])
            self.powerups.append({"kind": k, "rect": pygame.Rect(lane + 15, -30, 30, 30), "spawn": pygame.time.get_ticks()})
        if random.random() < 0.02:
            self.events.append({"kind": random.choice(["moving_barrier", "boost_strip"]), "rect": pygame.Rect(random.choice(LANES_X), -80, 60, 25), "dx": random.choice([-2, 2])})

    def difficulty_mult(self):
        d = self.settings.get("difficulty", "normal")
        return {"easy": 0.8, "normal": 1.0, "hard": 1.25}.get(d, 1.0)

    def update_run(self):
        now = pygame.time.get_ticks()
        mult = self.difficulty_mult()
        cur_speed = self.speed * mult
        if self.active_power == "nitro" and now < self.power_until:
            cur_speed += 4
        elif self.active_power == "nitro" and now >= self.power_until:
            self.active_power = None

        self.distance += cur_speed
        self.score = int(self.coin_score * 10 + self.distance / 8)

        self.spawn_tick += 1
        density = 1 + int(self.distance / 1200)
        if self.spawn_tick % max(10, int(30 / density)) == 0:
            self.spawn_objects()

        for car in self.traffic:
            car.y += int(cur_speed + 2)
        for h in self.hazards:
            h["rect"].y += int(cur_speed)
        for c in self.coins:
            c["rect"].y += int(cur_speed)
        for p in self.powerups:
            p["rect"].y += int(cur_speed)
        for ev in self.events:
            ev["rect"].y += int(cur_speed + 1)
            if ev["kind"] == "moving_barrier":
                ev["rect"].x += ev["dx"]
                if ev["rect"].x < 80 or ev["rect"].x > 340:
                    ev["dx"] *= -1

        self.traffic = [x for x in self.traffic if x.y < H + 120]
        self.hazards = [x for x in self.hazards if x["rect"].y < H + 80]
        self.coins = [x for x in self.coins if x["rect"].y < H + 40]
        self.events = [x for x in self.events if x["rect"].y < H + 80]
        self.powerups = [x for x in self.powerups if (x["rect"].y < H + 40 and now - x["spawn"] < 8000)]

        for c in self.coins[:]:
            if self.player.colliderect(c["rect"]):
                self.coin_score += c["value"]
                self.coins.remove(c)

        for p in self.powerups[:]:
            if self.player.colliderect(p["rect"]):
                if p["kind"] == "nitro":
                    self.active_power = "nitro"
                    self.power_until = now + random.randint(3000, 5000)
                elif p["kind"] == "shield":
                    self.active_power = "shield"
                    self.shield_hits = 1
                elif p["kind"] == "repair":
                    self.repair_count += 1
                self.powerups.remove(p)

        collisions = []
        collisions += [obj for obj in self.traffic if self.player.colliderect(obj)]
        collisions += [obj for obj in self.events if self.player.colliderect(obj["rect"]) and obj["kind"] == "moving_barrier"]
        for hz in self.hazards:
            if self.player.colliderect(hz["rect"]):
                if hz["kind"] == "slow":
                    self.speed = max(5, self.speed - 0.02)
                else:
                    collisions.append(hz)

        if collisions:
            if self.shield_hits > 0:
                self.shield_hits = 0
                self.active_power = None
            elif self.repair_count > 0:
                self.repair_count -= 1
            else:
                save_result(self.username or "player", self.score, self.distance)
                self.state = "game_over"

        if self.distance >= self.finish_distance:
            save_result(self.username or "player", self.score + 500, self.distance)
            self.state = "game_over"

    def draw_run(self):
        self.screen.fill((30, 30, 30))
        pygame.draw.rect(self.screen, (60, 60, 60), (70, 0, 360, H))
        self.road_scroll = (self.road_scroll + 8) % 60
        for y in range(-60, H, 60):
            pygame.draw.rect(self.screen, (255, 255, 255), (245, y + self.road_scroll, 10, 30))

        for c in self.coins:
            pygame.draw.circle(self.screen, (255, 220, 0), c["rect"].center, 10)
        for t in self.traffic:
            pygame.draw.rect(self.screen, (220, 70, 70), t)
        for hz in self.hazards:
            col = {"barrier": (220, 120, 80), "oil": (20, 20, 20), "pothole": (110, 90, 90), "slow": (80, 120, 220)}[hz["kind"]]
            pygame.draw.rect(self.screen, col, hz["rect"])
        for ev in self.events:
            col = (255, 0, 120) if ev["kind"] == "moving_barrier" else (0, 255, 120)
            pygame.draw.rect(self.screen, col, ev["rect"])
        for p in self.powerups:
            col = {"nitro": (0, 255, 255), "shield": (180, 0, 255), "repair": (0, 255, 120)}[p["kind"]]
            pygame.draw.rect(self.screen, col, p["rect"])

        pygame.draw.rect(self.screen, tuple(self.settings.get("car_color", [50, 180, 255])), self.player)
        self.screen.blit(self.small.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))
        self.screen.blit(self.small.render(f"Coins: {self.coin_score}", True, (255, 255, 255)), (10, 35))
        remain = max(0, int(self.finish_distance - self.distance))
        self.screen.blit(self.small.render(f"Distance: {int(self.distance)} / {self.finish_distance} (left {remain})", True, (255, 255, 255)), (10, 60))
        if self.active_power:
            label = self.active_power
            if self.active_power == "nitro":
                label += f" {(self.power_until - pygame.time.get_ticks()) // 1000}s"
            self.screen.blit(self.small.render(f"Power: {label}", True, (255, 230, 120)), (10, 85))

    def draw_menu(self):
        self.screen.fill((20, 25, 40))
        self.screen.blit(self.font.render("Racer TSIS3", True, (255, 255, 255)), (170, 80))
        self.screen.blit(self.small.render("Username: " + self.username, True, (220, 220, 220)), (150, 140))
        items = ["Play", "Leaderboard", "Settings", "Quit"]
        for i, it in enumerate(items):
            c = (255, 220, 120) if i == self.menu_index else (220, 220, 220)
            self.screen.blit(self.font.render(it, True, c), (200, 220 + i * 55))

    def draw_leaderboard(self):
        self.screen.fill((10, 10, 20))
        self.screen.blit(self.font.render("Top 10", True, (255, 255, 255)), (210, 40))
        rows = load_leaderboard()
        y = 110
        for i, r in enumerate(rows, 1):
            self.screen.blit(self.small.render(f"{i}. {r['name']}  Score:{r['score']}  Dist:{r['distance']}", True, (220, 220, 220)), (70, y))
            y += 34
        self.screen.blit(self.small.render("ESC - Back", True, (180, 180, 180)), (20, 660))

    def draw_settings(self):
        self.screen.fill((35, 20, 35))
        self.screen.blit(self.font.render("Settings", True, (255, 255, 255)), (180, 60))
        opts = [
            f"Sound: {'ON' if self.settings['sound'] else 'OFF'}",
            f"Car color: {self.settings['car_color']}",
            f"Difficulty: {self.settings['difficulty']}",
            "Save & Back",
        ]
        for i, opt in enumerate(opts):
            c = (255, 220, 120) if i == self.settings_index else (220, 220, 220)
            self.screen.blit(self.font.render(opt, True, c), (90, 170 + i * 70))

    def draw_game_over(self):
        self.screen.fill((50, 0, 0))
        self.screen.blit(self.font.render("Game Over", True, (255, 255, 255)), (170, 140))
        self.screen.blit(self.small.render(f"Score: {self.score}", True, (255, 255, 255)), (210, 220))
        self.screen.blit(self.small.render(f"Distance: {int(self.distance)}", True, (255, 255, 255)), (210, 250))
        self.screen.blit(self.small.render(f"Coins: {self.coin_score}", True, (255, 255, 255)), (210, 280))
        self.screen.blit(self.small.render("R: Retry  M: Main Menu", True, (255, 220, 120)), (150, 340))

    def run(self):
        running = True
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
                                self.reset_run()
                                self.state = "game"
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
                        if e.key == pygame.K_LEFT:
                            self.player.x = max(80, self.player.x - 100)
                        elif e.key == pygame.K_RIGHT:
                            self.player.x = min(320, self.player.x + 100)
                    elif self.state == "leaderboard" and e.key == pygame.K_ESCAPE:
                        self.state = "menu"
                    elif self.state == "settings":
                        if e.key == pygame.K_UP:
                            self.settings_index = (self.settings_index - 1) % 4
                        elif e.key == pygame.K_DOWN:
                            self.settings_index = (self.settings_index + 1) % 4
                        elif e.key == pygame.K_RETURN:
                            if self.settings_index == 0:
                                self.settings["sound"] = not self.settings["sound"]
                            elif self.settings_index == 1:
                                colors = [[50, 180, 255], [255, 120, 50], [120, 255, 120], [240, 240, 240]]
                                i = colors.index(self.settings["car_color"]) if self.settings["car_color"] in colors else 0
                                self.settings["car_color"] = colors[(i + 1) % len(colors)]
                            elif self.settings_index == 2:
                                dif = ["easy", "normal", "hard"]
                                i = dif.index(self.settings["difficulty"]) if self.settings["difficulty"] in dif else 1
                                self.settings["difficulty"] = dif[(i + 1) % len(dif)]
                            else:
                                save_settings(self.settings)
                                self.state = "menu"
                    elif self.state == "game_over":
                        if e.key == pygame.K_r:
                            self.reset_run()
                            self.state = "game"
                        elif e.key == pygame.K_m:
                            self.state = "menu"

            if self.state == "menu":
                self.draw_menu()
                fps = 30
            elif self.state == "game":
                self.update_run()
                self.draw_run()
                fps = 60
            elif self.state == "leaderboard":
                self.draw_leaderboard()
                fps = 30
            elif self.state == "settings":
                self.draw_settings()
                fps = 30
            else:
                self.draw_game_over()
                fps = 30

            pygame.display.flip()
            self.clock.tick(fps)

        pygame.quit()
