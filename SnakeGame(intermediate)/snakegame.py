import pygame
import random
from pygame import RESIZABLE
import cv2
import mediapipe as mp

# Constants
WIDTH, HEIGHT = 1080, 720
CELL_SIZE = 20  
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)

class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def fill(self, color):
        self.screen.fill(color)
    
    def update(self):
        pygame.display.flip()   
    
    def tick(self, fps):
        self.clock.tick(fps)

    def draw_text(self, text, position, color=WHITE):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

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
        self.score = 0  
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_hand_gestures(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark

                index_finger_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x, y = int(index_finger_tip.x * WIDTH), int(index_finger_tip.y * HEIGHT)

                head_x, head_y = self.snake.body[0]
                if abs(x - head_x) > abs(y - head_y):
                    if x > head_x:
                        self.snake.change_direction((CELL_SIZE, 0))  
                    else:
                        self.snake.change_direction((-CELL_SIZE, 0))
                else:
                    if y > head_y:
                        self.snake.change_direction((0, CELL_SIZE)) 
                    else:
                        self.snake.change_direction((0, -CELL_SIZE))  

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.running = False

    def update(self):
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn()
            self.score += 1 
        if self.snake.check_collision():
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen.screen)
        self.food.draw(self.screen.screen)
        self.screen.draw_text(f"Score: {self.score}", (10, 10))  
        self.screen.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.handle_hand_gestures()
            self.update()
            self.draw()
            self.screen.tick(10)
        self.cap.release()
        cv2.destroyAllWindows()
        pygame.quit()

if __name__ == "__main__":
    gm = GameEngine()
    gm.run()