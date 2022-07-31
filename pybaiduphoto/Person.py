import logging
from .General import getAllItemsBySinglePageFunction
from .OnlineItem import OnlineItem


class PersonAlbum:
    def __init__(self, info, req):
        self.info = info
        self.req = req

    def getID(self):
        return self.info['person_id']

    def getName(self):
        return self.info['name']

    def getctime(self):
        return self.info['ctime']

    def getmtime(self):
        return self.info['mtime']

    def getCount(self):
        return self.info['pic_count']

    def get_SinglePage(self, cursor=None) -> dict:
        params = {
            'tag_id': self.getID(),
            # 'need_thumbnail': '1',
            'status': '0',
            'cursor':cursor,
        }
        url = 'https://photo.baidu.com/youai/iclass/index/v1/search'
        resDict = self.req.getReqJson(url=url,params=params)
        return {
            "items": [OnlineItem(i, self.req) for i in resDict["list"]],
            "has_more": resDict["has_more"] == 1,
            "cursor": resDict["cursor"],
        }

    def getAllItems(self,max=-1):
        fun = self.get_SinglePage
        return getAllItemsBySinglePageFunction(SinglePageFunc=fun,max=max)
