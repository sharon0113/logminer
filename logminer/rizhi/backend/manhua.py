#!/usr/bin/env python

import sys,os 
import time
#cartoon_name_dic={}
#f=file('yiqiding_20141224.log')
#print f.readline(),
#line=f.readline()
def check():
	cartoon_name_dic={}
	filename_list=[]
	log_list=[]
	url="/home/redking/zhj/squid_web/rizhi/backend/yiqiding_"
	date1=int('1417363200')
	date2=int(time.time())
	while date1 < date2 :
		date_s=time.strftime("%Y%m%d",(time.localtime(date1)))
		#print date_s,
		filename=url+date_s+'.log'
		filename_list.append(filename)
		date1 += 86400
	for i in filename_list:
		try:
			f=file(i)
			log_list.extend(f.readlines())
		except IOError:
			pass
		
	for line in log_list:
		line=line.split('\"')
		log_url=line[1]
		cartoon_start=log_url.split()[1].split('/')[1]
		cartoon_php=log_url.split()[1].split('/')[-1]	
		#print cartoon_php,'__________________'
		if cartoon_php !='':
			cartoon_name=cartoon_php.split('.')[0]
			try:
				if cartoon_php.split('.')[1]== 'php' and cartoon_start == 'animation':
					if cartoon_name_dic.has_key(cartoon_name):
						cartoon_name_dic[cartoon_name] +=1	
					else:
						cartoon_name_dic[cartoon_name] =1
			except IndexError:
				pass
	return cartoon_name_dic,



if __name__== '__main__':
	result=check()
