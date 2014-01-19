#-*- coding: utf-8 -*-
__author__ = "Feng-Ming Lin (Taiwan)"
__copyright__ = "Copyright 2013"
__credits__ = ['Feng-Ming Lin',]
__license__ = "LGPL"
__version__ = "0.1.1"
__maintainer__ = "Feng-Ming Lin"
__email__ = "fabianwind@hotmail.com"
__status__ = "Developing"

import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError

class KVManager(object):

    def __init(self):
        self.__con = sqlite3.connect(self.__db_path)
        self.__cur = self.__con.cursor()

    def __close(self):
        self.__cur.close()
        self.__con.close()

    def __init__(self, db_path, c1='function', c2='config', c3='value'):
        self.__db_path = db_path
        self.__init()
        self.__c1=c1
        self.__c2=c2
        self.__c3=c3

    def create_table(self, table, c1_len=30, c2_len=60, c3_len=90, unique=1):
        c = [''] * 3
        c[unique] = 'UNIQUE'
        try:
            self.__init()
            self.__cur.execute('CREATE TABLE "{table_name}" ('
                        '"id" integer NOT NULL PRIMARY KEY,'
                        '"{c1}" varchar({len1}) NOT NULL{u1},'
                        '"{c2}" varchar({len2}) NOT NULL {u2},'
                        '"{c3}" varchar({len3}) NOT NULL {u3});'.format(table_name=table, c1=self.__c1, len1=c1_len, c2=self.__c2, len2=c2_len, c3=self.__c3, len3=c3_len, u1=c[0], u2=c[1], u3=c[2]))
            self.__con.commit()
        except OperationalError:
            print('table "{table}" already exists'.format(table=table))
        except:
            print('SOME ERROR, Please check the manual of kvsqlite for correct usage')

    def insert(self, table, data):
        try:
            self.__init()
            insert_sql = 'INSERT INTO {table} ({c1}, {c2}, {c3}) VALUES (?, ?, ?)'.format(table=table, c1=self.__c1 , c2=self.__c2, c3=self.__c3)
            self.__cur.executemany(insert_sql, data)
            self.__con.commit()
        except IntegrityError:
            print('column is not unique')
        except OperationalError:
            print('table "{table}" with columns: "{c1}", "{c2}", "{c3}" is not exists'.format(table=table, c1=self.__c1 , c2=self.__c2, c3=self.__c3))
        except:
            print('SOME ERROR, Please check the manual of kvsqlite for correct usage')
        finally:
            self.__close()

    def select(self, table):
        try:
            self.__init()
            select_sql = "SELECT id, {c1}, {c2}, {c3} FROM {table}".format(c1=self.__c1 , c2=self.__c2, c3=self.__c3, table=table)
            self.__cur.execute(select_sql)
            data = self.__cur.fetchall()
            return data
        except IntegrityError:
            print('column is not unique')
        except OperationalError:
            print('table "{table}" with columns: "{c1}", "{c2}", "{c3}" is not exists'.format(table=table, c1=self.__c1 , c2=self.__c2, c3=self.__c3))
        finally:
            self.__close()

    def update(self, table, data):
        try:
            self.__init()
            update_sql = 'update {table} set {c3} = ?, {c2} = ?, {c1} = ? where id = ?'.format(table=table, c1=self.__c1 , c2=self.__c2, c3=self.__c3)
            rev_data = []
            for i in data:
                rev_data.append(i[::-1])
            self.__cur.executemany(update_sql, rev_data)
            self.__con.commit()
        except ProgrammingError:
            print('Incorrect number of bindings supplied.')
        except OperationalError:
            print('table "{table}" with columns: "{c1}", "{c2}", "{c3}" is not exists'.format(table=table, c1=self.__c1 , c2=self.__c2, c3=self.__c3))
        except:
            print('SOME ERROR, Please check the manual of kvsqlite for correct usage')
        finally:
            self.__close()

    def delete(self, table, data, all=False):
        try:
            delete_sql = 'DELETE FROM {table} WHERE id = ? AND {c1} = ? AND {c2} = ? AND {c3} = ?'.format(table=table, c1=self.__c1, c2=self.__c2, c3=self.__c3)
            self.__init()
            self.__cur.executemany(delete_sql, data)
            self.__con.commit()
        except ProgrammingError:
            print('Incorrect number of bindings supplied.')
        except OperationalError:
            print('table "{table}" with columns: "{c1}", "{c2}", "{c3}" is not exists'.format(table=table, c1=self.__c1 , c2=self.__c2, c3=self.__c3))
        except:
            print('SOME ERROR, Please check the manual of kvsqlite for correct usage')
        finally:
            self.__close()

    def drop_table(self, table):
        try:
            self.__init()
            drop_sql = "DROP TABLE {table}".format(table=table)
            self.__cur.execute(drop_sql)
        except OperationalError:
            print('table "{table}" is not exists'.format(table=table))
        except:
            print('SOME ERROR, Please check the manual of kvsqlite for correct usage')
        finally:
            self.__close()



