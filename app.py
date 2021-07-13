import os
import requests
import json
import pandas as pd
import sys

from flask import Flask, request, render_template, send_from_directory

sys.path.insert(0, os.path.dirname(__file__))
app = Flask(__name__, static_url_path="", static_folder="static")
application = app


@app.route('/', defaults={'page': 'index'}, methods=['GET'])
@app.route('/<page>')
def show(page):
    if page == 'index':
        sido = get_sido_info()["regionList"]
        return render_template('/%s.html' % page, sido=sido, len=len(sido))
    return render_template('/%s.html' % page)


'''
@app.route('/complexes/<string:searchStr>', methods=['POST'])
def complexes(searchStr):
    return {
        'searchStr': searchStr,
    }
'''


@app.route('/complexes/<string:searchStr>', methods=['GET'])
def complexes(searchStr):
    sido = list(pd.DataFrame(get_sido_info()["regionList"])["cortarNo"])[0]
    gungu = list(pd.DataFrame(get_gungu_info(sido)["regionList"])["cortarNo"])[0]
    dong = list(pd.DataFrame(get_dong_info(gungu)["regionList"])["cortarNo"])[0]
    apt = get_apt_list(dong)

    return {'result': apt}


@app.route('/complexes/getGunguInfo/<string:sidoCd>', methods=['POST'])
def getGunguInfo(sidoCd):
    return {'result': get_gungu_info(sidoCd)["regionList"]}


@app.route('/complexes/getDongInfo/<string:gunguCd>', methods=['POST'])
def getDongInfo(gunguCd):
    return {'result': get_dong_info(gunguCd)["regionList"]}


@app.route('/complexes/getAptList/<string:dongCd>', methods=['POST'])
def getAptList(dongCd):
    return get_apt_list(dongCd)


@app.route('/complexes/getAptInfo/<string:aptCd>', methods=['POST'])
def getAptInfo(aptCd):
    return {'result': get_apt_info(aptCd)}


def get_sido_info():
    down_url = 'https://new.land.naver.com/api/regions/list?cortarNo=0000000000'
    r = requests.get(down_url, verify=False, data={"sameAddressGroup": "false"}, headers={
        "Accept-Encoding": "gzip",
        "Host": "new.land.naver.com",
        "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    # temp=list(pd.DataFrame(temp["regionList"])["cortarNo"])
    return temp


def get_gungu_info(sido_code):
    down_url = 'https://new.land.naver.com/api/regions/list?cortarNo=' + sido_code
    r = requests.get(down_url, verify=False, data={"sameAddressGroup": "false"}, headers={
        "Accept-Encoding": "gzip",
        "Host": "new.land.naver.com",
        "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    return temp


def get_dong_info(gungu_code):
    down_url = 'https://new.land.naver.com/api/regions/list?cortarNo=' + gungu_code
    r = requests.get(down_url, verify=False, data={"sameAddressGroup": "false"}, headers={
        "Accept-Encoding": "gzip",
        "Host": "new.land.naver.com",
        "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    # temp=list(pd.DataFrame(temp['regionList'])["cortarNo"])
    return temp


def get_apt_list(dong_code):
    down_url = 'https://new.land.naver.com/api/regions/complexes?cortarNo=' + dong_code + '&realEstateType=APT&order='
    r = requests.get(down_url, verify=False, data={"sameAddressGroup": "true"}, headers={
        "Accept-Encoding": "gzip",
        "Host": "new.land.naver.com",
        "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    try:
        # temp=list(pd.DataFrame(temp['complexList'])["complexNo"])
        temp = temp
    except:
        temp = []
    return temp


def get_apt_info(apt_code):
    URL = "https://m.land.naver.com/complex/getComplexArticleList"

    param = {
        'hscpNo': apt_code,
        'tradTpCd': 'A1',
        'order': 'date_',
        'showR0': 'N',
    }

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Referer': 'https://m.land.naver.com/'
    }

    page = 0

    aptInfo = []

    while True:
        page += 1
        param['page'] = page

        resp = requests.get(URL, verify=False, params=param, headers=header)
        if resp.status_code != 200:
            break

        data = json.loads(resp.text)
        result = data['result']
        if result is None:
            break

        for item in result['list']:
            aptInfo.append(item)

        if result['moreDataYn'] == 'N':
            break

    return aptInfo


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/v[nd.microsoft.icon')


if __name__ == '__main__':
    app.run()
