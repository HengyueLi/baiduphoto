import logging
from .General import getAllItemsBySinglePageFunction
from .OnlineItem import OnlineItem
from .apiObject import apiObject


class PersonAlbum(apiObject):
    @classmethod
    def get_self_1page(cls, req, cursor=None):
        url = "https://photo.baidu.com/youai/iclass/person/v2/list"
        params = {
            "cursor": cursor,
            "ishidden": "0",
            "isrelation": "0",
        }
        res = req.getReqJson(url=url, params=params)
        return {
            "items": [cls(info=info, req=req) for info in res["list"]],
            "has_more": res["has_more"] == 1,
            "cursor": res["cursor"],
        }

    def get_sub_1page(self, cursor=None):
        params = {
            "tag_id": self.getID(),
            # 'need_thumbnail': '1',
            "status": "0",
            "cursor": cursor,
        }
        url = "https://photo.baidu.com/youai/iclass/index/v1/search"
        resDict = self.req.getReqJson(url=url, params=params)
        return {
            "items": [OnlineItem(i, self.req) for i in resDict["list"]],
            "has_more": resDict["has_more"] == 1,
            "cursor": resDict["cursor"],
        }

    # def getInfo(self):
    #     return self.info

    def getID(self):
        return str(self.info["person_id"])

    def getName(self):
        return self.info["name"]

    def setName(self, name):
        params = {
            "person_id": self.getID(),
            "name": name,
        }
        resD = self.req.getReqJson(
            url="https://photo.baidu.com/youai/iclass/person/v1/label", params=params
        )
        # print(resD)
        if resD["errno"] == 0:
            self.info["name"] = name

    def rename(self, newName):
        self.setName(newName)

    def getctime(self):
        return self.info["ctime"]

    def getmtime(self):
        return self.info["mtime"]

    def getCount(self):
        return self.info["pic_count"]

    # def get_SinglePage(self, cursor=None) -> dict:
    #     params = {
    #         "tag_id": self.getID(),
    #         # 'need_thumbnail': '1',
    #         "status": "0",
    #         "cursor": cursor,
    #     }
    #     url = "https://photo.baidu.com/youai/iclass/index/v1/search"
    #     resDict = self.req.getReqJson(url=url, params=params)
    #     return {
    #         "items": [OnlineItem(i, self.req) for i in resDict["list"]],
    #         "has_more": resDict["has_more"] == 1,
    #         "cursor": resDict["cursor"],
    #     }

    # def getAllItems(self, max=-1):
    #     fun = self.get_SinglePage
    #     return getAllItemsBySinglePageFunction(SinglePageFunc=fun, max=max)
