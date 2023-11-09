import time
from typing import Union

import settings


class Informer:
    """
    The class is used to display the necessary current
    information about the events and processes of the game.
    """

    @staticmethod
    def greeting() -> None:
        """
        Displaying of game greeting.
        """
        for line in settings.signboard:
            print(line)
            time.sleep(0.5)

        time.sleep(0.5)

    def game_over_message(self) -> None:
        """
        Displaying of the game over message.
        """
        self.text_into_frame(
            [f'\n{settings.game_over_text}\n'],
            need_printing=True
        )

    def player_registration_intro(self) -> None:
        """
        Displaying of rules for registration of players.
        """
        self.text_into_frame(
            [
                settings.player_registration_text.upper(),
                settings.allowed_name_notice
            ],
            need_printing=True
        )

    @staticmethod
    def player_greeting(
            player_number: str,
            player_name: str
    ) -> None:
        """
        Displaying of greeting of the new player.
        """
        pgt1, pgt2, pgt3 = settings.player_greeting_text_array.copy()
        print(f'{pgt1} {player_name.upper()}! {pgt2} {player_number}, {pgt3}\n')

    def end_registration_message(
            self,
            player_count: int
    ) -> None:
        """
        The succesful registration message.
        """
        first, second = settings.players_registered_text
        self.text_into_frame([f'{first} {player_count} {second}'])

    def show_rules(self) -> None:
        """
        Display the game rules.
        """
        self.text_into_frame(settings.rule_text)

    @staticmethod
    def tap_to_game_starting() -> str:
        """
        Returns user's any input to start the game.
        """
        return input(f'{settings.tap_to_game_starting_text}: ')

    @staticmethod
    def text_into_frame(
            array_of_text_strings: Union[tuple, list],
            double_border: bool = True,
            need_printing: bool = True
    ) -> Union[str, None]:
        """
        Places an array of strings into a double or single frame.
        """
        spl_text = []

        for string in array_of_text_strings:
            # It separates text by a line break and placed
            # as separate elements in a special dictionary.
            for sub_string in string.split('\n'):
                spl_text.append(sub_string)

        # The length of resulting frame by the longest string of all strings.
        frame_length = len(sorted(spl_text, key=len)[-1])

        # Variables of frame elements.
        tl, tr, bl, br, st = ('╔', '╗', '╚', '╝', '═') if double_border else ('┌', '┐', '└', '┘', '─')
        lf_fr, rt_fr = ('║ ', ' ║') if double_border else ('│ ', ' │')

        # The length of space between a side border
        # of the frame and the beginning of strings.
        brd_space = 2

        # Form the top and bottom lines of the frame.
        top_frame = tl + st * (frame_length + brd_space) + tr
        bottom_frame = bl + st * (frame_length + brd_space) + br

        # Adding to each row side borders.
        frame_content = (lf_fr + txt.ljust(frame_length) + rt_fr for txt in spl_text)

        # We place all the lines in the array between the upper
        # and lower borders of the frame, gluing them together,
        # as well as all the lines in the array between each other
        # with a line break.
        framed_text = '\n'.join((top_frame, *frame_content, bottom_frame))

        if need_printing:
            # If necessary, print the result string.
            print(framed_text)
            return

        # Return the result string if it doesn't need to be printed.
        return framed_text

    def show_table_by_array(
            self,
            title_array: list,
            content_array: list,
            double_border: bool = True,
            need_printing: bool = True
    ) -> Union[str, None]:
        """
        The function takes an array of strings, each of which is
        the header of a separate table column. The second array
        the function receives contains arrays that contain rows
        for each column of a particular row. The function calculates
        the necessary sizes and intervals for correct printing
        of received data in table format.
        """

        # Merge a header array with a content array.
        common_array = [title_array] + content_array

        # Calculate the length of common array.
        common_array_size = len(common_array)

        # Get the table columns count which equal to length of title array.
        col_count = len(title_array)

        # Set the left, right and total indent for each column as well a column separator.
        left_indent = 1
        right_indent = 4
        ind = left_indent + right_indent
        column_separator = ' '

        # Forms a copy of the content array, in which each string
        # is replaced with a number equal to the length of this string.
        lengths = list(map(lambda x: list(map(len, x)), common_array))

        # Among the lengths of all the rows of each column, we find the
        # largest length value and adding to it the size of the total
        # indent, we thus obtain the width of this column.
        max_lengths = list(map(lambda i: max(map(lambda x: x[i], lengths)) + ind, range(col_count)))

        table_content = []

        for row_ind, row in enumerate(common_array):

            indented_row = []

            for col_ind, col_text in enumerate(row):

                # Format the ij(-row_ind-, -col_ind-) table cell
                # with the indent by the width of this column.
                text = col_text.ljust(max_lengths[col_ind])

                # Add left and right indents to this formatted
                # line and append it to the corresponding array.
                indented_row.append(' ' * left_indent + text + ' ' * right_indent)

            # Join all strings of the current column with the column separator.
            row_content = column_separator.join(indented_row)

            # Put the resulting string into the table row array.
            table_content.append(row_content)

            if row_ind != common_array_size - 1:
                # If the string is not the last one, then the bottom dividing
                # line is added to it. This line is double for the string of
                # titles (zero index) and single for all others.
                table_content.append({True: '═', False: '─'}[row_ind == 0] * len(row_content))

        # All lines of data received by the function are separated
        # by horizontal lines, and columns are separated by a column
        # separator. The outer frame is formed by the function below.
        #
        # The -return- operator is needed in case the table does not
        # need to be printed, but only formed.
        return self.text_into_frame(
            table_content,
            double_border=double_border,
            need_printing=need_printing
        )

    @staticmethod
    def show_guessable_track_titles(track_titles: list) -> None:
        """
        Displaying the list of guessable tracks with their numbers.
        """
        for i, title in enumerate(track_titles):
            print(i + 1, title)

    def show_positive_scores(
            self,
            positive_scores: list
    ) -> None:
        """
        Displaying none-zero scores of players.
        """
        if not positive_scores:
            # If nobody has non-zero scores then display the corresponding message.

            self.text_into_frame(
                [settings.players_have_0_text],
                need_printing=True
            )

        else:
            # Sort players data at first by name and then by scores.
            ps_srt_by_name = sorted(positive_scores, key=lambda x: x[1])
            ps_srt_by_scores = sorted(ps_srt_by_name, key=lambda x: x[2], reverse=True)

            # Display players scores information using a table.
            self.show_table_by_array(
                title_array=settings.positive_scores_title,
                content_array=list(map(lambda tpl: list(map(str, tpl)), ps_srt_by_scores))
            )

    def show_excluded_tracks_players(
            self,
            excluded_tracks: list,
            excluded_players: list
    ) -> None:
        """
        Displaying excluded players and tracks in table form.
        """
        if not excluded_tracks:
            return

        # The array for a table content.
        exclusion_information = []

        for ex_track, ex_player in zip(excluded_tracks, excluded_players):
            # Pair the names of melodys and players from the corresponding arrays.

            # Add the taken ifromation to the corresponding array.
            exclusion_information.append(
                [
                    f'[x] {ex_track[0]}. {ex_track[1]}',
                    f'[x] {ex_player[0]}. {ex_player[1]}'
                ]
            )

        self.show_table_by_array(
            title_array=settings.exclusion_title,
            content_array=exclusion_information
        )

    @staticmethod
    def guess_result_message(
            player_name: str,
            is_guessed: bool
    ) -> None:
        """
        Informing whether a given answer is correct or incorrect.
        """
        # Receive and unpack an array of text depending
        # on the correctness of the results.
        first, second = {
            True: settings.congratulation_text,
            False: settings.not_guessed_text
        }[is_guessed]

        print(f'{first} {player_name}, {second}\n')

    def win_message(
            self,
            winner_name: str
    ) -> None:
        """
        Displaying the message of a winner.
        """
        self.text_into_frame(
            ['', f'{winner_name.upper()} {settings.win_message}', '']
        )

    def round_over_message(self, round_number: int) -> None:
        """
        Displaying a message of the round ending with its number.
        """
        text = settings.this_round_over_text.copy()
        text[1] = f'The {round_number} {text[1]}'
        self.text_into_frame(text)


def format_key_text(text: str) -> str:
    """
    It clears a string of leading and trailing
    spaces and quotes as well converts the text
    to lower case.
    """
    return text.strip(" '\"").lower()
