# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3


class IpPoolPipeline(object):
    count = 0
    def process_item(self, item, spider):
        IpPoolPipeline.count += 1
        self.db.execute(f"INSERT INTO ALL_IP VALUES ("
                        f"'{item['ip']}',"
                        f"'{item['port']}',"
                        f"'{item['ip_location']}',"
                        f"'{item['is_high_anonymous']}',"
                        f"'{item['ip_type']}',"
                        f"'{item['ip_server']}')"
                        f"")
        if IpPoolPipeline.count == 100:
            self.db.commit()
            IpPoolPipeline.count = 0
        # self.db.commit()
        return item

    def __init__(self):
        db_path = ".\\IP_POOL.db"
        if not os.path.exists(db_path):
            self.db = sqlite3.connect(db_path)
            self.__createTable()
        self.db = sqlite3.connect(db_path, check_same_thread=False)

    def __createTable(self):
        """
        数据库建表
        :return:
        """
        self.db.execute("CREATE TABLE ALL_IP ("
                        "IP CHAR,"
                        "port CHAR,"
                        "SERVER_LOCATION CHAR,"
                        "IS_HIGH_ANONYMOUS CHAR,"
                        "IP_TYPE CHAR,"
                        "IP_SERVER CHAR)")
        self.db.commit()