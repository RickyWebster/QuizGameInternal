import os, time, random
try:
    import requests
except ImportError:
    print("You need to have the requests library installed before running this program")
    print("do this by entering 'pip install requests' into your computer's terminal")
    print("Try running this program again when you have done this")
    print("Exiting...")
    os._exit(1)


class Player:
    def __init__(self, name):
        self.name = name.title()
        self.score = 0
        self.incorrect = 0


    def print_players_stats(self):
        print(f'\n{self.name} had a total score of {self.score}!')
        print(f'They awnsered {(self.score / (self.score + self.incorrect)) * 100:.2f}% of their questions correct')

    
    def play_turn(self, question):
        print(f"\n{self.name}s turn")
        number_of_awnsers = len(question["incorrect_answers"]) + 1
        correct_awnser = random.randint(0, number_of_awnsers - 1)
        awnsers_list = question["incorrect_answers"]
        random.shuffle(awnsers_list)
        awnsers_list.insert(correct_awnser, question["correct_answer"])
        print(f'Question: {question["question"]}')
        for index, awnser in enumerate(awnsers_list):
            print(f'{index + 1}. {awnser}')
        while True:
            choice = get_int()
            if choice <= number_of_awnsers and choice > 0:
                break
            else:
                print(f'Please Chose one of the options(1-{number_of_awnsers})')
        if choice - 1 == correct_awnser:
            print('Correct!!!!')
            self.score += 1
        else:
            print('Incorect')
            self.incorrect += 1
            print(f'The correct awnser was: {correct_awnser + 1}. {question["correct_answer"]}')


class Questions:
    def __init__(self, num_players, category):
        self.opentrivia_url = "https://opentdb.com/api.php"
        self.ammount_url = "?amount=" + str(num_players)
        self.category_url = "&category=" + str(category)
#        self.dificulty_url = "&dificulty="
#        self.dificulty = ["easy", "medium", "hard"]


    def call_api(self):
        url = self.opentrivia_url + self.ammount_url + self.category_url
        try:
            response = requests.get(url)
        except:
            return(False)
        if response.status_code == 200:
            json_data = response.json()
            return(json_data)
        else:
            try:
                json_data = response.json()
                if json_data['response_code'] == 5:
                    print('Api called too many times. Wating 30 seconds before trying again')
                    time.sleep(30)
                    self.call_api(url)
                else:
                    return(False)
            except:
                return(False)
        

def get_int():
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


#variable defined 
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

#MAIN ROUTIENE
#Setting up the player objects
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

    print(f'How many questions do you want the player(s) on this topic?(Max 5)')
    while True:
        number_questions = get_int()
        if number_questions > 0 and number_questions <= 5:
            break
        else:
            print("Please choose a number 1 - 5.")

    rounds_questions = Questions(num_players, catagory_id)

    for i in range(number_questions):
        returned_questions = rounds_questions.call_api()
        if returned_questions == False:
            count -= 1
            print("API call Failed!!")
            print("Mabey you aren't connect to the internet??")
            print("Please try again.")
            break
        for index, player in enumerate(all_players):
            player.play_turn(returned_questions["results"][index])

    print('Press 0 to EXIT or ENTER to play another round(any other key also works to continue)')
    exit = input('> ')
    if exit == "0":
        for player in all_players:
            player.print_players_stats()
            all_scores.append(player.score)
        winners = [index for index, value in enumerate(all_scores) if value == max(all_scores)]
        if len(winners) > 1:
            print('\nTie!!!')
            print('\nOur winners are:')
            for player in winners:
                print(all_players[player].name)
        else:
            print(f'\n{all_players[winners[0]].name} Wins!!!!!!')
                
        print('\nThank you for playing')
        break

    count += 1
