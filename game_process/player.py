import random
from typing import List
from loguru import logger

logger.remove(0)
logger.add(
    "disc_bot.log",
    level="DEBUG",
    format="{time:DD/MM/YYYY HH:mm} | <level>{level: <8}</level> | {message}",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)


class PlayerHand:
    def __init__(self) -> None:
        # Initialize full shuffled deck and empty hands for both player and dealer
        self.deck = self.generate_full_deck()
        random.shuffle(self.deck)

        self.player_hand: List[str] = []
        self.dealer_hand: List[str] = []

        self.player_choice = 0
        self.dealer_choice = 0

    def generate_full_deck(self) -> List[str]:
        """Generate standard 52-card deck, without suits"""
        base_cards = [str(i) for i in range(2, 11)] + ["K", "Q", "A", "J"]
        logger.debug("Deck generated succefully")
        return base_cards * 4  # 4 of each card, like in standard deck

    def deal_initial_cards(self):
        """Deal two cards each to player and dealer from the top of the deck."""
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.card_comparison()

    def show_hands(self):
        """Display both hands and let user choose action if score < 21."""
        print(
            f"Player's hand: {self.player_hand} = {self.calculate_hand_value(self.player_hand)}"
        )
        print(
            f"Dealer's hand: {self.dealer_hand} = {self.calculate_hand_value(self.dealer_hand)}"
        )

        if self.calculate_hand_value(self.player_hand) < 21:
            self.player_choice = int(input("1 - stay, 2 - hit: "))

    def calculate_hand_value(self, hand: List[str]) -> int:
        """Calculate total score of a hand, taking into account flexible Ace."""
        value = 0
        aces = 0

        card_values = {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "K": 10,
            "Q": 10,
            "J": 10,
            "A": 11,
        }

        for card in hand:
            if card == "A":
                aces += 1
            value += card_values.get(card, 0)

        # downgrade Aces from 11 to 1 if hand is over 21
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def stay_user_command(self):
        """If player chooses to stay (1), show hand and return value."""
        if self.player_choice == 1:
            print(f"Player stayed, current score: {self.player_hand}")
            self.player_hand_result = self.calculate_hand_value(self.player_hand)
            return self.player_hand_result
        return None  # if else - return None for other case

    def stay_dealer_command(self):
        """Dealer stays: show hand and return value."""
        print(f"Dealer stayed, current score: {self.dealer_hand}")
        self.dealer_choice = 1
        return self.dealer_hand_result

    def hit_user_command(self):
        """User hit: add 1 card and show it"""
        self.player_hand.append(self.deck.pop())
        self.player_hand_result = self.calculate_hand_value(self.player_hand)
        self.player_choice = 2
        return self.player_hand_result

    def hit_dealer_command(self):
        """Dealer hits: take one card, recalc and return new score."""
        card = self.deck.pop()
        self.dealer_choice = 2
        self.dealer_hand.append(card)

        # Counting new score
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)
        return self.dealer_hand_result

    def card_comparison(self):
        self.player_hand_result = self.calculate_hand_value(self.player_hand)
        self.dealer_hand_result = self.calculate_hand_value(self.dealer_hand)

        # Natural Blackjack / bust
        if self.player_hand_result == 21 and len(self.player_hand) == 2:
            print("Player wins with Natural BlackJack!")

        elif self.dealer_hand_result == 21 and len(self.dealer_hand) == 2:
            print("Dealer wins with Natural BlackJack!")

        # Dealer auto-stay
        if 17 <= self.dealer_hand_result < 21:
            self.stay_dealer_command()

        # Dealer hit
        if self.dealer_hand_result < 17:
            self.hit_dealer_command()

        # Determine winner based on final scores
        if self.player_hand_result > 21:
            print("Player busts! Dealer wins!")
        elif self.dealer_hand_result > 21:
            print("Dealer busts! Player wins!")
        elif self.player_hand_result == self.dealer_hand_result:
            print("Push! It's a tie!")

        elif self.player_hand_result > self.dealer_hand_result:
            print("Player wins with higher score!")
        else:
            print("Dealer wins with higher score!")

        # Compare final scores
        print("\nFinal Results:")
        print(f"Player hand: {self.player_hand} = {self.player_hand_result}")
        print(f"Dealer hand: {self.dealer_hand} = {self.dealer_hand_result}")
