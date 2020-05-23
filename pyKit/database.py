import sqlite3

__author__ = 'Harry Lees'
__version__ = '1.0'

def setup_default_schema():

    create_card_table =   """
                        CREATE TABLE IF NOT EXISTS card(
                            'id' TEXT,
                            'version' INTEGER,
                            'title' TEXT,
                            'priority' TEXT,
                            'size' INTEGER,
                            'planned_start' TEXT,
                            'planned_finish' TEXT,
                            'actual_finish' TEXT,
                            'actual_start' TEXT,
                            'created_on' TEXT,
                            'archived_on' TEXT,
                            'updated_on' TEXT,
                            'moved_on' TEXT,
                            'tag_id' INTEGER,
                            'board_id' TEXT,
                            'custom_id' TEXT,
                            'lane_id' TEXT,
                            'type_id' TEXT,
                            PRIMARY KEY(id),
                            FOREIGN KEY(tag_id) REFERENCES tag(id),
                            FOREIGN KEY(board_id) REFERENCES board(id),
                            FOREIGN KEY(custom_id) REFERENCES custom_id(header),
                            FOREIGN KEY(lane_id) REFERENCES lane(id),
                            FOREIGN KEY(type_id) REFERENCES type(id)
                        )
                        """

    create_board_table =  """
                        CREATE TABLE IF NOT EXISTS board(
                            'id' TEXT,
                            'title' TEXT,
                            'version TEXT',
                            'is_archived TEXT',
                            PRIMARY KEY(id)
                        )
                        """

    create_lane_table =   '''
                        CREATE TABLE IF NOT EXISTS lane(
                            'card_limit' INTEGER,
                            'id' INTEGER,
                            'lane_class_type' TEXT,
                            'lane_type' TEXT,
                            'title' TEXT,
                            PRIMARY KEY(id)
                        )
                        '''

    create_type_table =   '''
                        CREATE TABLE IF NOT EXISTS type(
                            'id' TEXT,
                            'title' TEXT,
                            PRIMARY KEY(id)
                        )
                        '''

    create_custom_ids_table =  '''
                            CREATE TABLE IF NOT EXISTS custom_id(
                                'value' TEXT,
                                'prefix' TEXT,
                                'url' TEXT,
                                PRIMARY KEY(value)
                            )
                            '''

    create_tag_table =    '''
                        CREATE TABLE IF NOT EXISTS tag(
                            'card_id' TEXT,
                            'tag' TEXT,
                            PRIMARY KEY(card_id, tag),
                            FOREIGN KEY(card_id) REFERENCES card(id)
                        )
                        '''

    tables = [create_card_table, create_board_table, create_lane_table, create_type_table, create_custom_ids_table, create_tag_table]
    
    with sqlite3.connect('leankit.db') as connection:
        for table in tables:
            connection.execute(table)
        
    return

def default_card_schema():
    return ['id', 'version', 'title', 'priority', 'size', 'plannedStart', 'plannedFinish', 'actualFinish', 'actualStart', 'createdOn', 'archivedOn', 'updatedOn', 'movedOn', 'tagID', 'boardID', 'customID', 'laneID', 'typeID']

def default_board_schema():
    return ['id', 'title', 'version', 'isArchived']

def default_lane_schema():
    return ['cardLimit', 'id', 'laneClassType', 'laneType', 'title']

def default_type_schema():
    return ['id', 'title']

def default_custom_id_schema():
    return ['value', 'prefix', 'url']

def default_tag_schema():
    return ['cardID', 'tag']

class Upload:
    def __init__(self, database = 'leankit.db'):
        self.database = database
    
    def __commit(self, template, data):
        try:         
            with sqlite3.connect(self.database) as connection:
                connection.executemany(template, data)
        except Exception as e:
            print(template)
            raise Exception(f'failed to commit to database - {e}')
        return
    
    def card_data(self, card_data, table_name = 'card'):
        template = f'INSERT OR REPLACE INTO {table_name} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.__commit(template, card_data)
            
    def lane_data(self, lane_data, table_name = 'lane'):
        template = f'INSERT OR REPLACE INTO {table_name} VALUES(?, ?, ?, ?, ?)'
        self.__commit(template, lane_data)

    def board_data(self, board_data, table_name = 'board'):
        template = f'INSERT OR REPLACE INTO {table_name} VALUES(?, ?, ?, ?)'
        self.__commit(template, board_data)
        
    def tag_data(self, tag_data, table_name = 'tag'):
        template = f'INSERT OR REPLACE INTO {table_name} VALUES(?, ?)'
        self.__commit(template, tag_data)
        
    def type_data(self, type_data, table_name = 'type'):
        template = f'INSERT OR REPLACE INTO {table_name} VALUES(?, ?)'
        self.__commit(template, type_data)
            
    def custom_id_data(self, custom_id_data, table_name = 'custom_id'):
        template = f'INSERT OR REPLACE INTO {table_name} VALUES(?, ?, ?)'
        self.__commit(template, custom_id_data)
