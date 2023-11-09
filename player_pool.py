from typing import Union

import informer
import settings


class PlayerPool:
    """
    Class for storing and operating player data.
    """

    __slots__ = [
        'current_pool',
        'excluded_players'
    ]

    def __init__(self):

        # The dictionary for player registration.
        self.current_pool = {}

        # The array of excluded players who gave the wrong answer.
        self.excluded_players = []

    def player_name_request(self) -> Union[str, tuple]:
        """
        The function requests the user for his name in the correct form.
        """

        # If the dictionary is empty, then the first player is assigned number one,
        # otherwise the number one greater than the maximum number in the dictionary
        # will be assigned.
        player_number = 1 if not self.current_pool else max(self.current_pool) + 1

        while True:
            # The loop runs until the correct player name
            # or one of the provided text commands is received.

            # The option to stop registration is only shown if the
            # minimum allowed number of players has been reached.
            stop_option = {
                False: '',
                True: ' [or “stop”]'
            }[player_number > settings.PLAYERS_MIN_COUNT]

            # Get the player name using the -input()- function.
            player_name = input(f'THE PLAYER {player_number} NAME{stop_option}: ')

            # Formatted inputting.
            spl_text = informer.format_key_text(player_name)

            if spl_text in (settings.ORDER_STOP, settings.ORDER_QUIT):
                # If the user inputted one of the provided commands,
                # then send it for appropriate processing.
                return spl_text

            if not self.name_checking(player_name):
                # If the user inputted invalid characters, inform
                # him of this and repeat the input request.
                print(settings.use_letters_text + '\n')
                continue

            # Return the user data as a tuple if the data is correct.
            return player_number, player_name

    def new_player_registration(
            self,
            player_number: int,
            player_name: str
    ) -> None:
        """
        The function writes the name of the new player
        to the corresponding dictionary.
        """
        self.current_pool.update({player_number: {'name': player_name, 'score': 0}})

    @staticmethod
    def name_checking(name: str) -> bool:
        """
        The function checks entering string for checks for minimum length,
        allowed characters, and presence of at least one letter.
        """

        def allowed_char(ch: str) -> bool:
            """
            Check whether the character you entered
            is a letter, a dash, or a space.
            """
            return any((ch.isalpha(), ch in ' -'))

        # The variables contain boolean values for checks for minimum length,
        # allowed characters, and presence of at least one letter.
        correct_ln = len(name) > 0
        alowed_chars = all(map(allowed_char, name))
        at_least_one_letter = len(list(filter(lambda x: x.isalpha(), name))) > 0

        # Return the result of checking as a boolean value.
        return all((correct_ln, alowed_chars, at_least_one_letter))

    def get_positive_scores(self) -> list:
        """
        In the player pool, the function searches for players
        with non-zero points, placing information about the
        number of points, the name and the number of the
        players in a list as a tuple.
        """
        positive_scores = []

        for i, player in self.current_pool.items():
            if player['score'] > 0:
                positive_scores.append((i, *player.values()))
        return positive_scores

    def get_winner(self) -> Union[None, str]:
        """
        The function checks whether there is a player in the
        player pool with the сщгте of points required to win.
        """
        for i, player in self.current_pool.items():
            name, scores = player.values()
            if scores == settings.WIN_POINT:
                return name

    def clear_players_scores(self) -> None:
        """
        Function for resetting the scores of all players.
        """
        for player_num in self.current_pool:
            self.current_pool[player_num]['score'] = 0
