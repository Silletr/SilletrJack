import unittest
from unittest.mock import patch
from game_process.player import PlayerHand


class TestPlayerHand(unittest.TestCase):
    def setUp(self):
        self.hand = PlayerHand()

    def test_generate_full_deck(self):
        deck = self.hand.generate_full_deck()
        self.assertEqual(len(deck), 52)
        expected_cards = [str(i) for i in range(2, 11)] + ['K', 'Q', 'A', 'J']
        for card in expected_cards:
            self.assertEqual(deck.count(card), 4)

    @patch('random.shuffle')
    def test_init_shuffles_deck(self, mock_shuffle):
        PlayerHand()
        mock_shuffle.assert_called_once()

    def test_deal_initial_cards(self):
        self.hand.deal_initial_cards()
        self.assertEqual(len(self.hand.player_hand), 2)
        self.assertEqual(len(self.hand.dealer_hand), 2)
        self.assertEqual(len(self.hand.deck), 48)

    def test_calculate_hand_value_basic(self):
        self.assertEqual(self.hand.calculate_hand_value(['K', '9']), 19)
        self.assertEqual(self.hand.calculate_hand_value(['A', '8']), 19)

    def test_calculate_hand_value_aces(self):
        self.assertEqual(self.hand.calculate_hand_value(['A', 'A']), 12)

    def test_calculate_hand_value_bust_with_ace(self):
        self.assertEqual(self.hand.calculate_hand_value(['A', '10', '9']), 20)

    @patch('builtins.print')
    @patch('builtins.input', return_value='1')
    def test_show_hands_stay(self, mock_input, mock_print):
        self.hand.player_hand = ['K', '9']
        self.hand.dealer_hand = ['Q', '5']
        self.hand.show_hands()
        self.assertEqual(self.hand.player_choice, 1)

    @patch('builtins.print')
    @patch('builtins.input', return_value='2')
    def test_show_hands_hit(self, mock_input, mock_print):
        self.hand.player_hand = ['K', '9']
        self.hand.dealer_hand = ['Q', '5']
        self.hand.show_hands()
        self.assertEqual(self.hand.player_choice, 2)

    def test_stay_user_command(self):
        self.hand.player_hand = ['K', '9']
        self.hand.player_choice = 1
        result = self.hand.stay_user_command()
        self.assertEqual(result, 19)

    def test_stay_user_command_player_hits(self):
        self.hand.player_hand = ['K', '9']
        self.hand.player_choice = 2
        result = self.hand.stay_user_command()
        self.assertIsNone(result)

    def test_stay_dealer_command(self):
        """Covers line 98: dealer stays."""
        self.hand.dealer_hand = ['K', '9']
        self.hand.dealer_hand_result = 19
        result = self.hand.stay_dealer_command()
        self.assertEqual(result, 19)

    def test_hit_user_command(self):
        self.hand.deck = ['A']
        self.hand.player_hand = ['K', '9']
        result = self.hand.hit_user_command()
        self.assertEqual(result, 20)
        self.assertEqual(len(self.hand.player_hand), 3)

    def test_hit_dealer_command(self):
        self.hand.deck = ['A']
        self.hand.dealer_hand = ['K', '9']
        result = self.hand.hit_dealer_command()
        self.assertEqual(result, 20)
        self.assertEqual(len(self.hand.dealer_hand), 3)

    def test_card_comparison_natural_blackjack(self):
        self.hand.player_hand = ['A', 'K']
        self.hand.dealer_hand = ['Q', '9']
        self.hand.card_comparison()

    def test_card_comparison_dealer_blackjack(self):
        """Covers line 125: dealer wins with Blackjack."""
        self.hand.player_hand = ['K', '9']
        self.hand.dealer_hand = ['A', 'K']
        self.hand.card_comparison()

    def test_card_comparison_dealer_stay(self):
        self.hand.player_hand = ['K', '7']
        self.hand.dealer_hand = ['Q', '9']
        self.hand.card_comparison()

    def test_card_comparison_dealer_hit(self):
        self.hand.deck = ['K']
        self.hand.player_hand = ['K', '7']
        self.hand.dealer_hand = ['Q', '6']
        self.hand.card_comparison()
        self.assertEqual(len(self.hand.dealer_hand), 3)

    def test_card_comparison_bust_scenarios(self):
        self.hand.player_hand = ['K', 'Q', '9']
        self.hand.dealer_hand = ['Q', '9']
        self.hand.card_comparison()
        self.hand.player_hand = ['K', '9']
        self.hand.dealer_hand = ['K', 'Q', '9']
        self.hand.card_comparison()

    def test_card_comparison_player_wins_higher_score(self):
        """Covers line 128: player wins with higher score."""
        self.hand.player_hand = ['K', '9']
        self.hand.dealer_hand = ['Q', '8']
        self.hand.card_comparison()


if __name__ == '__main__':
    unittest.main()

