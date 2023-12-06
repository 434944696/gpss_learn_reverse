import execjs
import requests
import json
session = requests.session()
encrypt = open('test.js', encoding='utf-8').read()
get_header_en = execjs.compile(encrypt)


def get_data(host):
    headers = get_header_en.call('get_token', host)
    headers['content-type'] = "application/json"

    url = "https://icp.chinaz.com/index/api/queryPermit"
    data = {
        "keyword": host
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers,  data=data)
    print(response.text)
    print(response)


if __name__ == '__main__':
    get_data('oscs1024.com')