import pygame
import random
from pygame import RESIZABLE
# Constantsw
WIDTH, HEIGHT = 1080, 720
CELL_SIZE = 20  
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)

class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),RESIZABLE)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
    
    def fill(self, color):
        self.screen.fill(color)
    
    def update(self):
        pygame.display.flip()   
    
    def tick(self, fps):
        self.clock.tick(fps)

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)

    def move(self):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        x, y = self.body[0]
        return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or self.body[0] in self.body[1:]

    def change_direction(self, direction):
        if (direction[0] != -self.direction[0] or direction[1] != -self.direction[1]):
            self.direction = direction

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self):
        self.position = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

    def respawn(self):
        self.position = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))

class GameEngine:
    def __init__(self):
        self.screen = Screen()
        self.snake = Snake()
        self.food = Food()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_s:
                    self.snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_a:
                    self.snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_d:
                    self.snake.change_direction((CELL_SIZE, 0))

    def update(self):
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn()
        if self.snake.check_collision():
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen.screen)
        self.food.draw(self.screen.screen)
        self.screen.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.screen.tick(10)
        pygame.quit()

if __name__ == "__main__":
    gm = GameEngine()
    gm.run()
