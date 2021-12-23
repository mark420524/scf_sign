import time
import hmac
import hashlib
import base64
import urllib.parse
import requests

def generate_sign(sign_secret):

	timestamp = str(round(time.time() * 1000))
	
	secret_enc = sign_secret.encode('utf-8')
	string_to_sign = '{}\n{}'.format(timestamp, sign_secret)
	string_to_sign_enc = string_to_sign.encode('utf-8')
	hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
	sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
	
	return timestamp, sign


def push_msg(access_token, sign_secret, content):
	timestamp,sign = generate_sign(sign_secret)
	url = "https://oapi.dingtalk.com/robot/send?access_token=%s&timestamp=%s&sign=%s" % (access_token, timestamp, sign)

	headers = {
		"Content-Type": "application/json"
	}
	
	params = {
		"msgtype":"text",
		"text":{
			"content": content
		}
	}

	response = requests.post(url=url, headers=headers, data=str(params).encode("utf-8"))


