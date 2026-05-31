import random

# ─────────────────────────────────────────
#  Predefined word list
# ─────────────────────────────────────────
WORDS = ["python", "hangman", "keyboard", "journey", "science"]

# ─────────────────────────────────────────
#  Hangman ASCII art stages (0 = safe, 6 = dead)
# ─────────────────────────────────────────
HANGMAN_STAGES = [
    """
       ------
       |    |
            |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
    =========
    """
]

# ─────────────────────────────────────────
#  Helper functions
# ─────────────────────────────────────────
def display_state(wrong_count, guessed_letters, secret_word):
    """Print the hangman figure, guessed letters, and word progress."""
    print(HANGMAN_STAGES[wrong_count])

    # Show word with blanks for un-guessed letters
    display_word = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )
    print(f"  Word : {display_word}")
    print(f"  Wrong guesses left : {6 - wrong_count}")
    print(f"  Letters tried      : {', '.join(sorted(guessed_letters)) or 'None'}")
    print()


def is_won(secret_word, guessed_letters):
    """Return True if every letter in the word has been guessed."""
    return all(letter in guessed_letters for letter in secret_word)


def get_valid_guess(guessed_letters):
    """Prompt the player until they enter a single, un-tried letter."""
    while True:
        guess = input("  Guess a letter: ").strip().lower()
        if len(guess) != 1:
            print("  ⚠  Please enter exactly ONE letter.")
        elif not guess.isalpha():
            print("  ⚠  Only alphabetic characters are allowed.")
        elif guess in guessed_letters:
            print(f"  ⚠  You already tried '{guess}'. Pick a different letter.")
        else:
            return guess


# ─────────────────────────────────────────
#  Main game loop
# ─────────────────────────────────────────
def play_hangman():
    print("=" * 45)
    print("          W E L C O M E  T O  H A N G M A N")
    print("=" * 45)
    print("  Guess the hidden word — one letter at a time.")
    print("  You have 6 wrong guesses before it's over.\n")

    while True:
        # Setup for one round
        secret_word     = random.choice(WORDS)
        guessed_letters = set()
        wrong_count     = 0

        print(f"  A new word has been chosen ({len(secret_word)} letters). Good luck!\n")

        # ── Round loop ──────────────────────────────
        while wrong_count < 6:
            display_state(wrong_count, guessed_letters, secret_word)

            guess = get_valid_guess(guessed_letters)
            guessed_letters.add(guess)

            if guess in secret_word:
                print(f"\n  ✅  Nice! '{guess}' is in the word.\n")
                if is_won(secret_word, guessed_letters):
                    display_state(wrong_count, guessed_letters, secret_word)
                    print(f"  🎉  You won! The word was '{secret_word}'.\n")
                    break
            else:
                wrong_count += 1
                print(f"\n  ❌  Wrong! '{guess}' is not in the word. "
                      f"({6 - wrong_count} guess{'es' if 6 - wrong_count != 1 else ''} left)\n")
        else:
            # Ran out of guesses
            display_state(wrong_count, guessed_letters, secret_word)
            print(f"  💀  Game over! The word was '{secret_word}'.\n")

        # ── Play again? ─────────────────────────────
        again = input("  Play again? (y / n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing Hangman! Goodbye. 👋\n")
            break
        print("\n" + "=" * 45 + "\n")


if __name__ == "__main__":
    play_hangman()
