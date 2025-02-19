from orm import LikersModel
import json

likers = LikersModel()
INPUT_FILE = "likers_input.txt"
source_target = 'eloi'
post_id = ''

with open(INPUT_FILE, 'r', encoding='utf-8') as file:
    fmt_text = json.loads(file.read())
    insertion_list = []
    for user in fmt_text['users']:
        insertion_list.append((
            user['username'],
            user['full_name'],
            user['is_private'],
            source_target,
            post_id
        ))
    likers.insert_many(insertion_list)
