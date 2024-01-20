from pygame import *
from random import randint, randrange

init()
window_w = 700
window_h = 500
window = display.set_mode((window_w, window_h))
display.set_caption("snake")
Blue = (33, 186, 229)
window.fill(Blue)
run = True
bol = "right"
player_speed = 300
move_interval = 0.1
growth_rate = 5
snake_length = 5

class GameSprite(sprite.Sprite):
    def __init__(self, color, w, h, x, y):
        super().__init__()
        self.image = Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        draw.rect(window, (255, 255, 255), self.rect)
        draw.rect(window, self.image.get_at((0, 0)), self.rect)

class Apple(GameSprite):
    def __init__(self, color, w, h, x, y):
        super().__init__(color, w, h, x, y)
        self.move()

    def move(self):
        self.rect.x = randint(0, window_w - 30)
        self.rect.y = randint(0, window_h - 30)

    def hit(self):
        global snake
        for _ in range(growth_rate):
            color = (randrange(256), randrange(256), randrange(256))
            player = Player(color, 30, 30, snake[-1].rect.x, snake[-1].rect.y, player_speed)
            snake.append(player)
        self.move()

class Player(GameSprite):
    def __init__(self, color, w, h, x, y, speed):
        super().__init__(color, w, h, x, y)
        self.speed = speed

    def move_tail(self, new_x, new_y):
        self.old_x, self.old_y = self.rect.x, self.rect.y
        self.rect.x, self.rect.y = new_x, new_y

    def move(self, x, y):
        self.old_x, self.old_y = self.rect.x, self.rect.y
        self.rect.x += x
        self.rect.y += y

    def wall(self):
        if self.rect.x >= window_w:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = window_w - self.rect.width
        elif self.rect.y >= window_h:
            self.rect.y = 0
        elif self.rect.y < 0:
            self.rect.y = window_h - self.rect.height

apple = Apple((255, 0, 0), 30, 30, 0, 0)

# Define the walls
wall_color = (0, 0, 0)  # Color of the walls
walls = [
    GameSprite(wall_color, window_w, 10, 0, 0),          # Top wall
    GameSprite(wall_color, window_w, 10, 0, window_h-10), # Bottom wall
    GameSprite(wall_color, 10, window_h, 0, 0),          # Left wall
    GameSprite(wall_color, 10, window_h, window_w-10, 0)  # Right wall
]

snake = [Player((0, 255, 0), 30, 30, 10, 10, player_speed)]

curr_time = time.get_ticks()
last_move_time = curr_time

while run:
    time.wait(15)
    next_time = time.get_ticks()
    delta_time = (next_time - curr_time) / 1000.0
    curr_time = next_time

    apple_eaten = False

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w and bol != "down":
                bol = "up"
            elif e.key == K_s and bol != "up":
                bol = "down"
            elif e.key == K_a and bol != "right":
                bol = "left"
            elif e.key == K_d and bol != "left":
                bol = "right"

    player = snake[0]
    window.fill(Blue)

    # Check for collisions with walls
    if any(sprite.collide_rect(player, wall) for wall in walls):
        print("Game Over!")  # You can replace this with game over logic
        run = False

    # Move the head with a slight delay to create a gap
    if bol == "right":
        player.move(player_speed * delta_time, 0)
    elif bol == "left":
        player.move(-player_speed * delta_time, 0)
    elif bol == "down":
        player.move(0, player_speed * delta_time)
    elif bol == "up":
        player.move(0, -player_speed * delta_time)

    player.wall()

    if sprite.collide_rect(player, apple) and not apple_eaten:
        apple.hit()
        apple_eaten = True

    for ix, part in enumerate(snake[1:]):
        x, y = snake[ix].old_x, snake[ix].old_y
        part.move_tail(x, y)

    # Adjust the length of the snake based on snake_length
    while len(snake) < snake_length:
        # Create new segments with a random color
        color = (randrange(256), randrange(256), randrange(256))
        new_part = Player(color, 30, 30, snake[-1].rect.x, snake[-1].rect.y, player_speed)
        snake.append(new_part)

    # Draw the walls
    for wall in walls:
        wall.reset()

    apple.reset()
    for part in snake:
        part.reset()

    if curr_time - last_move_time >= move_interval * 1000:
        for ix, part in enumerate(snake[1:]):
            x, y = snake[ix].old_x, snake[ix].old_y
            
            part.move_tail(x, y)
        snake[0].move_tail(player.old_x, player.old_y)
        last_move_time = curr_time

    display.update()

quit()