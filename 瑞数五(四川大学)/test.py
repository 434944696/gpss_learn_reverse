import execjs
import requests
from parsel import Selector
from loguru import logger
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://www.scu.edu.cn/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

session = requests.session()
session.headers = headers

url = "https://www.scu.edu.cn/"


def get_202_index():
    response = session.get(url, headers=headers)
    selector = Selector(text=response.text)
    content = selector.xpath('''/html/head/meta[2]/@content''').get()
    ts_url = "https://www.scu.edu.cn" + selector.xpath('''/html/head/script[1]/@src''').get()
    ts_response = requests.get(ts_url).text
    function_str = selector.xpath('''/html/head/script[2]/text()''').get()
    env = open("huanjing.js", "r").read()
    get_ts_str = f'''
    {env}
    {ts_response}
    {function_str}
    '''
    get_ts_en = execjs.compile(get_ts_str)
    ts_array = get_ts_en.call("get_ts_function")
    # 替换数组
    content_array = get_ts_en.call("get_content_array", content)
    logger.info("get_202获取ts和content")
    return ts_array, content_array


def get_cookie(ts_array, content_array):
    ts_array_944 = []
    for i in ts_array:
        if type(ts_array[i]) == list and ts_array[i] != []:
            ts_array_944 = ts_array[i]
            break
    index_function_name = {
        "_$AN": 166,
        "_$xR": 196,
        "_$EJ": 43,
        "_$kn": 184,
        "_$Vs": 130,
        "_$rJ": 213,
        "_$Gs": 150,
        "_$jM": 137,
        "_$a7": 75,
        "_$Sr": 28,
        "_$77": 163,
        "_$EC": 94,

    }
    # 四位数组
    four_array = {
        195: 127,
        63: 224,
        97: 102,
        169: 181,
        154: 203,
        22: 102,
        175: 208,
        149: 126,
        162: 203,
        200: 240,
        189: 181,
        164: 11,
        208: 101,
        210: 225,
        185: 0,
        205: 103,
        197: 103,
        151: 108,
        114: 180,
        191: 100,

    }
    for key, value in index_function_name.items():
        ts_array[key] = ts_array[ts_array_944[value]]
    # 寻找四位数组的索引
    ts_array['_$a7'] = four_array.get(ts_array_944.index(ts_array['_$a7']))
    ts_array['_$Sr'] = four_array.get(ts_array_944.index(ts_array['_$Sr']))
    ts_array['_$77'] = four_array.get(ts_array_944.index(ts_array['_$77']))
    ts_array['_$EC'] = four_array.get(ts_array_944.index(ts_array['_$EC']))
    # rs5算法
    rs5_encrypt_js = open("rs5.js", "r").read()
    rs5_encrypt_str = f'''
        _$Iw = {ts_array}
        _$$N = {content_array}
        {rs5_encrypt_js}
        '''
    rs5_encrypt = execjs.compile(rs5_encrypt_str)
    cookie = rs5_encrypt.call("get_cookie")
    logger.info("cookie: {}".format(cookie))
    return cookie


def check_request(cookie):
    cookies = {
        "FSSBBIl1UgzbN7NP":  cookie
    }
    for i in range(2):
        response = session.get(url, headers=headers, cookies=cookies)
        logger.info("请求地址: {} 请求状态: {}".format(url, response.status_code))


if __name__ == '__main__':
    ts_array, content_array = get_202_index()
    cookie = get_cookie(ts_array, content_array)
    check_request(cookie)