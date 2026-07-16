import json
import os

SEQUENCE = ["Big", "Small", "Small", "Big", "Big", "Big", "Small", "Small", "Small", "Small"]
LEVEL_FILE = 'level.json'

def get_level():
    if os.path.exists(LEVEL_FILE):
        with open(LEVEL_FILE, 'r') as f:
            return json.load(f).get('level', 0)
    return 0

def save_level(level):
    with open(LEVEL_FILE, 'w') as f:
        json.dump({'level': level}, f)

def reset_level():
    save_level(0)

def get_prediction(game='30S'):
    level = get_level()
    return {
        'prediction': SEQUENCE[level],
        'level': level + 1,
        'max_level': len(SEQUENCE),
        'game': game
    }

def handle_result(is_win):
    if is_win:
        reset_level()
    else:
        current = get_level()
        if current < len(SEQUENCE) - 1:
            save_level(current + 1)
        else:
            reset_level()