import pymysql

import os


class Game:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        user = os.environ.get("DBUSER")
        pwd = os.environ.get("DBPWD")
        host = os.environ.get("DBHOST")
        conn = pymysql.connect(
            user="root",
            password="dbuserdbuser",
            host="game.cthaaibiwku7.us-east-2.rds.amazonaws.com",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_key(key):

        sql = "SELECT * FROM game.nba_game where game_id=%s";
        conn = Game._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

