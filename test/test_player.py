import pytest
from unittest.mock import patch
from game_process.player import PlayerHand

@pytest.fixture
def hand():
    return PlayerHand()

def test_initial_deal_not_enough_cards():
    hand = PlayerHand()
    hand.deck = ["A"]
    with pytest.raises(ValueError):
        hand.deal_initial_cards()


def test_full_game_flow(hand):
    """Basic full game flow to cover all lines"""

    # Force known deck for deterministic behavior
    hand.deck = ['A', 'K', '9', '5', '8', 'Q', 'J', '2', '3', '4', '6', '7', '10'] * 4

    # Case 1: Player natural blackjack
    hand.player_hand = ['A', 'K']
    hand.dealer_hand = ['Q', '9']
    hand.player_hand_result = hand.calculate_hand_value(hand.player_hand)
    hand.dealer_hand_result = hand.calculate_hand_value(hand.dealer_hand)
    assert hand.play_round() == "Player wins with Natural BlackJack!"

    # Case 2: Player busts
    hand.player_hand = ['K', '9']
    hand.dealer_hand = ['5', '6']
    hand.deck = ['9']  # Will cause player to hit and bust
    hand.player_choice = 2  # hit
    assert hand.play_round() == "Player busts!"

    # Case 3: Dealer busts
    hand.player_hand = ['K', '9']
    hand.dealer_hand = ['10', '6']
    hand.deck = ['7']  # Dealer will hit and bust
    hand.player_choice = 1  # stay
    assert hand.play_round() == "Dealer busts!"

    # Case 4: Push / tie
    hand.player_hand = ['K', '9']
    hand.dealer_hand = ['Q', '9']
    hand.player_choice = 1  # stay
    assert hand.play_round() == "Push! It's a tie!"

    # Case 5: Player wins by higher score
    hand.player_hand = ['K', '9']  # Total: 19
    hand.dealer_hand = ['Q', '8']  # Total: 18
    hand.deck = ['A', '2', '3']
    hand.player_choice = 1  # stay
    assert hand.play_round() == "Player wins with higher score!"

    # Case 6: Dealer wins by higher score
    hand.player_hand = ['Q', '8']
    hand.dealer_hand = ['K', '9']
    hand.deck = []  # no hits
    hand.player_choice = 1  # stay
    assert hand.play_round() == "Dealer wins with higher score!"


@pytest.mark.parametrize("player,dealer,expected", [
    (['K', '9'], ['Q', '9'], "Push! It's a tie!"),
    (['A', 'K'], ['Q', '9'], "Player wins with Natural BlackJack!"),
    (['Q', '9'], ['A', 'K'], "Dealer wins with Natural BlackJack!"),
    (['K', '9'], ['Q', '8'], "Player wins with higher score!"),
    (['Q', '8'], ['K', '9'], "Dealer wins with higher score!"),
    (['K', '9', '9'], ['Q', '9'], "Player busts!"),
    (['Q', '9'], ['K', '9', '9'], "Dealer busts!"),
])
@patch("builtins.print")
def test_card_comparison(mock_print, hand, player, dealer, expected):
    """Test all possible game outcomes in card comparison"""
    hand.player_hand = player
    hand.dealer_hand = dealer
    result = hand.card_comparison()

    # Verify both the print message and return value
    mock_print.assert_any_call(expected)
    assert result == expected


def test_empty_deck_handling():
    """Test behavior when deck runs out of cards."""
    hand = PlayerHand()
    hand.deck = []  # Empty deck
    with pytest.raises(ValueError):
        hand.hit_user_command()

def test_stay_user_command():
    """Test stay functionality."""
    hand = PlayerHand()
    hand.player_hand = ['K', '9']
    hand.player_hand_result = 19
    hand.player_choice = 1
    result = hand.stay_user_command()
    assert result == 19

def test_dealer_turn_with_stay():
    """Test dealer turn staying on 17+."""
    hand = PlayerHand()
    hand.dealer_hand = ['K', '7']
    hand.deck = []  # Empty deck to prevent hitting
    hand.dealer_turn()
    assert hand.dealer_choice == 1


@patch("builtins.print")
@patch("builtins.input", return_value="1")
def test_show_hands_with_input(mock_input, mock_print):
    hand = PlayerHand()
    hand.player_hand = ["K", "9"]
    hand.dealer_hand = ["Q", "8"]
    hand.show_hands()
    assert hand.player_choice == 1

@patch("builtins.print")
@patch("builtins.input", side_effect=Exception("fail"))
def test_show_hands_input_exception(mock_input, mock_print):
    hand = PlayerHand()
    hand.player_hand = ["K", "9"]
    hand.dealer_hand = ["Q", "8"]
    hand.show_hands()
    assert hand.player_choice == 1  # fallback

def test_stay_user_command_none():
    hand = PlayerHand()
    hand.player_choice = 0
    assert hand.stay_user_command() is None

@patch("builtins.print")
def test_stay_dealer_command(mock_print):
    hand = PlayerHand()
    hand.dealer_hand = ["K", "9"]
    val = hand.stay_dealer_command()
    assert val == 19


def test_hit_dealer_no_cards():
    hand = PlayerHand()
    hand.deck = []
    with pytest.raises(ValueError):
        hand.hit_dealer_command()

@patch("builtins.print")
def test_player_turn_natural_blackjack(mock_print):
    hand = PlayerHand()
    hand.player_hand = ["A", "K"]
    hand.dealer_hand = ["Q", "9"]
    hand.player_turn()
    mock_print.assert_any_call("🎮 Player has Natural Blackjack!")

@patch("builtins.print")
def test_player_turn_bust(mock_print):
    hand = PlayerHand()
    hand.player_hand = ["K", "9", "5"]  # 24
    hand.dealer_hand = ["Q", "9"]
    hand.player_turn()
    mock_print.assert_any_call("🎮 Player busts!")


@patch("builtins.print")
def test_card_comparison_dealer_bust(mock_print):
    hand = PlayerHand()
    hand.player_hand = ["K", "9"]  # 19
    hand.dealer_hand = ["K", "6"]  # 16
    hand.deck = ["K"]  # будет 26
    result = hand.card_comparison()
    assert result == "Dealer busts!"


def test_determine_winner_dealer_bust():
    hand = PlayerHand()
    hand.player_hand = ["K", "9"]
    hand.dealer_hand = ["K", "6", "K"]
    assert hand.determine_winner() == "Dealer busts!"


@patch("builtins.input", return_value="1")
def test_play_round_autodeal(mock_input):
    hand = PlayerHand()
    hand.deck = ["A", "K", "Q", "J"] * 4
    result = hand.play_round()
    assert isinstance(result, str)

