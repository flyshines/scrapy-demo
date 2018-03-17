# -*- coding: utf-8 -*-

import MySQLdb
from miao import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_DB = settings.MYSQL_DB

db = MySQLdb.connect(host=MYSQL_HOSTS,user=MYSQL_USER,passwd=MYSQL_PASSWORD,db=MYSQL_DB,port=3306,charset='utf8')
cur = db.cursor()


class Sql:

    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        sql = 'insert into dd_name (`xs_name`,`xs_author`,`category`,`name_id`) values (%(xs_name)s, %(xs_author)s, %(category)s,%(name_id)s)'
        value = {
            'xs_name': xs_name,
            'xs_author': xs_author,
            'category': category,
            'name_id': name_id
        }
        cur.execute(sql, value)
        db.commit()

    @classmethod
    def select_name(cls, name_id):
        sql = 'select count(*) from dd_name where name_id = %(name_id)s'
        value = {
            'name_id': name_id
        }
        cur.execute(sql, value)
        tuple_list = cur.fetchall()
        return tuple_list[0]

# 测试代码
#Sql.insert_dd_name('1','2','4',4)
# print Sql.select_name(4)
