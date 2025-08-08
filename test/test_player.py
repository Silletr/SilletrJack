import pytest
from game_process.player import PlayerHand

def test_generate_full_deck():
    u = PlayerHand()
    assert len(u.deck) == 52 
    assert u.deck.count('A') == 4
    assert u.deck.count('10') == 4

def test_deal_initial_cards():
    u = PlayerHand()
    u.deal_initial_cards()
    assert len(u.player_hand) == 2
    assert len(u.dealer_hand) == 2
    assert len(u.deck) == 48

def test_calculate_hand_value_simple():
    u = PlayerHand()
    assert u.calculate_hand_value(['2', '3']) == 5
    assert u.calculate_hand_value(['K', 'Q']) == 20
    assert u.calculate_hand_value(['A', '9']) == 20
    assert u.calculate_hand_value(['A', 'A', '9']) == 21
    assert u.calculate_hand_value(['A', 'A', '9', 'K']) == 21
    assert u.calculate_hand_value(['A', 'A', '9', 'K', '5']) == 26  # bust

def test_show_hands_input_stay(monkeypatch, capsys):
    u = PlayerHand()
    u.player_hand = ['2', '3']
    u.dealer_hand = ['4', '5']

    monkeypatch.setattr('builtins.input', lambda _: "1")
    u.show_hands()

    captured = capsys.readouterr()
    assert "Player's hand: ['2', '3'] = 5" in captured.out
    assert u.user_choice == 1

def test_show_hands_input_hit(monkeypatch, capsys):
    u = PlayerHand()
    u.player_hand = ['2', '3']
    u.dealer_hand = ['4', '5']

    monkeypatch.setattr('builtins.input', lambda _: "1")
    u.show_hands()

    assert u.user_choice == 1

def test_stay_user_command():
    u = PlayerHand()
    u.user_choice = 1
    u.player_hand = ['10', 'J']
    u.user_hand_result = u.calculate_hand_value(u.player_hand)

    result = u.stay_user_command()
    assert result == 20

def test_stay_dealer_command():
    u = PlayerHand()
    u.dealer_choice = 1
    u.dealer_hand = ['5', '10']
    u.dealer_hand_result = u.calculate_hand_value(u.dealer_hand)

    result = u.stay_dealer_command()
    assert result == 15

def test_hit_dealer_command():
    u = PlayerHand()
    u.dealer_choice = 2
    u.dealer_hand = ['1', '3']
    u.deck = ['4']
    result = u.hit_dealer_command()
    assert result == 8 

@pytest.mark.parametrize("ph, dh, expected_output", [
    (['A', 'K'], ['10', '9', '3'], "User wins with Natural BlackJack!"),
    (['10', '9'], ['A', 'K'], "Dealer wins with Natural BlackJack!"),
])
def test_card_comparison_win_cases(ph, dh, expected_output, capsys):
    u = PlayerHand()
    u.player_hand = ph
    u.dealer_hand = dh
    u.card_comparison()

    output = capsys.readouterr().out
    assert expected_output in output

def test_card_comparison_dealer_stay(capsys):
    u = PlayerHand()
    u.player_hand = ['10', '5']
    u.dealer_hand = ['10', '7']

    u.card_comparison()

    output = capsys.readouterr().out
    assert "Dealer stayed" in output
