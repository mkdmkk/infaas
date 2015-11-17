__author__ = 'mkk'

import pymysql

connection = pymysql.connect(host='203.253.23.37',
                             user='ssel',
                             password='ssel0909',
                             db='mhealth',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "select * from `Context` as c left join `ContextData` as d on c.context_id=d.context_id where 'user_id'=%s and 'type'=%s order by c.time desc"
        cursor.execute(sql, ('mkkim', 'ecg'))
        result = cursor.fetch()
        print(result)
finally:
    connection.close()