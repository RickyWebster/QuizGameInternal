"""
This program is a trivia game.

Or more spesifically, Ricky's Level 3 Python Internal Using OOP and APIs Trivia Game!!!
In this game, playes awnser trivia questions from the OpenTrivia API and try to get the highest score.
"""

# Library Imports
import os
import time
import random
import html
try:
    import requests
except ImportError:
    print("You need to have the requests library installed before running this program")
    print("do this by entering 'pip install requests' into your computer's terminal")
    print("Try running this program again when you have done this")
    print("Exiting...")
    os._exit(1)


class Player:
    """Represents a player in the game."""

    def __init__(self, name):
        """
        Initializes a player with a name, score, and incorrect answers count.

        name: string
        score: int
        incorrect: int
        """
        self.name = name.title()
        self.score = 0
        self.incorrect = 0

    def print_players_stats(self):
        """Prints the players name, score, and correct percentage."""
        print(f'\n{self.name} had a total score of {self.score}!')
        correct_percentage = (self.score / (self.score + self.incorrect)) * 100
        print(f'They awnsered {correct_percentage:.2f}% of their questions correct')

    def play_turn(self, question):
        """
        Allows the player to play a turn by answering a question.

        Parameters:
        question (dict): Dictionary containing the question, the awnsers, and some wrong awnsers
        """
        print(f"\n{self.name}s turn")
        number_of_awnsers = len(question["incorrect_answers"]) + 1
        correct_awnser = random.randint(0, number_of_awnsers - 1)  # Chooses placing of awnser in list of awnsers
        awnsers_list = question["incorrect_answers"]  # Creates a list of incorrect awnsers.
        random.shuffle(awnsers_list)
        awnsers_list.insert(correct_awnser, question["correct_answer"])  # Adds correct awnser to list of awnsers
        decoded_question = html.unescape(question["question"])  # Displays " and & correctly
        print(f'Question: {decoded_question}')
        for index, awnser in enumerate(awnsers_list):  # Prints awnsers
            print(f'{index + 1}. {awnser}')
        while True:
            choice = get_int()
            if choice <= number_of_awnsers and choice > 0:  # Input validation
                break
            else:
                print(f'Please Chose one of the options(1-{number_of_awnsers})')
        if choice - 1 == correct_awnser:  # Cheacking for correct or not awnsers
            print('Correct!!!!')
            self.score += 1
        else:
            print('Incorect')
            self.incorrect += 1
            print(f'The correct awnser was: {correct_awnser + 1}. {question["correct_answer"]}')


class Questions:
    """Creates trivia questions."""

    def __init__(self, num_players, category):
        """
        Initializes a set of questions with the URLs.

        opentrivia_url: sting
        ammount_url: string
        category_url: string
        difficulty_url: string
        """
        self.opentrivia_url = "https://opentdb.com/api.php"
        self.ammount_url = "?amount=" + str(num_players)
        self.category_url = "&category=" + str(category)
        self.difficulty_url = "&difficulty="

    def call_api(self, difficulty):
        """
        Calls the OpenTrivia API to get a set of questions.

        Parameters:
        difficulty (string): A string like 'easy' that is apart of the url
        """
        url = self.opentrivia_url + self.ammount_url + self.category_url + self.difficulty_url + difficulty
        try:
            response = requests.get(url)  # Calls API
        except:
            return(False)
        if response.status_code == 200:
            json_data = response.json()  # Converts response to JSON
            return(json_data)
        else:  # Below is input validation cheacking API call had no problems
            try:
                json_data = response.json()
                if json_data['response_code'] == 5:
                    print('Api called too many times. Wating 20 seconds before trying again')
                    time.sleep(20)
                    return(self.call_api(url))
                else:
                    return(False)
            except:
                return(False)


def get_int():
    """Get's input from the user and ensures it's a positive integer(Input validation)."""
    while True:
        try:
            output = int(input("> "))
            print()
            if output < 0:
                print("Please enter a positive integer!")
            else:
                return(output)
        except ValueError:
            print("Please enter a integer!")


if __name__ == "__main__":
    # variables defined
    all_players = []
    all_scores = []
    count = 1
    catagorys_list = [
        ["Books", 10],
        ["Film", 11],
        ["Science & Nature", 17],
        ["Computers", 18],
        ["Mathmatics", 19],
        ["Sports", 21],
        ["Geography", 22],
        ["History", 23],
        ["Animals", 27],
        ["Vehicles", 28]
    ]
    difficulty_options = ["easy", "medium", "hard"]

    # Setting up the player objects. Players are asked how many players and for names.
    # Player objects are then set up and stored in list.
    print("\nWelcome to Ricky's Level 3 Python Internal Using OOP and APIs Trivia Game!!!")
    while True:
        print("how many players will be playing?(max 5)")
        num_players = get_int()
        if num_players > 5 or num_players < 1:
            print("You can have a maximum number of 5 players and you have to have at least 1")
        else:
            break
    for i in range(num_players):
        print(f"what is player {i + 1}'s name?")
        name = str(input('> '))
        all_players.append(Player(name))

    while True:
        # Choosing the catagory. All catagories in the catagorys_list are printed out in two colloums
        # Using a .format and :<{22} to set the width of the left feild to 22
        # Input is then go t form the user when they enter in the number corosponding to a catagory
        print(f'\nRound {count}!')
        print(f'What catagory do you choose for round {count}:')
        for index, catagories in enumerate(catagorys_list[::2]):
            coloum1 = f"{index * 2 + 1}. {catagories[0]}"
            coloum2 = F"{index * 2 + 2}. {catagorys_list[index * 2 + 1][0]}"
            print("{:<{}} {}".format(coloum1, 22, coloum2))
        while True:
            catagory = get_int()
            if catagory < 11 and catagory > 0:
                break
            else:
                print("Please choose one of the options(1-10).")
        catagory_id = catagorys_list[catagory - 1][1]

        # Choosing the ammount of questions per player
        print('How many questions do you want the player(s) on this topic?(Max 5)')
        while True:
            number_questions = get_int()
            if number_questions > 0 and number_questions <= 5:
                break
            else:
                print("Please choose a number 1 - 5.")

        # Setting up the questions object for this round's questions
        rounds_questions = Questions(num_players, catagory_id)

        # Calling the call_api function in the Questions class to get the set of questions
        # And the play_turn function in the player class so the player can play ther turn
        for i in range(number_questions):
            local_difficulty = difficulty_options[random.randint(0, 2)]
            returned_questions = rounds_questions.call_api(local_difficulty)
            if returned_questions is False:  # Cheacking if API call failed
                count -= 1
                print("API call Failed!!")
                print("Mabey you aren't connect to the internet??")
                print("Please try again.")
                break
            for index, player in enumerate(all_players):
                player.play_turn(returned_questions["results"][index])

        # Allows the player to exit or continue. If they exit, the stats of the players are shown.
        print('Press 0 to EXIT or ENTER to play another round(any other key also works to continue)')
        exit = input('> ')
        if exit == "0":
            for player in all_players:
                player.print_players_stats()
                all_scores.append(player.score)
            winners = []
            for index, value in enumerate(all_scores):  # Getting and displaying the winners
                if value == max(all_scores):
                    winners.append(index)
            if len(winners) > 1:
                print('\nTie!!!')
                print('\nOur winners are:')
                for player in winners:
                    print(all_players[player].name)
            else:
                print(f'\n{all_players[winners[0]].name} Wins!!!!!!')
            print('\nThank you for playing')
            break

        # Adds one to the count verable that keeps track of what round it is.
        count += 1
