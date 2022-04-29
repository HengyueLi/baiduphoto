# pybaiduphoto
一刻相册 API


(请PR的同学方向指向`develop`分支）


# 安装
```
pip install pybaiduphoto
```

# 初始化api

```
from pybaiduphoto import API
api = API(cookies=cookies)
```
其中`cookies` 从网页中抠取，如下:
```
cookies = {
            'BAIDUID': 'F...',
            '__yjs_duid': '1...',
            'BIDUPSID': 'FD...',
            'BDUSS_BFESS': 'lRLNl...',
            'STOKEN': 'be2...',
            ...
        }
```
方便起见，也可以通过`browser_cookie3`(注意自己pip安装一下)直接从浏览器中抽取cookies(注意先登陆)，以chrome为例:
```
from pybaiduphoto import API
import browser_cookie3

api = API(cookies = browser_cookie3.chrome() )
```


# 获取对象

## 数据对象
数据对象是指图片或者视频。首先要得到对象的列表信息。因为量比较大，所以信息是分页的。获取第一页的方式如下:
```
list1 = api.get_SinglePage()
```
其返回值包含以下内容：
```
list1.keys()
>>
dict_keys(['items', 'has_more', 'cursor'])
```
`items` 是该分页中的对象集合，是一个list。可以直接通过`.info`查看对象的信息:
```
L=list1["items"]
L[0].info

>>
{'fsid': 63.....,
 'path': '.....',
 'md5': '49dda......',
  ...
 'collect_status': 0}
```
对象可以直接下载到本地目录:
```
L=list1["items"]
L[0].download(DirPath='/Users/XXXX/Desktop')
```
通过`has_more`来判断该页面是否为最后一页。如果不是最后一页，下一页的获得方式为:
```
if list1['has_more']:
    cursor_nextpage = list1['cursor']
    list2 = api.get_SinglePage(cursor=cursor_nextpage)
```
可以删除:
```
L[0].delete()
```

## 相册对象
```
list1 = api.getAlbumList()
list1.keys()
>>
dict_keys(['items', 'has_more', 'cursor'])
```
其中`has_more`, `cursor`意义上同。items中的对象是`相册对象`。可以用过`append`将图片添加到相册。例子: 将最后一张照片添加到第一个相册:
```
ilist = api.get_SinglePage()
alist = api.getAlbumList()
a = alist['items'][0]
a.append( ilist['items'][0]  )
```
也可以添加多个对象，`a.append( ilist['items'][0:3]  )`

可以删除该相册:`a.delete()`,默认会删除相册中的子内容。如果只删除相册但是保留子内容，可使用: `a.delete(isWithItems=False)`

获得相册中的所有对象:
```
res = a.get_OnlineItems()
res.keys()
>>
dict_keys(['items', 'has_more', 'cursor'])
```
看key大约就知道怎么用了吧？其中`items`是一个list，内容是上面讲的`数据对象`。

# 上传文件

```
api.upload_1file(filePath='/Users/XXXX/Desktop/test.png')
```

# 创建相册
创建一个名字为`test`的相册：
```
a = api.createNewAlbum(Name='test')
```
返回的是相册对象（见上面解释）。!!!注意，可以创建名字相同的相册。另外，此处后台来看会用到一个`tid`的信息，来唯一标识一个相册。我不知道这个是怎么生成的，目前用一个18位的随机数来代替测试可行。但这带来一个未来失效的风险。有聪明的同学可以帮我研究研究这个`tid`从哪里来的。


# 网络代理
在初始化对象的时候加入`proxies`字段,例如
`api = API(cookies = browser_cookie3.chrome() , proxies = {"https":"socks5://127.0.0.1:1080"} )`。`proxies`的格式同`requests`库需求一致。

# To do list
- 批量下载，遇到一些困难，有js比较好的同学可以去[issue](https://github.com/HengyueLi/baiduphoto/issues/4)帮着看看。
- ...


# 总结
虽然只在mac上测试了一下，但是应该其他系统也能用。大致看起来能跑通，基本功能可以实现。有各种问题的话再慢慢研究修复。

# 免责申明
此脚本（API）仅供学习交流，禁止商业使用。使用软件过程中，发生意外造成的损失由使用者承担。您必须在下载后的24小时内从计算机或其他各种设备中完全删除本项目所有内容。您使用或者复制了以上的任何内容，则视为已接受此声明，请仔细阅读。
