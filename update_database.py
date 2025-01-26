import sqlite3
"""
songlist导出服务器数据库chart表
"""


def connect_to_databases(database_a, database_b):
    connection_a = sqlite3.connect(database_a)
    connection_b = sqlite3.connect(database_b)
    return connection_a, connection_b


def fetch_data(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    return cursor.fetchall()


def update_data(connection, table_name, id_column, id_value, update_column, update_value):
    cursor = connection.cursor()
    cursor.execute(f'UPDATE {table_name} SET {update_column} = ? WHERE {id_column} = ?', (update_value, id_value))
    connection.commit()


def update_db(database_a, database_b, table_a, table_b, id_column):
    connection_a, connection_b = connect_to_databases(database_a, database_b)

    data_a = fetch_data(connection_a, table_a)
    data_b = fetch_data(connection_b, table_b)

    for row in range(2, 7):
        if row == 2:
            update_column = 'rating_pst'
        elif row == 3:
            update_column = 'rating_prs'
        elif row == 4:
            update_column = 'rating_ftr'
        elif row == 5:
            update_column = 'rating_byn'
        else:
            update_column = 'rating_etr'
        for row_b in data_b:
            id_value_b = row_b[0]  # Assuming id is the first column
            update_value = row_b[row]  # Getting index of update_column from first row

            for row_a in data_a:
                id_value_a = row_a[0]  # Assuming id is the first column

                if id_value_a == id_value_b:
                    update_data(connection_a, table_a, id_column, id_value_a, update_column, update_value)
                    break

    connection_a.close()
    connection_b.close()


if __name__ == '__main__':
    update_db('new_database.db', 'arcaea_database.db', 'charts', 'chart', 'song_id')
