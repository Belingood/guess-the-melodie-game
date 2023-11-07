import time
from typing import Union

import tools


class Informer:

    @staticmethod
    def greeting() -> None:
        """
        TODO
        """
        for line in tools.signboard:
            print(line)
            time.sleep(0.5)

        time.sleep(0.5)

    def game_over_message(self) -> None:
        """
        TODO
        """
        self.text_into_frame(
            [f'\n{tools.game_over_text}\n'],
            need_printing=True
        )

    def player_registration_intro(self) -> None:
        """
        TODO
        """
        self.text_into_frame(
            [
                tools.player_registration_text.upper(),
                tools.allowed_name_notice
            ],
            need_printing=True
        )

    @staticmethod
    def player_greeting(
            player_number: str,
            player_name: str
    ) -> None:
        """
        TODO
        """
        pgt1, pgt2, pgt3 = tools.player_greeting_text_array.copy()
        print(f'{pgt1} {player_name.upper()}! {pgt2} {player_number}, {pgt3}\n')

    def end_registration_message(
            self,
            player_count
    ) -> None:
        """
        TODO
        """
        first, second = tools.players_registered_text
        self.text_into_frame([f'{first} {player_count} {second}'])

    def show_rules(self) -> None:
        """
        TODO
        """
        self.text_into_frame(tools.rule_text)

    @staticmethod
    def tap_to_game_starting() -> input:
        """
        TODO
        """
        return input(f'{tools.tap_to_game_starting_text}: ')

    @staticmethod
    def text_into_frame(
            array_of_text_strings: Union[tuple, list],
            double_border: bool = True,
            need_printing: bool = True
    ) -> Union[str, None]:
        """
        TODO
        """
        spl_text = []

        for string in array_of_text_strings:
            for sub_string in string.split('\n'):
                spl_text.append(sub_string)

        frame_length = len(sorted(spl_text, key=len)[-1])
        tl, tr, bl, br, st = ('╔', '╗', '╚', '╝', '═') if double_border else ('┌', '┐', '└', '┘', '─')
        lf_fr, rt_fr = ('║ ', ' ║') if double_border else ('│ ', ' │')
        brd_space = 2

        top_frame = tl + st * (frame_length + brd_space) + tr
        bottom_frame = bl + st * (frame_length + brd_space) + br
        frame_content = (lf_fr + txt.ljust(frame_length) + rt_fr for txt in spl_text)
        framed_text = '\n'.join((top_frame, *frame_content, bottom_frame))

        if need_printing:
            print(framed_text)
            return

        return framed_text

    def show_table_by_array(
            self,
            title_array: list,
            content_array: list,
            double_border: bool = True,
            need_printing: bool = True
    ) -> Union[str, None]:
        """
        TODO
        """

        common_array = [title_array] + content_array
        common_array_size = len(common_array)
        col_count = len(title_array)
        left_indent = 1
        right_indent = 4
        ind = left_indent + right_indent

        lengths = list(map(lambda x: list(map(len, x)), common_array))
        max_lengths = list(map(lambda i: max(map(lambda x: x[i], lengths)) + ind, range(col_count)))
        table_content = []

        for row_ind, row in enumerate(common_array):

            indented_row = []

            for col_ind, col_text in enumerate(row):

                text = col_text.ljust(max_lengths[col_ind])
                indented_row.append(' ' * left_indent + text + ' ' * right_indent)

            row_content = ' '.join(indented_row)
            table_content.append(row_content)
            if row_ind != common_array_size - 1:
                table_content.append({True: '═', False: '─'}[row_ind == 0] * len(row_content))

        return self.text_into_frame(
            table_content,
            double_border=double_border,
            need_printing=need_printing
        )

    @staticmethod
    def show_guessable_track_titles(track_titles: list) -> None:
        """
        TODO
        """
        for i, title in enumerate(track_titles):
            print(i + 1, title)

    def show_positive_scores(
            self,
            positive_scores: list
    ) -> None:
        """
        TODO
        """
        if not positive_scores:

            self.text_into_frame(
                [tools.players_have_0_text],
                need_printing=True
            )

        else:
            ps_srt_by_name = sorted(positive_scores, key=lambda x: x[1])
            ps_srt_by_scores = sorted(ps_srt_by_name, key=lambda x: x[2], reverse=True)

            self.show_table_by_array(
                title_array=tools.positive_scores_title,
                content_array=list(map(lambda tpl: list(map(str, tpl)), ps_srt_by_scores))
            )

    def show_excluded_tracks_players(
            self,
            excluded_tracks: list,
            excluded_players: list
    ) -> None:
        """
        TODO
        """
        if not excluded_tracks:
            return

        # The array for a table content.
        exclusion_information = []

        for ex_track, ex_player in zip(excluded_tracks, excluded_players):
            # Pair the names of melodies and players from the corresponding arrays.

            # Add the taken ifromation to the corresponding array.
            exclusion_information.append(
                [
                    f'[✕] {ex_track[0]}. {ex_track[1]}',
                    f'[✕] {ex_player[0]}. {ex_player[1]}'
                ]
            )

        self.show_table_by_array(
            title_array=tools.exclusion_title,
            content_array=exclusion_information
        )

    @staticmethod
    def guess_result_message(
            player_name: str,
            is_guessed: bool
    ) -> None:
        """
        TODO
        """
        first, second = tools.congratulation_text if is_guessed else tools.not_guessed_text
        print(f'{first} {player_name}, {second}\n')

    def win_message(self, winner_name):
        """
        TODO
        """
        self.text_into_frame(
            ['', f'{winner_name.upper()} {tools.win_message}', '']
        )

    def round_over_message(self):
        self.text_into_frame(
            tools.this_round_over_text
        )
