from game_process import player
import builtins
import pytest


def test_show_hands(monkeypatch):
    from game_process.player import UserHands
    g = UserHands()
    g.player_hand = ['10', 'A']
    g.dealer_hand = ['9', '7']
    g.user_hand_result = 21
    g.dealer_hand_result = 16

    monkeypatch.setattr('builtins.input', lambda _: '')
    g.show_hands()

