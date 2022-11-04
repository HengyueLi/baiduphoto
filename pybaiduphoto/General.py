import os
import io
import random
import logging
import hashlib
import datetime
import base64
import json
import cv2
import filetype
from PIL import Image


# import execjs

# import js2py
from .Requests import Requests
def G(e):
    '''
    function G(e) {
    for (var t = [], n = 0, i = e.length; n < i; ++n)
        t.push(e.charCodeAt(n));
    var o = new Uint8Array(t);
    return o
}
    '''
    t = []
    for iii in e:
        t.append(ord(iii))
    o = t
    return o


def Q(e):
    H = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
         30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
         58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85,
         86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
         111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
         133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154,
         155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176,
         177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198,
         199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220,
         221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242,
         243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]

    '''
    function Q(e) {
    for (var t = 0, n = H.slice(), i = e.length, o = 0; o < 256; ++o)
        t = (t + n[o] + e[o % i]) % 256,
            n[t] = [n[o], n[o] = n[t]][0];
    return n
}
    '''
    t = 0
    n = H
    i = len(e)
    o = 0
    while o < 256:
        t = (t + n[o] + e[o % i]) % 256
        tmp = n[t]
        n[t] = n[o]
        n[o] = tmp
        o += 1
    return n


def Vchange(e):
    '''
    V.prototype.change = function (e) {
    this.key = new Array(e.length);
    for (var t = G(e), n = 0, i = t.length; n < i; ++n)
        this.key[n] = t[n];
    return this.ksa = Q(this.key), this.ksa
}
    '''
    key = [0 for i in range(len(e))]
    t = G(e)
    n = 0
    i = len(t)
    while n < i:
        key[n] = t[n]
        n += 1
    ksa = Q(key)
    return ksa


def q(e, t, n, i):
    '''
    function q(e, t, n, i) {
    for (var o = 0, r = 0, a = n, s = t.slice(), c = 0; c < i; ++c)
        o = (o + 1) % 256,
            r = (r + s[o]) % 256,
            s[r] = [s[o], s[o] = s[r]][0],
            a[c] = e[c] ^ s[(s[o] + s[r]) % 256];
    return a
}
    '''
    o = 0
    r = 0
    a = n
    s = t
    c = 0
    while c < i:
        o = (o + 1) % 256
        r = (r + s[o]) % 256
        tmp = s[r]
        s[r] = s[o]
        s[o] = tmp
        a[c] = e[c] ^ s[(s[o] + s[r]) % 256]
        c += 1
    return a


def W(e):
    '''
    function W(e) {
    for (var t = "", n = 0; n < e.length; n++)
        t += String.fromCharCode(e[n]);
    return t
}
    '''
    t = ''
    n = 0
    tttt = []
    ee = bytes(e)
    # print(ee)
    # ret = ee.decode('unicode_escape')
    # while n < len(ee):
    #     # tt = hex(e[n])
    #     t+=ee[n].encode('utf-8')
    #     # t += chr(e[n])
    #     tttt.append(ee[n].encode('utf-8'))
    #     n += 1
    return ee


def Rencode(e):
    '''
encode: function (e) {
            var t, n, i, o = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=", r = 0, a = e.length,
                s = "";
            while (r < a) {
                if (t = 255 & e.charCodeAt(r++),
                r == a) {
                    s += o.charAt(t >> 2),
                        s += o.charAt((3 & t) << 4),
                        s += "==";
                    break
                }
                if (n = e.charCodeAt(r++),
                r == a) {
                    s += o.charAt(t >> 2),
                        s += o.charAt((3 & t) << 4 | (240 & n) >> 4),
                        s += o.charAt((15 & n) << 2),
                        s += "=";
                    break
                }
                i = e.charCodeAt(r++),
                    s += o.charAt(t >> 2),
                    s += o.charAt((3 & t) << 4 | (240 & n) >> 4),
                    s += o.charAt((15 & n) << 2 | (192 & i) >> 6),
                    s += o.charAt(63 & i)
            }
            return s
        },
    '''
    en = base64.b64encode(e)
    return en.decode('utf-8')

    # return e.encode('utf-8')[0]
    # t=0
    # n=0
    # i=0
    # o = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    # r = 0
    # a= len(e)
    # s=''
    # while r<a:
    #     1


def JencodeString(strin):
    '''

        V.prototype.encodeString = function (e) {
        var t = G(e)
            , n = t.length
            , i = Uint8Array.from(q(t, this.ksa, new Uint8Array(n), n));
        return R.encode(W(i))
    }
;
var J = new V("7FED2719FC7E4D5602FB1D9D11AFA01B")
    '''
    e = "7FED2719FC7E4D5602FB1D9D11AFA01B"
    t = G(strin)
    n = len(t)
    i = q(t, Vchange(e), [0 for i in range(n)], n)
    # i = Uint8Array.from(q(t, this.ksa, new Uint8Array(n), n));

    # return R.encode(W(i))
    # return W(i)
    return Rencode(W(i))

def timestamp_to_strtime(timestamp):
    """将 13 位整数的毫秒时间戳转化成本地普通时间 (字符串格式)
    :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
    :return: 返回字符串格式 {str}'2016-02-25 20:21:04.242000'
    """
    local_str_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y:%m:%d %H:%M:%S')
    return local_str_time

def timestamp_to_strtime2(timestamp):
    """将 13 位整数的毫秒时间戳转化成本地普通时间 (字符串格式)
    :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
    :return: 返回字符串格式 {str}'2016-02-25 20:21:04.242000'
    """
    # timestamp += 8*3600
    utc_time = datetime.datetime.utcfromtimestamp(timestamp)
    stadardTime = utc_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    # local_str_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return stadardTime

def getCreateTime(media_path):
    create_time = int(os.path.getctime(media_path))  # 创建时间
    update_time = int(os.path.getmtime(media_path))  # 修改时间
    access_time = int(os.path.getatime(media_path))  # 访问时间
    return min(create_time,update_time,access_time)


def getMediaType(media_path):
    kind = filetype.guess(media_path)
    if 'video' in kind.mime:
        return 'video'
    if 'image' in kind.mime:
        return 'image'

def get_video_duration(filename):
    try:
        cap = cv2.VideoCapture(filename)
    except:
        return 0,0,0
    if cap.isOpened():
        rate = cap.get(5)
        frame_num =cap.get(7)
        duration = frame_num/rate
        width = cap.get(3)
        height = cap.get(4)
        return duration, width, height
    return 0,0,0

def getMediaInfo(shoot_time, media_path):
    media_type = getMediaType(media_path)
    # media_info_dic = {}
    
    if media_type == 'image':
        wh = Image.open(media_path).size
        # media_info_dic = {"width": wh[0], "height": wh[1], "orientation": 1, "date_time": timestamp_to_strtime(shoot_time)}
        # media_info_str = '{"width":828,"height":828,"orientation":1,"date_time":"2022:08:10 16:23:18"}'
        media_info_str = '{"width":%s,"height":%s,"orientation":1,"date_time":"%s"}'%(int(wh[0]),int(wh[1]),timestamp_to_strtime(shoot_time))
    else:
        duration, width, height = get_video_duration(media_path)
        dur = '%.3f'%duration
        # media_info_dic = {
        #     "file": {"creation_time": timestamp_to_strtime2(shoot_time), "duration": dur, "duration_ms": int(eval(dur)*1000),
        #              "file_size": os.path.getsize(media_path)}, "video": {"width": int(width), "height": int(height)}}
        # media_info_str = '{"file":{"creation_time":"2021-12-21T16:04:31.000Z","duration":9.264,"duration_ms":9264,"file_size":2101011},"video":{"width":720,"height":1280}}'
        media_info_str = '{"file":{"creation_time":"%s","duration":%s,"duration_ms":%s,"file_size":%s},"video":{"width":%s,"height":%s}}'%(timestamp_to_strtime2(shoot_time),dur,int(eval(dur)*1000),os.path.getsize(media_path),int(width),int(height))
    # media_info_str = json.dumps(media_info_dic)
    print('media_info_str {}'.format(media_info_str))
    # js_o = ''
    # with open('1.js', mode='r', encoding='utf-8') as jsf:
    #     js_o = jsf.read()
    # ctx = execjs.compile(js_ooo)
    # video_title = ctx.call('K', media_info_str)
    retinfo = JencodeString(media_info_str)
    # print(ret)
    # print(video_title)
    return retinfo

def getAllItemsBySinglePageFunction(SinglePageFunc, max=-1):
    # ----------------------------------------------------------------
    # def SinglePageFunc(cursor=None) -> dict:
    #     return { 'items':[] , "has_more":True/False, "cursor"  }
    # ----------------------------------------------------------------
    cursor = None
    r = []
    while True:
        page = SinglePageFunc(cursor=cursor)
        r += page["items"]
        if page["has_more"]:
            cursor = page["cursor"]
            if max > 0:
                if len(r) >= max:
                    break
        else:
            break
    if max <= 0:
        return r
    else:
        return r[:max]


class General:
    def __init__(self, req):
        self.req = req

    @staticmethod
    def get_file_fullContent(filePath):
        with open(filePath, "rb") as f:
            binString = f.read()
            md5 = hashlib.md5(binString).hexdigest()
        ct_ = getCreateTime(filePath)
        print({
            "fileName": os.path.basename(filePath),
            "localFilePath": filePath,
            "size": os.path.getsize(filePath),
            "ctime": ct_,
            "mtime": ct_,
            "shoot_time": ct_,
            "md5": md5,
            "media_info":getMediaInfo(ct_,filePath)
            # "bin": binString,
        })
        return {
            "fileName": os.path.basename(filePath),
            "localFilePath": filePath,
            "size": os.path.getsize(filePath),
            # "ctime": int(os.path.getctime(filePath))*1000,
            # "mtime": int(os.path.getmtime(filePath))*1000,
            
            "ctime": ct_,
            "mtime": ct_,
            # "ctime": int(os.path.getctime(filePath)),
            # "mtime": int(os.path.getmtime(filePath)),
            # "shoot_time": int(os.path.getctime(filePath)),
            "md5": md5,
            "bin": binString,
            "media_info":getMediaInfo(ct_,filePath)
        }

    def upload_step1_preCreate(self, fileFull):
        postdata = {
            "autoinit": "1",
            "block_list": '["{}"]'.format(fileFull["md5"]),
            "isdir": "0",
            "rtype": "1",
            "ctype": "11",  # required
            "path": "/" + fileFull["fileName"],  # required
            "size": fileFull["size"],  # required
            #   'slice-md5': '4fe8d73cf1ee838b...',
            "slice-md5": fileFull["md5"],
            "content-md5": fileFull["md5"],  # required
            "local_ctime": fileFull["ctime"],
            "local_mtime": fileFull["mtime"],
            # "shoot_time": fileFull["shoot_time"],
            # 'media_info': 'QD1xoOXfdIsFhss...' # 包含shoot_time
            'media_info': fileFull["media_info"], # 包含shoot_time
        }
        params = {
            "clienttype": "70",
            #             'bdstoken': self.req.bdstoken, # requird
        }
        logging.debug("upload_step1,postData={}".format(postdata))
        data = self.req.postReqJson(
            url="https://photo.baidu.com/youai/file/v1/precreate",
            params=params,
            data=postdata,
        )
        print('upload_step1_preCreate {}'.format(data))
        return data

    #         exist: {'data': {'fs_id': 9630...305088, 'size': 14...74, 'md5': '0379955f9bd...002f773217b', 'server_filename': 'Screen.png', 'path': '/youa/web/Screen.png', 'ctime': 16470..., 'mtime': 16470..., 'isdir': 0, 'category': 3, 'server_md5': '9af01bd...7bebeded', 'shoot_time': 1647...309}, 'return_type': 3, 'errno': 0, 'request_id': 48666...003049}
    #         New: {'return_type': 1, 'path': '/youa/web/Screen.png', 'uploadid': 'N1-MTAuNj...DA2MzY3OTQx', 'block_list': [0], 'errno': 0, 'request_id': 48669...67941}

    def upload_step2_superfile2(self, preCreateInfo, fileFull):
        params = dict(
            (
                ("method", "upload"),
                ("app_id", "16051585"),
                ("channel", "chunlei"),
                ("clienttype", "70"),
                ("web", "1"),
                #             ('logid', 'MTY.........'), # ? , changed every time
                ("path", "/" + fileFull["fileName"]),
                ("uploadid", preCreateInfo["uploadid"]),
                ("partseq", "0"),
            )
        )

        logging.debug("upload_step2,postParams={}".format(params))
        response = self.req.post(
            "https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2",
            params=params,
            files={fileFull["fileName"]: io.BytesIO(fileFull["bin"])},
        )
        return response.json()

    def upload_step3_create(self, preCreateInfo, fileFull):
        params = dict(
            (
                ("clienttype", "70"),
                #             ('bdstoken', self.req.bdstoken),
            )
        )

        data = {
            "path": "/" + fileFull["fileName"],
            "size": fileFull["size"],
            "uploadid": preCreateInfo["uploadid"],
            "block_list": '["{}"]'.format(fileFull["md5"]),
            "isdir": "0",
            "rtype": "1",
            "content-md5": fileFull["md5"],
            "ctype": "11",
            'media_info': fileFull["media_info"]
            #           'media_info': 'QD1xoOX.....'
        }
        logging.debug("upload_step3,postData={}".format(data))
        return self.req.post(
            "https://photo.baidu.com/youai/file/v1/create", params=params, data=data
        ).json()

    def upload_1file(self, filePath):
        # get_file_fullContent,fileName,localFilePath,size,ctime,mtime,md5,bin
        fobj = self.get_file_fullContent(filePath)
        preC = self.upload_step1_preCreate(fobj)
        if preC.get("uploadid", None) is not None:
            reqJson1 = self.upload_step2_superfile2(preCreateInfo=preC, fileFull=fobj)
            reqJson2 = self.upload_step3_create(preCreateInfo=preC, fileFull=fobj)
            return preC, reqJson1, reqJson2
        else:
            pass
            # file exsis online, 確認網頁操作時也沒有重新上傳
            return preC, None, None

    def createNewAlbum(self, Name, tid=None):
        url = "https://photo.baidu.com/youai/album/v1/create"
        if tid is None:
            tid = str(random.randint(100000000000000000, 999999999999999999))
        params = {
            "title": Name,  #
            "source": "0",
            "tid": tid,  # tid 用来唯一标识，title相同的相册可以同时存在 exam=316511988232386428
        }
        res = self.req.getReqJson(url=url, params=params)
        return res

    @staticmethod
    def funcS(j, r):
        a = []
        p = []
        o = ""
        v = len(j)
        for q in range(256):
            a.append(ord(j[q % v]))
            p.append(q)
            q += 1
        u = 0
        for q in range(256):
            u = (u + p[q] + a[q]) % 256
            t = p[q]
            p[q] = p[u]
            p[u] = t
            q += 1
        i = u = q = 0
        for q in range(len(r)):
            i = (i + 1) % 256
            u = (u + p[i]) % 256
            t = p[i]
            p[i] = p[u]
            p[u] = t
            k = p[((p[i] + p[u]) % 256)]
            o += chr(ord(r[q]) ^ k)
            q += 1
        return o

    @classmethod
    def get_sign_by_sign1sign2sign3(cls, sign1, sign2, sign3):
        funcS = (
            cls.funcS
        )  # fun_s = js2py.eval_js(sign2); notice to import js2py and in requirements
        sign = base64.encodebytes(funcS(sign3, sign1).encode("latin1")).decode()
        return sign

    def batchDonwload_precondition(self):
        # bacth download 之前，此requrest能够得到几条信息（其中还有一个js函数），
        # 需要通过该函数返回的信息计算处sign用于真正的batchdownload，现在还不知道是如何转换的
        url = "https://photo.baidu.com/youai/file/v1/batchdownloadvariable"
        params = {"fields": '["sign1","sign2","sign3","timestamp"]', "clienttype": "70"}
        rdata = self.req.getReqJson(url=url, params=params)
        sign = self.get_sign_by_sign1sign2sign3(
            rdata["sign1"], rdata["sign2"], rdata["sign3"]
        )
        return {"sign": sign, "timestamp": rdata["timestamp"]}

    def getdlLink_batchDonwload(self, items, zipname=None):
        preData = self.batchDonwload_precondition()
        url = "https://photo.baidu.com/youai/file/v1/batchdownload"
        fsid_list = [i.get_fsid() for i in items]
        if zipname is None:
            now = datetime.datetime.now()
            zipname = now.strftime("【一刻相册】%H时%M分-批量下载 {} 项.zip").format(len(fsid_list))
        params = {
            "clienttype": 70,
            "fsid_list": "[{}]".format(",".join(fsid_list)),
            "zipname": zipname,
            "sign": preData["sign"],
            "timestamp": preData["timestamp"],
        }
        resJson = self.req.getReqJson(url=url, params=params)
        return resJson["dlink"]

    def getDownloadZip(self, items, dirPath, zipname=None):
        from .contribution import downLoader

        dl = downLoader(req=self.req)
        url = self.getdlLink_batchDonwload(items=items, zipname=zipname)
        dl.getDownloadZip(url=url, dirPath=dirPath, fileName=zipname)
