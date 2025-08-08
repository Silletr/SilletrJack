import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_process.player import PlayerHand

def main():
    game = PlayerHand()
    game.deal_initial_cards()

    while True:
        game.show_hands()
        
        if game.user_choice == 1:  # Stay
            print("Player stays.")
            break 
        elif game.user_choice == 2:  # Hit
            card = game.deck.pop()
            game.player_hand.append(card)
            print(f"Player hits and gets: {card}")
            if game.calculate_hand_value(game.player_hand) > 21:
                print("Player busts!")
                break
        else:
            print("Invalid choice, please enter 1 (stay) or 2 (hit).")

    game.card_comparison()

if __name__ == "__main__":
    main()

