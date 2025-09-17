import game_screen

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 750

TOTAL_LEVEL = 6
CURRENT_LEVEL = 1

SETTLEMENT_SCREEN = False   #结算界面
GAME_SCREEN = False  #游戏界面
START_SCREEN = True    #开始界面
SELECT_SCREEN = False   #关卡选择界面

FAILURE = False
SUCCESS = False
RUNNING = True

GAMES = dict()

def games_init():
    global GAMES
    GAMES = {
        'level1': game_screen.Game('map1'),
        'level2': game_screen.Game('map2'),
        'level3': game_screen.Game('map3'),
        'level4': game_screen.Game('map4'),
        'level5': game_screen.Game('map5'),
        'level6': game_screen.Game('map6')
    }

def level_reset():
    global CURRENT_LEVEL

def next_level():
    global CURRENT_LEVEL
    CURRENT_LEVEL += 1

def stop_game():
    global RUNNING
    RUNNING = False

def switch_to_settlement():
    global SETTLEMENT_SCREEN
    global GAME_SCREEN
    global START_SCREEN
    global SELECT_SCREEN
    global SUCCESS

    GAME_SCREEN = False
    START_SCREEN = False
    SETTLEMENT_SCREEN = True
    SELECT_SCREEN = False
    SUCCESS = False

def game_start(level):
    global SETTLEMENT_SCREEN
    global GAME_SCREEN
    global START_SCREEN
    global SELECT_SCREEN
    global SUCCESS
    global FAILURE

    GAME_SCREEN = True
    START_SCREEN = False
    SETTLEMENT_SCREEN = False
    SELECT_SCREEN = False
    FAILURE = False
    SUCCESS = False

    global CURRENT_LEVEL
    CURRENT_LEVEL = level

def switch_to_startscreen():
    global SETTLEMENT_SCREEN
    global GAME_SCREEN
    global START_SCREEN
    global SELECT_SCREEN
    global SUCCESS
    global FAILURE

    GAME_SCREEN = False
    START_SCREEN = True
    SETTLEMENT_SCREEN = False
    SELECT_SCREEN = False
    FAILURE = False
    SUCCESS = False

def switch_to_selectscreen():
    global SETTLEMENT_SCREEN
    global GAME_SCREEN
    global START_SCREEN
    global SELECT_SCREEN
    global SUCCESS
    global FAILURE

    GAME_SCREEN = False
    START_SCREEN = False
    SETTLEMENT_SCREEN = False
    SELECT_SCREEN = True
    FAILURE = False
    SUCCESS = False

def success_or_fail(result):
    global SETTLEMENT_SCREEN
    global GAME_SCREEN
    global START_SCREEN
    global SUCCESS
    global FAILURE

    SUCCESS = True if result == 'success' else False
    FAILURE = True if result == 'failure' else False

