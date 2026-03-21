import random

import pygame

import Queens
import KnightTour
import WordyBot


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("AI Project")

font = pygame.font.SysFont(None, 30)
error_font = pygame.font.SysFont(None, 25)
title_font = pygame.font.SysFont(None, 52)
wordy_info_font = pygame.font.SysFont(None, 28)
wordy_tile_font = pygame.font.SysFont(None, 46)
wordy_button_font = pygame.font.SysFont(None, 34)
clock = pygame.time.Clock()

pygame.mixer.init()
hover_sound = pygame.mixer.Sound("assets/hover.mp3")

background_image = pygame.image.load("assets/bg.png").convert()
background_image = pygame.transform.smoothscale(background_image, (1280, 720))

wordy_image = pygame.image.load("assets/wordy.png").convert_alpha()
queens_image = pygame.image.load("assets/queens.png").convert_alpha()
knight_image = pygame.image.load("assets/knight.png").convert_alpha()

activeQ = False
activeK = False
running = True
mode = "menu"
launch_action = None
wordy_state = None
errorQ = ""
errorK = ""
textQ = "Board Size?"
textK = "Start Position?"
UItext = "Puzzle Solver & Minigame"

base_r1 = pygame.Rect(180, 200, 280, 280)
base_r2 = pygame.Rect(500, 200, 280, 280)
base_r3 = pygame.Rect(820, 200, 280, 280)
r11 = pygame.Rect(180, 495, 280, 80)
r33 = pygame.Rect(820, 495, 280, 80)
r1 = base_r1.copy()
r2 = base_r2.copy()
r3 = base_r3.copy()
r1_scale = 1.0
r2_scale = 1.0
r3_scale = 1.0
last_hover_card = None

WORDY_TILE_SIZE = 72
WORDY_TILE_GAP = 10
WORDY_BOARD_WIDTH = 5 * WORDY_TILE_SIZE + 4 * WORDY_TILE_GAP
WORDY_BOARD_X = (1280 - WORDY_BOARD_WIDTH) // 2
WORDY_BOARD_Y = 130
WORDY_SUBMIT_RECT = pygame.Rect(555, 58, 170, 46)

def scaled_rect(rect, scale):
    scaled_width = int(rect.width * scale)
    scaled_height = int(rect.height * scale)
    return pygame.Rect(
        rect.centerx - scaled_width // 2,
        rect.centery - scaled_height // 2,
        scaled_width,
        scaled_height,
    )


def wordy_tile_rect(row, col):
    return pygame.Rect(
        WORDY_BOARD_X + col * (WORDY_TILE_SIZE + WORDY_TILE_GAP),
        WORDY_BOARD_Y + row * (WORDY_TILE_SIZE + WORDY_TILE_GAP),
        WORDY_TILE_SIZE,
        WORDY_TILE_SIZE,
    )


def current_hover_card(mouse_pos):
    if r1.collidepoint(mouse_pos):
        return "r1"
    if r2.collidepoint(mouse_pos):
        return "r2"
    if r3.collidepoint(mouse_pos):
        return "r3"
    return None


def start_wordy_game():
    bot = WordyBot.WordyBot()
    bot.load_words()
    bot.reset_game_state()
    bot.word = random.choice(bot.dictionary)

    return {
        "bot": bot,
        "turn": 0,
        "game_over": False,
        "message": "Click tiles for feedback.",
        "review_marks": ["0"] * 5,
        "board_words": [""] * 6,
        "board_reviews": [[""] * 5 for _ in range(6)],
    }


def submit_wordy_turn():
    global wordy_state

    if wordy_state is None:
        return

    bot = wordy_state["bot"]
    turn = wordy_state["turn"]

    if wordy_state["game_over"] or not bot.word or turn >= 6:
        return

    guess = bot.word
    review = "".join(wordy_state["review_marks"])

    wordy_state["board_words"][turn] = guess.upper()
    wordy_state["board_reviews"][turn] = list(review)
    bot.used_guesses.add(guess)

    if review == "11111":
        wordy_state["message"] = f"I got it in {turn + 1} guesses."
        wordy_state["game_over"] = True
        return

    bot.apply_review(review)
    next_guess = bot.get_next_guess()

    if turn == 5:
        wordy_state["message"] = "I used all guesses."
        wordy_state["game_over"] = True
        return

    if not next_guess:
        bot.word = ""
        wordy_state["message"] = "Word missing from dictionary."
        wordy_state["game_over"] = True
        return

    bot.word = next_guess
    wordy_state["turn"] += 1
    wordy_state["review_marks"] = ["0"] * 5
    wordy_state["message"] = "Next guess ready."


def draw_menu(mouse_pos):
    global r1, r2, r3, r1_scale, r2_scale, r3_scale

    target_r1_scale = 1.08 if base_r1.collidepoint(mouse_pos) else 1.0
    target_r2_scale = 1.08 if base_r2.collidepoint(mouse_pos) else 1.0
    target_r3_scale = 1.08 if base_r3.collidepoint(mouse_pos) else 1.0
    animation_speed = 0.18

    r1_scale += (target_r1_scale - r1_scale) * animation_speed
    r2_scale += (target_r2_scale - r2_scale) * animation_speed
    r3_scale += (target_r3_scale - r3_scale) * animation_speed

    r1 = scaled_rect(base_r1, r1_scale)
    r2 = scaled_rect(base_r2, r2_scale)
    r3 = scaled_rect(base_r3, r3_scale)

    if background_image is not None:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill("black")
    surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    pygame.draw.rect(surface, "yellow", r1, 2)

    scaled_queens = pygame.transform.smoothscale(
        queens_image, (max(1, r1.width - 10), max(1, r1.height - 10))
    )
    queens_rect = scaled_queens.get_rect(center=r1.center)
    surface.blit(scaled_queens, queens_rect)
    pygame.draw.rect(surface, "black", r11)
    box_colorQ = "yellow" if activeQ else "gray"
    pygame.draw.rect(surface, box_colorQ, r11, 2)

    scaled_wordy = pygame.transform.smoothscale(
        wordy_image, (max(1, r2.width - 10), max(1, r2.height - 10))
    )
    wordy_rect = scaled_wordy.get_rect(center=r2.center)
    surface.blit(scaled_wordy, wordy_rect)
    pygame.draw.rect(surface, "green", r2, 2)

    scaled_knight = pygame.transform.smoothscale(
        knight_image, (max(1, r3.width - 10), max(1, r3.height - 10))
    )
    knight_rect = scaled_knight.get_rect(center=r3.center)
    surface.blit(scaled_knight, knight_rect)
    pygame.draw.rect(surface, "cyan", r3, 2)

    pygame.draw.rect(surface, "black", r33)
    box_colorK = "cyan" if activeK else "gray"
    pygame.draw.rect(surface, box_colorK, r33, 2)

    screen.blit(surface, (0, 0))

    textUI_surface = title_font.render(UItext, True, "white")
    textUI_rect = textUI_surface.get_rect(center=(640, 95))
    screen.blit(textUI_surface, textUI_rect)

    textQ_surface = font.render(textQ, True, "yellow")
    textQ_rect = textQ_surface.get_rect(center=r11.center)
    screen.blit(textQ_surface, textQ_rect)

    textK_surface = font.render(textK, True, "cyan")
    textK_rect = textK_surface.get_rect(center=r33.center)
    screen.blit(textK_surface, textK_rect)

    errorQ_surface = error_font.render(errorQ, True, "red")
    errorQ_rect = errorQ_surface.get_rect(midtop=(r11.centerx, r11.bottom + 8))
    screen.blit(errorQ_surface, errorQ_rect)

    errorK_surface = error_font.render(errorK, True, "red")
    errorK_rect = errorK_surface.get_rect(midtop=(r33.centerx, r33.bottom + 8))
    screen.blit(errorK_surface, errorK_rect)


def draw_wordy():
    bot = wordy_state["bot"]
    turn = wordy_state["turn"]
    game_over = wordy_state["game_over"]
    current_guess = bot.word.upper() if not game_over and bot.word else ""

    if background_image is not None:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((18, 18, 19))

    title = title_font.render("WORDY BOT", True, (240, 240, 240))
    screen.blit(title, title.get_rect(center=(640, 38)))

    pygame.draw.rect(screen, (83, 141, 78), WORDY_SUBMIT_RECT, border_radius=8)
    submit_text = wordy_button_font.render("Submit", True, (255, 255, 255))
    screen.blit(submit_text, submit_text.get_rect(center=WORDY_SUBMIT_RECT.center))

    help_text = wordy_info_font.render(
        "Left click = Wrong Place || Right click = Correct",
        True,
        (180, 180, 180),
    )
    screen.blit(help_text, help_text.get_rect(center=(640, 640)))

    for row in range(6):
        row_word = wordy_state["board_words"][row]
        row_marks = wordy_state["board_reviews"][row]
        live_row = row == turn and not game_over

        if live_row:
            row_word = current_guess
            row_marks = wordy_state["review_marks"]

        for col in range(5):
            tile_rect = wordy_tile_rect(row, col)
            mark = row_marks[col] if col < len(row_marks) else ""
            fill = bot.tile_color(mark, live_row)

            pygame.draw.rect(screen, fill, tile_rect, border_radius=6)
            pygame.draw.rect(screen, (210, 214, 218), tile_rect, 2, border_radius=6)

            if col < len(row_word):
                letter = wordy_tile_font.render(row_word[col], True, (255, 255, 255))
                screen.blit(letter, letter.get_rect(center=tile_rect.center))

    message_text = wordy_info_font.render(wordy_state["message"], True, (230, 230, 230))
    screen.blit(message_text, message_text.get_rect(center=(640, 690)))


while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif mode == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            activeQ = r11.collidepoint(event.pos)
            if activeQ and textQ == "Board Size?":
                textQ = ""
            elif not activeQ and textQ == "":
                textQ = "Board Size?"
            elif not activeQ and textQ.isalpha():
                errorQ = "Use Integers"
                textQ = "Board Size?"

            activeK = r33.collidepoint(event.pos)
            if activeK and textK == "Start Position?":
                textK = ""
            elif not activeK and textK == "":
                textK = "Start Position?"
            elif not activeK and textK.isalpha():
                errorK = "Use Integers"
                textK = "Start Position?"

            queensGame = r1.collidepoint(event.pos)
            if queensGame:
                if textQ == "Board Size?":
                    errorQ = "Select the board size"
                else:
                    board_size = int(textQ)
                    launch_action = ("queens", board_size)
                    running = False

            wordyGame = r2.collidepoint(event.pos)
            if wordyGame:
                wordy_state = start_wordy_game()
                mode = "wordy"

            knightTour = r3.collidepoint(event.pos)
            if knightTour:
                if textK == "Start Position?":
                    errorK = "Select the starting position"
                else:
                    try:
                        x, y = map(int, textK.replace(",", " ").split())
                        if 0 <= x < 8 and 0 <= y < 8:
                            launch_action = ("knight", x, y)
                            running = False
                        else:
                            errorK = "Use coordinates from 0 to 7"
                    except ValueError:
                        errorK = "Use x,y integers"

        elif mode == "menu" and event.type == pygame.KEYDOWN:
            if activeQ:
                if event.key == pygame.K_BACKSPACE:
                    textQ = textQ[:-1]
                elif event.key != pygame.K_RETURN:
                    textQ += event.unicode
            elif activeK:
                if event.key == pygame.K_BACKSPACE:
                    textK = textK[:-1]
                elif event.key != pygame.K_RETURN:
                    textK += event.unicode

        elif mode == "wordy" and event.type == pygame.MOUSEBUTTONDOWN:
            if WORDY_SUBMIT_RECT.collidepoint(event.pos):
                submit_wordy_turn()
                continue

            if not wordy_state["game_over"] and wordy_state["turn"] < 6:
                turn = wordy_state["turn"]
                for col in range(5):
                    tile_rect = wordy_tile_rect(turn, col)
                    if tile_rect.collidepoint(event.pos):
                        if event.button == 1:
                            current = wordy_state["review_marks"][col]
                            wordy_state["review_marks"][col] = "0" if current == "?" else "?"
                        elif event.button == 3:
                            current = wordy_state["review_marks"][col]
                            wordy_state["review_marks"][col] = "0" if current == "1" else "1"
                        else:
                            wordy_state["review_marks"][col] = "0"
                        break

        elif mode == "wordy" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mode = "menu"
                wordy_state = None
            elif event.key == pygame.K_RETURN:
                submit_wordy_turn()

    if mode == "menu":
        hover_card = current_hover_card(mouse_pos)
        if hover_card != last_hover_card and hover_card is not None and hover_sound is not None:
            hover_sound.play()
        last_hover_card = hover_card

        if r11.collidepoint(mouse_pos) or r33.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        elif r1.collidepoint(mouse_pos) or r2.collidepoint(mouse_pos) or r3.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        draw_menu(mouse_pos)
    else:
        last_hover_card = None
        hover_wordy = WORDY_SUBMIT_RECT.collidepoint(mouse_pos)
        if wordy_state and not wordy_state["game_over"] and wordy_state["turn"] < 6:
            turn = wordy_state["turn"]
            for col in range(5):
                if wordy_tile_rect(turn, col).collidepoint(mouse_pos):
                    hover_wordy = True
                    break
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if hover_wordy else pygame.SYSTEM_CURSOR_ARROW
        )
        draw_wordy()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()

if launch_action:
    if launch_action[0] == "queens":
        Queens.n = launch_action[1]
        Queens.main()
    elif launch_action[0] == "knight":
        _, x, y = launch_action
        solver = KnightTour.KnightTourSolver(8)
        success = solver.solve(x, y)
        if success:
            solver.animate_solution(interval=600)