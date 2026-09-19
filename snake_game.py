import turtle
import random
import math

DELAY = 100
SEGMENT_SIZE = 20
WIDTH, HEIGHT = 600, 600

screen = turtle.Screen()
screen.title("🐍 Snake Game")
screen.bgcolor("black")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)

# ---------------- BOARD ----------------
def draw_chessboard():
    board = turtle.Turtle()
    board.hideturtle()
    board.penup()
    colors = ["#00ff51", "#FFFF00"]  # Dark green tones for a realistic feel

    for row in range(HEIGHT // SEGMENT_SIZE):
        for col in range(WIDTH // SEGMENT_SIZE):
            board.goto(-WIDTH//2 + col*SEGMENT_SIZE,
                       -HEIGHT//2 + row*SEGMENT_SIZE)
            board.fillcolor(colors[(row + col) % 2])
            board.begin_fill()
            for _ in range(4):
                board.forward(SEGMENT_SIZE)
                board.left(90)
            board.end_fill()

draw_chessboard()

# ---------------- REALISTIC APPLE ----------------
apple_turtle = turtle.Turtle()
apple_turtle.hideturtle()
apple_turtle.penup()
apple_leaf = turtle.Turtle()
apple_leaf.hideturtle()
apple_leaf.penup()
apple_stem = turtle.Turtle()
apple_stem.hideturtle()
apple_stem.penup()

def draw_apple(x, y):
    # Main apple body
    apple_turtle.clear()
    apple_turtle.goto(x, y - 8)
    apple_turtle.color("#ff0000", "#ff0000")
    apple_turtle.begin_fill()
    apple_turtle.circle(10)
    apple_turtle.end_fill()

    # Apple highlight (shine)
    apple_turtle.goto(x - 3, y + 2)
    apple_turtle.color("#ff8888", "#ffaaaa")
    apple_turtle.begin_fill()
    apple_turtle.circle(3)
    apple_turtle.end_fill()

    # Stem
    apple_stem.clear()
    apple_stem.goto(x, y + 2)
    apple_stem.color("#5a3010")
    apple_stem.pendown()
    apple_stem.pensize(2)
    apple_stem.goto(x + 2, y + 8)
    apple_stem.penup()

    # Leaf
    apple_leaf.clear()
    apple_leaf.goto(x + 2, y + 6)
    apple_leaf.color("#228B22", "#32CD32")
    apple_leaf.begin_fill()
    apple_leaf.goto(x + 10, y + 10)
    apple_leaf.goto(x + 6, y + 4)
    apple_leaf.goto(x + 2, y + 6)
    apple_leaf.end_fill()

food_x, food_y = 0, 100
draw_apple(food_x, food_y)

# ---------------- SNAKE ----------------
# Head with eyes
head = turtle.Turtle()
head.shape("square")
head.color("#49e804")
head.penup()
head.direction = "stop"
head.shapesize(1, 1)

# Eyes on the head
eye_left = turtle.Turtle()
eye_left.shape("circle")
eye_left.color("white")
eye_left.penup()
eye_left.shapesize(0.25, 0.25)

eye_right = turtle.Turtle()
eye_right.shape("circle")
eye_right.color("white")
eye_right.penup()
eye_right.shapesize(0.25, 0.25)

pupil_left = turtle.Turtle()
pupil_left.shape("circle")
pupil_left.color("black")
pupil_left.penup()
pupil_left.shapesize(0.12, 0.12)

pupil_right = turtle.Turtle()
pupil_right.shape("circle")
pupil_right.color("black")
pupil_right.penup()
pupil_right.shapesize(0.12, 0.12)

segments = []

SNAKE_COLORS = [
    "#10ee00", "#0fdd00", "#30cc00", "#38bb00", "#28aa00",
    "#1A9900", "#1B8800", "#227700", "#166600", "#0E5500"
]

def update_eyes():
    d = head.direction
    hx, hy = head.xcor(), head.ycor()
    offset = 5
    if d == "up":
        eye_left.goto(hx - offset, hy + 3)
        eye_right.goto(hx + offset, hy + 3)
        pupil_left.goto(hx - offset, hy + 5)
        pupil_right.goto(hx + offset, hy + 5)
    elif d == "down":
        eye_left.goto(hx - offset, hy - 3)
        eye_right.goto(hx + offset, hy - 3)
        pupil_left.goto(hx - offset, hy - 5)
        pupil_right.goto(hx + offset, hy - 5)
    elif d == "left":
        eye_left.goto(hx - 3, hy + offset)
        eye_right.goto(hx - 3, hy - offset)
        pupil_left.goto(hx - 5, hy + offset)
        pupil_right.goto(hx - 5, hy - offset)
    elif d == "right":
        eye_left.goto(hx + 3, hy + offset)
        eye_right.goto(hx + 3, hy - offset)
        pupil_left.goto(hx + 5, hy + offset)
        pupil_right.goto(hx + 5, hy - offset)
    else:
        eye_left.goto(hx + 3, hy + offset)
        eye_right.goto(hx + 3, hy - offset)
        pupil_left.goto(hx + 5, hy + offset)
        pupil_right.goto(hx + 5, hy - offset)

def hide_eyes():
    eye_left.goto(2000, 2000)
    eye_right.goto(2000, 2000)
    pupil_left.goto(2000, 2000)
    pupil_right.goto(2000, 2000)

hide_eyes()

# ---------------- UI ----------------
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(0, HEIGHT//2 - 30)

ui_pen = turtle.Turtle()
ui_pen.hideturtle()
ui_pen.penup()

panel = turtle.Turtle()
panel.hideturtle()
panel.penup()

button_pen = turtle.Turtle()
button_pen.hideturtle()
button_pen.penup()

# Decorative turtles for game over effects
deco1 = turtle.Turtle()
deco1.hideturtle()
deco1.penup()
deco2 = turtle.Turtle()
deco2.hideturtle()
deco2.penup()
deco3 = turtle.Turtle()
deco3.hideturtle()
deco3.penup()

play_btn = (-120, -80, 120, -40)
quit_btn = (-120, -140, 120, -100)

score = 0
high_score = 0
game_running = False
current_screen = "start"
hovered_button = None

# ---------------- SCORE ----------------
def write_score():
    pen.clear()
    pen.color("#7a0b9c")
    pen.write(f"Score: {score}   High Score: {high_score}",
              align="center", font=("Comic Sans MS", 14, "bold"))

# ---------------- GAME OVER PANEL ----------------
def draw_gradient_panel():
    """Draw a dark semi-transparent panel with border effect."""
    panel.clear()

    # Outer glow border layer (dark red/orange)
    panel.goto(-225, -185)
    panel.color("#0a36e8")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(450)
        panel.left(90)
        panel.forward(370)
        panel.left(90)
    panel.end_fill()

    # Middle border (orange)
    panel.goto(-220, -180)
    panel.color("#01eeff")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(440)
        panel.left(90)
        panel.forward(360)
        panel.left(90)
    panel.end_fill()

    # Inner panel (very dark, near-black background)
    panel.goto(-215, -175)
    panel.color("#000000")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(430)
        panel.left(90)
        panel.forward(350)
        panel.left(90)
    panel.end_fill()

    # Decorative horizontal divider line top
    deco1.clear()
    deco1.color("#e1ff00")
    deco1.goto(-200, 80)
    deco1.pendown()
    deco1.pensize(2)
    for i in range(400):
        deco1.goto(-200 + i, 80)
    deco1.penup()

    # Decorative horizontal divider line bottom
    deco1.goto(-200, -30)
    deco1.pendown()
    for i in range(400):
        deco1.goto(-200 + i, -30)
    deco1.penup()

    # Corner decorations (top-left)
    deco2.clear()
    deco2.color("#22ff00")
    deco2.goto(-215, 175)
    deco2.pendown()
    deco2.pensize(3)
    deco2.goto(-175, 175)
    deco2.penup()
    deco2.goto(-215, 175)
    deco2.pendown()
    deco2.goto(-215, 135)
    deco2.penup()

    # Corner decorations (top-right)
    deco2.goto(215, 175)
    deco2.pendown()
    deco2.goto(175, 175)
    deco2.penup()
    deco2.goto(215, 175)
    deco2.pendown()
    deco2.goto(215, 135)
    deco2.penup()

    # Corner decorations (bottom-left)
    deco2.goto(-215, -175)
    deco2.pendown()
    deco2.goto(-175, -175)
    deco2.penup()
    deco2.goto(-215, -175)
    deco2.pendown()
    deco2.goto(-215, -135)
    deco2.penup()

    # Corner decorations (bottom-right)
    deco2.goto(215, -175)
    deco2.pendown()
    deco2.goto(175, -175)
    deco2.penup()
    deco2.goto(215, -175)
    deco2.pendown()
    deco2.goto(215, -135)
    deco2.penup()

    # Small decorative diamonds on border
    deco3.clear()
    deco3.color("#00ff00")
    for px, py in [(-215, 0), (215, 0), (0, 175), (0, -175)]:
        deco3.goto(px, py)
        deco3.begin_fill()
        deco3.goto(px + 6, py + 6)
        deco3.goto(px + 12, py)
        deco3.goto(px + 6, py - 6)
        deco3.goto(px, py)
        deco3.end_fill()

def draw_start_panel():
    """Simpler green-toned panel for start screen."""
    panel.clear()
    deco1.clear()
    deco2.clear()
    deco3.clear()

    # Outer border
    panel.goto(-225, -185)
    panel.color("#0022ff")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(450)
        panel.left(90)
        panel.forward(370)
        panel.left(90)
    panel.end_fill()

    panel.goto(-220, -180)
    panel.color("#00FBFF")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(440)
        panel.left(90)
        panel.forward(360)
        panel.left(90)
    panel.end_fill()

    panel.goto(-215, -175)
    panel.color("#050f05")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(430)
        panel.left(90)
        panel.forward(350)
        panel.left(90)
    panel.end_fill()

# ---------------- BUTTON ----------------
def draw_button(x1, y1, x2, y2, text, hover=False, style="green"):
    button_pen.penup()
    button_pen.goto(x1, y1)
    button_pen.pendown()
    button_pen.pensize(2)

    if style == "red":
        fill_color = "#3a0000" if not hover else "#660000"
        border_color = "#ff2200"
        text_color = "#ff8888" if not hover else "#ffdddd"
    else:
        fill_color = "#003300" if not hover else "#005500"
        border_color = "#00ff44"
        text_color = "#88ff88" if not hover else "#ddffdd"

    button_pen.color(border_color, fill_color)
    button_pen.begin_fill()
    for _ in range(2):
        button_pen.forward(x2 - x1)
        button_pen.left(90)
        button_pen.forward(y2 - y1)
        button_pen.left(90)
    button_pen.end_fill()
    button_pen.penup()

    button_pen.goto((x1 + x2) // 2, y1 + 6)
    button_pen.color(text_color)
    button_pen.write(text, align="center",
                     font=("Comic Sans MS", 14, "bold"))

# ---------------- SCREENS ----------------
def show_start_screen():
    global current_screen
    current_screen = "start"

    ui_pen.clear()
    button_pen.clear()
    draw_start_panel()

    # Title
    ui_pen.color("#00ff44")
    ui_pen.goto(0, 80)
    ui_pen.write("SNAKE", align="center",
                 font=("Comic Sans MS", 40, "bold"))

    ui_pen.color("#88ff88")
    ui_pen.goto(0, 40)
    ui_pen.write("G  A  M  E", align="center",
                 font=("Comic Sans MS", 18, "normal"))

    ui_pen.color("#aaaaaa")
    ui_pen.goto(0, -10)
    ui_pen.write("Use Arrow Keys to Move", align="center",
                 font=("Comic Sans MS", 11, "bold"))

    draw_button(*play_btn, "▶  PLAY", hovered_button == "play", style="green")

def show_game_over():
    global current_screen
    current_screen = "game_over"

    ui_pen.clear()
    button_pen.clear()
    draw_gradient_panel()

    # "GAME OVER" — big, dramatic, red/orange
    ui_pen.color("#00ffae")
    ui_pen.goto(0, 117)
    ui_pen.write("GAME", align="center",
                 font=("Comic Sans MS", 36, "bold"))

    ui_pen.color("#00ffae")
    ui_pen.goto(0, 76)
    ui_pen.write("OVER", align="center",
                 font=("Comic Sans MS", 36, "bold"))

    # Score section between dividers
    ui_pen.color("#c800ff")
    ui_pen.goto(0, 45)
    ui_pen.write(f"SCORE", align="center",
                 font=("Comic Sans MS", 13, "normal"))

    ui_pen.color("#b3ff00")
    ui_pen.goto(0, 15)
    ui_pen.write(f"{score}", align="center",
                 font=("Comic Sans MS", 22, "bold"))

    ui_pen.color("#007bff")
    ui_pen.goto(0, -5)
    ui_pen.write(f"★  HIGH SCORE:  {high_score}  ★", align="center",
                 font=("Comic Sans MS", 12, "bold"))

    if score == high_score and score > 0:
        ui_pen.color("#ffff00")
        ui_pen.goto(0, -30)
        ui_pen.write("✦ NEW RECORD! ✦", align="center",
                     font=("Comic Sans MS", 13, "bold"))

    draw_button(*play_btn, "▶  PLAY AGAIN", hovered_button == "play", style="green")
    draw_button(*quit_btn, "✕  QUIT", hovered_button == "quit", style="red")

# ---------------- RESET ----------------
def reset_game():
    global score, game_running, food_x, food_y

    ui_pen.clear()
    panel.clear()
    button_pen.clear()
    deco1.clear()
    deco2.clear()
    deco3.clear()

    head.goto(0, 0)
    head.direction = "stop"
    head.color("#00ff00")

    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()

    food_x, food_y = 0, 100
    draw_apple(food_x, food_y)

    score = 0
    write_score()

    game_running = True
    game_loop()

# ---------------- CLICK ----------------
def check_click(x, y):
    global game_running

    if play_btn[0] < x < play_btn[2] and play_btn[1] < y < play_btn[3]:
        if not game_running:
            reset_game()

    if current_screen == "game_over":
        if quit_btn[0] < x < quit_btn[2] and quit_btn[1] < y < quit_btn[3]:
            screen.bye()

screen.onscreenclick(check_click)

# ---------------- HOVER ----------------
def update_hover():
    global hovered_button

    try:
        x = screen.cv.winfo_pointerx() - screen.cv.winfo_rootx()
        y = screen.cv.winfo_pointery() - screen.cv.winfo_rooty()
        y = screen.cv.winfo_height() - y
    except:
        screen.ontimer(update_hover, 100)
        return

    prev = hovered_button
    hovered_button = None

    if play_btn[0] < x < play_btn[2] and play_btn[1] < y < play_btn[3]:
        hovered_button = "play"
    elif current_screen == "game_over":
        if quit_btn[0] < x < quit_btn[2] and quit_btn[1] < y < quit_btn[3]:
            hovered_button = "quit"

    if prev != hovered_button:
        if current_screen == "start":
            show_start_screen()
        elif current_screen == "game_over":
            show_game_over()

    screen.ontimer(update_hover, 100)

update_hover()

# ---------------- CONTROLS ----------------
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# ---------------- MOVE ----------------
def move():
    if head.direction == "up":
        head.sety(head.ycor() + SEGMENT_SIZE)
    elif head.direction == "down":
        head.sety(head.ycor() - SEGMENT_SIZE)
    elif head.direction == "left":
        head.setx(head.xcor() - SEGMENT_SIZE)
    elif head.direction == "right":
        head.setx(head.xcor() + SEGMENT_SIZE)

# ---------------- FOOD ----------------
def random_food_position():
    max_x = WIDTH//2 - SEGMENT_SIZE
    max_y = HEIGHT//2 - SEGMENT_SIZE * 2
    return (
        random.randint(-max_x, max_x) // SEGMENT_SIZE * SEGMENT_SIZE,
        random.randint(-max_y, max_y) // SEGMENT_SIZE * SEGMENT_SIZE
    )

# ---------------- GAME LOOP ----------------
def game_loop():
    global score, high_score, game_running, food_x, food_y

    if not game_running:
        return

    screen.update()

    if abs(head.xcor()) > WIDTH//2 - SEGMENT_SIZE or abs(head.ycor()) > HEIGHT//2 - SEGMENT_SIZE:
        game_running = False
        hide_eyes()
        head.color("#FF0000")
        show_game_over()
        return

    if head.distance(food_x, food_y) < SEGMENT_SIZE:
        fx, fy = random_food_position()
        food_x, food_y = fx, fy
        draw_apple(food_x, food_y)

        new_seg = turtle.Turtle()
        new_seg.shape("square")
        idx = min(len(segments), len(SNAKE_COLORS) - 1)
        new_seg.color(SNAKE_COLORS[idx])
        new_seg.penup()
        segments.append(new_seg)

        score += 10
        if score > high_score:
            high_score = score
        write_score()

    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i-1].pos())
        # Gradient color effect along body
        color_idx = min(i, len(SNAKE_COLORS) - 1)
        segments[i].color(SNAKE_COLORS[color_idx])

    if segments:
        segments[0].goto(head.pos())
        segments[0].color(SNAKE_COLORS[0])

    move()
    update_eyes()

    for seg in segments:
        if seg.distance(head) < SEGMENT_SIZE / 2:
            game_running = False
            hide_eyes()
            head.color("#FF0000")
            show_game_over()
            return

    screen.ontimer(game_loop, DELAY)

# ---------------- INIT ----------------
write_score()
show_start_screen()

turtle.done()