import random
from typing import Dict, Any, List

class UserHands:
    def __init__(self) -> None:
        self.deck = self.generate_full_deck()
        random.shuffle(self.deck)

        self.player_hand: List[str] = []
        self.dealer_hand: List[str] = []
        self.choise = 0

    def generate_full_deck(self) -> List[str]:
        """ Generating standart deck, only numbers without ranks """
        base_cards = [str(i) for i in range(2, 11)] + ['K', 'Q', 'A']
        deck = base_cards * 4 # 4 cards as in defaul deck 
        return deck

    def deal_initial_cards(self):
        """Giving 2 cards for dealer and player"""
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def show_hands(self):
        print(f"Player's hand: {self.player_hand} = {self.calculate_hand_value(self.player_hand)}")
        print(f"Dealer's hand: {self.dealer_hand} = {self.calculate_hand_value(self.dealer_hand)}")
        if self.calculate_hand_value(self.player_hand) < 21:
            self.choise = int(input("1 - stay, 2 - hit"))

    def calculate_hand_value(self, hand: List[str]) -> int:
        value = 0
        aces = 0

        card_values = {
           '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'K': 10, 'Q': 10, 'J': 10, 'A': 11
        }

        for card in hand:
            if card == 'A':
                aces += 1
            value += card_values.get(card, 0)

        # recount aces if bust
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value
    
    def stay_user_command(self):
        if self.choise == 1:
            print(f"Player stayed, current score: {self.player_hand}")
            return self.user_hand_result
    def stay_dealer_command(self):
        if self.choise == 1:
            print(f"Dealer stayed, current score: {self.dealer_hand}")
            return self.dealer_hand_result

    def card_comparison(self):
        self.user_hand_result = self.calculate_hand_value(self.player_hand)
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)
    
        if self.user_hand_result == 21 or self.dealer_hand_result > 21: 
            print(f"User win with Natural BlackJack!")

        if self.dealer_hand_result == 21:
            print(f"Dealer win with Natural BlackJack! User need a little bit bigger luck")

        if self.dealer_hand_result >= 17 and not self.dealer_hand_result != 21: 
            self.stay_dealer_command()
