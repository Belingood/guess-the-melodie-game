from typing import Union

import informer
import settings


class PlayerPool:
    """
    TODO
    """

    __slots__ = [
        'current_pool',
        'excluded_players'
    ]

    def __init__(self):

        self.current_pool = {}
        self.excluded_players = []

    def player_name_request(self) -> Union[str, tuple]:
        """
        TODO
        """

        player_number = 1 if not self.current_pool else max(self.current_pool) + 1

        while True:

            player_name = input(f"THE PLAYER {player_number} NAME [or 'stop']: ")

            spl_text = informer.format_key_text(player_name)

            if spl_text in (settings.STOP_WORD, settings.QUIT_WORD):
                return spl_text

            if not self.name_checking(player_name):
                print(settings.use_letters_text + '\n')
                continue

            return player_number, player_name

    def new_player_registration(
            self,
            player_number: int,
            player_name: str
    ) -> None:
        """
        TODO
        """
        self.current_pool.update({player_number: {'name': player_name, 'score': 0}})

    @staticmethod
    def name_checking(name: str) -> bool:
        """
        TODO
        """

        def alch(ch):
            return any((ch.isalpha(), ch in ' -'))

        correct_ln = len(name) > 0
        alowed_chars = all(map(alch, name))
        at_least_one_letter = len(list(filter(lambda x: x.isalpha(), name))) > 0

        return all((correct_ln, alowed_chars, at_least_one_letter))

    def get_positive_scores(self):
        """
        TODO
        """
        positive_scores = []

        for i, player in self.current_pool.items():
            if player['score'] > 0:
                positive_scores.append((i, *player.values()))
        return positive_scores

    def get_winner(self) -> Union[None, str]:
        """
        TODO
        """
        for i, player in self.current_pool.items():
            name, scores = player.values()
            if scores == settings.WIN_POINT:
                return name

    def clear_players_scores(self) -> None:
        for player_num in self.current_pool:
            self.current_pool[player_num]['score'] = 0
