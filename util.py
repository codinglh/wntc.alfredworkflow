# -*- coding: utf-8
import os
import pip
import imp
import requests
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

debug = os.getenv('debug')=="true" and True or False

"""
oss 阿里云配置
"""
AccessKeyId = os.getenv('oss.AccessKeyId')
AccessKeySecret = os.getenv('oss.AccessKeySecret')
bucket_name = os.getenv('oss.bucket_name')
endpoint = os.getenv('oss.endpoint')
endpointurl = "http://%s" % endpoint
"""
cos 腾讯云配置
"""
cos_bucket_name = os.getenv('cos_bucket_name')
cos_is_cdn = os.getenv('cos_is_cdn')
cos_region = os.getenv('cos_region')
cos_secret_id = os.getenv('cos_secret_id')
cos_secret_key = os.getenv('cos_secret_key')


def notice(msg, title="【万能图床】提示", subtitle=''):
    ''' notoce message in notification center'''
    os.system('osascript -e \'display notification "%s" with title "%s"\'' % (msg, title))


def install_and_load(package):
    pip.main(['install', package])

    f, fname, desc = imp.find_module(package)
    return imp.load_module(package, f, fname, desc)


"""
检查指定云是否配置正确
"""


def checkConfig(yuncode):
    if 'oss' == yuncode:
        return checkOssConfig()
    elif yuncode == 'cos':
        return checkCosConfig()
    else:
        return False


"""
获取所以配置正确的云code
"""


def getAllConfiged():
    list = []
    if (checkOssConfig()):
        list.append('oss')
    if (checkCosConfig()):
        list.append('cos')
    return list

"""检查阿里云云配置是否配全"""
def checkOssConfig():
    if (AccessKeyId is not None
            and AccessKeySecret is not None
            and bucket_name is not None
            and endpoint is not None
    ):
        return True
    else:
        return False

"""检查腾讯云配置是否配全"""
def checkCosConfig():
    if (cos_bucket_name is not None
            and cos_is_cdn is not None
            and cos_region is not None
            and cos_secret_id is not None
            and cos_secret_key is not None
    ):
        return True
    else:
        return False


"""
上传到阿里云
"""
def uploadOssObj(objtype, name, obj):
    return
    try:
        import oss2
    except:
        oss2 = install_and_load('oss2')
    auth = oss2.Auth(AccessKeyId, AccessKeySecret)
    bucket = oss2.Bucket(auth, endpointurl, bucket_name)
    if debug : notice("上传到阿里云！%s %s" % (endpointurl,bucket_name))
    if ('localfile' == objtype):
        bucket.put_object_from_file(name, obj)
    elif 'url' == objtype:
        input = requests.get(obj)
        bucket.put_object(name, input)
    else:
        if debug: notice("阿里云不支持【%s】上传" % objtype)

def getOssMKurl(upload_name):
    return '![](http://%s.%s/%s)' % (bucket_name,endpoint,upload_name)

"""
上传到腾讯云
"""
def uploadCosObj(objtype, name, obj):
    token = ''
    config = CosConfig(Region=cos_region, Secret_id=cos_secret_id, Secret_key=cos_secret_key, Token=token)
    # 2. 获取客户端对象
    client = CosS3Client(config)
    if debug: notice("上传到腾讯云！%s" % ( cos_bucket_name))
    if ('localfile' == objtype):
        response = client.put_object_from_local_file(
            Bucket=cos_bucket_name,
            LocalFilePath=obj,
            Key=name,
        )
        if debug: notice("上传到腾讯云返回：%s" % (response))
    elif 'url' == objtype:
        if debug: notice("腾讯云不支持url上传" )
    else:
        if debug: notice("腾讯云不支持【%s】上传" % objtype)

def getCosMKurl(upload_name):
    if 'true' == cos_is_cdn:
        return '![](http://%s.cos.ap-guangzhou.myqcloud.com/%s)' % (cos_bucket_name,upload_name)
    else:
        return '![](http://%s.file.myqcloud.com/%s)' % (cos_bucket_name,upload_name)

if __name__ == "__main__":
    try:
        import oss2
    except:
        print("err p")
