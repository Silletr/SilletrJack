import random
from typing import List, Optional
from time import sleep

class PlayerHand:
    def __init__(self) -> None:
        # Initialize full shuffled deck and empty hands for both player and dealer
        self.deck = self.generate_full_deck()
        random.shuffle(self.deck)

        self.player_hand: List[str] = []
        self.dealer_hand: List[str] = []

        self.player_choice = 0
        self.dealer_choice = 0
        
        # Improved messages dictionary with all game outcomes
        self.messages = {
            "Dealer": {
                "blackjack": "Dealer wins with Natural BlackJack!",
                "bust": "Dealer busts!",
                "win": "Dealer wins with higher score!",
                "stay": "Dealer stayed, current score: {}"
            },
            "User": {
                "blackjack": "Player wins with Natural BlackJack!",
                "bust": "Player busts!",
                "win": "Player wins with higher score!",
                "stay": "Player stayed, current score: {}"
            }
        }
        
        self.player_hand_result: Optional[int] = None
        self.dealer_hand_result: Optional[int] = None

    def generate_full_deck(self) -> List[str]:
        """Generate standard 52-card deck, without suits."""
        base_cards = [str(i) for i in range(2, 11)] + ['K', 'Q', 'A', 'J']
        return base_cards * 4  # 4 of each card, like in standard deck

    def deal_initial_cards(self):
        """Deal two cards each to player and dealer from the top of the deck."""
        if len(self.deck) < 4:
            raise ValueError("Not enough cards in deck for initial deal!")
            
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def show_hands(self):
        """Display both hands and let user choose action if score < 21."""
        self.player_hand_result = self.calculate_hand_value(self.player_hand)
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)

        print(f"🎮 Player's hand: {self.player_hand} = {self.player_hand_result}\n")
        print(f"🤖 Dealer's hand: {self.dealer_hand} = {self.dealer_hand_result}\n")

        if self.player_hand_result < 21:
            if self.player_choice not in (1, 2):
                try:
                    self.player_choice = int(input("1 - stay, 2 - hit: "))
                except Exception:
                    self.player_choice = 1  # fallback to stay


    def calculate_hand_value(self, hand: List[str]) -> int:
        """Calculate total score of a hand, taking into account flexible Ace."""
        value = 0
        aces = 0

        card_values = {
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'K': 10, 'Q': 10, 'J': 10, 'A': 11
        }

        for card in hand:
            if card == 'A':
                aces += 1
            value += card_values.get(card, 0)

        # downgrade Aces from 11 to 1 if hand is over 21
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    # --- basic actions (hit/stay) ---
    def stay_user_command(self) -> Optional[int]:
        """If player chooses to stay (1), show stayed message."""
        if self.player_choice == 1:
            self.player_hand_result = self.calculate_hand_value(self.player_hand)
            msg = self.messages["User"]["stay"].format(self.player_hand)
            print(msg)
            return self.player_hand_result
        return None

    def stay_dealer_command(self) -> int:
        """Dealer stays: show hand and return value."""
        self.dealer_choice = 1
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)
        msg = self.messages["Dealer"]["stay"].format(self.dealer_hand_result)
        print(f"{msg} ({self.dealer_hand})")
        return self.dealer_hand_result

    def hit_user_command(self) -> int:
        """User hit: add 1 card and return new score."""
        if not self.deck:
            raise ValueError("No more cards available in deck!")
    
        card = self.deck.pop()
        self.player_hand.append(card)
        self.player_hand_result = self.calculate_hand_value(self.player_hand)
        self.player_choice = 2
        print(f"Player hits and gets: {card}")
        return self.player_hand_result
    
    def hit_dealer_command(self) -> int:
        """User hit: add 1 card and return new score."""
        if not self.deck:
            raise ValueError("No more cards available in deck!")
    
        card = self.deck.pop()
        self.dealer_hand.append(card)
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)
        self.dealer_choice = 2
        print(f"Dealer hits and gets: {card}")
        return self.dealer_hand_result



    # --- game flow helpers ---
    def player_turn(self):
        """Handles the player turn until stay/bust/blackjack."""
        while True:
            self.player_hand_result = self.calculate_hand_value(self.player_hand)
            self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)

            print(f"🎮 Player's hand: {self.player_hand} = {self.player_hand_result}\n")
            print(f"🤖 Dealer's hand: {self.dealer_hand} = {self.dealer_hand_result}\n")

            if self.player_hand_result == 21 and len(self.player_hand) == 2:
                print("🎮 Player has Natural Blackjack!")
                return
            if self.player_hand_result > 21:
                print("🎮 Player busts!")
                return

            if self.player_choice not in (1, 2):
                try:
                    self.player_choice = int(input("1 - stay, 2 - hit: "))
                except Exception:
                    self.player_choice = 1

            if self.player_choice == 2:
                self.hit_user_command()
                self.player_choice = 0 
            if self.player_hand_result >= 21:
                return
            else:
                self.stay_user_command()
                return


    def dealer_turn(self):
        """Dealer plays automatically: hits while <17, stands on >=17."""
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)

        while self.dealer_hand_result < 17:
            print("Dealer thinking... ")
            sleep(1)
            self.hit_dealer_command()

        if self.dealer_hand_result > 21:
            print(self.messages["Dealer"]["bust"])
        elif 17 <= self.dealer_hand_result <= 21:
            sleep(1)
            print("Dealer thinking..")
            self.stay_dealer_command()

    def card_comparison(self) -> str:
        """
        Backwards-compatible method for tests:
    - computes current scores
    - checks for natural blackjack
    - makes dealer play (hits while <17, stands on >=17)
    - prints intermediate messages (Dealer stayed, Dealer busts, etc.)
    - prints final result and returns result string
    """
        self.player_hand_result = self.calculate_hand_value(self.player_hand)
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)

        if self.player_hand_result == 21 and len(self.player_hand) == 2 and not (self.dealer_hand_result == 21 and len(self.dealer_hand) == 2):
            print(self.messages["User"]["blackjack"])
            return self.messages["User"]["blackjack"]

        if self.dealer_hand_result == 21 and len(self.dealer_hand) == 2 and not (self.player_hand_result == 21 and len(self.player_hand) == 2):
            print(self.messages["Dealer"]["blackjack"])
            return self.messages["Dealer"]["blackjack"]

        while self.dealer_hand_result < 17:
            self.hit_dealer_command()
        if self.dealer_hand_result > 21:
            print(self.messages["Dealer"]["bust"])
        if 17 <= self.dealer_hand_result <= 21:
            self.stay_dealer_command()

        result = self.determine_winner()
        print(result)
        return result

    def determine_winner(self) -> str:
        """Return result string (also prints)."""
        self.player_hand_result = self.calculate_hand_value(self.player_hand)
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)

        print("\nFinal Results:")
        print(f"Player hand: {self.player_hand} = {self.player_hand_result}")
        print(f"Dealer hand: {self.dealer_hand} = {self.dealer_hand_result}")

        # natural blackjack
        if self.player_hand_result == 21 and len(self.player_hand) == 2 and not (self.dealer_hand_result == 21 and len(self.dealer_hand) == 2):
            return self.messages["User"]["blackjack"]

        if self.dealer_hand_result == 21 and len(self.dealer_hand) == 2 and not (self.player_hand_result == 21 and len(self.player_hand) == 2):
            return self.messages["Dealer"]["blackjack"]

        if self.player_hand_result > 21:
            return self.messages["User"]["bust"]

        if self.dealer_hand_result > 21:
            return self.messages["Dealer"]["bust"]

        if self.player_hand_result == self.dealer_hand_result:
            return "Push! It's a tie!"

        elif self.player_hand_result > self.dealer_hand_result:
            return self.messages["User"]["win"]

        else:
            return self.messages["Dealer"]["win"]
    
    def play_round(self) -> str:
        """High-level round flow:
        1) deal initial cards
        2) player turn (interactive or pre-set choice via player_choice)
        3) dealer turn (auto)
        4) determine winner and return result string
        """
        if not self.player_hand and not self.dealer_hand:
            self.deal_initial_cards()

        # quick check for initial naturals
        self.player_hand_result = self.calculate_hand_value(self.player_hand)
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)
        # Player turn
        self.player_turn()
        if self.player_hand_result > 21:
            print(self.messages["User"]["bust"])
            return self.messages["User"]["bust"]

        # Dealer turn
        self.dealer_turn()
        """Dealer plays automatically: hits while <17, stands on >=17."""
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)

        while self.dealer_hand_result < 17:
            print("Dealer thinking... ")
            sleep(2)
            self.hit_dealer_command() 

        if self.dealer_hand_result > 21:
            print(self.messages["Dealer"]["bust"])
            return self.messages["Dealer"]["bust"]

        if 17 <= self.dealer_hand_result <= 21:
            sleep(2)
            print("Dealer thinking..")
            self.stay_dealer_command()

        # Final comparison
        return self.determine_winner()
