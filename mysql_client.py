import MySQLdb
import os
from tornado.log import app_log


class MySQLClient:
    def get_connection(self):
        connection = MySQLdb.connect(
                host=os.environ.get('MYSQL_HOST'),
                user=os.environ.get('MYSQL_USER'),
                passwd=os.environ.get('MYSQL_PASSWORD'),
                db=os.environ.get('MYSQL_DBNAME'),
                charset='utf8')
        return connection

    def close_connection(self, connection):
        connection.close()

    def get_audio(self, keyword):
        connection = self.get_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT *
            FROM audios 
            WHERE keyword = "%s"
            """ % keyword
        affected = cursor.execute(sql)
        if affected == 0:
            self.close_connection(connection)
            return None
        res = cursor.fetchone()
        self.close_connection(connection)
        return res.get("file_path")

    def get_audio_type_list(self):
        connection = self.get_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT *
            FROM audio_type
            """
        cursor.execute(sql)
        res = cursor.fetchall()
        self.close_connection(connection)
        return res

    def get_current_audio_type(self):
        connection = self.get_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT *
            FROM current_audio_type
            INNER JOIN audio_type
            ON current_audio_type.audio_type = audio_type.audio_type_id
            """
        cursor.execute(sql)
        res = cursor.fetchone()
        self.close_connection(connection)
        return res

    def set_current_audio_type(self, audio_type):
        connection = self.get_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            UPDATE current_audio_type
            SET audio_type = "%d"
            """ % audio_type
        cursor.execute(sql)
        connection.commit()
        self.close_connection(connection)

