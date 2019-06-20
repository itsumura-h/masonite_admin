"""
FIELD_TYPE = {
    '0': 'DECIMAL',
    '1': 'TINY',
    '2': 'SHORT',
    '3': 'LONG',
    '4': 'FLOAT',
    '5': 'DOUBLE',
    '6': 'NULL',
    '7': 'TIMESTAMP',
    '8': 'LONGLONG',
    '9':'INT24',
    '10': 'DATE',
    '11': 'TIME',
    '12': 'DATETIME',
    '13': 'YEAR',
    '14': 'NEWDATE',
    '15': 'VARCHAR',
    '16': 'BIT',
    '245': 'JSON',
    '246': 'NEWDECIMAL',
    '247': 'ENUM',
    '248': 'SET',
    '249': 'TINY_BLOB',
    '250': 'MEDIUM_BLOB',
    '251': 'LONG_BLOB',
    '252': 'BLOB',
    '253': 'VAR_STRING',
    '254': 'STRING',
    '255': 'GEOMETRY',

    #CHAR = TINY ',
    #INTERVAL = ENUM ',
}
"""
# https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/constants/FIELD_TYPE.py



MYSQL_FIELD_TYPE = {
    '1': 'TINYINT',
    '2': 'INTEGER',
    '3': 'INTEGER',
    '5': 'FLOAT',
    '7': 'TIMESTAMP',
    '8': 'INTEGER',
    '9': 'INTEGER',
    '10': 'DATE',
    '11': 'TIME',
    '12': 'DATETIME',
    '245': 'TEXT',
    '246': 'NUMERIC',
    '252': 'TEXT',
    '253': 'VARCHAR',
    '254': 'STRING',
    '255': 'GEOMETRY',

    #CHAR = TINY ',
    #INTERVAL = ENUM ',
}

PGSQL_FIELD_TYPE = {
    'integer': 'INTEGER',
    'bigint': 'INTEGER',
    'bytea': 'BLOB',
    'boolean': 'TINYINT',
    'character': 'VARCHAR',
    'date': 'DATE',
    'timestamp': 'DATETIME',
    'numeric': 'NUMERIC',
    'double': 'FLOAT',
    'json': 'json',
    'text': 'TEXT',
    'smallint': 'INTEGER',
    'time': 'TIME',
    'timestamp': 'DATETIME'
}