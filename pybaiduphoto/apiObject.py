from abc import abstractmethod
from .General import getAllItemsBySinglePageFunction


class apiObject:
    def __init__(self, info, req):
        self.info = info
        self.req = req

    def getInfo(self):
        return self.info

    @classmethod
    @abstractmethod
    def get_self_1page(cls, req, cursor=None):
        pass
        # return {"items":*,"has_more":*,"cursor":*}

    @classmethod
    def get_self_All(cls, req, max=-1) -> list:
        fun = lambda cursor=None: cls.get_self_1page(req=req, cursor=cursor)
        return getAllItemsBySinglePageFunction(SinglePageFunc=fun, max=max)

    @abstractmethod
    def get_sub_1page(self, cursor=None):
        pass
        # return {"items":*,"has_more":*,"cursor":*}

    def get_sub_All(self, max=-1) -> list:
        fun = self.get_sub_1page
        return getAllItemsBySinglePageFunction(SinglePageFunc=fun, max=max)

    @classmethod
    def loadSelfByInfo(cls, info, req):
        return cls(info=info, req=req)
