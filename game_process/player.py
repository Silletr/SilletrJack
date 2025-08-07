from typing import Dict, Any

class User_Hands:
    def __init__(self, deck: Dict[str, Any]) -> None:
        self.deck_nums = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9
        }
        self.main_deck = {
            "K": 10,
            "Q": 10,
            "A": 11
        }


    def get_deck(self, deck: Dict[str, Any]) -> None:
       pass 
