import time
from typing import Union

import informer
import music_player
import player_pool
import tools


class GTMGame:

    def __init__(self):

        self.info = informer.Informer()
        self.pl_pool = player_pool.PlayerPool()
        self.mus_player = music_player.MidiPlayer()
        self.round_number = 0
        self.player_data = ()

    def execute(self):

        self.info.greeting()
        self.info.player_registration_intro()

        while True:

            # Game starting/restarting.
            match self.new_round_initiator():
                case 'quit': return self.info.game_over_message()

            while True:

                match self.new_melodie_starting():
                    case 'round': break

                match self.new_try_to_guess():
                    case 'quit': return self.info.game_over_message()
                    case 'next': continue

    def new_round_initiator(self):
        """
        TODO
        """
        self.round_number += 1

        if self.round_number != 1:

            need_new_pool = tools.format_key_text(
                input(f'{tools.need_new_pool_text}: ')
            )

            if need_new_pool == tools.NEW_POOL_TEXT:

                self.player_data = ()
                self.pl_pool.current_pool.clear()

            else:

                if need_new_pool in tools.QUIT_WORDS:
                    return 'quit'

                self.pl_pool.clear_players_scores()

        while isinstance(self.player_data, tuple):

            self.player_data = self.pl_pool.player_name_request()

            if not isinstance(self.player_data, str):
                self.pl_pool.new_player_registration(*self.player_data)
                self.info.player_greeting(*self.player_data)

        if self.player_data in tools.QUIT_WORDS:
            return 'quit'

        self.info.end_registration_message(
            player_count=len(self.pl_pool.current_pool)
        )

        time.sleep(tools.ATTENTION_TIME)

        if self.round_number == 1:
            self.info.show_rules()

        self.mus_player.new_round_tracks_setter()

        is_game_starting = self.info.tap_to_game_starting()

        if is_game_starting in tools.QUIT_WORDS:
            return 'quit'

    def new_melodie_starting(self):
        """
        TODO
        """

        self.clear_exclusion_data()

        winner = self.pl_pool.get_winner()

        if winner:
            self.info.win_message(winner)
            self.info.round_over_message()
            return 'round'

        self.info.show_positive_scores(
            positive_scores=self.pl_pool.get_positive_scores()
        )

        self.mus_player.set_random_singer_track()
        self.mus_player.set_guessble_tracks_list()

        self.info.show_guessable_track_titles(
            self.mus_player.get_guessable_track_titles()
        )

        self.mus_player.preseted_track_loading()

    def new_try_to_guess(self):
        """
        TODO
        """

        while True:
            # New try to guess.

            self.info.show_excluded_tracks_players(
                self.mus_player.excluded_tracks,
                self.pl_pool.excluded_players
            )

            stop_track_text = self.mus_player.track_playback(
                self.input_deliver
            )

            if stop_track_text in tools.QUIT_WORDS:
                return 'quit'

            if stop_track_text == 'next':
                self.mus_player.track_stop_unload()
                return 'next'

            player_track_number = self.get_check_inputting()

            if player_track_number in tools.QUIT_WORDS:
                return 'quit'

            if player_track_number == tools.NEXT_MELODY_TEXT:
                return 'next'

            if isinstance(player_track_number, tuple):

                is_guessed, player_num, track_num = player_track_number

                self.info.guess_result_message(
                    player_name=self.pl_pool.current_pool[player_num]['name'],
                    is_guessed=is_guessed
                )

                time.sleep(tools.ATTENTION_TIME)

                if is_guessed:
                    self.pl_pool.current_pool[player_num]['score'] += 1
                    return 'next'

                else:
                    ex_track_tpl = self.mus_player.guessable_tracks_list[track_num - 1]
                    ex_player_name = self.pl_pool.current_pool[player_num]['name']

                    self.mus_player.excluded_tracks.append(
                        (
                            track_num,
                            self.mus_player.file_name_to_title(ex_track_tpl)
                        )
                    )

                    self.pl_pool.excluded_players.append((player_num, ex_player_name))

                    if len(self.pl_pool.excluded_players) == len(self.pl_pool.current_pool):
                        print(tools.no_one_guessed_text + '\n')
                        return 'next'

    @staticmethod
    def input_deliver() -> str:
        """
        TODO
        """
        return tools.format_key_text(
            input('\n' + tools.stop_melodie_text)
        )

    def clear_exclusion_data(self) -> None:
        """
        TODO
        """
        self.mus_player.excluded_tracks.clear()
        self.pl_pool.excluded_players.clear()

    def get_check_inputting(self) -> Union[tuple, str]:
        """
        The function polls the player for his number and
        the song number which has been playing.
        """

        # Array for allowed answers and variable for inputting string in each loop.
        answers = []

        for i, text in enumerate(tools.player_track_number_text):
            # Two loops for player\'s name and melodie\'s name.

            while True:
                # Until will get an allowed inputted text.

                # Format the inputted text.
                spl_answer = tools.format_key_text(input(text))

                # If the text is equal to commands below.
                if spl_answer in (
                        tools.NEXT_MELODY_TEXT,
                        tools.CONTINUE_GAME_TEXT,
                        *tools.QUIT_WORDS
                ):
                    # Then return this command.
                    return spl_answer

                try:
                    # In other cases, try to cast the inputted text type to integer.
                    spl_answer = int(spl_answer)

                except (ValueError, Exception):
                    # If casting to integer is not possible then display the message
                    # and let input it again.
                    print(tools.input_numbers_only_text)
                    continue

                not_correct_number = self.is_number_not_correct(i, spl_answer)

                if not_correct_number:
                    # If the function returs a not empty string then it means
                    # it has gotten a wrong player's or melodie's number,
                    # so let try input it again.
                    print(not_correct_number)
                    continue

                # If an inputted number is allowed then go to the next loop.
                break

            # If data was cast successful and the number is correct
            # then add it to the corresponding array.
            answers.append(spl_answer)

        # Get a current playing melodie index.
        current_track_index = self.mus_player.guessable_tracks_list.index(
            self.mus_player.current_singer_track_tuple
        )

        # If all two numbers were gotten successful then return a tuple in wich
        # the first element is a boolean value if inputted melodie number and
        # playing melodie number are equal. And the next values are the melodie
        # number and the gamer number.
        return answers[1] == (current_track_index + 1), *answers

    def is_number_not_correct(self, i: int, answer: int) -> str:
        """
        The function checks whether the numbers entered by
        the user exceed the acceptable parameters.
        # i == 0: If expected a gamer number.
        # key1: If the number is an excluded gamer number.
        # key2: If the gamer number is greater than a total gamers number.
        # i == 1: If expected a melodie number.
        # key1: If the number is an excluded melodie number.
        # key2: If the melodie number is greater than a total melodies number.
        """

        def get_nums(array):
            return range(1, len(array) + 1)

        def get_tpl_nums(tpl_array):
            return list(map(lambda x: x[0], tpl_array))

        cases = {
            0: {
                answer in get_tpl_nums(self.pl_pool.excluded_players): tools.player_already_answered_text,
                answer not in get_nums(self.pl_pool.current_pool): tools.wrong_player_number_text
            },
            1: {
                answer in get_tpl_nums(self.mus_player.excluded_tracks): tools.melodie_already_named_text,
                answer not in get_nums(self.mus_player.guessable_tracks_list): tools.wrong_melodie_number_text
            }
        }[i]

        if True in cases:
            return cases[True] + f' or input "{tools.CONTINUE_GAME_TEXT}" to continue the melody.'


if __name__ == '__main__':
    game = GTMGame()
    game.execute()
