import pyodbc


def connect():
    conn = pyodbc.connect('Driver={MySQL ODBC 8.0 Unicode Driver};'
                          'Server=157.90.175.64;'
                          'UID=lalakisss;'
                          'PWD=lalakis;'
                          'DATABASE=laravel;')
    print('Connection successful')
    return conn


def writer(conn, item_dict, table):
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(item_dict))
    columns = ', '.join(item_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, placeholders)
    print('Inserting: ', list(item_dict.values()))
    cursor.execute(sql, list(item_dict.values()))


def reader(conn, table, filter=''):
    cursor = conn.cursor()
    select_record = '''SELECT id FROM ''' + table + ' ' + filter + ';'
    cursor.execute(select_record)
    out = []
    for row in cursor:
        rowlist = list(row)
        out.append(rowlist)
    return out


# Connect
conn = connect()

# Write from dict
writer(conn=conn, table='google_authors', item_dict=author_dict)

# commit action
conn.commit()


# Read convert to list
publications_list = reader(conn=conn, table='google_publications')

conn.close()
del conn
