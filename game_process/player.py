import random
from typing import Dict, Any, List

# TODO:
#    1. Create Win or Lose system for dealer


class PlayerHand:
    def __init__(self) -> None:
        # Initialize full shuffled deck and empty hands for both player and dealer
        self.deck = self.generate_full_deck()
        random.shuffle(self.deck)

        self.player_hand: List[str] = []
        self.dealer_hand: List[str] = []
        
        # choices: 1 - stay, 2 - hit (for both player and dealer if needed)
        self.user_choice = 0
        self.dealer_choice = 0

    def generate_full_deck(self) -> List[str]:
        """Generate standard 52-card deck, without suits (only ranks)."""
        base_cards = [str(i) for i in range(2, 11)] + ['K', 'Q', 'A', 'J']
        return base_cards * 4  # 4 of each card, like in standard deck

    def deal_initial_cards(self):
        """Deal two cards each to player and dealer from the top of the deck."""
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def show_hands(self):
        """Display both hands and let user choose action if score < 21."""
        print(f"Player's hand: {self.player_hand} = {self.calculate_hand_value(self.player_hand)}")
        print(f"Dealer's hand: {self.dealer_hand} = {self.calculate_hand_value(self.dealer_hand)}")

        if self.calculate_hand_value(self.player_hand) < 21:
            self.user_choice = int(input("1 - stay, 2 - hit: "))

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

    def stay_user_command(self):
        """If player chooses to stay (1), show hand and return value."""
        if self.user_choice == 1:
            print(f"Player stayed, current score: {self.player_hand}")
            return self.user_hand_result

    def stay_dealer_command(self):
        """Dealer stays: show hand and return value."""
        print(f"Dealer stayed, current score: {self.dealer_hand}")
        return self.dealer_hand_result
    
    def hit_user_command(self):
        """ User hit: add 1 card and show it """
        self.player_hand.append(self.deck.pop()) # Add new card to player hand
        self.user_hand_result = self.calculate_hand_value(self.player_hand)  # count new hand result
        return self.user_hand_result  # return new sum
    
        
    def hit_dealer_command(self):
        """Dealer hits: take one card, recalc and return new score."""
        card = self.deck.pop()
        self.dealer_hand.append(card)
        # Counting new score

        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)
        return self.dealer_hand_result



    def card_comparison(self):
        self.user_hand_result = self.calculate_hand_value(self.player_hand)
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)

        # Natural Blackjack / bust
        if self.user_hand_result == 21 or self.dealer_hand_result > 21:
            print("User wins with Natural BlackJack!")
            return
        if self.dealer_hand_result == 21:
            print("Dealer wins with Natural BlackJack!")
            return
        # Dealer auto-stay
        if 17 <= self.dealer_hand_result < 21:
            self.stay_dealer_command()
            return
