import pymysql

# 获取连接对象conn，建立数据库的连接


def get_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='missions')  # db:表示数据库名称
    return conn


def query(table):
    sql = 'SELECT * FROM ' + table + ';'
    return p_query(sql, None)


def p_query(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, args)
    results = cur.fetchall()
    print(type(results))  # 返回<class 'tuple'> tuple元组类型
    for row in results:
        print(row)
        id = row[0]
        name = row[1]
        age = row[2]
        print('id: ' + str(id) + ' name: ' + name + ' age: ' + str(age))
        pass
    return results
    conn.commit()
    cur.close()
    conn.close()


def insert(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    result = cur.execute(sql, args)
    print(result)
    conn.commit()
    cur.close()
    conn.close()
