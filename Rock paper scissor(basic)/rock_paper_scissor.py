import random

class RockPaperScissors:
    def __init__(self):
        self.options = ['Rock', 'Paper', 'Scissor']
        self.endgame = True

    def get_human_choice(self):
        try:
            user_input = int(input("Enter a number (1 for Rock, 2 for Paper, 3 for Scissor): "))
            if user_input in [1, 2, 3]:
                return self.options[user_input - 1]
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                return None
        except ValueError:
            print("Please enter a valid number.")
            return None

    def get_computer_choice(self):
        return random.choice(self.options)

    def decide_winner(self, human, computer):
        print(f"You chose: {human}")
        print(f"Computer chose: {computer}")

        if human == computer:
            print("It's a draw!")
        elif (human == "Rock" and computer == "Scissor") or \
             (human == "Paper" and computer == "Rock") or \
             (human == "Scissor" and computer == "Paper"):
            print("You win!")
        else:
            print("Computer wins!")

    def play(self):
        print("""
Welcome to the Rock, Paper, and Scissor Game!
Rules:
  Enter 1 for Rock
  Enter 2 for Paper
  Enter 3 for Scissor
""")
        while self.endgame:
            human_choice = None
            while human_choice is None:
                human_choice = self.get_human_choice()

            computer_choice = self.get_computer_choice()
            self.decide_winner(human_choice, computer_choice)

            play_again = input("Type 'y' to play again or 'n' to quit: ").lower()
            if play_again == 'n':
                self.endgame = False
                print("Thanks for playing!")

# Start the game
game = RockPaperScissors()
game.play()
