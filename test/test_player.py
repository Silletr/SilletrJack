import unittest
from unittest.mock import patch, MagicMock
from typing import List
from game_process.player import PlayerHand

class TestPlayerHand(unittest.TestCase):
    def setUp(self):
        self.hand = PlayerHand()
        
    def test_generate_full_deck(self):
        # Verify deck size and composition
        deck = self.hand.generate_full_deck()
        self.assertEqual(len(deck), 52)
        expected_cards = [str(i) for i in range(2, 11)] + ['K', 'Q', 'A', 'J']
        for card in expected_cards:
            self.assertEqual(deck.count(card), 4)

    @patch('random.shuffle')
    def test_init_shuffles_deck(self, mock_shuffle):
        # Verify deck is shuffled during initialization
        PlayerHand()
        mock_shuffle.assert_called_once()

    def test_deal_initial_cards(self):
        # Test initial card dealing
        self.hand.deal_initial_cards()
        self.assertEqual(len(self.hand.player_hand), 2)
        self.assertEqual(len(self.hand.dealer_hand), 2)
        self.assertEqual(len(self.hand.deck), 48)

    def test_calculate_hand_value_basic(self):
        # Test basic card calculations
        self.hand.player_hand = ['K', '9']
        self.assertEqual(self.hand.calculate_hand_value(['K', '9']), 19)
        self.hand.player_hand = ['A', '8']
        self.assertEqual(self.hand.calculate_hand_value(['A', '8']), 19)

    def test_calculate_hand_value_aces(self):
        # Test Ace value adjustments
        self.hand.player_hand = ['A', 'A']
        self.assertEqual(self.hand.calculate_hand_value(['A', 'A']), 12)

    @patch('builtins.print')
    @patch('builtins.input', return_value='1')
    def test_show_hands_stay(self, mock_input, mock_print):
        # Test stay scenario
        self.hand.player_hand = ['K', '9']
        self.hand.dealer_hand = ['Q', '5']
        self.hand.show_hands()
        mock_input.assert_called_once_with("1 - stay, 2 - hit: ")
        self.assertEqual(self.hand.player_choice, 1)

    @patch('builtins.print')
    @patch('builtins.input', return_value='2')
    def test_show_hands_hit(self, mock_input, mock_print):
        # Test hit scenario
        self.hand.player_hand = ['K', '9']
        self.hand.dealer_hand = ['Q', '5']
        self.hand.show_hands()
        mock_input.assert_called_once_with("1 - stay, 2 - hit: ")
        self.assertEqual(self.hand.player_choice, 2)

    def test_stay_user_command(self):
        # Test stay command behavior
        self.hand.player_hand = ['K', '9']
        result = self.hand.stay_user_command()
        self.assertEqual(result, None)  # Since player_choice is 0 initially

    def test_hit_user_command(self):
        # Test hit command behavior
        self.hand.deck = ['A']  # Add an ace to deck
        self.hand.player_hand = ['K', '9']  # Initial score 19
        result = self.hand.hit_user_command()
        self.assertEqual(len(self.hand.player_hand), 3)  # Verify card was added
        self.assertEqual(result, 20)  # Corrected assertion - should be 20 (K=10, 9=9, A=1)
        self.assertEqual(self.hand.player_choice, 2)  # Verify hit choice was recorded

    def test_card_comparison_natural_blackjack(self):
        # Test natural blackjack scenarios
        self.hand.player_hand = ['A', 'K']  # Player natural blackjack
        self.hand.dealer_hand = ['Q', '9']
        self.hand.card_comparison()

    def test_card_comparison_dealer_stay(self):
        # Test dealer stay scenario (score >= 17)
        self.hand.player_hand = ['K', '7']  # Score 17
        self.hand.dealer_hand = ['Q', '9']  # Score 19
        self.hand.card_comparison()
