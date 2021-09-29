import requests
import re
import json


global allpage
allpage = 1
# 手动设置爬取次数 大于 0 生效
global nextpage
nextpage = 0

url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&callback=getLiveListJsonpCallback&page=' + \
    str(allpage)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
}


def GoToNextPage(limt):
    # 下一页链接
    global allpage
    global nextpage
    if allpage <= limt:
        allpage = allpage + 1
        return 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&callback=getLiveListJsonpCallback&page=' + str(allpage)
    else:
        exit()


def GetTitleAndUrl(url_):
    if nextpage > 0:
        limt_page = nextpage

    # 获取直播间标题和链接
    try:
        r = requests.get(url_, headers=headers)
        jResponse = re.findall(
            r'getLiveListJsonpCallback\((.*?)\)', r.text, re.S)[0]
        jdata = json.loads(jResponse)
        # print(type(jdata))
        room_data = jdata['data']['datas']
        
        # 判断变量 limt_page 是否存在
        try:
            limt_page
        except NameError:
            var_exists = False
        else:
            var_exists = True

        if var_exists == False:
            limt_page = jdata['data']['totalPage']
        for zb in room_data:
            # 直播间标题
            zbj_url = 'https://www.huya.com/' + zb['privateHost']
            # 直播间链接
            zbj_name = zb['roomName']
            print(zbj_name + ' === ' + zbj_url)
        GetTitleAndUrl(GoToNextPage(limt_page))
    except:
        GetTitleAndUrl(GoToNextPage(limt_page))


if __name__ == '__main__':
    GetTitleAndUrl(url)


# "gameFullName":"英雄联盟",
# "gameHostName":"lol",
# "boxDataInfo":null,
# "totalCount":"3879963",
# "roomName":"一刀秒杀！无限火力之王！",
# "bussType":"1",
# "screenshot":"https://anchorpost.msstatic.com/cdnimage/anchorpost/1008/b7/36b005e3ab0cac6636b54a550bb601_01_1632737892.jpg",
# "privateHost":"saonan",
# "nick":"骚男",
# "avatar180":"https://huyaimg.msstatic.com/avatar/1008/b7/36b005e3ab0cac6636b54a550bb601_180_135.jpg?1585823993",
# "gid":"1",
# "introduction":"20一刀秒杀！无限火力之王！",
# "recommendStatus":"545",
# "recommendTagName":"超级明星",
# "isBluRay":"1",
# "bluRayMBitRate":"8M",
# "screenType":"1",
# "liveSourceType":"8",
# "uid":"900821317",
# "channel":"900821317",
# "liveChannel":"900821317",
# "imgRecInfo":null,
# "aliveNum":"0",
# "attribute":{
#     "ListPos1":{
#         "sContent":"超级明星",
#         "sIcon":""
#     }
# },
# "profileRoom":"520520",
# "isRoomPay":"0",
# "roomPayTag":"",
# "isWatchTogetherVip":0
