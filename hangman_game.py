import random
import string

WORDLIST_FILENAME = "hangman_words.txt"

def load_words():
    """
    returns: list, a list of valid words. Words are strings of lowercase letters.
    """
    # inFile: file
    with open(WORDLIST_FILENAME, 'r') as inFile:
        # line: string
        line = inFile.readline()
        # wordlist: list of strings
        wordlist = line.split()
    print(" ", len(wordlist), "words loaded.")
    return wordlist
    
def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

# Loading list of words in global scope
wordlist = load_words()

def has_player_won(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    """
    guessed_dict = {letter: True for letter in letters_guessed}

    for required_letter in secret_word:
       if guessed_dict.get(required_letter, False) == False:
            return False
       
    return True

def get_word_progress(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters and asterisks (*) that represents
        which letters in secret_word have not been guessed so far
    """
    letters_guessed_set = set(letters_guessed)

    answer_results = ''.join(i if i in letters_guessed_set else '*' for i in secret_word)

    return answer_results


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
      letters have not yet been guessed. The letters should be returned in
      alphabetical order
    """
    letters_guessed_set = set(letters_guessed)
    unguessed_letters = ''.join(i for i in string.ascii_lowercase if i not in letters_guessed_set)
    
    return unguessed_letters


def get_help(secret_word, get_available_letters):
    """
    wordlist (list): list of valid words (strings) to choose from.

    returns: string, a single word chosen randomly from the wordlist.
    """
    choose_from = []
    for i in secret_word:
       if i in set(get_available_letters):
          choose_from.append(i)

    new = random.randint(0, len(choose_from)-1)
    revealed_letter = choose_from[new]

    return revealed_letter
  
# starts game of hangman
def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.
    with_help: boolean, this enables help functionality if true.

    """
    print("Welcome to Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print('-------------------')

    guesses = 10
    letters_guessed = []
    correct_letters = []

    while guesses > 0:
        print(f"You have {guesses} guesses left")
        print(f"available letters: {get_available_letters(letters_guessed)}")
        print(f"used letters: {set(letters_guessed)}")
        guess = input("Please guess a letter: ").lower()

        while len(guess) > 1 or guess not in (string.ascii_lowercase + "!"):
          if guess not in string.ascii_lowercase:
              guess = input("Incorrect Input, Please guess a letter: ").lower()
          else:
              guess = input("Invalid input, please enter a letter (a-z): ").lower()

        if guess != '!':
            letters_guessed.append(guess)
        
        if guess == '!':
           if guesses <= 3:
            print(f"You Only Have {guesses} Guesses Left, You Cannot Use a Hint")
           else:
            available_letters = get_available_letters(letters_guessed)
            revealed_letter = get_help(secret_word, available_letters)
            letters_guessed.append(revealed_letter)
            print(f"Here's Your Hint: {get_word_progress(secret_word, letters_guessed)}")
            guesses -= 3
        
        else:
            for i in guess:
                if i not in secret_word:
                  if i in correct_letters:
                      print(f"you have already guessed this letter, try again: {get_word_progress(secret_word, letters_guessed)}")
                  else:
                    print(f"Oops! That letter is not in my word: {get_word_progress(secret_word, letters_guessed)}")
                    if guess in 'aeiou':
                      guesses -= 2
                    else:
                      guesses -= 1
                elif i in correct_letters:
                  print(f"you have already guessed this letter, try again")
                else:
                  print(f"Good guess: {get_word_progress(secret_word, letters_guessed)}")

        correct_letters.append(guess)
        if has_player_won(secret_word, letters_guessed) == True:
           break

    if has_player_won(secret_word, letters_guessed) == True:
          print("You Guessed Correctly!")
          unique_letters = [i for i in set(secret_word)]
          print(f"Your total Score is: {(guesses + 4 * len(unique_letters)) + (3 * len(secret_word))}")
    else: #if guesses <= 0 and has_player_won(secret_word, letters_guessed) == False
        print(f"You Lost, The Secret Word Was '{secret_word}'")

if __name__ == "__main__":

    secret_word = choose_word(wordlist)
    hangman(secret_word)
