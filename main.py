try:
    import requests
except ImportError:
    print("You need to install the requests library")
    print("EDIT TO PROVIDE INSTRUCTIONS AND CRASH CODE")

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class QuizApi:
    def __init__(self):
        self.url = ""


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


if __name__ == "__main__":
    print()











