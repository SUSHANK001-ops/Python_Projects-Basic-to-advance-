import pygame
import numpy as np
import cv2
import mediapipe as mp
from pygame import RESIZABLE
pygame.init()

WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT),RESIZABLE)
pygame.display.set_caption("3D Cube Controlled by Hand Gesture")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 150)
LIGHT_BLUE = (100, 100, 255)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Increased cube size by adjusting vertices
vertices = np.array([
    [-1.2, -1.2, -1.2], [1.2, -1.2, -1.2], [1.2, 1.2, -1.2], [-1.2, 1.2, -1.2],
    [-1.2, -1.2, 1.2], [1.2, -1.2, 1.2], [1.2, 1.2, 1.2], [-1.2, 1.2, 1.2],
])

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def rotate_x(angle):
    rotation = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])
    return rotation

def rotate_y(angle):
    rotation = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    return rotation

def rotate_z(angle):
    rotation = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    return rotation

def calculate_scale_and_position(hand_landmarks):
    wrist = hand_landmarks.landmark[0]
    index_finger = hand_landmarks.landmark[8]
    distance = np.sqrt((index_finger.x - wrist.x) ** 2 + (index_finger.y - wrist.y) ** 2)
    scale = max(0.5, min(3.0, 1 / distance))  # Scale based on hand distance
    position_x = (index_finger.x - 0.5) * WIDTH
    position_y = (index_finger.y - 0.5) * HEIGHT
    return scale, position_x, position_y

def project(point):
    scale = 100
    x = int(point[0] * scale) + WIDTH // 2
    y = int(point[1] * scale) + HEIGHT // 2
    return (x, y)

cap = cv2.VideoCapture(0)
angle_x = angle_y = angle_z = 0
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    screen.fill(WHITE)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Get first hand
        # Draw hand landmarks
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        scale, position_x, position_y = calculate_scale_and_position(hand_landmarks)
        index_finger = hand_landmarks.landmark[8]
        # Calculate rotation angles based on hand position
        angle_x = (index_finger.y - 0.5) * 2 * np.pi
        angle_y = (index_finger.x - 0.5) * 2 * np.pi

    # Cube transformation 
    rotation_x = rotate_x(angle_x)
    rotation_y = rotate_y(angle_y)
    rotation_z = rotate_z(angle_z)

    transformed_vertices = []
    for vertex in vertices:
        rotated = np.dot(rotation_x, vertex)
        rotated = np.dot(rotation_y, rotated)
        rotated = np.dot(rotation_z, rotated)
        transformed_vertices.append(rotated)

    for edge in edges:
        points = []
        for vertex_index in edge:
            point = project(transformed_vertices[vertex_index])
            points.append(point)
        pygame.draw.line(screen, BLUE, points[0], points[1], 2)

    pygame.display.flip()
    clock.tick(60)

    cv2.imshow("Hand Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
hands.close()