import random
import sys
import time

try:
    import pygame

    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


class WordyBot:
    def __init__(self, type_speed=0.02):
        self.type_speed = type_speed
        self.dictionary = []
        self.reset_game_state()

    def reset_game_state(self):
        # Reset solver state
        self.word = ""
        self.confirmed = [None] * 5
        self.required_letters = set()
        self.forbidden_letters = set()
        self.wrong_spots = [set() for _ in range(5)]
        self.used_guesses = set()

    def _type(self, text):
        # Console typing effect
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.type_speed)
        print()

    def greeting(self):
        # Console game rules
        self._type("Hello there! I'am Wordy, wanna play a game?")
        self._type("--- WORDY BOT RULES ---")
        self._type("1. I will guess a 5-letter word.")
        self._type("2. You must reply with 5 marks based on my guess:")
        self._type("   [ 1 ] = Letter is correct and in the right spot.")
        self._type("   [ ? ] = Letter is in the word, but in the wrong spot.")
        self._type("   [ 0 ] = Letter is not in the word at all.")
        self._type("3. Example: If I guess HELLO and only 'H' is right, enter 10000.")
        self._type("4. I have exactly 6 guesses to find your word!")
        self._type("WARNING: WORDY COULD POSSIBLY CRASH IF THE WORD YOU SEEK ISN'T IN HIS DICTIONARY")
        self._type("-----------------------")

    def load_words(self):
        # Load dictionary words
        try:
            with open("five_letter_words.txt", "r") as f:
                self.dictionary = [
                    line.strip().lower()
                    for line in f.readlines()
                    if len(line.strip()) == 5
                ]
        except FileNotFoundError:
            self._type("Error: five_letter_words.txt not found!")
            sys.exit()

    def get_next_guess(self):
        # Filter possible matches
        possible_matches = []

        for pos_answer in self.dictionary:
            if pos_answer in self.used_guesses:
                continue

            is_possible = True
            for i in range(5):
                char = pos_answer[i]
                if self.confirmed[i] and char != self.confirmed[i]:
                    is_possible = False
                    break
                if char in self.forbidden_letters and char not in self.required_letters:
                    is_possible = False
                    break
                if char in self.wrong_spots[i]:
                    is_possible = False
                    break

            if is_possible and all(req in pos_answer for req in self.required_letters):
                possible_matches.append(pos_answer)

        return random.choice(possible_matches) if possible_matches else None

    def valid_review(self, review):
        # Check review shape
        return len(review) == 5 and all(c in "01?" for c in review)

    def apply_review(self, review):
        # Apply one review
        for i in range(5):
            char = self.word[i]
            if review[i] == "1":
                self.confirmed[i] = char
                self.required_letters.add(char)
            elif review[i] == "?":
                self.wrong_spots[i].add(char)
                self.required_letters.add(char)
            elif review[i] == "0":
                if char not in self.required_letters:
                    self.forbidden_letters.add(char)

    def score_guess(self, answer, guess):
        # Score duplicate letters
        review = ["0"] * 5
        leftovers = {}

        for i in range(5):
            if guess[i] == answer[i]:
                review[i] = "1"
            else:
                leftovers[answer[i]] = leftovers.get(answer[i], 0) + 1

        for i in range(5):
            if review[i] != "0":
                continue
            char = guess[i]
            if leftovers.get(char, 0) > 0:
                review[i] = "?"
                leftovers[char] -= 1

        return "".join(review)

    def in_the_game(self):
        # Console game loop
        self.reset_game_state()
        self.word = random.choice(self.dictionary)

        for turn in range(1, 7):
            self.used_guesses.add(self.word)
            self._type(f"\nGuess #{turn}/6: {self.word.upper()}")
            review = input("Your Feedback (1, 0, ?): ").strip().lower()

            if review == "11111":
                self._type(f"I got it! It only took me {turn} guesses.")
                return

            if not self.valid_review(review):
                self._type("Invalid input! Please use 1, 0, or ?.")
                continue

            self.apply_review(review)
            self.word = self.get_next_guess()
            if not self.word:
                self._type("It seems the word you're looking for is not in my dictionary")
                break
        else:
            self._type("\nI used my 6 guesses and failed. You win!")

    def tile_color(self, mark, live_row):
        # Pick tile color
        if mark == "1":
            return (83, 141, 78)
        if mark == "?":
            return (181, 159, 59)
        if mark == "0" and live_row:
            return (120, 124, 126)
        if mark == "0":
            return (170, 45, 45)
        return (58, 58, 60)

    def start_gui(self):
        # Launch pygame window
        if not GUI_AVAILABLE:
            self.start_game()
            return

        self.load_words()
        self.reset_game_state()
        self.word = random.choice(self.dictionary)

        pygame.init()
        screen = pygame.display.set_mode((920, 780))
        pygame.display.set_caption("Wordy Bot")
        clock = pygame.time.Clock()

        title_font = pygame.font.SysFont(None, 52)
        info_font = pygame.font.SysFont(None, 28)
        tile_font = pygame.font.SysFont(None, 46)
        button_font = pygame.font.SysFont(None, 34)

        board_x = 260
        board_y = 150
        tile_size = 72
        tile_gap = 10
        submit_rect = pygame.Rect(382, 80, 155, 42)

        running = True
        turn = 0
        game_over = False
        message = "Click tiles for feedback."
        review_marks = ["0"] * 5
        board_words = [""] * 6
        board_reviews = [[""] * 5 for _ in range(6)]

        def submit_turn():
            nonlocal turn, game_over, message, review_marks

            # Stop bad submits
            if game_over or not self.word or turn >= 6:
                return

            guess = self.word
            review = "".join(review_marks)

            board_words[turn] = guess.upper()
            board_reviews[turn] = list(review)
            self.used_guesses.add(guess)

            if review == "11111":
                message = f"I got it in {turn + 1} guesses."
                game_over = True
                return

            self.apply_review(review)
            next_guess = self.get_next_guess()

            if turn == 5:
                message = "I used all guesses."
                game_over = True
                return

            if not next_guess:
                self.word = ""
                message = "Word missing from dictionary."
                game_over = True
                return

            self.word = next_guess
            turn += 1
            review_marks = ["0"] * 5
            message = "Next guess ready."

        while running:
            current_guess = self.word.upper() if not game_over and self.word else ""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Submit by click
                    if submit_rect.collidepoint(event.pos):
                        submit_turn()
                        continue

                    # Tile click review
                    if not game_over and turn < 6:
                        for col in range(5):
                            tile_rect = pygame.Rect(
                                board_x + col * (tile_size + tile_gap),
                                board_y + turn * (tile_size + tile_gap),
                                tile_size,
                                tile_size,
                            )
                            if tile_rect.collidepoint(event.pos):
                                if event.button == 1:
                                    review_marks[col] = "0" if review_marks[col] == "?" else "?"
                                elif event.button == 3:
                                    review_marks[col] = "0" if review_marks[col] == "1" else "1"
                                else:
                                    review_marks[col] = "0"
                                break

                elif event.type == pygame.KEYDOWN:
                    # Leave on escape
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        continue

                    # Submit by enter
                    if event.key == pygame.K_RETURN:
                        submit_turn()

            screen.fill((18, 18, 19))

            # Draw title
            title = title_font.render("WORDY BOT", True, (240, 240, 240))
            screen.blit(title, title.get_rect(center=(460, 42)))

            # Draw submit button
            pygame.draw.rect(screen, (83, 141, 78), submit_rect, border_radius=8)
            submit_text = button_font.render("Submit", True, (255, 255, 255))
            screen.blit(submit_text, submit_text.get_rect(center=submit_rect.center))

            # Draw help text
            help_text = info_font.render("Left click = Wrong Place || Right click = Correct", True, (180, 180, 180))
            screen.blit(help_text, (240, 690))

            # Draw board rows
            for row in range(6):
                row_word = board_words[row]
                row_marks = board_reviews[row]
                live_row = row == turn and not game_over
                if live_row:
                    row_word = current_guess
                    row_marks = review_marks

                for col in range(5):
                    tile_rect = pygame.Rect(
                        board_x + col * (tile_size + tile_gap),
                        board_y + row * (tile_size + tile_gap),
                        tile_size,
                        tile_size,
                    )

                    mark = row_marks[col] if col < len(row_marks) else ""
                    fill = self.tile_color(mark, live_row)
                    pygame.draw.rect(screen, fill, tile_rect, border_radius=6)
                    pygame.draw.rect(screen, (210, 214, 218), tile_rect, 2, border_radius=6)

                    if col < len(row_word):
                        letter = tile_font.render(row_word[col], True, (255, 255, 255))
                        screen.blit(letter, letter.get_rect(center=tile_rect.center))

            # Draw message line
            message_text = info_font.render(message, True, (230, 230, 230))
            screen.blit(message_text, message_text.get_rect(center=(460, 735)))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def start_game(self):
        # Start console mode
        self.load_words()
        self.greeting()
        self._type("\nAre you ready? (y/n):")
        if input("> ").lower() == "y":
            self.in_the_game()


if __name__ == "__main__":
    bot = WordyBot()
    bot.start_gui()
