import pyodbc


def connect():
    conn = pyodbc.connect('Driver={MySQL ODBC 8.0 Unicode Driver};'
                          'Server=157.90.175.64;'
                          'UID=lalakisss;'
                          'PWD=lalakis;'
                          'DATABASE=laravel;')
    print('Connection successful')
    return conn

item = {'name':'asda'
        'gold':'1000'
}

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

   # def deleter(conn,table='T_Items', filter = ''):
   #      cursor_read=conn.cursor()
   #      cursor_delete=conn.cursor()
   #
   #      # READ
   #      print('THE FOLLOWING RECORDS WILL BE DELETED')
   #      select_record = '''SELECT * FROM ''' + table + ' '+ filter+ ' ORDER BY Item_ID'
   #      cursor_read.execute(select_record)
   #      for i in cursor_read:
   #          print(i[-1],i[0], i[-4])
   #
   #      sure=input('Type yes to delete ')
   #      if sure.lower()=='yes':
   #          print('deleting')
   #          delete_query = '''DELETE FROM '''+table+' '+filter
   #          print(delete_query)
   #          cursor_delete.execute(delete_query )
   #          print('executed')
   #          conn.commit()
   #          print('comitted')

# Connect
import 1_DATABASES AS A

conn = A.connect()

# Write from dict
writer(conn=conn, table='google_authors', item_dict=author_dict)

# commit action
conn.commit()


# Read convert to list
publications_list = reader(conn=conn, table='google_publications')

conn.close()
del conn
