from games import snake
from models import Player, Session
import os
import pygame

def main():
    pygame.mixer.init()
    session = Session()

    while True:
        os.system("clear")
        print('''
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
        ''')

        print("S ==> Play snake")
        print("T ==> Top 10 scores")
        print("Q ==> Quit")

        choice = input("Please enter your choice: ")

        if choice in ('S', 's'):
            print("Enter your player name (leave it blank if you don't want to record your score):")
            player_name = input("> ").strip()  # Remove leading/trailing spaces

            while True:
                # Play the game and get the score
                score, play_again = snake.play()  

                # Only create a new Player object if player_name is not empty
                if player_name:
                    new_player = Player(name=player_name, score=score)
                    session.add(new_player)
                    session.commit()
                    print(f"Final score = {score}")
                else:
                    print(f"Final score = {score}, but it's not recorded as no player name was provided")
                
                if not play_again:
                    break
        elif choice in ('T', 't'):
            top_players = session.query(Player).order_by(Player.score.desc()).limit(10).all()
            print("\nTop 10 players:")
            for player in top_players:
                print(f"{player.name} - {player.score}")
            input("\nPress any key to return to the main menu.")
        elif choice in ('Q', 'q'):
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
