import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

def generate_sign(timestamp, secret):
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return sign

def download_image(url, folder_path, filename):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_path = os.path.join(folder_path, filename)
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"图片下载成功: {image_path}")
        return image_path
    else:
        print(f"图片下载失败: {url}")
        return None

def send_image_to_dingtalk(image_url, robot_webhook, secret):
    timestamp = str(round(time.time() * 1000))
    sign = generate_sign(timestamp, secret)
    webhook_url = f"{robot_webhook}&timestamp={timestamp}&sign={sign}"

    # 构建消息内容
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "60s图片",
            "text": f"![image]({image_url})"
        }
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200 and response.json().get('errcode') == 0:
        print("图片发送成功")
    else:
        print("图片发送失败")
        print(response.text)

# 主函数
def main():
    image_source_url = 'https://api.03c3.cn/api/zb'
    folder_path = '60s'
    filename = '01.jpg'
    
    # 先下载图片并保存
    local_image_path = download_image(image_source_url, folder_path, filename)
    
    if local_image_path:
        # 本地文件服务器路径
        local_server_image_url = '###'#提供一个支持https的稳定网站，要网站能访问到图片地址
        
        robot_webhook = '###'
        secret = '###'
        
        # webhook里是机器人地址，secret是加签
        send_image_to_dingtalk(local_server_image_url, robot_webhook, secret)

if __name__ == '__main__':
    main()
