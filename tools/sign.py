import hmac
import hashlib

#签名算法函数hmac_sha256
def addSign(p_dict, app_secret):
	try:
		para_list = []
		for key in sorted(p_dict.keys()):
			if key != 'sign':
				param = "%s=%s" % (key, p_dict[key])
				para_list.append(param)
		content = '&'.join(para_list)

		message = content.encode('utf-8')
		secret = app_secret.encode('utf-8')

		# signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
		signature = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
		return signature

	except Exception as err:
		print(u"签名异常", err)
