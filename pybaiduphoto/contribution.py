class downLoader:
    def __init__(self, req):
        self.req = req

    def getDownloadZip(self, url, dirPath, fileName):
        # 通过url下载文件<fileName>，文件存储到路径<dirPath>下
        # 希望这是一个支持断点续传功能的（还不确定支持不支持）
        # 希望这是一个带进度条的 (推荐使用rich,https://pypi.org/project/rich/)
        # 网路参数请从self.req中取出，最好直接用self.req。可以参考Requests.py中的说明
        pass
        print(url, dirPath, fileName)
