import sqlite3


def insert_charts(connection, song_id, name, rating_pst, rating_prs, rating_ftr, rating_byn, rating_etr):
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO charts (song_id, name, rating_pst, rating_prs, rating_ftr, rating_byn, rating_etr) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (song_id, name, rating_pst, rating_prs, rating_ftr, rating_byn, rating_etr))
    connection.commit()


def db_charts(slst):
    # 连接到SQLite数据库文件，如果不存在则创建
    connection = sqlite3.connect('new_database.db')

    # 创建表格（如果不存在）
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS charts (
                song_id TEXT,
                name TEXT,
                rating_pst INTEGER,
                rating_prs INTEGER,
                rating_ftr INTEGER,
                rating_byn INTEGER,
                rating_etr INTEGER
            )
        ''')
    connection.commit()

    for song in slst["songs"]:
        # 从用户输入获取数据
        song_id = song["id"]
        diff = song["difficulties"]
        name = song["title_localized"]["en"]

        rating_pst, rating_prs, rating_ftr, rating_byn, rating_etr = 0, 0, 0, 0, 0

        if int(diff[0]["rating"]) == -1:
            rating_pst = -1
        if int(diff[1]["rating"]) == -1:
            rating_prs = -1
        if int(diff[2]["rating"]) <= 0:
            rating_ftr = -1
        try:
            if int(diff[3]["rating"]) <= 0:
                rating_byn = -1
        except Exception:
            rating_byn = -1

        try:
            if int(diff[4]["rating"]) <= 0:
                rating_etr = -1
        except Exception:
            rating_etr = -1

        # print(rating_pst, rating_prs, rating_ftr, rating_byn, rating_etr)
        # input()
        # 将数据插入表格
        insert_charts(connection, song_id, name, rating_pst, rating_prs, rating_ftr, rating_byn, rating_etr)

    # 关闭数据库连接
    connection.close()


def insert_items(connection, item_id, datatype, is_available):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO items (item_id, type, is_available) VALUES (?, ?, ?)',
                   (item_id, datatype, is_available))
    connection.commit()


def db_items(slst, plst):
    # 连接到SQLite数据库文件，如果不存在则创建
    connection = sqlite3.connect('new_database.db')

    # 创建表格（如果不存在）
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                item_id TEXT,
                type TEXT,
                is_available INTEGER
            )
        ''')
    connection.commit()

    for pack in plst["packs"]:
        # 从用户输入获取数据
        item_id = pack["id"]
        datatype = "pack"
        is_available = 1

        # 将数据插入表格
        insert_items(connection, item_id, datatype, is_available)

    for song in slst["songs"]:
        # 从用户输入获取数据
        song_id = song["id"]
        diff = song["difficulties"]
        if int(diff[2]["rating"]) == -2:
            item_id = song_id
            datatype = "single"
            is_available = 1
            insert_items(connection, item_id, datatype, is_available)

    # 关闭数据库连接
    connection.close()
