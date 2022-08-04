import logging
from .OnlineItem import OnlineItem
from .General import getAllItemsBySinglePageFunction
from .apiObject import apiObject


class Location(apiObject):
    @classmethod
    def get_self_1page(cls, req, cursor=None):
        params = {"type": "2", "cursor": cursor}
        url = "https://photo.baidu.com/youai/iclass/tag/v1/list"
        resD = req.getReqJson(url=url, params=params)
        return {
            "has_more": resD["has_more"] == 1,
            "cursor": resD["cursor"],
            "items": [cls(info=i, req=req) for i in resD["list"]],
        }

    def get_sub_1page(self, cursor=None):
        url = "https://photo.baidu.com/youai/iclass/index/v1/search"
        params = {
            "cursor": cursor,
            "tag_id": self.getID(),
            # 'need_thumbnail': '1',
        }
        resD = self.req.getReqJson(url=url, params=params)
        return {
            "has_more": resD["has_more"] == 1,
            "cursor": resD["cursor"],
            "items": [OnlineItem(info=i, req=self.req) for i in resD["list"]],
        }

    def getID(self):
        return str(self.info["tag_id"])

    def getName(self):
        return self.info["tag_name"]
