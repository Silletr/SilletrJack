import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game_process.player import PlayerHand


g = PlayerHand()
g.play_round()
