from ApiServer.ApiMainServer import ApiMainServer
from DbServer.DbMainServer import DbMainServer
import FileCache.FileCacheServer as Fcs
import Config.ConfigServer as Cs
from OutPut.outPut import *
import schedule


class PushMainServer:
    def __init__(self, wcf):
        self.wcf = wcf
        self.Ams = ApiMainServer()
        self.Dms = DbMainServer()
        configData = Cs.returnConfigData()
        self.morningPageTime = configData['pushConfig']['morningPageTime']
        self.eveningPageTime = configData['pushConfig']['eveningPageTime']
        self.offWorkTime = configData['pushConfig']['offWorkTime']
        self.offWorkMsg = configData['pushConfig']['keyWord']['offWorkMsg']
        self.fishTime = configData['pushConfig']['fishTime']
        self.kfcTime = configData['pushConfig']['kfcTime']

    def pushMorningPage(self, ):
        """
        定时早报推送
        :return:
        """
        op('[*]: 定时早报推送中... ...')
        morningMsg = self.Ams.getMorningNews()
        room_dicts = self.Dms.showPushRoom()
        for roomId in room_dicts.keys():
            self.wcf.send_text(msg=morningMsg, receiver=roomId)
        op('[+]: 定时早报推送成功！！！')

    def pushEveningPage(self, ):
        """
        定时晚报推送
        :return:
        """
        op('[*]: 定时晚报推送中... ...')
        eveningMsg = self.Ams.getEveningNews()
        room_dicts = self.Dms.showPushRoom()
        for roomId in room_dicts.keys():
            self.wcf.send_text(msg=eveningMsg, receiver=roomId)
        op('[+]: 定时晚报推送成功！！！')

    def pushOffWork(self, ):
        """
        定时下班推送
        :return:
        """
        op('[*]: 定时下班消息推送中... ...')
        offWorkMsg = self.offWorkMsg.replace('\\n', '\n')
        room_dicts = self.Dms.showPushRoom()
        for room_id in room_dicts.keys():
            self.wcf.send_text(msg=offWorkMsg, receiver=room_id)
        op('[+]: 定时下班消息推送成功！！！')

    # 摸鱼日记推送
    def pushFish(self):
        """
        定时摸鱼日记推送
        :return:
        """
        op(f'[*]: 定时摸鱼日记推送中... ...')
        room_dicts = self.Dms.showPushRoom()
        fishPath = self.Ams.getFish()
        for room_id in room_dicts.keys():
            self.wcf.send_image(path=fishPath, receiver=room_id)
        op('[+]: 定时摸鱼日记推送成功！！！')

    # 每周四KFC推送
    def pushKfc(self, ):
        """
        每周四KFC推送
        :return:
        """
        op(f'[*]: 定时KFC文案推送中... ...')
        kfcMsg = self.Ams.getKfc()
        room_dicts = self.Dms.showPushRoom()
        for room_id in room_dicts.keys():
            self.wcf.send_text(msg=kfcMsg, receiver=room_id)
        op(f'[+]: 定时KFC文案发送成功！！！')

    # 定时签到表清空
    def clearSign(self, ):
        """
        定时签到表清空
        :return:
        """
        op(f'[*]: 定时签到表清空中... ...')
        self.Dms.clearSign()
        op(f'[+]: 定时签到表清空成功！！！')

    # 定时缓存文件清空
    def clearCacheFile(self, ):
        """
        定时缓存文件清空
        :return:
        """
        op(f'[*]: 定时缓存文件清空中... ...')
        Fcs.clearCacheFolder()
        op(f'[+]: 定时缓存文件清空成功！！！')

    def run(self, ):
        schedule.every().day.at(self.morningPageTime).do(self.pushMorningPage)
        schedule.every().day.at(self.fishTime).do(self.pushFish)
        schedule.every().thursday.at(self.kfcTime).do(self.pushKfc)
        schedule.every().day.at(self.eveningPageTime).do(self.pushEveningPage)
        schedule.every().day.at(self.offWorkTime).do(self.pushOffWork)
        schedule.every().day.at('00:00').do(self.clearSign)
        schedule.every().day.at('03:00').do(self.clearCacheFile)
        op(f'[+]: 已开启定时推送服务！！！')
        while True:
            schedule.run_pending()

