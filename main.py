import os, time
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
        self.name = name
        self.score = 0

    def print_players_stats(self):
        print(f'{self.name} has a total score of {self.score}!')


class Questions:
    def __init__(self, num_questions, category):
        self.opentrivia_url = "https://opentdb.com/api.php"
        self.ammount_url = "?amount=" + str(num_questions)
        self.category_url = "&category=" + str(category)
#        self.dificulty_url = "&dificulty="
#        self.dificulty = ["easy", "medium", "hard"]

    def call_api(self):
        url = self.opentrivia_url + self.ammount_url + self.category_url
        response = requests.get(url)
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
                    print('API call failled, try again')
                    return(False)
            except:
                print('API call failled, try again')
                return(False)

    


def get_int(msg):
    while True:
        try:
            output = int(input(msg))
            if output < 0:
                print("Please enter a positive integer!")
            else:
                return(output)
        except ValueError:
            print("Please enter a integer!")
    