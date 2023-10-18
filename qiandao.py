# _*_ coding:utf-8 _*_

import requests
from bs4 import BeautifulSoup
import json

admin_url = "https://www.xianyudanji.cn/wp-admin/admin-ajax.php"
username = "" # 填你的用户名
pwd = "" #填你的密码

def login_and_get_session_and_get_cf_clearance():    
    login_payload = "action=user_login&username="+username+"&password="+pwd+"&rememberme=1"
    login_headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.xianyudanji.cn',
    'pragma': 'no-cache',
    'referer': 'https://www.xianyudanji.cn/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'Host': 'www.xianyudanji.cn'
    }
    try:
        session = requests.session()
        session.post(admin_url,headers=login_headers,data=login_payload)
    except requests.exceptions.RequestException as e:
        print("登录请求发生异常:", e)
    cf_clearance_url='https://www.xianyudanji.cn/cdn-cgi/challenge-platform/h/g/jsd/r/816034c4aa731583'
    cf_clearance_headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.xianyudanji.cn',
    'Referer': '',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Host': 'www.xianyudanji.cn'
    }
    try:
        cf_clearance_response = session.post(cf_clearance_url, headers=cf_clearance_headers)
    except requests.exceptions.RequestException as e:
        print("获取cf_clearance请求发生异常:", e)
    try:
        cf_clearance_cookie = requests.utils.dict_from_cookiejar(cf_clearance_response.cookies).get('cf_clearance')
        custom_cookie = {
            'cf_clearance': cf_clearance_cookie
        }
        session.cookies.update(custom_cookie)
        return session
    except requests.exceptions.RequestException as e:
            print("获取cf_clearance cookie发生异常:", e)

def get_nonce_and_balance(session):
    data_nonce = ''
    balance_values = ''
    index_url = "https://www.xianyudanji.cn/user/index"  
    try:
        index_response = session.get(index_url) 
        if index_response.status_code == 200:
            html_content = index_response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            data_nonce = soup.find('button', class_='go-user-qiandao')['data-nonce']
            balance_values = soup.find('span', class_='badge badge-warning-lighten').get_text(strip=True)
        else:
            print("请求nonce和balance失败，状态码:", index_response.status_code)
    except requests.exceptions.RequestException as e:
        print("请求nonce和balance发生异常:", e)
    return data_nonce, balance_values

def qiandao(session, data_nonce): 
    qiandao_payload = 'action=user_qiandao&nonce=' + data_nonce
    qiandao_headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.xianyudanji.cn',
        'referer': 'https://www.xianyudanji.cn/user/index',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'Host': 'www.xianyudanji.cn'
    }
    try:
        qiandao_response = session.post(admin_url, headers=qiandao_headers, data=qiandao_payload)
        return qiandao_response
    except requests.exceptions.RequestException as e:
        print("签到发生异常:", e)

def main():
    session = login_and_get_session_and_get_cf_clearance()
    data_nonce, old_balance_values = get_nonce_and_balance(session)
    qiandao_response = qiandao(session, data_nonce)
    if qiandao_response.status_code == 200:
        response_data = json.loads(qiandao_response.text)
        status = response_data["status"]
        msg = response_data["msg"]
        print("status：", status)
        print("msg：", msg)
        if status == '1':
            print("昨日余额：", old_balance_values)
            try:
                _, new_balance_values = get_nonce_and_balance(session)
                print("今日余额：", new_balance_values)
            except requests.exceptions.RequestException as e:
                print("获取今日余额请求发生异常:", e)
        else:
            if msg =='今日已签到，请明日再来':
                print("当前余额：", old_balance_values)
    else:
        print("签到失败，状态码:", qiandao_response.status_code)    
        print("签到失败:", qiandao_response.text)   

if __name__ == "__main__":
    main()        
