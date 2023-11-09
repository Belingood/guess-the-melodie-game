import os
import random
from os import environ

import settings

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # It cancels a pygame greating (must be before -pygame- importing)
import pygame

freq = 44100  # audio CD quality
bitsize = -16  # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024  # samples number
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.set_volume(1.0)  # optional volume 0 to 1.0


class MidiPlayer:
    """
    The class is used to play music files, as well
    as to generate playlists based on files available
    in the game repository.
    """

    __slots__ = [
        'main_directory',
        'pygame_clock',
        'singer_track_tuples',
        'extra_singer_track_tuples',
        'tracks_for_round_playback',
        'current_singer_track_tuple',
        'guessable_tracks_list',
        'excluded_tracks'
    ]

    def __init__(self):

        # The main directory path.
        self.main_directory = os.path.dirname(os.path.abspath(__file__))

        # The pygame clock object for checking the melody playback status.
        self.pygame_clock = pygame.time.Clock()

        # The list of tuples like (singer_name, melody_name) of all tracks in game repository.
        self.singer_track_tuples = self.singer_track_tuples_getting('sound_library')

        # The list of tuples like (singer_name, melody_name) of extra tracks (not played).
        self.extra_singer_track_tuples = self.singer_track_tuples_getting('extra_sound_library')

        # The shuffled list of played tracks for a current game round.
        self.tracks_for_round_playback = []

        # The tuple of a current playing track like (singer_name, melody_name).
        self.current_singer_track_tuple = ('', '')

        # A list of a set number of tracks containing a playable track to guess.
        self.guessable_tracks_list = []

        # The list for wrong guessed tracks.
        self.excluded_tracks = []

    def singer_track_tuples_getting(
            self,
            target_dir_name: str
    ) -> list:
        """
        The function takes the name of the target directory from which
        it collects information about subdirectories named after the
        artist and the tracks contained in these directories. The
        function stores the collected data in an array as tuples with
        two string elements - the name of the artist and the name of
        the track of this artist.
        """

        # Path to the directory with all track directories.
        midi_directory = os.path.join(self.main_directory, target_dir_name)

        # The generator object which contains an array of track
        # directories and content arrays of these directories.
        midi_store_gen = os.walk(midi_directory)

        # The generator of names of all singers (folder names).
        all_singers = (elm for i, elm in enumerate(next(midi_store_gen)) if i == 1)

        # The array with arrays of tracks.
        all_track_arrays = (el[-1] for el in midi_store_gen)

        # The empty array for tuples like (singer_name, track_name)
        # of all tracks in the game repository.
        singers_tracks_tuples = []

        for singer in next(all_singers):
            # Get the index and name of folder (folders are named after the singers)

            for track in next(all_track_arrays):
                # Go throu the current singer tracks
                # (singer track array has the same index to singer name in singer names array).

                # Add the tuple with the singer name and track name to the corresponding array.
                singers_tracks_tuples.append((singer, track))

        # A list with tuples wich contain pairs like a (singer name, track name).
        return singers_tracks_tuples

    def new_round_tracks_setter(self) -> None:
        """
        While playing each of the melodys available in the repository,
        this melody is temporarily removed from the list compiled on the
        basis of the existing repository. At the beginning of each new round,
        this function regenerates a list of tracks for playback from all
        tracks available in the repository, re-shuffles this list randomly
        and assigns the resulting list to the corresponding class attribute.
        """
        tracks = self.singer_track_tuples.copy()
        random.shuffle(tracks)
        self.tracks_for_round_playback = tracks

    def set_random_singer_track(self) -> None:
        """
        Returns a random artist and one of his songs chosen at random.
        And it also assigns this data to the corresponding class attribute.
        """
        random_singer_track = random.choice(self.tracks_for_round_playback)
        self.tracks_for_round_playback.remove(random_singer_track)
        self.current_singer_track_tuple = random_singer_track

    def preseted_track_loading(
            self,
            library: str = None
    ) -> None:
        """
        By default, loads a preset random track into the music player.
        But it can also load an arbitrary track specified in a special
        parameter.
        """
        if pygame.mixer.music.get_pos() != -1:
            # If the player has the old track (new tracks have a playing
            # position == -1), then unload it from the player.
            self.track_stop_unload()

        match library:
            # If not -library- data then build a path to the playing track repository.
            case None:
                target_path = ('sound_library', *self.current_singer_track_tuple)

            # If -library- has any string path then replace all slashes and form a list
            # by spaces to build the path by -os.path.join()- method.
            case _:
                target_path = library.replace('/', ' ').replace('\\', ' ').split(' ')

        # Get the path of the playing melody.
        track_path = os.path.join(
            self.main_directory,
            *target_path
        )

        try:
            # Try to load the melody file.
            pygame.mixer.music.load(track_path)
        except pygame.error:
            # Report an error if it occurs while loading the file.
            print(
                f'File {" - ".join(self.current_singer_track_tuple)}'
                f' not found! {pygame.get_error()}'
            )
            return

    def track_playback(
            self,
            input_deliver
    ) -> str:
        """
        The function plays music files. It checks whether playback
        has been paused; in this case, playback continues from where
        it was stopped. If the function determines that playback of
        a newly downloaded song is required, it is launched using
        the appropriate method.
        """

        if pygame.mixer.music.get_pos() == -1:
            # If the music player has loaded the new track then start playing.
            pygame.mixer.music.play()

        else:
            # Start playing the loaded melody.
            pygame.mixer.music.unpause()

        while pygame.mixer.music.get_busy():
            # Check with the loop if playback has finished.

            # Checking time interval (milliseconds).
            self.pygame_clock.tick(30)

            # Call the input function which the link was passed as a parameter.
            # And assign an inputting result to the variable below.
            text = input_deliver()

            if text or text == '':
                # If a user has inputed anything.

                if pygame.mixer.music.get_busy():
                    # Pause the melody if it is still playing.
                    pygame.mixer.music.pause()

                # Return inputted user data.
                return text

        # If there was no text input from the user until
        # the end of playback then unload this track.
        self.track_stop_unload()

    @staticmethod
    def track_stop_unload() -> None:
        """
        The function stops and unloads a previously downloaded music file.
        """
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def set_guessble_tracks_list(self) -> None:
        """
        Before playing each new melody, the function randomly selects
        the count of track names specified in the settings. Then it
        adds the name of the melody being played to the resulting list
        and shuffles this final list, which serves as a hint for the
        players.
        """
        # Combine tracks for playback with tracks for extras.
        # This array has not a track for playing.
        tracks_except_current = self.tracks_for_round_playback + self.extra_singer_track_tuples

        # Shuffle the resulting array.
        random.shuffle(tracks_except_current)

        # Slice this array to the size specified in the settings,
        # reduced by one, and add a track to it for playback.
        tracks_except_current = (tracks_except_current[: settings.TRACK_LIST_SIZE - 1]
                                 + [self.current_singer_track_tuple])

        # Shuffle this array again so that the track being played
        # is not always the last element of the array.
        random.shuffle(tracks_except_current)

        # Assign the resulting array to the corresponding class attribute.
        self.guessable_tracks_list = tracks_except_current

    def get_guessable_track_titles(self) -> list:
        """
        Form from file names track titles to print.
        """
        return list(map(self.file_name_to_title, self.guessable_tracks_list))

    @staticmethod
    def file_name_to_title(track_tpl: tuple) -> str:
        """
        The function takes a tuple with the name of the artist
        and song and forms a title for printing from this data.
        """
        siger, track_name = map(lambda x: x.replace('_', ' ').title(), track_tpl)
        dot_index = track_name.rfind('.')
        return f'{siger} - {track_name[:dot_index]}'

    def play_fanfare(self) -> None:
        """
        Fanfare playing for the winner. About 7 sec.
        """
        self.preseted_track_loading('fanfares/fanfare7.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            # Check with the loop if playback has finished.

            # Checking time interval.
            self.pygame_clock.tick(30)

        self.track_stop_unload()
