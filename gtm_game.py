import time
from typing import Union

import informer
import music_player
import player_pool
import settings


class GTMGame:
    """
    TODO
    """

    __slots__ = [
        'info',
        'pl_pool',
        'mus_player',
        'round_number',
        'player_data'
    ]

    def __init__(self):

        # The informer class object.
        self.info = informer.Informer()

        # The PlayerPool class object.
        self.pl_pool = player_pool.PlayerPool()

        # The object of music player class.
        self.mus_player = music_player.MidiPlayer()

        # Game round counter.
        self.round_number = 0

        # Variable for saving data of a registration player.
        self.player_data = ()

    def execute(self):

        self.info.greeting()
        self.info.player_registration_intro()

        while True:

            match self.new_round_initiator():
                case settings.QUIT_WORD: return self.info.game_over_message()

            while True:

                match self.new_melody_starting():
                    case settings.NEW_ROUND_TEXT: break

                match self.new_try_to_guess():
                    case settings.QUIT_WORD: return self.info.game_over_message()
                    case settings.NEXT_MELODY_TEXT: continue

    def new_round_initiator(self):
        """
        TODO
        """
        self.round_number += 1

        if self.round_number != 1:

            need_new_pool = informer.format_key_text(
                input(f'{settings.need_new_pool_text}: ')
            )

            if need_new_pool == settings.QUIT_WORD:
                return settings.QUIT_WORD

            if need_new_pool == settings.NEW_POOL_TEXT:

                self.player_data = ()
                self.pl_pool.current_pool.clear()

            else:
                self.pl_pool.clear_players_scores()

        while isinstance(self.player_data, tuple):

            self.player_data = self.pl_pool.player_name_request()

            if not isinstance(self.player_data, str):
                self.pl_pool.new_player_registration(*self.player_data)
                self.info.player_greeting(*self.player_data)

            if len(self.pl_pool.current_pool) == settings.PLAYERS_MAX_COUNT:
                # Players pool overload.
                break

            else:
                # It may be only the “stop” or “quit” string.

                if self.player_data == settings.QUIT_WORD:
                    # “quit” case
                    return settings.QUIT_WORD

                if len(self.pl_pool.current_pool) < settings.PLAYERS_MIN_COUNT:
                    # “stop” case
                    print(settings.wrong_players_count_text)
                    self.player_data = ()

        self.info.end_registration_message(
            player_count=len(self.pl_pool.current_pool)
        )

        time.sleep(settings.ATTENTION_TIME)

        if self.round_number == 1:
            self.info.show_rules()

        self.mus_player.new_round_tracks_setter()

        is_game_starting = self.info.tap_to_game_starting()

        if is_game_starting == settings.QUIT_WORD:
            return settings.QUIT_WORD

    def new_melody_starting(self):
        """
        TODO
        """

        self.clear_exclusion_data()

        winner = self.pl_pool.get_winner()

        if winner:
            self.info.win_message(winner)
            self.mus_player.play_fanfare()
            self.info.round_over_message(self.round_number)
            return settings.NEW_ROUND_TEXT

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

            user_input_data = None

            for i in range(2):

                match i:
                    case 0: user_input_data = self.mus_player.track_playback(self.input_deliver)
                    case 1: user_input_data = self.get_check_inputting()

                if user_input_data in (settings.NEXT_MELODY_TEXT, settings.QUIT_WORD):
                    self.mus_player.track_stop_unload()
                    return user_input_data

            if isinstance(user_input_data, tuple):

                checking_result = self.guess_checking(user_input_data)

                if checking_result:
                    return checking_result

    @staticmethod
    def input_deliver() -> str:
        """
        TODO
        """
        return informer.format_key_text(
            input('\n' + settings.stop_melody_text)
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

        for i, text in enumerate(settings.player_track_number_text):
            # Two loops for player\'s name and melody\'s name.

            while True:
                # Until will get an allowed inputted text.

                # Format the inputted text.
                spl_answer = informer.format_key_text(input(text))

                # If the text is equal to commands below.
                if spl_answer in (
                        settings.NEXT_MELODY_TEXT,
                        settings.CONTINUE_GAME_TEXT,
                        settings.QUIT_WORD
                ):
                    # Then return this command.
                    return spl_answer

                try:
                    # In other cases, try to cast the inputted text type to integer.
                    spl_answer = int(spl_answer)

                except (ValueError, Exception):
                    # If casting to integer is not possible then display the message
                    # and let input it again.
                    print(settings.input_numbers_only_text)
                    continue

                not_correct_number = self.is_number_not_correct(i, spl_answer)

                if not_correct_number:
                    # If the function returs a not empty string then it means
                    # it has gotten a wrong player's or melody's number,
                    # so let try input it again.
                    print(not_correct_number)
                    continue

                # If an inputted number is allowed then go to the next for-loop.
                break

            # If data was cast successful and the number is correct
            # then add it to the corresponding array.
            answers.append(spl_answer)

        # Get a current playing melody index.
        current_track_index = self.mus_player.guessable_tracks_list.index(
            self.mus_player.current_singer_track_tuple
        )

        # If all two numbers were gotten successful then return a tuple in wich
        # the first element is a boolean value if inputted melody number and
        # playing melody number are equal. And the next values are the melody
        # number and the gamer number.
        return answers[1] == (current_track_index + 1), *answers

    def is_number_not_correct(
            self,
            i: int,
            answer: int
    ) -> Union[None, str]:
        """
        The function checks whether the numbers entered by
        the user exceed the acceptable parameters.
        # i == 0: If expected a gamer number.
        # key1: If the number is an excluded gamer number.
        # key2: If the gamer number is greater than a total gamers number.
        # i == 1: If expected a melody number.
        # key1: If the number is an excluded melody number.
        # key2: If the melody number is greater than a total melodys number.
        """

        def get_nums(array):
            return range(1, len(array) + 1)

        def get_tpl_nums(tpl_array):
            return list(map(lambda x: x[0], tpl_array))

        cases = {
            0: {
                answer in get_tpl_nums(self.pl_pool.excluded_players): settings.player_already_answered_text,
                answer not in get_nums(self.pl_pool.current_pool): settings.wrong_player_number_text
            },
            1: {
                answer in get_tpl_nums(self.mus_player.excluded_tracks): settings.melody_already_named_text,
                answer not in get_nums(self.mus_player.guessable_tracks_list): settings.wrong_melody_number_text
            }
        }[i]

        if True in cases:
            return cases[True] + f' or input "{settings.CONTINUE_GAME_TEXT}" to continue the melody.'

    def guess_checking(
            self,
            user_feedback: tuple
    ) -> Union[None, str]:
        """
        TODO
        """
        is_guessed, player_num, track_num = user_feedback

        self.info.guess_result_message(
            player_name=self.pl_pool.current_pool[player_num]['name'],
            is_guessed=is_guessed
        )

        time.sleep(settings.ATTENTION_TIME)

        if is_guessed:
            self.pl_pool.current_pool[player_num]['score'] += 1
            return settings.NEXT_MELODY_TEXT

        else:
            self.add_new_exclusion(track_num, player_num)

            if len(self.pl_pool.excluded_players) == len(self.pl_pool.current_pool):
                print(settings.no_one_guessed_text + '\n')
                return settings.NEXT_MELODY_TEXT

    def add_new_exclusion(
            self,
            track_number: int,
            player_number: int
    ) -> None:
        """
        TODO
        """
        ex_track_tpl = self.mus_player.guessable_tracks_list[track_number - 1]
        ex_player_name = self.pl_pool.current_pool[player_number]['name']

        self.mus_player.excluded_tracks.append(
            (
                track_number,
                self.mus_player.file_name_to_title(ex_track_tpl)
            )
        )

        self.pl_pool.excluded_players.append((player_number, ex_player_name))


if __name__ == '__main__':
    game = GTMGame()
    game.execute()
