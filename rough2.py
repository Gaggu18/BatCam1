import random, pygame, cv2, mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import numpy as np
print('Next ball')
pygame.init()

font = pygame.font.Font(None, 36)  # None uses the default font, 36 is the size

# Set the dimensions of the window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BatCam")  # Set the title of the window
background_image = pygame.image.load("assets/BG.jpg").convert()
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Set the position and size of the webcam feed
webcam_x, webcam_y, webcam_width, webcam_height = 430, 280, 350, 300

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

runs = 0
def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera!")
        exit()
    return cap

def draw_webcam_feed(window, frame):
    # Resize frame to fit the window
    frame = cv2.resize(frame, (webcam_width, webcam_height))
    # Convert frame to Pygame surface
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    frame = pygame.transform.flip(frame, True, False)
    # Draw webcam feed onto Pygame window
    window.blit(frame, (webcam_x, webcam_y))

def score_board(runs, truns ):
    global score
    print('Score: ', score, " = ", score, " + ", runs, " = ", runs + truns)
    score += runs
    print("Total score: ", score)

def finger_count(hands, num_hands, detector, score):
    print('yeah!')
    if num_hands > 0:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        if fingers == [1, 0, 0, 0, 0]:
            runs = 6
            print("It's a Six: ", runs)
        elif fingers == [0, 0, 0, 0, 1]:
            runs = 4
            print("It's a four", runs)
        elif fingers == [0, 1, 1, 0, 0]:
            print("Peace")
        else:
            print(fingers)
    score_board(runs, score)
def game_logic(cap):
    global score
    score = 0
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    running = True
    text1 = font.render(" ", True, (255, 255, 255))  # Render text
    while running:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame!")
            return
        hands, _ = detector.findHands(frame)
        num_hands = len(hands)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    random_number = random.randint(1, 6)
                    #print(random_number)
                    text1 = font.render(str(random_number), True, (255, 255, 255))  # Render text
                    window.blit(text1, (100, 100))  # Draw text onto Pygame window
                    finger_count(hands, num_hands, detector, score)

        # Draw the background image
        window.blit(background_image, (0, 0))
        text = font.render("Press 'q' to quit", True, (255, 255, 255))  # Render text
        window.blit(text, (10, 10))  # Draw text onto Pygame window
        window.blit(text1, (100, 100))  # Draw text onto Pygame window
        text3 = font.render("Score: ", str(score), True, (255, 255, 255))  # Render text
        window.blit(text3, (200, 100))  # Draw text onto Pygame window

        # Draw the webcam feed
        draw_webcam_feed(window, frame)

        pygame.display.update()

def main():
    cap = initialize_camera()
    game_logic(cap)
    cap.release()
    hands.close()
    pygame.quit()

if __name__ == "__main__":
    main()
