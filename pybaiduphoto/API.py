import hashlib
import os
import io
import logging

from .Requests import Requests




# def get_md5_by_binString(binString):
#     return hashlib.md5(binString).hexdigest()
#
# def get_md5_by_LocalFile(filePath):
#     with open(filePath,'rb') as f:
#         return hashlib.md5(f.read()).hexdigest()
#
# def get_metadata_localFile(filePath):
#     return {
#         'fileName' : os.path.basename(filePath),
#         'localFilePath' : filePath,
#         'size' : os.path.getsize(filePath),
#         'ctime': int(os.path.getctime(filePath)),
#         'mtime': int(os.path.getmtime(filePath)),
#         'md5':get_md5_by_LocalFile(filePath),
#     }

def get_file_fullContent(filePath):
    with open(filePath,'rb') as f:
        binString = f.read()
        md5 = hashlib.md5(binString).hexdigest()
    return {
        'fileName' : os.path.basename(filePath),
        'localFilePath' : filePath,
        'size' : os.path.getsize(filePath),
        'ctime': int(os.path.getctime(filePath)),
        'mtime': int(os.path.getmtime(filePath)),
        'md5':md5,
        'bin':binString,
    }





class OnlineIterm():

    def __init__(self,info,req):
        self.info = info
        self.req = req

    def download(self,DirPath,isCheckMd5=True):
        r = self.req.getReqJson(
            url= 'https://photo.baidu.com/youai/file/v2/download',
            params={
                'clienttype': '70',
    #             'bdstoken': 'ba0b17594add5...?',
                'fsid':self.info['fsid'],
            },
        )
        fileName = self.info['path'].split('/')[-1]
        filePath = os.path.join(DirPath,fileName)
        req = self.req.get(r['dlink'])
        with open(filePath,'wb') as f:
            f.write(req.content)
        os.utime(filePath,(self.info.get('mtime',None),self.info.get('ctime',None)),) # reset ctime,mtime
        if isCheckMd5:
            localMd5 = hashlib.md5(req.content).hexdigest()
            if self.info['md5'] != localMd5:
                info.error('md5 check error, file=[{}]'.format(filePath))

    def delete(self,fdis_list=None):
        url = 'https://photo.baidu.com/youai/file/v1/delete'
        if fdis_list is None:
            fdis_list = [self.get_fsid()]
        params = {
            'clienttype' : '70',
            'fsid_list' : '[{}]'.format( ",".join(fdis_list) ),
        }
        logging.debug('item-delete:get params=[{}]'.format(params))
        r = self.req.getReqJson(url,params=params)
        return r

    def get_fsid(self):
        return str(self.info['fsid'])



class Album():

    def __init__(self,info,req):
        self.info = info
        self.req = req

    def append(self,itemObjs):
        if type(itemObjs) is not list:
            itemObjlist = [itemObjs]
        else:
            itemObjlist = itemObjs

        url = 'https://photo.baidu.com/youai/album/v1/addfile'
        params = dict( (
            ('clienttype', '70'),
            # ('bdstoken', '26.....'),
            ('album_id', self.info['album_id']),
            ('tid', self.info['tid']),
            ('list', '[{}]'.format(",".join( ['''{{"fsid":{}}}'''.format(item.info['fsid']) for item in itemObjlist] ) )),
        ))
        logging.debug('Album-append, getParams=[{}]'.format(params))
        response = self.req.getReqJson(url,params=params)
        return response









class API():

    def __init__(self,cookies,proxies={}):
        self.req = Requests(cookies=cookies,proxies=proxies)


#     def get(self,method,params):
#         urlPrefix = 'https://photo.baidu.com/youai/file/v1/'
#         data = self.req.getReqJson(url = urlPrefix+method.strip(), params=params)
#         return data

    def get_SinglePage(self,cursor=None) -> dict:
        # info of one page.   contains a list of photon info
        params={
            'clienttype':70,
        #     'bdstoken':'ba0b17594ad...這有啥用？',
        #     'need_thumbnail':1,
            'need_filter_hidden':0,
            }
        if cursor is not None:
            params['cursor'] = cursor
        pageInfo = self.req.getReqJson(url='https://photo.baidu.com/youai/file/v1/list',params=params)
        return {
            'items'    : [ OnlineIterm(i,self.req) for i in pageInfo['list']] ,
            'has_more' : pageInfo['has_more'] == 1,
            'cursor':  pageInfo['cursor'],
        }


    def getAlbumList(self,limit=30):
        url = 'https://photo.baidu.com/youai/album/v1/list'
        params = dict( (
            ('clienttype', '70'),
            # ('bdstoken', '263...'),
            ('limit', limit),
            ('need_amount', '1'),
            ('need_member', '1'),
            ('field', 'mtime'),
        ))
        pageInfo = self.req.getReqJson(url,params=params)
        if pageInfo['list'] is None:
            return []
        return {
            'items' : [ Album(i,self.req) for i in pageInfo['list'] ],
            'has_more' : pageInfo['has_more'] == 1,
            'cursor':  pageInfo['cursor'],
        }





    def upload_step1_preCreate(self,fileFull):
        postdata = {
          'autoinit': '1',
          'block_list': '["{}"]'.format(fileFull['md5']),
          'isdir': '0',
          'rtype': '1',
          'ctype': '11', # required
          'path': '/'+fileFull['fileName'], # required
          'size': fileFull['size'],# required
        #   'slice-md5': '4fe8d73cf1ee838b...',
          'content-md5': fileFull['md5'], # required
          'local_ctime': fileFull['ctime'],
          'local_mtime': fileFull['mtime'],
        #   'media_info': 'QD1xoOXfdIsFhss...'
        }
        params = {
            'clienttype': '70',
#             'bdstoken': self.req.bdstoken, # requird
        }
        logging.debug('upload_step1,postData={}'.format(postdata))
        data = self.req.postReqJson(url = 'https://photo.baidu.com/youai/file/v1/precreate',params =params,data=postdata )
        return data

#         exist: {'data': {'fs_id': 9630...305088, 'size': 14...74, 'md5': '0379955f9bd...002f773217b', 'server_filename': 'Screen.png', 'path': '/youa/web/Screen.png', 'ctime': 16470..., 'mtime': 16470..., 'isdir': 0, 'category': 3, 'server_md5': '9af01bd...7bebeded', 'shoot_time': 1647...309}, 'return_type': 3, 'errno': 0, 'request_id': 48666...003049}
#         New: {'return_type': 1, 'path': '/youa/web/Screen.png', 'uploadid': 'N1-MTAuNj...DA2MzY3OTQx', 'block_list': [0], 'errno': 0, 'request_id': 48669...67941}


    def upload_step2_superfile2(self,preCreateInfo,fileFull):
        params = dict((
            ('method', 'upload'),
            ('app_id', '16051585'),
            ('channel', 'chunlei'),
            ('clienttype', '70'),
            ('web', '1'),
#             ('logid', 'MTY.........'), # ? , changed every time
            ('path', '/'+fileFull['fileName']),
            ('uploadid', preCreateInfo['uploadid']),
            ('partseq', '0'),
        ))
        # with open(filePath, 'rb') as f:
            # response = self.req.post('https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2', params=params, files={fileName: f} )
        logging.debug('upload_step2,postParams={}'.format(params))
        response = self.req.post('https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2', params=params, files={fileFull['fileName']: io.BytesIO(fileFull['bin']) } )
        return response.json()

    def upload_step3_create(self,preCreateInfo,fileFull):
        params = dict((
            ('clienttype', '70'),
#             ('bdstoken', self.req.bdstoken),
        ))

        data = {
          'path': '/'+fileFull['fileName'],
          'size': fileFull['size'],
          'uploadid': preCreateInfo['uploadid'],
          'block_list': '["{}"]'.format(fileFull['md5']),
          'isdir': '0',
          'rtype': '1',
          'content-md5': fileFull['md5'],
          'ctype': '11',
#           'media_info': 'QD1xoOX.....'
        }
        logging.debug('upload_step3,postData={}'.format(data))
        return self.req.post('https://photo.baidu.com/youai/file/v1/create', params=params, data=data).json()


    def upload_1file(self,filePath):
        # get_file_fullContent,fileName,localFilePath,size,ctime,mtime,md5,bin
        fobj = get_file_fullContent(filePath)
        preC = self.upload_step1_preCreate(fobj)
        if preC.get('uploadid',None) is not None:
            reqJson1 = self.upload_step2_superfile2(preCreateInfo=preC,fileFull=fobj)
            reqJson2 = self.upload_step3_create(preCreateInfo=preC,fileFull=fobj)
            return preC,reqJson1,reqJson2
        else:
            pass
            # file exsis online, 確認網頁操作時也沒有重新上傳
            return preC,None,None
