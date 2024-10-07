import random
import os
from datetime import datetime  # Import datetime module

# Categories of words for the game
categories = {
    'fruits': ['apple', 'banana', 'grape', 'orange', 'pineapple'],
    'animals': ['elephant', 'tiger', 'giraffe', 'kangaroo', 'penguin'],
    'countries': ['france', 'germany', 'brazil', 'japan', 'canada']
}

# Display hangman stages
def display_hangman(tries):
    stages = [
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / 
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |      
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|
           |      |
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |    
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      
           |    
           |      
           |     
           -
        """
    ]
    return stages[tries]

# Function to choose a random word from a chosen category
def get_word(category):
    return random.choice(categories[category]).lower()

# Function to allow the player to choose a category
def choose_category():
    print("Choose a category:")
    for idx, category in enumerate(categories.keys(), 1):
        print(f"{idx}. {category.capitalize()}")
    while True:
        try:
            choice = int(input("Enter the number of the category: "))
            if 1 <= choice <= len(categories):
                return list(categories.keys())[choice - 1]
            else:
                print("Please enter a valid category number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to provide hints (first and last letter of the word)
def provide_hint(word):
    return f"The first letter is '{word[0]}' and the last letter is '{word[-1]}'."

# Load scores from file, including date and time
def load_scores(filename="scores.txt"):
    scores = {}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    try:
                        name, score, date_time = line.strip().split(":")
                        scores[name] = (int(score), date_time)
                    except ValueError:
                        print(f"Malformed line in scores.txt: {line}")
    return scores

# Save scores to file with date and time
def save_scores(scores, filename="scores.txt"):
    with open(filename, "w") as file:
        for name, (score, date_time) in scores.items():
            file.write(f"{name}:{score}:{date_time}\n")

# Display leaderboard with date and time
def display_leaderboard(scores):
    if scores:
        print("\nLeaderboard:")
        sorted_scores = sorted(scores.items(), key=lambda item: item[1][0], reverse=True)
        for rank, (name, (score, date_time)) in enumerate(sorted_scores, 1):
            print(f"{rank}. {name}: {score} points (achieved on {date_time})")
    else:
        print("\nNo scores yet.")

# Calculate score based on remaining tries
def calculate_score(tries_left):
    return tries_left * 10  # Example scoring: 10 points per remaining try

# Function to play the Hangman game
def play_hangman():
    # Load previous scores
    scores = load_scores()
    
    # Ask for player's name
    player_name = input("Enter your name: ")

    # Category selection
    category = choose_category()
    word = get_word(category)
    word_letters = set(word)  # letters in the word to be guessed
    guessed_letters = set()   # letters guessed by the player
    tries = 6  # number of tries before the player loses
    guessed_word = ['_'] * len(word)  # current state of guessed word
    hints_available = 1  # Player can use 1 hint per game

    print(f"Let's play Hangman! The category is {category.capitalize()}.")

    # Main game loop
    while tries > 0 and ''.join(guessed_word) != word:
        print(display_hangman(tries))
        print('Current word:', ' '.join(guessed_word))
        print(f'Guessed letters: {", ".join(guessed_letters)}')
        print(f'You have {tries} tries left.')

        # Ask the player if they want a hint
        if hints_available > 0:
            use_hint = input("Would you like a hint? (yes/no): ").lower()
            if use_hint == 'yes':
                print(provide_hint(word))
                hints_available -= 1
                continue

        guess = input('Guess a letter: ').lower()

        # Input validation: ensure only a single letter is entered
        if len(guess) != 1 or not guess.isalpha():
            print("Please guess a single valid letter.")
            continue

        # Check if the letter was already guessed
        if guess in guessed_letters:
            print("You've already guessed this letter.")
            continue

        guessed_letters.add(guess)

        # Check if the guess is correct
        if guess in word_letters:
            print(f"Good guess! {guess} is in the word.")
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_word[i] = guess
        else:
            tries -= 1
            print(f"Sorry, {guess} is not in the word. You have {tries} tries left.")

    # Check if the player won or lost
    if ''.join(guessed_word) == word:
        print(f"Congratulations! You've guessed the word: {word}")
        score = calculate_score(tries)  # Calculate score based on remaining tries
        print(f"Your score: {score} points")
    else:
        print(display_hangman(tries))
        print(f"Sorry, you ran out of tries. The word was: {word}")
        score = 0

    # Get the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update and save player score
    if player_name in scores:
        scores[player_name] = (max(scores[player_name][0], score), current_time)  # Keep the highest score and update the time
    else:
        scores[player_name] = (score, current_time)
    save_scores(scores)

    # Show leaderboard
    display_leaderboard(scores)

# Run the enhanced game with scoring system and date/time tracking
play_hangman()