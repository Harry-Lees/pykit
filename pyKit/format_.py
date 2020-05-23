import json
import re
import logging

import dateutil.parser

'''
This file contains functions for formatting the Leankit API data for the predefined database for this package.
Formatting includes escaping illegal characters and removing duplicates from any ticket.
'''

__author__ = 'Harry Lees'
__version__ = '1.0'

def format_lanes(leankit_data, table_schema):
    formatted_lane_data = []

    try:
        lane_data = set([json.dumps(card['lane']) for card in leankit_data['cards']])    
        temp = [json.loads(lane) for lane in lane_data]
        
        for index, _ in enumerate(temp):
            formatted_lane_data.append([temp[index][item] for item in table_schema])

    except KeyError as error:
        logging.warning(f'{error} in format_lanes, database data may now be corrupt')

    return formatted_lane_data

def format_cards(leankit_data, table_schema):
    formatted_card_data = []
    
    try:
        for card in leankit_data['cards']:
            formatted_card_data.append([
                                        card['lane']['id'] if item == 'laneID' 
                                        else card['board']['id'] if item == 'boardID'
                                        else card['type']['id'] if item == 'typeID'
                                        else card['customId']['value'] if item == 'customID'
                                        else None if item in ('tagID', 'null', None)
                                        else re.sub(',|;|"|\'', '', card[item]) if item == 'title' # escaping all characters that might interfear with the database
                                        else card[item] for item in table_schema
                                    ])
    
    except KeyError as error:
        logging.warning(f'{error} in format_cards, database data may now be corrupt')

    return formatted_card_data

def format_boards(leankit_data, table_schema):
    formatted_board_data = []

    try:
        board_data = set([json.dumps(card['board']) for card in leankit_data['cards']])    
        temp = [json.loads(board) for board in board_data]
        
        for index, _ in enumerate(temp):
            formatted_board_data.append([temp[index][item] for item in table_schema])
    
    except KeyError as error:
        logging.warning(f'{error} in format_boards, database data may now be corrupt')

    return formatted_board_data

def format_tags(leankit_data, table_schema):
    formatted_tag_data = []
    
    try:
        for card in leankit_data['cards']:
            formatted_tag_data += [(card['id'], card['tags'][index]) for index, _ in enumerate(card['tags']) if card['tags']]
    
    except KeyError as error:
        logging.warning(f'{error} in format_tags, database data may now be corrupt')

    return formatted_tag_data

def format_types(leankit_data, table_schema):
    temp = []
    
    try:
        for card in leankit_data['cards']:
            temp.append([card['type'][item] for item in table_schema])

        formatted_type_data = tuple(tuple(item) for item in temp)

    except KeyError as error:
        logging.warning(f'{error} in format_types, database data may now be corrupt')

    return set(formatted_type_data)

def format_custom_id(leankit_data, table_schema):
    formatted_custom_id = []
    
    try:
        for card in leankit_data['cards']:
            if card['customId']:
                formatted_custom_id.append([card['customId'][item] for item in table_schema])
    
    except KeyError as error:
        logging.warning(f'{error} in format_custom_id, database data may now be corrupt')

    return formatted_custom_id