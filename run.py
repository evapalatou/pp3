import random
import os

ascii_art = r'''
 /$$$$$$$$ /$$                       /$$   /$$                                                                
|__  $$__/| $$                      | $$  | $$                                                                
   | $$   | $$$$$$$   /$$$$$$       | $$  | $$  /$$$$$$  /$$$$$$$   /$$$$$$  /$$$$$$/$$$$   /$$$$$$  /$$$$$$$ 
   | $$   | $$__  $$ /$$__  $$      | $$$$$$$$ |____  $$| $$__  $$ /$$__  $$| $$_  $$_  $$ |____  $$| $$__  $$
   | $$   | $$  \ $$| $$$$$$$$      | $$__  $$  /$$$$$$$| $$  \ $$| $$  \ $$| $$ \ $$ \ $$  /$$$$$$$| $$  \ $$
   | $$   | $$  | $$| $$_____/      | $$  | $$ /$$__  $$| $$  | $$| $$  | $$| $$ | $$ | $$ /$$__  $$| $$  | $$
   | $$   | $$  | $$|  $$$$$$$      | $$  | $$|  $$$$$$$| $$  | $$|  $$$$$$$| $$ | $$ | $$|  $$$$$$$| $$  | $$
   |__/   |__/  |__/ \_______/      |__/  |__/ \_______/|__/  |__/ \____  $$|__/ |__/ |__/ \_______/|__/  |__/
                                                                   /$$  \ $$                                  
                                                                  |  $$$$$$/                                  
                                                                   \______/                                   
'''

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

# Function to choose a category
def choose_category():
    print("Choose a category:")
    for idx, category in enumerate(categories.keys(), 1):
        print(f"{idx}. {category.capitalize()}")
    choice = int(input("Enter the number of the category: ")) - 1
    return list(categories.keys())[choice]

# Load scores from file
def load_scores(filename="scores.txt"):
    scores = {}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                try:
                    name, score = line.strip().split(":")
                    scores[name] = int(score)
                except ValueError:
                    print(f"Skipping malformed line: {line.strip()}")  # Debugging output
    return scores

# Save scores to file
def save_scores(scores, filename="scores.txt"):
    with open(filename, "w") as file:
        for name, score in scores.items():
            file.write(f"{name}:{score}\n")

# Function to play the Hangman game
def play_hangman(scores):
    category = choose_category()
    word = get_word(category)
    word_letters = set(word)
    guessed_letters = set()
    tries = 6
    guessed_word = ['_'] * len(word)

    print(f"\nLet's play Hangman! The category is {category.capitalize()}.")

    while tries > 0 and ''.join(guessed_word) != word:
        print(display_hangman(tries))
        print('Current word:', ' '.join(guessed_word))
        print(f'Guessed letters: {", ".join(guessed_letters)}')
        print(f'You have {tries} tries left.')

        guess = input('Guess a letter: ').lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please guess a single valid letter.")
            continue

        if guess in guessed_letters:
            print("You've already guessed this letter.")
            continue

        guessed_letters.add(guess)

        if guess in word_letters:
            print(f"Good guess! {guess} is in the word.")
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_word[i] = guess
        else:
            tries -= 1
            print(f"Sorry, {guess} is not in the word. You have {tries} tries left.")

    # Score calculation
    if ''.join(guessed_word) == word:
        print(f"Congratulations! You've guessed the word: {word}")
        score = tries * 10  # 10 points for each try left
        print(f"Your score: {score} points")
        return score
    else:
        print(display_hangman(tries))
        print(f"Sorry, you ran out of tries. The word was: {word}")
        return 0

# Main game loop
def main():
    scores = load_scores()
    player_name = input("Enter your name: ")

    while True:
        score = play_hangman(scores)
        if player_name in scores:
            scores[player_name] += score  # Accumulate score
        else:
            scores[player_name] = score  # Add new player

        save_scores(scores)  # Save updated scores
        print(f"Updated Scores: {scores}")  # Debugging output for scores

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye.")
            break

# Run the game
if __name__ == "__main__":
    main()