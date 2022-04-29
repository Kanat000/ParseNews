import sqlite3


class Sqlite:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def create_resource_table(self):
        self.cur.execute('Create Table if not exists resource('
                         'resource_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,'
                         'resource_name varchar(255),'
                         'resource_url varchar(255),'
                         'top_tag varchar(255),'
                         'bottom_tag varchar(255),'
                         'title_cut varchar(255),'
                         'date_cut varchar(255)'
                         ')'
                         )

    def create_items_table(self):
        self.cur.execute('Create Table if not exists items('
                         'id integer PRIMARY KEY AUTOINCREMENT NOT NULL,'
                         'res_id integer,'
                         'link varchar(255),'
                         'title Text,'
                         'content Text,'
                         'nd_date integer(11),'
                         's_date integer(11),'
                         'not_date date,'
                         'foreign key(res_id) references resource(resource_id)'
                         ')'
                         )

    def insert_resource(self, resource_name, resource_url, top_tag, bottom_tag, title_cut, date_cut):
        print(self.conn)
        self.cur.execute('Insert into resource(resource_name, resource_url, top_tag, bottom_tag, title_cut, date_cut) '
                         'values (?,?,?,?,?,?);',
                         (resource_name, resource_url, top_tag, bottom_tag, title_cut, date_cut))
        self.conn.commit()

    def insert_items(self, res_id, link, title, content, nd_date, s_date, not_date):
        self.cur.execute('Insert into items(res_id, link, title, content, nd_date, s_date, not_date) '
                         'values (?,?,?,?,?,?,?);', (res_id, link, title, content, nd_date, s_date, not_date))
        self.conn.commit()

    def exists_resource(self, res_url):
        self.cur.execute(f"Select count(*) from resource where resource_url = '{res_url}'")
        return self.cur.fetchone()[0] > 0

    def get_resource(self, resource_url):
        self.cur.execute(f"Select * from resource where resource_url = '{resource_url}'")
        return self.cur.fetchone()

    def exists_item(self, link):
        self.cur.execute(f"Select count(*) from items where link='{link}'")
        return self.cur.fetchone()[0] > 0

    def close(self):
        self.cur.close()
        self.conn.close()
