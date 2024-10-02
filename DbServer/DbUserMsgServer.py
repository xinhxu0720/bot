import time

import DbServer.DbDomServer as Dds
import Config.ConfigServer as Cs
from OutPut.outPut import op


class DbUserMsgServer:
    def __init__(self):
        pass

    def addMessage(self, wxId, roomId, question, answer):
        """
        增加管理员
        :param wxId: 微信ID
        :param roomId: 群聊ID
        :param question: 问题
        :param answer: 答案
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnUserMsgPath())
        try:
            cursor.execute('INSERT INTO UserMsg VALUES (?, ?, ?, ?,?)', (wxId, roomId, question, answer,int(round(time.time() * 1000))))
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 增加用户消息出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def getUserMsg(self, wxId, roomId):
        """
        查询用户消息
        :param wxId: 微信ID
        :param roomId: 群聊ID
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnUserMsgPath())
        try:
            cursor.execute('SELECT * FROM UserMsg WHERE wxId=? AND roomId=?', (wxId, roomId))
            result = cursor.fetchall()
            Dds.closeDb(conn, cursor)
            return result
        except Exception as e:
            op(f'[-]: 查询用户消息, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False
