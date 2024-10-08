import random

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

# Function to play the Hangman game
def play_hangman():
    category = choose_category()
    word = get_word(category)
    word_letters = set(word)
    guessed_letters = set()
    tries = 6
    guessed_word = ['_'] * len(word)

    print(f"Let's play Hangman! The category is {category.capitalize()}.")

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

    if ''.join(guessed_word) == word:
        print(f"Congratulations! You've guessed the word: {word}")
    else:
        print(display_hangman(tries))
        print(f"Sorry, you ran out of tries. The word was: {word}")

# Main game loop
def main():
    while True:
        play_hangman()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye.")
            break

# Run the game
if __name__ == "__main__":
    main()