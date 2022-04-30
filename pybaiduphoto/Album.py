import logging


class Album:
    def __init__(self, info, req):
        self.info = info
        self.req = req

    def append(self, itemObjs):
        if type(itemObjs) is not list:
            itemObjlist = [itemObjs]
        else:
            itemObjlist = itemObjs

        url = "https://photo.baidu.com/youai/album/v1/addfile"
        params = dict(
            (
                ("clienttype", "70"),
                # ('bdstoken', '26.....'),
                ("album_id", self.info["album_id"]),
                ("tid", self.info["tid"]),
                (
                    "list",
                    "[{}]".format(
                        ",".join(
                            [
                                """{{"fsid":{}}}""".format(item.info["fsid"])
                                for item in itemObjlist
                            ]
                        )
                    ),
                ),
            )
        )
        logging.debug("Album-append, getParams=[{}]".format(params))
        response = self.req.getReqJson(url, params=params)
        return response

    def delete(self, isWithItems=True):
        data = {
            "album_id": self.info["album_id"],
            "delete_origin_image": {True: "1", False: "0"}[isWithItems],
            "tid": self.info["tid"],
        }
        url = "https://photo.baidu.com/youai/album/v1/delete"
        return self.req.postReqJson(url, data=data)

    def get_OnlineItems(self, cursor=""):
        data = {
            "cursor": cursor,
            "album_id": self.info["album_id"],
            "need_amount": "1",
            "limit": "100",
            "passwd": "",
        }
        url = "https://photo.baidu.com/youai/album/v1/listfile"
        res = self.req.postReqJson(url=url, data=data)
        return {
            "items": [
                OnlineItem(info=itemInfo, req=self.req) for itemInfo in res["list"]
            ],
            "has_more": res["has_more"] == 1,
            "cursor": res["cursor"],
        }

    def getName(self):
        return self.info["title"]
