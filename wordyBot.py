#This code implements a bot(named wordy) that need to guess a word(5 letters) prompted by the user
#The concept of this code is similar to the concept of the game Wordle
#Wordy need to guess the word within 6 guesses and if not the user the game

import sys
import time
import random

class WordyBot:
    def __init__(self, type_speed=0.02):
        self.type_speed = type_speed
        self.word = "" #Wordy's guess
        self.dictionary = []#The used words but not the answer
        self.confirmed = [None] * 5 # a list that stores the right letter with the right position(marked as 1)
        self.required_letters = set()# a set that stores the right letter but with the wrong position or with the right position(marked as 1 or ?)
        self.forbidden_letters = set()# a set that stores the wrong letter and not to be used in later guesses
        self.wrong_spots = [set() for _ in range(5)]# this set stores the wrong were each letter (marked as ?)where ws the position when they were marked to never put the same letter in the same position
        self.used_guesses = set() 

    def _type(self, text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.type_speed)
        print() 

    def greeting(self):
        self._type("Hello there!I'am Wordy, wanna play a game?")
        self._type("--- WORDY BOT RULES ---")
        self._type("1. I will guess a 5-letter word.")
        self._type("2. You must reply with 5 marks based on my guess:")
        self._type("   [ 1 ] = Letter is correct and in the right spot.")
        self._type("   [ ? ] = Letter is in the word, but in the wrong spot.")
        self._type("   [ 0 ] = Letter is not in the word at all.")
        self._type("3. Example: If I guess HELLO and only 'H' is right, enter 10000.")
        self._type("4. I have exactly 6 guesses to find your word!")
        self._type("-----------------------")

    def load_words(self):
        #Error handling for the file
        try:
            with open("five_letter_words.txt", "r") as f:
                self.dictionary = [line.strip().lower() for line in f.readlines() if len(line.strip()) == 5]
        except FileNotFoundError:
            self._type("Error: five_letter_words.txt not found!")
            sys.exit()

    def get_next_guess(self):
        possible_matches = []
        for candidate in self.dictionary:
            if candidate in self.used_guesses:
                continue
            is_possible = True
            for i in range(5):
                char = candidate[i]
                if self.confirmed[i] and char != self.confirmed[i]:
                    is_possible = False; break
                if char in self.forbidden_letters and char not in self.required_letters:
                    is_possible = False; break
                if char in self.wrong_spots[i]:
                    is_possible = False; break
            
            if is_possible and all(req in candidate for req in self.required_letters):
                possible_matches.append(candidate)
        
        return random.choice(possible_matches) if possible_matches else None

    def in_the_game(self):
        self.word = random.choice(self.dictionary)
        for turn in range(1, 7):
            self.used_guesses.add(self.word)
            self._type(f"\nGuess #{turn}/6: {self.word.upper()}")
            review = input("Your Feedback (1, 0, ?): ").strip().lower()

            if review == "11111":
                self._type(f"I got it! It only took me {turn} guesses.")
                return

            if len(review) != 5 or not all(c in "01?" for c in review):
                self._type("Invalid input! Please use 1, 0, or ?.")
                continue

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

            self.word = self.get_next_guess()
            if not self.word:
                self._type("I've run out of words!")
                break
        else:
            self._type("\nI used my 6 guesses and failed. You win!")

    def start_game(self):
        self.load_words()
        self.greeting()
        self._type("\nAre you ready? (y/n):")
        if input("> ").lower() == 'y':
            self.in_the_game()


if __name__ == "__main__":
    bot = WordyBot()
    bot.start_game()