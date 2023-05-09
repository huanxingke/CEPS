# coding=utf8
"""
操作数据库
"""
import sqlite3


def dict_factory(cursor, row):
    """将 sqlite 的返回转换成字典

    :param cursor: sqlite 游标
    :param row: sqlite 行
    :return:
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect(r"./static/chemicals.s3db", check_same_thread=False)
        self.conn.row_factory = dict_factory
        self.c = self.conn.cursor()
        self.tableKeys = {
            "details": ["dangerous_goods_number", "cas_number", "category", "secondary_category", "status", "chemical_id", "name", "enName", "weixianxingleibie", "xiangxingtu", "weixianxingshuoming", "lihuatexing", "zhuyaoyongtu", "ranshaoyubaozhaweixianxing", "huoxingfanying", "jinjiwu", "duxing", "zhongdubiaoxian", "zhiyejiechuxianzhi", "huanjingweihai", "jijiucuoshi", "xielouyingjichuzhi", "miehuofangfa", "ghsType", "ghsjingshici", "critical_quantity"]
        }
        self.create()
        self.c.execute("PRAGMA synchronous = OFF;")

    def select(self, table, key=None, items=None):
        """查

        :param table: 表名
        :param key: 需要查找的字段名
        :param items: 查找条件, 格式为: [(by_key, by_item)...]
        :return:
        """
        if not key:
            sql = '''select * from {}'''.format(table)
        else:
            where = []
            for by_data_key, by_data_value in items:
                where.append('''{}="{}"'''.format(
                    by_data_key.replace('\\', "").replace('"', "'"),
                    by_data_value.replace('\\', "").replace('"', "'")
                ))
            sql = '''select {} from {} where {};'''.format(
                key.replace('\\', "").replace('"', "'"),
                table, " and ".join(where)
            )
        cursor = self.c.execute(sql)
        result = cursor.fetchall()
        return result

    def insert(self, table, data):
        """增

        :param table: 表名
        :param data: 数据
        :return:
        """
        sql = '''insert into %s(%s) values(%s);''' % (
            table,
            ", ".join(self.tableKeys[table]),
            '"' + '", "'.join([str(i).replace('\\', "").replace('"', "'") for i in data]) + '"'
        )
        self.c.execute(sql)
        self.conn.commit()

    def update(self, table, new_items, by_items):
        """改

        :param table: 表名
        :param new_items: 要改的数据, 格式为: [(new_key, new_item)...]
        :param by_items: 查找条件, 格式为: [(by_key, by_item)...]
        :return:
        """
        update = []
        for new_data_key, new_data_value in new_items:
            update.append('''{}="{}"'''.format(
                str(new_data_key).replace('\\', "").replace('"', "'"),
                str(new_data_value).replace('\\', "").replace('"', "'")
            ))
        if by_items:
            where = []
            for by_data_key, by_data_value in by_items:
                where.append('''{}="{}"'''.format(
                    str(by_data_key).replace('\\', "").replace('"', "'"),
                    str(by_data_value).replace('\\', "").replace('"', "'")
                ))
            sql = '''update {} set {} where {};'''.format(table, ", ".join(update), " and ".join(where))
        else:
            sql = '''update {} set {};'''.format(table, ", ".join(update))
        self.c.execute(sql)
        self.conn.commit()

    def add_column(self, table, column_name):
        """增加列

        :param table: 表名
        :param column_name: 列名
        :return:
        """
        sql = f"alter table {table} add {column_name} text"
        self.c.execute(sql)
        self.conn.commit()

    def delete(self, table, by_items):
        """删

        :param table: 表名
        :param by_items: 查找条件, 格式为: [(by_key, by_item)...]
        :return:
        """
        where = []
        for by_data_key, by_data_value in by_items:
            where.append('''{}="{}"'''.format(
                str(by_data_key).replace('\\', "").replace('"', "'"),
                str(by_data_value).replace('\\', "").replace('"', "'")
            ))
        sql = '''delete from {} where {};'''.format(table, " and ".join(where))
        self.c.execute(sql)
        self.conn.commit()

    def create(self):
        """初始化数据库, 建立数据表

        :return:
        """
        try:
            for table, fields in self.tableKeys.items():
                sql = '''create table {} (id INTEGER PRIMARY KEY, {});'''.format(table, ", ".join(
                    [i + " text" for i in fields]))
                self.c.execute(sql)
                self.conn.commit()
        except:
            pass
