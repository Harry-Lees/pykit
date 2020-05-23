import datetime
import time

import progressbar
import yaml

from pyKit import database, format_, leankit

'''
This program will loop through every board in Leankit and upload all data to the database.
The database will be named leankit.db and is stored in the current directory.
'''

with open('config.yaml') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
    path, username, password = config_data.values()

startTime = datetime.datetime.now()

leankit_data = dict()

database.setup_default_schema()
upload = database.Upload()

with leankit.connect(path, username, password) as conn:
    boards = conn.getBoardIDs()

    with progressbar.ProgressBar(max_value = len(boards)) as bar:
        for i, board in enumerate(boards):
            leankit_data = conn.getBoardData(str(board[0]))

            lane_data = format_.format_lanes(leankit_data, database.default_lane_schema())
            upload.lane_data(lane_data)

            card_data = format_.format_cards(leankit_data, database.default_card_schema())
            upload.card_data(card_data)

            board_data = format_.format_boards(leankit_data, database.default_board_schema())
            upload.board_data(board_data)

            tag_data = format_.format_tags(leankit_data, database.default_tag_schema())
            upload.tag_data(tag_data)

            type_data = format_.format_types(leankit_data, database.default_type_schema())
            upload.type_data(type_data)

            custom_id_data = format_.format_custom_id(leankit_data, database.default_custom_id_schema())
            upload.custom_id_data(custom_id_data)

            bar.update(i)

endTime = datetime.datetime.now()

print('all boards complete')
print(f'runtime: {endTime - startTime}')
