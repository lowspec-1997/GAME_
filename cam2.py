import os
import pygame
import time
import random
import cv2
import mediapipe as mp
import numpy as np

# Minimalkan log TensorFlow (hanya error yang ditampilkan)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

pygame.init()

# Inisialisasi crash sound
try:
    crash_sound = pygame.mixer.Sound("crash.wav")
except pygame.error:
    crash_sound = None
    print("Warning: crash.wav not found.")

# Konstanta ukuran layar
display_width = 800
display_height = 600

# Warna yang digunakan
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
block_color = (53, 115, 255)

Dol_width = 73

# Inisialisasi layar game
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('UBM Racey')
clock = pygame.time.Clock()

# Load gambar mobil dengan pengecekan error
try:
    DolImg = pygame.image.load('raceDol.png')
except pygame.error:
    print("Error: File raceDol.png tidak ditemukan. Pastikan file ada di folder yang sama.")
    pygame.quit()
    quit()

pygame.display.set_icon(DolImg)

# Variabel Global untuk pause
pause = False

# Inisialisasi Mediapipe untuk deteksi wajah dan kepala
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Konfigurasi tampilan kamera di dalam game (proporsional)
CAMERA_WIDTH = 200
CAMERA_HEIGHT = 150
CAMERA_POS_X = display_width - CAMERA_WIDTH - 10  # Pojok kanan atas
CAMERA_POS_Y = 10

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, block_color, [thingx, thingy, thingw, thingh])

def Dol(x, y):
    gameDisplay.blit(DolImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 75)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def crash():
    if crash_sound:
        pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    
    # Tampilan crash dengan pilihan restart atau quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        button("Play Again", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(15)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def paused():
    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("comicsansms", 75)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(15)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 75)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)
        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(15)

def detect_head_direction():
    """
    Deteksi arah kepala berdasarkan posisi hidung.
    Jika nilai x hidung < 0.40 dianggap kepala menghadap ke kiri,
    jika nilai x > 0.60 dianggap menghadap ke kanan,
    selain itu dianggap center.
    """
    try:
        ret, frame = cap.read()
        if not ret or frame is None:
            dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            return "center", dummy_frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        head_direction = "center"
        if results.multi_face_landmarks:
            # Gunakan wajah pertama
            face_landmarks = results.multi_face_landmarks[0]
            nose = face_landmarks.landmark[1]  # Landmark 1 sebagai ujung hidung
            # Atur threshold agar tidak terlalu sensitif
            if nose.x < 0.40:
                head_direction = "left"
            elif nose.x > 0.60:
                head_direction = "right"
            else:
                head_direction = "center"
        return head_direction, frame
    except Exception as e:
        print("Error in head detection:", e)
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        return "center", dummy_frame

def render_camera(frame):
    """
    Menampilkan frame kamera secara proporsional di pojok kanan atas.
    Jika terjadi error saat resize atau konversi, gunakan dummy frame.
    """
    try:
        if frame is None or frame.size == 0:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
    except Exception as e:
        print("Error in resizing frame:", e)
        frame = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), dtype=np.uint8)
    try:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print("Error in color conversion:", e)
        frame = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), dtype=np.uint8)
    frame = np.rot90(frame)  # Rotasi agar sesuai dengan orientasi Pygame
    frame_surface = pygame.surfarray.make_surface(frame)
    gameDisplay.blit(frame_surface, (CAMERA_POS_X, CAMERA_POS_Y))

def game_loop():
    global pause
    pygame.mixer.music.load('low.wav')
    pygame.mixer.music.play(-1)

    x = display_width * 0.45
    y = display_height * 0.8
    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 3
    thing_width = 100
    thing_height = 100

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Pause hanya melalui keyboard P
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()

        # Deteksi arah kepala berdasarkan posisi hidung
        head_direction, frame = detect_head_direction()
        if head_direction == "left":
            x_change = -5
        elif head_direction == "right":
            x_change = 5
        else:
            x_change = 0

        x += x_change

        # Lakukan clamping agar posisi mobil tetap dalam layar
        if x < 0:
            x = 0
        if x > display_width - Dol_width:
            x = display_width - Dol_width

        gameDisplay.fill(white)

        # Buat objek obstacle dengan pygame.Rect untuk deteksi tabrakan
        dol_rect = pygame.Rect(x, y, Dol_width, DolImg.get_height())
        thing_rect = pygame.Rect(thing_startx, thing_starty, thing_width, thing_height)

        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        Dol(x, y)
        things_dodged(dodged)

        render_camera(frame)

        # Reset obstacle jika sudah melewati layar dan naikkan kesulitan
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width - thing_width)
            dodged += 1
            thing_speed = min(thing_speed + 0.5, 10)
            thing_width = min(thing_width + (dodged * 1.2), 200)

        # Deteksi tabrakan antara mobil dan obstacle
        if dol_rect.colliderect(thing_rect):
            crash()

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
cap.release()
pygame.quit()
quit()
