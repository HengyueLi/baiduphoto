import os
import hashlib
import logging
from .apiObject import apiObject


class OnlineItem(apiObject):
    # def __init__(self, info, req):
    #     self.info = info
    #     self.req = req

    @classmethod
    def get_self_1page(cls, req, cursor=None):
        params = {
            "cursor": cursor,
            #     'need_thumbnail':1,
            "need_filter_hidden": 0,
        }
        pageInfo = req.getReqJson(
            url="https://photo.baidu.com/youai/file/v1/list", params=params
        )
        return {
            "items": [cls(i, req) for i in pageInfo["list"]],
            "has_more": pageInfo["has_more"] == 1,
            "cursor": pageInfo["cursor"],
        }

    def getContent_byRequest(self):
        r = self.req.getReqJson(
            url="https://photo.baidu.com/youai/file/v2/download",
            params={
                "clienttype": "70",
                #             'bdstoken': 'ba0b17594add5...?',
                "fsid": self.info["fsid"],
            },
        )
        req = self.req.get(r["dlink"])
        return req.content

    def download(self, DirPath=None, fileName=None, isCheckMd5=True):
        if DirPath is None:
            DirPath = os.getcwd()
        if fileName is None:
            fileName = self.getFileName()
        filePath = os.path.join(DirPath, fileName)
        fileContent = self.getContent_byRequest()
        with open(filePath, "wb") as f:
            f.write(fileContent)
        os.utime(
            filePath,
            (self.info.get("mtime", None), self.info.get("ctime", None)),
        )  # reset ctime,mtime
        if isCheckMd5:
            localMd5 = hashlib.md5(fileContent).hexdigest()
            if self.info["md5"] != localMd5:
                info.error("md5 check error, file=[{}]".format(filePath))

    def delete(self, fdis_list=None):
        url = "https://photo.baidu.com/youai/file/v1/delete"
        if fdis_list is None:
            fdis_list = [self.get_fsid()]
        params = {
            "clienttype": "70",
            "fsid_list": "[{}]".format(",".join(fdis_list)),
        }
        logging.debug("item-delete:get params=[{}]".format(params))
        r = self.req.getReqJson(url, params=params)
        return r

    # def get_fsid(self):
    # return str(self.info["fsid"])
    def get_fsid(self):
        if "fsid" in self.info:
            return str(self.info["fsid"])
        if "fs_id" in self.info:
            return str(self.info["fs_id"])
        logging.error("cannot get fsid!!!")

    def getID(self):
        return self.get_fsid()

    # def getInfo(self):
    #     return self.info

    def getFileName(self):
        return self.info["path"].split("/")[-1]

    def getName(self):
        return self.getFileName()

    def getSize(self):
        return self.info["size"]

    def getCreationDate(self):
        return self.info["ctime"]

    def getModificationDate(self):
        return self.info["mtime"]
