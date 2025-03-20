import random
from pygame import Rect

WIDTH = 960
HEIGHT = 780

# game states: "menu", "playing", "game_over"
state = "menu"

hero_lives = 3
kill_count = 0
extra_life_counter = 0

# Music on by default
music_on = True
menu_sound = "background"
game_sound = "xwing"

if music_on and state == "menu":
    sounds.background.play(-1)  # loop

hero_frames = ["playership2_red", "playership2_orange"]
hero_frame_index = 0
hero_frame_timer = 0
hero_frame_delay = 35
hero = Actor(hero_frames[hero_frame_index], (WIDTH // 2, HEIGHT - 50))

enemies = []
for i in range(5):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(-150, -50)
    enemy = Actor("enemyblack2", (x, y))
    enemy.speed = random.randint(2, 10)
    enemies.append(enemy)

bullets = []
bullet_speed = 7

enemy_spawn_timer = 300
game_timer = 0
# boss comes after 1 minute
boss = None

def update():
    global state, hero_lives, kill_count, extra_life_counter, enemy_spawn_timer, game_timer, boss
    global hero_frame_timer, hero_frame_index
    if state == "playing":
        game_timer += 1
        hero_frame_timer += 1
        if hero_frame_timer >= hero_frame_delay:
            hero_frame_index = (hero_frame_index + 1) % len(hero_frames)
            hero.image = hero_frames[hero_frame_index]
            hero_frame_timer = 0
        # hero (xwing) moves
        if keyboard.left:
            hero.x -= 5
        if keyboard.right:
            hero.x += 5
        if keyboard.up:
            hero.y -= 5
        if keyboard.down:
            hero.y += 5
        hero.x = max(0, min(WIDTH, hero.x))
        hero.y = max(0, min(HEIGHT, hero.y))
        if enemy_spawn_timer > 0:
            enemy_spawn_timer -= 1
        else:
            for enemy in enemies:
                enemy.y += enemy.speed
                if enemy.y > HEIGHT + 50:
                    enemy.x = random.randint(50, WIDTH - 50)
                    enemy.y = random.randint(-150, -50)
                    enemy.speed = random.randint(2, 10)
                if hero.colliderect(enemy):
                    hero_lives -= 1
                    enemy.x = random.randint(50, WIDTH - 50)
                    enemy.y = random.randint(-150, -50)
                    enemy.speed = random.randint(2, 10)
                    if hero_lives <= 0:
                        state = "game_over"
                        if music_on:
                            sounds.game_over.play()
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)
            else:
                if enemy_spawn_timer <= 0:
                    for enemy in enemies:
                        if bullet.colliderect(enemy):
                            bullets.remove(bullet)
                            kill_count += 1
                            sounds.hit.play()
                            enemy.x = random.randint(50, WIDTH - 50)
                            enemy.y = random.randint(-150, -50)
                            enemy.speed = random.randint(2, 10)
                            if kill_count // 10 > extra_life_counter:
                                hero_lives += 1
                                extra_life_counter = kill_count // 10
                            break
                if boss is not None:
                    if bullet.colliderect(boss):
                        bullets.remove(bullet)
                        boss.health -= 1
                        sounds.hit.play()
                        if boss.health <= 0:
                            boss = None
                            kill_count += 1
                        break
        if game_timer >= 3600 and boss is None:
            boss = Actor("boss", (WIDTH // 2, -100))
            boss.health = 5
            boss.dx = 2
        if boss is not None:
            boss.y += 1
            boss.x += boss.dx
            if boss.x < 50 or boss.x > WIDTH - 50:
                boss.dx = -boss.dx
            if hero.colliderect(boss):
                hero_lives -= 2
                boss.y = -100
                if hero_lives <= 0:
                    state = "game_over"
                    if music_on:
                        sounds.game_over.play()

def draw():
    screen.clear()
    if state == "menu":
        screen.fill("darkblue")
        screen.draw.text("X-Wing", center=(WIDTH // 2, 100), fontsize=60, color="white")
        start_button = Rect((WIDTH // 2 - 100, 225), (200, 50))
        screen.draw.filled_rect(start_button, "darkred")
        screen.draw.text("Oyuna Başla", center=(WIDTH // 2, 250), fontsize=30, color="white")
        sound_button = Rect((WIDTH // 2 - 100, 295), (200, 50))
        screen.draw.filled_rect(sound_button, "darkred")
        screen.draw.text("Ses Aç/Kapa", center=(WIDTH // 2, 320), fontsize=30, color="white")
        exit_button = Rect((WIDTH // 2 - 100, 365), (200, 50))
        screen.draw.filled_rect(exit_button, "darkred")
        screen.draw.text("Çıkış", center=(WIDTH // 2, 390), fontsize=30, color="white")
    elif state == "playing":
        screen.fill("black")
        hero.draw()
        if enemy_spawn_timer <= 0:
            for enemy in enemies:
                enemy.draw()
        if boss is not None:
            boss.draw()
        for bullet in bullets:
            bullet.draw()
        screen.draw.text("Lives: " + str(hero_lives), (10, 10), fontsize=30, color="white")
        screen.draw.text("Kills: " + str(kill_count), (10, 50), fontsize=30, color="white")
    elif state == "game_over":
        screen.fill("black")
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        screen.draw.text("Kills: " + str(kill_count), center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")
        screen.draw.text("Press Enter ", center=(WIDTH // 2 , HEIGHT // 2-250),fontsize=40, color="white")

def on_mouse_down(pos):
    global state, music_on
    if state == "menu":
        start_button = Rect((WIDTH // 2 - 100, 225), (200, 50))
        sound_button = Rect((WIDTH // 2 - 100, 295), (200, 50))
        exit_button = Rect((WIDTH // 2 - 100, 365), (200, 50))
        if start_button.collidepoint(pos):
            state = "playing"
            sounds.start.play()
            if music_on:
                sounds.background.stop()
                sounds.xwing.play(-1)
        elif sound_button.collidepoint(pos):
            music_on = not music_on
            if music_on:
                if state == "menu":
                    sounds.background.play(-1)
                elif state == "playing":
                    sounds.xwing.play(-1)
            else:
                if state == "menu":
                    sounds.background.stop()
                elif state == "playing":
                    sounds.xwing.stop()
        elif exit_button.collidepoint(pos):
            exit()

def on_key_down(key):
    global state
    if state == "playing" and key == keys.SPACE:
        bullet = Actor("laser", (hero.x, hero.y))
        bullets.append(bullet)
    elif state == "game_over" and key == keys.RETURN:
        state = "menu"

