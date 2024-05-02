import random, pygame, cv2, sys, mediapipe as mp
from button import Button
from cvzone.HandTrackingModule import HandDetector

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

# Fonts used in the programs
font = pygame.font.Font(None, 58)  # None uses the default font, 36 is the size
font1 = pygame.font.Font(None, 67)  # None uses the default font, 36 is the size
font3 = pygame.font.Font(None, 34)  # None uses the default font, 36 is the size
# font4 = pygame.font.Font(None, 34)  # None uses the default font, 36 is the size


# Set the dimensions of the window
window_width, window_height = 1050, 750
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BatCam")  # Set the title of the window

#Background Music
pygame.mixer.music.load("assets/bm.mp3")
cheering = pygame.mixer.Sound("assets/cheering.mp3")
booing = pygame.mixer.Sound("assets/booing8.mp3")


pygame.mixer.music.set_volume(0.1)

# Take the pictures for background
background_image = pygame.image.load("assets/BG4_bat.png").convert()
background_image = pygame.transform.scale(background_image, (window_width, window_height))
background_image3 = pygame.image.load("assets/BG4_bowl2.png").convert()
background_image3 = pygame.transform.scale(background_image3, (window_width, window_height))
BG = pygame.image.load("assets/Background.png").convert()
BG = pygame.transform.scale(BG, (window_width, window_height))

# Set the position and size of the webcam feed
webcam_x, webcam_y, webcam_width, webcam_height = 588, 45, 350, 300

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


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


def match_result():
    global music
    if batting:
        if inning == 2:
            if aiScore > score:
                if music == False:
                    booing.play(0)
                    music = True
                text10 = font3.render("Ai won by 7 wickets ", True, (255, 0, 0))  # Render text
                window.blit(text10, (430, 720))  # Draw text onto Pygame window
            elif AiWicket == False:
                if score > aiScore:
                    if music == False:
                        cheering.play(0)
                        music = True
                    text10 = font3.render("You won by "+ str(score - aiScore) +" runs!!", True, (255, 0, 0))  # Render text
                    window.blit(text10, (430, 720))  # Draw text onto Pygame window
                else:
                    text10 = font3.render("Game Tied!", True,
                                          (255, 0, 0))  # Render text
                    window.blit(text10, (430, 720))  # Draw text onto Pygame window
    else:
        if inning == 2:
            if aiScore < score:
                if score > aiScore:
                    if music == False:
                        cheering.play(0)
                        music = True
                text10 = font3.render("You won by 7 wickets ", True, (255, 0, 0))  # Render text
                window.blit(text10, (430, 720))  # Draw text onto Pygame window
            elif wicket == False:
                if score < aiScore:
                    if music == False:
                        booing.play(0)
                        music = True
                    text10 = font3.render("Ai won by "+ str(aiScore - score) +" runs!!", True, (255, 0, 0))  # Render text
                    window.blit(text10, (430, 720))  # Draw text onto Pygame window
                else:
                    text10 = font3.render("Game Tied!", True,
                                          (255, 0, 0))  # Render text
                    window.blit(text10, (430, 720))  # Draw text onto Pygame window


def update_over(runs):
    global over
    over.append(runs)
    # Keep only the last 6 elements in the list
    if len(over) > 6:
        over.pop(0)


def score_board():
    global score, runs
    print(score, " + ", runs, " = ", runs + score)
    score += runs
    print("Total score: ", score)
    update_over(runs)


def AiScoreCard():
    global aiScore, score
    if batting:
        if aiScore > score:
            print("Ai won by 7 wickets")
        else:
            print(aiScore, " + ", random_number, " = ", random_number + aiScore)
            aiScore += random_number
            print("Total score of Ai: ", aiScore)
            update_over(random_number)


def list_clear():
    inn = inning
    if inn == 1:
        over.clear()
        inn = 3


def ScoreCard_B():
    global aiScore, score
    if aiScore < score:
        print("You won by 7 wickets")
    else:
        print(score, " + ", runs, " = ", runs + score)
        score += runs
        print("Total score of Ai: ", score)
        update_over(runs)


def SecondInning():
    global AiWicket, aiScore, score, runs, ai_nuksaan, wicketMark, wicket, inn
    list_clear()
    print("Target: ", score + 1)
    if AiWicket:
        if random_number == runs:
            print("AI is Out!!")
            AiWicket = False
            inn = 1
            wicketMark = True
            ai_nuksaan = 1
            if score > aiScore:
                print("You won by ", score - aiScore, " runs!!")
                # match_result()
                # time.sleep(3)
                # quit()
            else:
                print("OHHHHH!! It's a draw")

        else:
            AiScoreCard()


def score_board_B():
    global aiScore, random_number
    print(aiScore, " + ", random_number, " = ", random_number + aiScore)
    aiScore += random_number
    print("Total Ai Score: ", aiScore)
    update_over(random_number)


def SecondInning_B(runs):
    global AiWicket, aiScore, score, nuksaan, wicketMark, wicket, inn
    list_clear()
    if wicket:
        if random_number == runs:
            wicket = False
            wicketMark = True
            nuksaan = 1
            if score < aiScore:
                print("Ai won by ", aiScore - score, " runs!!")
            else:
                print("OHHHHH!! It's a draw")
        else:
            ScoreCard_B()


def thirdUmpire():
    global wicket, runs, inning, nuksaan, over, wicketMark, inn, AiWicket, ai_nuksaan
    if batting:
        if nuksaan == 0:
            if random_number == runs:
                wicket = False
                nuksaan = 1
                wicketMark = True
            else:
                score_board()
        else:
            SecondInning()
            inning = 2
    else:
        if AiWicket:
            if random_number == runs:
                AiWicket = False
                wicketMark = True
                ai_nuksaan = 1
            else:
                score_board_B()
        else:
            SecondInning_B(runs)
            inning = 2

def finger_count( hands, num_hands, detector):
    global runs
    if num_hands > 0:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        num_fingers_up = sum(fingers)
        if fingers == [1, 0, 0, 0, 0]:
            runs = 6
        elif fingers == [0, 0, 0, 0, 1]:
            runs = 4
        else:
            if num_fingers_up == 1:
                runs = 1  # Assign 1 run for any single finger raised
            elif num_fingers_up == 2:
                runs = 2  # Assign 2 runs for two fingers raised
            elif num_fingers_up == 3:
                runs = 3  # Assign 3 runs for two fingers raised
            elif num_fingers_up == 4:
                runs = 4  # Assign 4 runs for two fingers raised
            elif num_fingers_up == 5:
                runs = 5  # Assign 4 runs for two fingers raised
            else:
                runs = 0
                print("No valid gesture detected")
    else:
        runs = 0
        print("No hands detected")
    thirdUmpire()


def render_last_six_balls(window):
    text_x = 640  # Starting Y position for rendering the text
    for index, xruns in enumerate(over):
        text = font.render(str(xruns), True, (255, 255, 255))
        window.blit(text, (text_x, 650))
        text_x += 52
    return text_x


def w_m_c(window, text_x):
    text7 = font1.render("OUT!! wicket", True, (255, 0, 0))  # Render text
    window.blit(text7, (370, 180))  # Draw text onto Pygame window
    text_x -= 7
    text = font.render("W", True, (255, 255, 255))
    window.blit(text, (text_x, 648))


def wicket_mark(window, text_x):
    global wicketMark
    if batting:
        if wicket == False:
            if inning == 1:
                w_m_c(window, text_x)
        if AiWicket == False:
            if inning == 2:
                w_m_c(window, text_x)
    else:
        if AiWicket == False:
            if inning == 1:
                w_m_c(window, text_x)
        if wicket == False:
            if inning == 2:
                w_m_c(window, text_x)


def render_score_board(window, score, ai_score, random_number):
    # Render the score board text
    global wicket, AiWicket, inning
    if batting:
        if inning == 1:
            score_text = font.render(str(score), True, (255, 0, 0))
            text7 = font.render(str(nuksaan), True, (255, 0, 0))  # Render text
            text_x = render_last_six_balls(window)

        elif inning == 2:
            score_text = font.render(str(ai_score), True, (255, 0, 0))
            text7 = font.render(str(ai_nuksaan), True, (255, 0, 0))  # Render text
            text_x = render_last_six_balls(window)
        if nuksaan == 1:
            target_txt = font3.render("Target", True, (255, 0, 0))
            window.blit(target_txt, (536, 638))  # Draw text onto Pygame window
            target = font3.render(str(score + 1), True, (255, 0, 0))
            window.blit(target, (556, 669))  # Draw text onto Pygame window
    else:
        if inning == 1:
            score_text = font.render(str(ai_score), True, (255, 0, 0))
            text7 = font.render(str(ai_nuksaan), True, (255, 0, 0))  # Render text
            text_x = render_last_six_balls(window)

        elif inning == 2:
            score_text = font.render(str(score), True, (255, 0, 0))
            text7 = font.render(str(nuksaan), True, (255, 0, 0))  # Render text
            text_x = render_last_six_balls(window)
        if ai_nuksaan == 1:
            target_txt = font3.render("Target", True, (255, 0, 0))
            window.blit(target_txt, (536, 638))  # Draw text onto Pygame window
            target = font3.render(str(ai_score + 1), True, (255, 0, 0))
            window.blit(target, (556, 669))  # Draw text onto Pygame window

    window.blit(score_text, (378, 648))  # Draw text onto Pygame window
    window.blit(text7, (480, 648))  # Draw text onto Pygame window

    aiMove = font1.render("Ai Move: " + str(random_number), True, (255, 255, 0))  # Render text
    window.blit(aiMove, (150, 290))  # Draw text onto Pygame window
    myMove = font1.render("Your Move: " + str(runs), True, (255, 255, 0))  # Render text
    window.blit(myMove, (620, 290))  # Draw text onto Pygame window

    wicket_mark(window, text_x)


def game_logic(cap):
    global score, wicket, AiWicket, aiScore, runs, inning, nuksaan, over, ai_nuksaan, wicketMark, random_number
    random_number, score, runs, aiScore, inning, nuksaan, over, ai_nuksaan, inn = 0, 0, 0, 0, 1, 0, [], 0, 1
    wicket, AiWicket, wicketMark = True, True, False
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    running = True

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
                elif event.key == pygame.K_n:
                    random_number = random.randint(1, 6)
                    #random_number = 3
                    finger_count(hands, num_hands, detector)
                elif event.key == pygame.K_r:
                    main_menu()

        # Draw the background image
        if batting:
            if inning == 1:
                window.blit(background_image, (0, 0))
            elif inning == 2:
                window.blit(background_image3, (0, 0))
        else:
            if inning == 1:
                window.blit(background_image3, (0, 0))
            elif inning == 2:
                window.blit(background_image, (0, 0))
        # Draw the score board
        draw_webcam_feed(window, frame)

        render_score_board(window, score, aiScore, random_number)
        match_result()
        text = font.render("Press 'q' to quit", True, (255, 255, 255))  # Render text
        window.blit(text, (10, 10))  # Draw text onto Pygame window
        pygame.display.update()


def main():
    cap = initialize_camera()
    game_logic(cap)
    cap.release()
    hands.close()
    pygame.quit()


def main_menu():
    pygame.mixer.music.play(-1)
    global batting, music
    music = False
    batting = True
    while True:
        window.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(72).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(410, 100))
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 240),
                             text_input="Bat First", font=get_font(36), base_color="#006400", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 390),
                                text_input="Bowl First", font=get_font(36), base_color="#006400",
                                hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 520),
                             text_input="QUIT", font=get_font(36), base_color="#006400", hovering_color="White")
        window.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    batting = False
                    main()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
