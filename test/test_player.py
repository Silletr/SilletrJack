import pytest
from unittest.mock import patch
from game_process.player import PlayerHand


@pytest.fixture
def hand():
    return PlayerHand()

  
def test_generate_full_deck(hand):
    """Test that deck generation creates 52 cards with correct distribution"""
    deck = hand.generate_full_deck()
    assert len(deck) == 52
    # Check each card appears exactly 4 times
    for card in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'K', 'Q', 'A', 'J']:
        assert deck.count(card) == 4

def test_calculate_hand_value(hand):
    """Test hand value calculation with various card combinations"""
    # Test basic card values
    assert hand.calculate_hand_value(['K', '9']) == 19
    assert hand.calculate_hand_value(['A', '9']) == 20
    assert hand.calculate_hand_value(['A', 'A']) == 12  # Should handle two aces correctly
    
    # Test bust scenarios with aces
    assert hand.calculate_hand_value(['A', '10', '9']) == 20  # Ace should be worth 1
    assert hand.calculate_hand_value(['A', 'A', '10']) == 12  # Two aces should be worth 1 each

@patch("builtins.print")
def test_stay_user_command(mock_print, hand):
    """Test player stay command functionality"""
    hand.player_hand = ['K', '9']
    hand.player_hand_result = 19
    hand.player_choice = 1
    
    result = hand.stay_user_command()
    assert result == 19
    mock_print.assert_called_once_with("Player stayed, current score: ['K', '9']")

@patch("builtins.print")
def test_stay_dealer_command(mock_print, hand):
    """Test dealer stay command functionality"""
    hand.dealer_hand = ['K', '9']
    hand.dealer_hand_result = 19
    
    result = hand.stay_dealer_command()
    assert result == 19
    assert hand.dealer_choice == 1
    mock_print.assert_called_once_with("Dealer stayed, current score: ['K', '9']")

def test_hit_user_command(hand):
    """Test player hit command functionality"""
    hand.deck = ['A']  # Mock deck with single card
    hand.player_hand = ['K', '9']
    
    result = hand.hit_user_command()
    assert result == 20
    assert hand.player_choice == 2
    assert len(hand.player_hand) == 3

def test_hit_dealer_command(hand):
    """Test dealer hit command functionality"""
    hand.deck = ['A']  # Mock deck with single card
    hand.dealer_hand = ['K', '9']
    
    result = hand.hit_dealer_command()
    assert result == 20
    assert hand.dealer_choice == 2
    assert len(hand.dealer_hand) == 3

@pytest.mark.parametrize("player,dealer,expected", [
    (['K', '9'], ['Q', '9'], "Push! It's a tie!"),  # Tie
    (['A', 'K'], ['Q', '9'], "Player wins with Natural BlackJack!"),  # Player natural blackjack
    (['Q', '9'], ['A', 'K'], "Dealer wins with Natural BlackJack!"),  # Dealer natural blackjack
    (['K', '9'], ['Q', '8'], "Player wins with higher score!"),  # Player wins by points
    (['Q', '8'], ['K', '9'], "Dealer wins with higher score!"),  # Dealer wins by points
    (['K', '9', '9'], ['Q', '9'], "Player busts! Dealer wins!"),  # Player busts
    (['Q', '9'], ['K', '9', '9'], "Dealer busts! Player wins!"),  # Dealer busts
])
@patch("builtins.print")
def test_card_comparison(mock_print, hand, player, dealer, expected):
    """Test all possible game outcomes in card comparison"""
    hand.player_hand = player
    hand.dealer_hand = dealer
    hand.card_comparison()
    mock_print.assert_any_call(expected)