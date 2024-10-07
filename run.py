import random
import os
import time
from datetime import datetime

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

# Function to provide hints
def provide_hint(word):
    return f"The first letter is '{word[0]}' and the last letter is '{word[-1]}'."

# Function to load scores from file
def load_scores(filename="scores.txt"):
    scores = {}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split(":")
                    if len(parts) == 4:  # Ensure there are exactly four parts
                        name, total_score, current_score, date_time = parts
                        try:
                            scores[name] = (int(total_score), int(current_score), date_time)
                        except ValueError:
                            print(f"Invalid score value for {name}: {total_score} or {current_score}. Skipping this entry.")
                    else:
                        print(f"Malformed line in scores.txt: {line.strip()}")
    print("Loaded scores:", scores)  # Debugging statement
    return scores

# Function to save scores to file
def save_scores(scores, filename="scores.txt"):
    with open(filename, "w") as file:
        for name, (total_score, current_score, date_time) in scores.items():
            file.write(f"{name}:{total_score}:{current_score}:{date_time}\n")
    print("Saved scores:", scores)  # Debugging statement

# Function to display leaderboard
def display_leaderboard(scores):
    if scores:
        print("\nLeaderboard:")
        sorted_scores = sorted(scores.items(), key=lambda item: item[1][0], reverse=True)
        for rank, (name, (total_score, current_score, date_time)) in enumerate(sorted_scores, 1):
            print(f"{rank}. {name}: {total_score} total points (last score: {current_score} on {date_time})")
    else:
        print("\nNo scores yet.")

# Function to calculate score based on remaining tries
def calculate_score(tries_left):
    return tries_left * 10  # Example scoring: 10 points per remaining try

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
    time_limit = 10  # seconds to guess a letter

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

        # Timer for guessing
        start_time = time.time()
        guess = input(f'Guess a letter (you have {time_limit} seconds): ').lower()
        elapsed_time = time.time() - start_time

        if elapsed_time > time_limit:
            print("Time's up! You took too long to guess.")
            tries -= 1
            continue

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
        current_score = calculate_score(tries)  # Calculate score based on remaining tries
        print(f"Your score: {current_score} points")
    else:
        print(display_hangman(tries))
        print(f"Sorry, you ran out of tries. The word was: {word}")
        current_score = 0

    # Get the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update and save player score
    if player_name in scores:
        total_score, _, _ = scores[player_name]
        total_score += current_score  # Update total score
        scores[player_name] = (total_score, current_score, current_time)  # Save total and current score
        print(f"Updated {player_name}'s total score to {total_score}.")  # Debugging statement
    else:
        scores[player_name] = (current_score, current_score, current_time)  # First entry
        print(f"Added new player {player_name} with score {current_score}.")  # Debugging statement

    # Save updated scores to file
    save_scores(scores)

    # Show leaderboard
    display_leaderboard(scores)

# Main game loop with restart option
def main():
    while True:
        play_hangman()
        # Ask if the player wants to play again or exit
        play_again = input("Do you want to play again or exit? (Type 'play' to play again, 'exit' to leave): ").lower()
        while play_again not in ['play', 'exit']:
            play_again = input("Invalid choice. Type 'play' to play again, or 'exit' to leave: ").lower()
        if play_again == 'exit':
            print("Thanks for playing! Goodbye.")
            break  # Exit the game loop and end the program

# Run the game with restart option
if __name__ == "__main__":
    main()