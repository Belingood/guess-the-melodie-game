import time
from typing import Union

import informer
import music_player
import player_pool
import settings


class GTMGame:
    """
    The class implements the basic procedures of the game.
    The -execute()- class function contains the main algorithm
    of the program, in which the main operating functions
    are divided into more compact execution scripts.
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

    def execute(self) -> None:
        """
        The main function for game executing.
        """

        # Display text greeting.
        self.info.greeting()

        # Displaying the rule of player registration.
        self.info.player_registration_intro()

        while True:
            # The main working loop. On this level starts the new game round.

            match self.new_round_initiator():
                # Finish the game if it has gotten the corresponding order.
                case settings.QUIT_WORD: return self.info.game_over_message()

            while True:
                # This level starts each melody to be guessed.

                match self.new_melody_starting():
                    # If it is a winner, and it has an order to start the game again
                    # then go to the start game level.
                    case settings.NEW_ROUND_TEXT: break

                match self.new_try_to_guess():
                    # If it has gotten an order to finish the game on
                    # this try-guess level then finish the game.
                    case settings.QUIT_WORD: return self.info.game_over_message()

                    # Skip to the beginning of the loop to start playing a new melody.
                    case settings.NEXT_MELODY_TEXT: continue

    def new_round_initiator(self) -> Union[None, str]:
        """
        This function performs all the necessary operations
        to prepare and start a new game round.
        """
        # Increment game-round counter.
        self.round_number += 1

        if self.round_number != 1:
            # If it is not the first round.

            if self.ask_for_new_player_pool() == settings.QUIT_WORD:
                # In this point, program asks a user if they need a new player pool.
                return settings.QUIT_WORD

        if self.player_registration() == settings.QUIT_WORD:
            # In this point it has a process of registration.
            return settings.QUIT_WORD

        # Display the message of the end of the registration process.
        self.info.end_registration_message(
            player_count=len(self.pl_pool.current_pool)
        )

        # Just time to focus on current information.
        time.sleep(settings.ATTENTION_TIME)

        if self.round_number == 1:
            # Display the game rules if it is not the first game round.
            self.info.show_rules()

        # Form a set of tracks from the game repository for the new round.
        self.mus_player.new_round_tracks_setter()

        if self.info.tap_to_game_starting() == settings.QUIT_WORD:
            # Asking to tap any key to start the game.
            return settings.QUIT_WORD

    def new_melody_starting(self) -> Union[None, str]:
        """
        The function selects a random track to guess and places
        it in a list formed from other random tracks at a random
        position. Finally, it loads the file of guessable track into
        the music player.
        """

        # Clear information about players and erroneous
        # melodies excluded during the previous track.
        self.clear_exclusion_data()

        # Check if there is a winner.
        winner = self.pl_pool.get_winner()

        if winner:
            # If there is a winner then display a message and play a fanfare,
            # then inform about the end of the game round and send the “round”
            # key-word to let know the program it needs the new round initiation.

            self.info.win_message(winner)
            self.mus_player.play_fanfare()
            self.info.round_over_message(self.round_number)
            return settings.NEW_ROUND_TEXT

        # If there is no winner yet:

        # Display the players with their positive scores, if any.
        self.info.show_positive_scores(
            positive_scores=self.pl_pool.get_positive_scores()
        )

        # Get and assign to the class attribute another random track.
        self.mus_player.set_random_singer_track()

        # Form and assign to the class attribute another
        # track list including the guessble melody.
        self.mus_player.set_guessble_tracks_list()

        # Display the resulting track list.
        self.info.show_guessable_track_titles(
            self.mus_player.get_guessable_track_titles()
        )

        # Load the preseted guessble melody.
        self.mus_player.preseted_track_loading()

    def new_try_to_guess(self) -> Union[None, str]:
        """
        The function, at the user's initiative, stops the
        playing of a track, receives from him information
        about his own number and the track number which he
        thinks is the number of the track being played.
        Next, the function checks whether the user's answer
        is correct or not, according to which it activates
        the procedures provided for each case.
        """

        while True:
            # New try to guess.

            # Display a table with ecluded players and tracks, if any.
            self.info.show_excluded_tracks_players(
                self.mus_player.excluded_tracks,
                self.pl_pool.excluded_players
            )

            user_input_data = None

            for i in range(2):
                # Execute two functions using a loop.

                match i:
                    # The first one starts the music player and gets user inputting.
                    case 0: user_input_data = self.mus_player.track_playback(self.input_deliver)

                    # The second one gets and checks inputted by
                    # user numbers of a track and theyselves.
                    case 1: user_input_data = self.get_check_inputting()

                if user_input_data in (settings.NEXT_MELODY_TEXT, settings.QUIT_WORD):
                    # If it has gotten any keywords then it stops the music player
                    # and return these keywords to process on the higher level.

                    self.mus_player.track_stop_unload()
                    return user_input_data

            if isinstance(user_input_data, tuple):
                # If the user data is a tuple like (is_answer_correct, player_number, track_number).

                # User answering result processing.
                result_checking = self.guess_checking(user_input_data)

                if result_checking:
                    # If it has gotten any keyword then return it.
                    return result_checking

    def ask_for_new_player_pool(self) -> Union[None, str]:
        """
        At the beginning of each round, with the exception of the first,
        this function receives information from the user about whether
        to form a new pool of players or start a new round with the same
        composition.
        """

        match informer.format_key_text(
            input(f'{settings.need_new_pool_text}: ')
        ):
            # Ask if they need to create a new player pool
            # or continue with the previous pool.

            case settings.QUIT_WORD:
                # If it has gotten the order to quit.
                return settings.QUIT_WORD

            case settings.NEW_POOL_TEXT:
                # If it has gotten the order to start
                # another round with the new player-pool.
                self.player_data = ()
                self.pl_pool.current_pool.clear()

            case _:
                # For other cases. /type(self.player_data) == str/
                self.pl_pool.clear_players_scores()

    def player_registration(self) -> Union[None, str]:
        """
        The function queries each player in turn for their name,
        assigning each of them their own unique number and
        registering them in the system.
        """

        while isinstance(self.player_data, tuple):
            # If the user data is a tuple like (player_number, player_name).

            if len(self.pl_pool.current_pool) == settings.PLAYERS_MAX_COUNT:
                # If the players pool is overloaded the leave the registration process
                # with the existing player count which is the maximum count.
                return

            self.player_data = self.pl_pool.player_name_request()

            if not isinstance(self.player_data, str):
                # If user data is not a string then register and greet the new player.
                self.pl_pool.new_player_registration(*self.player_data)
                self.info.player_greeting(*self.player_data)

            else:
                # In this point it may be only the “stop” or “quit” string.

                if self.player_data == settings.QUIT_WORD:
                    # “quit” case
                    return settings.QUIT_WORD

                if len(self.pl_pool.current_pool) < settings.PLAYERS_MIN_COUNT:
                    # “stop” case

                    # Inform the user of the incorrect action and set the class attribute
                    # to a tuple type (this will prevent the loop from breaking) to continue
                    # with the registration attempt.
                    print(settings.wrong_players_count_text)
                    self.player_data = ()

    @staticmethod
    def input_deliver() -> str:
        """
        This function object is passed inside the melody playback
        function to be activated when the track is played. Calling
        this function activates the input module, which, having
        received any input from the user, immediately sends it for
        further processing in other functions, having previously
        paused the player.
        """
        return informer.format_key_text(
            input('\n' + settings.stop_melody_text)
        )

    def clear_exclusion_data(self) -> None:
        """
        This fuction clears information about players and erroneous
        melodies excluded during the previous track playing.
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

                not_correct_number = self.is_number_incorrect(i, spl_answer)

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

    def is_number_incorrect(
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

        def get_nums(array: Union[list, dict, tuple]) -> range:
            """
            Returns the serial numbers of the array elements starting from one.
            """
            return range(1, len(array) + 1)

        def get_tpl_nums(tpl_array: list) -> list:
            """
            Collects the first elements of the tuples in the array into a list.
            """
            return list(map(lambda x: x[0], tpl_array))

        # When entering a previously entered number or a number that is outside
        # the permissible limits, it assigns a corresponding text alert to this variable.
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
            # If one of the above cases occurs then the allert will be return as a string.
            return cases[True] + f' or input "{settings.CONTINUE_GAME_TEXT}" to continue the melody.'

    def guess_checking(
            self,
            user_feedback: tuple
    ) -> Union[None, str]:
        """
        The function receives data about the player’s answers
        and notifies the user about the correctness of this answer.
        If the answer is correct, the program adds a point to the
        player who gave the correct answer. Otherwise, the program
        adds the player who gave the wrong answer to the exclusion
        list, which eliminates the possibility of giving repeated
        answers by this player for the current track. This feature
        will be restored with the start of a new track.
        The wrong track is also eliminated so that other players do
        not select it again.
        """
        # Unpack the tuple with user data in the next view
        # (is_answer_correct, player_number, track_number).
        is_guessed, player_num, track_num = user_feedback

        # Inform the user about the result of they guess trying.
        self.info.guess_result_message(
            player_name=self.pl_pool.current_pool[player_num]['name'],
            is_guessed=is_guessed
        )

        # Just time to focus on current information.
        time.sleep(settings.ATTENTION_TIME)

        if is_guessed:
            # If it was guessed successful then increment this player's scores.
            # And send the order to next track starting.
            self.pl_pool.current_pool[player_num]['score'] += 1
            return settings.NEXT_MELODY_TEXT

        else:
            # If guess trying wasn't successful.

            # Exclude the player and this track to reselect.
            self.add_new_exclusion(track_num, player_num)

            if len(self.pl_pool.excluded_players) == len(self.pl_pool.current_pool):
                # If all the players have answered incorrectly then start the next track.
                print(settings.no_one_guessed_text + '\n')
                return settings.NEXT_MELODY_TEXT

    def add_new_exclusion(
            self,
            track_number: int,
            player_number: int
    ) -> None:
        """
        The function, based on the corresponding numbers, receives
        the name of the erroneous track and the name of the player
        who selected this track. This information is then placed
        into appropriate arrays.
        """
        # Get the incorrect track name by its index in the list.
        ex_track_tpl = self.mus_player.guessable_tracks_list[track_number - 1]

        # Get the player name from player pool dictionary by their number.
        ex_player_name = self.pl_pool.current_pool[player_number]['name']

        # Add the excluded track number and name to the corresponding list as a tuple.
        self.mus_player.excluded_tracks.append(
            (
                track_number,
                self.mus_player.file_name_to_title(ex_track_tpl)
            )
        )

        # Add the excluded player number and name to the corresponding list as a tuple.
        self.pl_pool.excluded_players.append((player_number, ex_player_name))


if __name__ == '__main__':
    game = GTMGame()
    game.execute()
