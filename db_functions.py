import sqlite3, config

connection = sqlite3.connect(config.db_file, check_same_thread=False)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

"""""
    Accounts
"""""
def init_user(tg_id, tg_username):
    cursor = connection.cursor()
    query = f"INSERT INTO `accounts`(`tg_id`, `tg_username`, `status`) VALUES('{tg_id}', '{tg_username}', '-1')"
    cursor.execute(query)

    connection.commit()

def set_value(table_name, tg_id, column, value):
    cursor = connection.cursor()
    query = f"UPDATE `{table_name}` SET `{column}`='{value}' WHERE `tg_id`='{tg_id}'"
    cursor.execute(query)

    connection.commit()

def select_where(table_name, field, param):
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name} WHERE `{field}` = '{param}'"
    cursor.execute(query)
    return cursor.fetchall()

def select_param(table_name, tg_id, param):
    cursor = connection.cursor()
    query = f"SELECT `{param}` FROM `{table_name}` WHERE `tg_id`='{tg_id}'"
    cursor.execute(query)
    return cursor.fetchone()[param]

def select_param_account(tg_id, param):
    cursor = connection.cursor()
    query = f"SELECT `{param}` FROM `accounts` WHERE `tg_id`='{tg_id}'"
    cursor.execute(query)
    return cursor.fetchone()

"""""
    Referal 
"""""
def init_referal(from_id, to_id):
    cursor = connection.cursor()
    query = f"INSERT INTO `referals`(`from_id`, `to_id`) VALUES('{from_id}', '{to_id}')"
    cursor.execute(query)
    connection.commit()