from game_process import player

def test_userhands_creation():
    u = player.UserHands()
    assert isinstance(u, player.UserHands)
    u.deal_initial_cards()  # <- deal cards
    u.show_hands()          # <- print cards
