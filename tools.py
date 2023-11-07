QUIT_WORD = 'quit'
STOP_WORD = 'stop'
NEXT_MELODY_TEXT = 'next'
CONTINUE_GAME_TEXT = 'continue'
NEW_ROUND_TEXT = 'round'
NEW_POOL_TEXT = 'new'
ATTENTION_TIME = 2
TRACK_LIST_SIZE = 10
WIN_POINT = 3

player_registration_text = 'Please registr all the players. Input “stop” to finish registration.'
allowed_name_notice = 'Use only letters (at least 1) and characters of space and dash.'
use_letters_text = 'Please use only letters and characters of space and dash.'
tap_to_game_starting_text = 'Input whatever to START THE GAME or input “quit” to finish the game'
stop_melodie_text = '🎵 🎶 If anyone guess this melody press ENTER 🎵 🎶: '
player_already_answered_text = 'This player already answered, please input another player'
wrong_player_number_text = 'The wrong player number. Please input another number'
melodie_already_named_text = 'This melodie already named, please input another melody'
wrong_melodie_number_text = 'The wrong melodie number. Please input another number'
input_numbers_only_text = 'Please input numbers only.'
players_have_0_text = 'ALL PLAYERS HAVE 0 POINTS'
exclusion_title = ['[✕] EXCLUDED MELODIES', '[✕] EXCLUDED PLAYERS']
positive_scores_title = ['PLAYER NUMBER', 'PLAYER NAME', 'PLAYER SCORES']
no_one_guessed_text = 'Unfortunately no one guessed this melodie, so we are starting the next one.'
need_new_pool_text = 'Input your choice: '
win_message = 'won! :)'
game_over_text = 'THE GAME IS OVER'

player_greeting_text_array = [
    'Welcom to the game',
    'Your number is',
    'remember it.'
]

players_registered_text = [
    'ALL',
    'PLAYERS HAVE BEEN SUCCESSFULLY REGISTERED'
]

player_track_number_text = [
    'Input the answering player number: ',
    'Input the playing melody number: '
]
congratulation_text = [
    ':) Well done',
    'it is the correct answer!'
]
not_guessed_text = [
    ':( Sorry',
    'but it is not a correct answer!'
]

this_round_over_text = [
    '',
    'This round is over.',
    '',
    f'input “{NEW_POOL_TEXT}”'.ljust(22) + '- to start a new game with a new players pool',
    'input whatever'.ljust(22) + '- to start a new game with the previouse players pool',
    'input “quit”'.ljust(22) + '- to finish'
]

signboard = [
    "   ____                      _____ _            __  __      _           _ _      ",
    "  / ___|_   _  ___ ___ ___  |_   _| |__   ___  |  \\/  | ___| | ___   __| (_) ___ ",
    " | |  _| | | |/ _ / __/ __|   | | | '_ \\ / _ \\ | |\\/| |/ _ | |/ _ \\ / _` | |/ _ \\",
    " | |_| | |_| |  __\\__ \\__ \\   | | | | | |  __/ | |  | |  __| | (_) | (_| | |  __/",
    "  \\____|\\__,_|\\___|___|___/   |_| |_| |_|\\___| |_|  |_|\\___|_|\\___/ \\__,_|_|\\___|"
]

rule_text = [
    'THE RULE of the GUESS THE MELODY game',
    '',
    'From 1 to 20 people take part in the game. When the game starts, you',
    'will hear a melody. If you guessed what it is called, then press the',
    'ENTER key or any symbols and ENTER.',
    '',
    'After stopping the melody, you need to enter the amount of the player',
    'who will answer, and then the amount the name of the melody. Variants',
    'of names, of which only one is correct, will be on the screen while the',
    'song is playing.',
    '',
    'If the answer was correct, then the player gets 1 point. If the answer',
    'is not correct, then the melody will continue to sound again until one',
    'of the players stops it again. Each player has only one attempt to answer',
    'each melody. If the song ends and remains unguessed by anyone, then no',
    'points are awarded to anyone, in this case the next random song will begin.',
    '',
    f'To stop a song early and move on to the next one, enter the word "{NEXT_MELODY_TEXT}".',
    f'The game continues until 3 points. To exit the game, enter the word "{QUIT_WORD}"',
    'at any time. To stop the song, you can give each player access to independently',
    'press the ENTER key or assign a manager who will stop the song by shouting “STOP”.',
    '',
    'Based on the TV show of the same name.'
]


def format_key_text(text: str) -> str:
    return text.strip(" '\"").lower()
