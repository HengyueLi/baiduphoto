import os
import logging


from .Requests import Requests
from .OnlineItem import OnlineItem
from .Album import Album
from .General import General

# from .General import getAllItemsBySinglePageFunction
from .Person import PersonAlbum
from .Location import Location
from .Thing import Thing


class API:
    def __init__(self, cookies, proxies={}):
        self.req = Requests(cookies=cookies, proxies=proxies)
        self.g = General(self.req)

    @staticmethod
    def getObjectClass(name):
        table = {
            "Item": OnlineItem,
            "Album": Album,
            "Person": PersonAlbum,
            "Location": Location,
            "Thing": Thing,
        }
        if name not in table:
            logging.error("not registrat class by name = [{}]".format(name))
        else:
            return table[name]

    def get_self_1page(self, typeName, cursor=None) -> dict:
        cls = self.getObjectClass(typeName)
        return cls.get_self_1page(req=self.req, cursor=cursor)

    def get_SinglePage(self, cursor=None) -> dict:
        logging.warning("Deprecated method!!! use get_self_1page instead!")
        return self.get_self_1page(typeName="Item", cursor=cursor)

    def get_self_All(self, typeName, max=-1) -> list:
        cls = self.getObjectClass(typeName)
        if cls is None:
            return None
        else:
            return cls.get_self_All(req=self.req, max=max)

    def getAllItems(self, max=-1) -> list:
        logging.warning("Deprecated method!!! use getAllTargetList instead!")
        return self.getAllTargetList(typeName="Item", max=max)

    def getAlbumList(self, limit=30, cursor=None):
        url = "https://photo.baidu.com/youai/album/v1/list"
        params = dict(
            (
                ("clienttype", "70"),
                # ('bdstoken', '263...'),
                ("limit", limit),
                ("need_amount", "1"),
                ("need_member", "1"),
                ("field", "mtime"),
            )
        )
        if cursor is not None:
            params["cursor"] = cursor
        pageInfo = self.req.getReqJson(url, params=params)
        if pageInfo["list"] is None:
            return {"items": [], "has_more": False, "cursor": None}
        return {
            "items": [Album(i, self.req) for i in pageInfo["list"]],
            "has_more": pageInfo["has_more"] == 1,
            "cursor": pageInfo["cursor"],
        }

    def getAlbumList_All(self, max=-1):
        r = []
        cursor = None
        c = 0
        while True:
            albs = self.getAlbumList(cursor=cursor)
            r += albs["items"]
            if albs["has_more"]:
                cursor = albs["cursor"]
            else:
                return r

    def upload_1file_directly(self, filePath):
        preC, reqJson1, reqJson2 = self.g.upload_1file(filePath)
        logging.debug(
            "upload file: preC=\n{}\n,reqJson1=\n{}\n, reqJson2=\n{}\n ".format(
                preC, reqJson1, reqJson2
            )
        )
        if preC["return_type"] == 1:  # new upload
            # if reqJson2 is not None:
            info = reqJson2["data"]
            if "fsid" not in info:
                info["fsid"] = info["fs_id"]
            return OnlineItem(info, self.req)
        elif preC["return_type"] == 3:  # already exist
            logging.warning("upload item already exist on remote")
            return self.getOnlineItem_ByInfo(info=preC["data"])
        else:
            logging.error(
                "unknow return_type ={} @upload_1file_directly".format(
                    preC["return_type"]
                )
            )
            logging.error("full response = [{}]".format(str(preC)))
            return

    def upload_1file(self, filePath, album=None):
        # consider upload into alumb
        item = self.upload_1file_directly(filePath=filePath)
        if album is not None and item is not None:
            logging.debug(
                "append item into album. item=[{}],album=[{}]".format(
                    item.info, album.info
                )
            )
            album.append(item)
        return item

    def createNewAlbum(self, Name, tid=None):
        res = self.g.createNewAlbum(Name, tid)
        return Album(res["info"], req=self.req)

    def get_batchDownloadLink(self, items, zipname=None):
        return self.g.getdlLink_batchDonwload(items=items, zipname=zipname)

    def getOnlineItem_ByInfo(self, info):
        return OnlineItem(info=info, req=self.req)

    def getAlbum_ByInfo(self, info):
        return Album(info=info, req=self.req)

    def getPerson_ByInfo(self, info):
        return PersonAlbum(info=info, req=self.req)

    def getAlbum_ByID(self, ID):
        params = {
            "album_id": str(ID),
        }
        data = self.req.getReqJson(
            url="https://photo.baidu.com/youai/album/v1/detail",
            params=params,
        )
        if data["errno"] == 0:
            return self.getAlbum_ByInfo(info=data)
        else:
            logging.error("return error in getAlbum_ByID")

    def getPersonList_Onepage(self):
        # Currently, keep it as internal function. Since when numo of person increase, cursor may be used.
        url = "https://photo.baidu.com/youai/iclass/person/v2/list"
        params = {
            "ishidden": "0",
            "isrelation": "0",
        }
        res = self.req.getReqJson(url=url, params=params)
        PersonList = [PersonAlbum(info=info, req=self.req) for info in res["list"]]
        return PersonList

    def getAllPersonList(self, max=-1):
        return self.getPersonList_Onepage()

    def loadSelfByInfo(self, typeName, info):
        cls = self.getObjectClass(typeName)
        return cls.loadSelfByInfo(info=info, req=self.req)

    def albumSearch(self, keyword, limit=30, start=0):
        R = {}
        params = {
            "clienttype": "70",
            "keyword": keyword,
            "limit": limit,
            "start": start,
        }
        req = self.g.req
        res = req.getReqJson(
            url="https://photo.baidu.com/youai/album/v1/search",
            params=params,
        )
        abList = []
        for info in res["list"]:
            abList.append(self.getAlbum_ByInfo(info=info))
        R["items"] = abList
        R["has_more"] = res["has_more"] == 1
        return R
