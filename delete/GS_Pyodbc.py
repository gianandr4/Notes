import pyodbc, json


def connect():
    try:
        with open('config.json', encoding='utf-8') as cf:
            config = json.load(cf)
    except Exception as e:
        raise e
    config = config['Database_connection_mysql']

    conn = psycopg2.connect(user=config['username'],
                                  password=config['password'],
                                  host=config['host'],
                                  port=config['port'],
                                  database=config['database'])
    print('Connection successful')
    return conn


def writer(conn, dict, table):
    # conn=connect()
    cursor = conn.cursor()
    # item_dict=dict

    placeholders = ', '.join(['?'] * len(dict))
    columns = ', '.join(dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, placeholders)
    print(sql, columns, placeholders)
    cursor.execute(sql, list(dict.values()))
    return sql


def reader(conn, rows, table, filter=''):
    cursor = conn.cursor()
    select_record = '''SELECT {} FROM {} {};'''.format(rows, table, filter)
    # print(select_record)
    cursor.execute(select_record)
    out = []
    for row in cursor.fetchall():
        rowlist = list(row)
        out.append(rowlist)
    return out


