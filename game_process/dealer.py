from game_process.player import PlayerHand  # Using scoring and deck 
class Dealer(PlayerHand):
    """
    Dealer - just PlayerHand() with decide() method,
    Dealer taking the cards while hes score <=17, else - staying. 
    """

    def __init__(self) -> None:
        super().__init__()

    def decide(self) -> int:
        """
        Return 1 (stay) or 2 (hit) depending on the current hand,
        Rule: hit, if <17; else - stay.
        """
        score = self.calculate_hand_value(self.dealer_hand)
        if score < 17:
            self.dealer_choice = 2 # hit
        else:
            self.dealer_choice = 1 # stay
        return self.dealer_choice

    def play(self) -> None:
        """
        Automatic giving cards to dealer while decide() == 2
        In the end - printing score.
        """
        while True:
            choice = self.decide()
            if choice == 2:
                # taking card
                card = self.deck.pop()
                self.dealer_hand.append(card)
            else:
                # staying
                print(f"Dealer stayed, final hand: {self.dealer_hand} = "
                      f"{self.calculate_hand_value(self.dealer_hand)}")
                break
