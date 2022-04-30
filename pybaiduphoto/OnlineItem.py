import os
import hashlib
import logging


class OnlineItem:
    def __init__(self, info, req):
        self.info = info
        self.req = req

    def download(self, DirPath=None, fileName=None, isCheckMd5=True):
        r = self.req.getReqJson(
            url="https://photo.baidu.com/youai/file/v2/download",
            params={
                "clienttype": "70",
                #             'bdstoken': 'ba0b17594add5...?',
                "fsid": self.info["fsid"],
            },
        )
        if DirPath is None:
            DirPath = os.getcwd()
        if fileName is None:
            fileName = self.getFileName()
        filePath = os.path.join(DirPath, fileName)
        req = self.req.get(r["dlink"])
        with open(filePath, "wb") as f:
            f.write(req.content)
        os.utime(
            filePath,
            (self.info.get("mtime", None), self.info.get("ctime", None)),
        )  # reset ctime,mtime
        if isCheckMd5:
            localMd5 = hashlib.md5(req.content).hexdigest()
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

    def get_fsid(self):
        return str(self.info["fsid"])

    def getFileName(self):
        return self.info["path"].split("/")[-1]
