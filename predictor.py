import json
import os

SEQUENCE = ["Big", "Small", "Small", "Big", "Big", "Big", "Small", "Small", "Small", "Small"]

def get_level_file(game):
    return f'level_{game}.json'

def get_level(game='30S'):
    file = get_level_file(game)
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f).get('level', 0)
    return 0

def save_level(level, game='30S'):
    file = get_level_file(game)
    with open(file, 'w') as f:
        json.dump({'level': level}, f)

def reset_level(game='30S'):
    save_level(0, game)

def get_prediction(game='30S'):
    level = get_level(game)
    return {
        'prediction': SEQUENCE[level],
        'level': level + 1,
        'max_level': len(SEQUENCE),
        'game': game
    }

def handle_result(is_win, game='30S'):
    if is_win:
        reset_level(game)
    else:
        current = get_level(game)
        if current < len(SEQUENCE) - 1:
            save_level(current + 1, game)
        else:
            reset_level(game)