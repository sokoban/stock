'''
PyMysql Singleton DB Connection
Created by sokoban@naver.com
2020-03-29
'''

import pymysql


class sqldata:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if sqldata.__instance == None:
            sqldata()
        return sqldata.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.host = "3.34.139.77"
        self.user = ""
        self.password = ""
        self.db = "STOCKDB"

        if sqldata.__instance != None:
            print("Singleton")
            raise Exception("This class is a singleton!")
        else:
            try:
                self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                           charset='utf8',port=13309 , cursorclass=pymysql.cursors.DictCursor)
                self.curs = self.conn.cursor()
            except Exception as e:
                print(e)

            print("Database Connected")
            sqldata.__instance = self

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.curs.close()

    def executes(self, statements):
        queries = []
        data = []

        if type(statements) == str:
            # all statements must be in a list
            statements = [statements]
        if statements:
            #print(statements)
            for statement in statements:
                try:
                    # reset the test statement

                    self.curs.execute(statement)
                    # retrieve selected data
                    data = self.curs.fetchall()
                    self.conn.commit()

                except Exception as e:
                    print('Error : ', e.args)
                    print('For the statement:', statement)
        return data
