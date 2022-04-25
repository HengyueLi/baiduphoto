from .API import Album
import asyncio
import os
import logging
import threading

logger = logging.getLogger(__name__)


def download(item, download_path: str):
    try:
        file_path = os.path.join(download_path, os.path.basename(item.info["path"]))
        logger.info("下载 {} 到 {}".format(item.info["path"], download_path))
        if os.path.exists(file_path):
            logger.debug("文件 {} 已经存在，跳过".format(file_path))
            return

        item.download(DirPath=download_path)
    except Exception as e:
        logger.error(e)


def download_album(album: Album, download_path: str):
    """
    默认情况下 download_album 启用了对协程池的支持。并且只开启了两个协程，这是因为协程开启过多会导致 HTTP 请求失败。
    如果需要设置其它数量的协程，请在第一次调用此函数前调用 CoroutinePool.get_default(n)
    """
    album_info = album.get_pictures()
    pool = CoroutinePool.get_default(2)

    while True:
        for pic in album_info["items"]:
            pool.add(download, pic, download_path)

        if not album_info["has_more"]:
            break

        album_info = album.get_pictures(cursor=album_info["cursor"])


class CoroutinePool:
    """
    协程池

    协程池可以将函数添加到池中运行。协程池在析构时会自动等待所有任务结束
    """

    __default = None

    @classmethod
    def get_default(cls, value: int = 10):
        """
        获取一个默认的协程池

        :param value: 开启的协程数量。此参数只在第一次调用此函数时有效
        """
        if cls.__default is None:
            cls.__default = CoroutinePool(value=value)
        return cls.__default

    def __init__(self, value: int = 10) -> None:
        self.__sem = threading.Semaphore(value)
        self.__tasks = []
        self.__loop = asyncio.new_event_loop()

    def add(self, func, *args):
        def wrap():
            with self.__sem:
                func(*args)

        self.__tasks.append(self.__loop.run_in_executor(None, wrap))

    def wait(self):
        """
        等待协程池中的任务结束
        """
        self.__loop.run_until_complete(asyncio.wait(self.__tasks))
        self.__tasks = []

    def __del__(self):
        self.wait()
        self.__loop.close()
