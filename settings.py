PLAYERS_MIN_COUNT = 2
PLAYERS_MAX_COUNT = 20
ATTENTION_TIME = 2
TRACK_LIST_SIZE = 10
WIN_POINT = 3
ORDER_QUIT = 'quit'
ORDER_STOP = 'stop'
ORDER_NEXT_MELODY = 'next'
ORDER_CONTINUE_GAME = 'continue'
ORDER_NEW_ROUND = 'round'
ORDER_NEW_POOL = 'new'

player_registration_text = f'Please registr all the players. Input “{ORDER_STOP}” to finish registration.'
allowed_name_notice = 'Use only letters (at least 1) and characters of space and dash.'
use_letters_text = 'Please use only letters and characters of space and dash.'
wrong_players_count_text = f'The players count must be from {PLAYERS_MIN_COUNT} to {PLAYERS_MAX_COUNT}.'
tap_to_game_starting_text = 'Input whatever to START THE GAME or input “quit” to finish the game'
stop_melody_text = '••• If anyone guess this melody press ENTER •••: '
player_already_answered_text = 'This player already answered, please input another player'
wrong_player_number_text = 'The wrong player number. Please input another number'
melody_already_named_text = 'This melody already named, please input another melody'
wrong_melody_number_text = 'The wrong melody number. Please input another number'
input_numbers_only_text = 'Please input numbers only.'
players_have_0_text = 'ALL PLAYERS HAVE 0 POINTS'
exclusion_title = ['[x] EXCLUDED MELODIES', '[x] EXCLUDED PLAYERS']
positive_scores_title = ['PLAYER NUMBER', 'PLAYER NAME', 'PLAYER SCORES']
no_one_guessed_text = '[x] Unfortunately no one guessed this melody, so we are starting the next one.'
need_new_pool_text = 'Input your choice'
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
    'round is over.',
    '',
    f'input “{ORDER_NEW_POOL}”'.ljust(22) + '- to start a new game with a new players pool',
    'input whatever'.ljust(22) + '- to start a new game with the previouse players pool',
    'input “quit”'.ljust(22) + '- to finish'
]

signboard = [
    "   _____                       _______ _            __  __      _           _       ",
    "  / ____|                     |__   __| |          |  \\/  |    | |         | |      ",
    " | |  __ _   _  ___  ___ ___     | |  | |__   ___  | \\  / | ___| | ___   __| |_   _ ",
    " | | |_ | | | |/ _ \\/ __/ __|    | |  | '_ \\ / _ \\ | |\\/| |/ _ \\ |/ _ \\ / _` | | | |",
    " | |__| | |_| |  __/\\__ \\__ \\    | |  | | | |  __/ | |  | |  __/ | (_) | (_| | |_| |",
    "  \\_____|\\__,_|\\___||___/___/    |_|  |_| |_|\\___| |_|  |_|\\___|_|\\___/ \\__,_|\\__, |",
    "                                                                               __/ |",
    "                                                                              |___/ "
]

rule_text = [
    'THE RULE of the GUESS THE MELODY game',
    '',
    f'From {PLAYERS_MIN_COUNT} to {PLAYERS_MAX_COUNT} people',
    'take part in the game. When the game starts, you will hear a melody.',
    'If you guessed what it is playing, then press the ENTER key or any',
    'symbols and ENTER.',
    '',
    'After stopping the melody, you need to enter the number of the player',
    'who will answer, and then the number of the melody name. Variants of names,',
    'of which only one is correct, will be on the screen while the song is playing.',
    '',
    'If the answer was correct, then the player gets 1 point. If the answer is',
    'not correct, then the melody will continue to sound again until one of the',
    'players stops it again. Each player has only one attempt to answer each melody.',
    '',
    'If the song ends and remains unguessed by anyone, then no points are awarded',
    'to anyone, in this case the next random song will begin.',
    '',
    f'To stop a song early and move on to the next one, enter the word “{ORDER_NEXT_MELODY}”.',
    f'The game continues until {WIN_POINT} points.',
    f'To quit the game, enter the word “{ORDER_QUIT}” at any time.',
    '',
    'To stop the song to guess it, you can give each player access to independently',
    'press the ENTER key or assign a manager who will stop the song by any player',
    'shouting “STOP”.',
    '',
    'Based on the TV show of the same name.'
]
