import os
import random
from os import environ

import tools

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # It cancels a pygame greating (must be before pygame importing)
import pygame

freq = 44100  # audio CD quality
bitsize = -16  # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024  # samples number
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.set_volume(1.0)  # optional volume 0 to 1.0


class MidiPlayer:

    def __init__(self):

        # The main directory path.
        self.main_directory = os.getcwd()

        # The pygame clock object for checking the melodie playback status.
        self.pygame_clock = pygame.time.Clock()

        self.singer_track_tuples = self.singer_track_tuples_getting('sound_library')

        self.extra_singer_track_tuples = self.singer_track_tuples_getting('extra_sound_library')

        self.tracks_for_round_playback = []

        self.current_singer_track_tuple = ('', '')

        self.guessable_tracks_list = []

        self.excluded_tracks = []

    def singer_track_tuples_getting(self, target_dir_name: str) -> list:
        """
        TODO
        """

        # Path to the directory with all track directories.
        midi_directory = os.path.join(self.main_directory, target_dir_name)

        # The generator object which contains an array of track
        # directories and content arrays of these directories.
        midi_store_gen = os.walk(midi_directory)

        # The array of names of all singers.
        all_singers = next(el for i, el in enumerate(next(midi_store_gen)) if i == 1)

        # The array with arrays of tracks.
        all_track_arrays = [el[-1] for el in midi_store_gen]

        singers_tracks_tuples = []

        for i, singer in enumerate(all_singers):
            for track in all_track_arrays[i]:
                singers_tracks_tuples.append((singer, track))

        # A list with tuples wich contain pairs like a (singer name, track name).
        return singers_tracks_tuples

    def new_round_tracks_setter(self) -> None:
        """
        TODO
        """
        tracks = self.singer_track_tuples.copy()
        random.shuffle(tracks)
        self.tracks_for_round_playback = tracks

    def set_random_singer_track(self) -> None:
        """
        Returns a random artist and one of his songs chosen at random.
        """

        random_singer_track = random.choice(self.tracks_for_round_playback)
        self.tracks_for_round_playback.remove(random_singer_track)
        self.current_singer_track_tuple = random_singer_track

    def preseted_track_loading(self):

        if pygame.mixer.music.get_pos() != -1:
            self.track_stop_unload()

        # Get the path of the playing melodie.
        track_path = os.path.join(
            self.main_directory,
            'sound_library',
            *self.current_singer_track_tuple
        )

        try:
            # Try to load the melodie file.
            pygame.mixer.music.load(track_path)
        except pygame.error:
            # Report an error if it occurs while loading the file.
            print(
                f'File {" - ".join(self.current_singer_track_tuple)}'
                f' not found! {pygame.get_error()}'
            )
            return

    def track_playback(self, input_deliver) -> str:
        """
        TODO
        """

        if pygame.mixer.music.get_pos() == -1:
            pygame.mixer.music.play()
        else:
            # Start playing the loaded melodie.
            pygame.mixer.music.unpause()

        while pygame.mixer.music.get_busy():
            # Check with the loop if playback has finished.

            # Checking time interval.
            self.pygame_clock.tick(30)

            text = input_deliver()

            if text or text == '':

                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()

                return text

        self.track_stop_unload()

    @staticmethod
    def track_stop_unload() -> None:
        """
        TODO
        """
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def set_guessble_tracks_list(self):
        """
        TODO
        """
        tracks_except_current = self.tracks_for_round_playback + self.extra_singer_track_tuples
        random.shuffle(tracks_except_current)
        tracks_except_current = tracks_except_current[: tools.TRACK_LIST_SIZE - 1] + [self.current_singer_track_tuple]
        random.shuffle(tracks_except_current)
        self.guessable_tracks_list = tracks_except_current

    def get_guessable_track_titles(self):
        """
        TODO
        """
        return list(map(self.file_name_to_title, self.guessable_tracks_list))

    @staticmethod
    def file_name_to_title(track_tpl: tuple) -> str:
        """
        TODO
        """
        siger, track_name = map(lambda x: x.replace('_', ' ').title(), track_tpl)
        dot_index = track_name.rfind('.')
        return f'{siger} - {track_name[:dot_index]}'
