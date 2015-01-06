#!/user/bin/evn python


import json,urllib2


def get_region(url):
	#res = urllib2.Request(url)
	result = urllib2.urlopen(url)
	region_ip_dic = json.loads(result.read())
	#return region_ip_dic
#	print region_ip_dic,
#
#	print region_ip_dic['data']['area']
	print region_ip_dic['data']['region']
	print region_ip_dic['data']['ip']



#get_region('http://ip.taobao.com/service/getIpInfo.php?ip=112.224.19.48')
#get_region('http://ip.taobao.com/service/getIpInfo.php?ip=24.84.130.104')
