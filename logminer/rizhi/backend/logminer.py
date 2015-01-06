#!/bin/env python
#coding=utf8
import json
import get_source_ip
import threading
import socket,struct
import time,datetime
#f=file('access_20141102.log')

def ip_ranges():
    f = file('/home/redking/zhj/squid_web/rizhi/backend/ipv2.txt')
    ip_range_key_list = []
    ip_dic = {}
    for line in f.xreadlines():
        line = line.split('|')
        ip_start, ip_end, ip_long_start, ip_long_end,country, province,city,district,isp,isp_id = line
        ip_dic[int(ip_long_start)] = {
            'ip_start' : ip_start,
            'ip_end': ip_end,
            'ip_long_end': int(ip_long_end),
            'ip_long_start': int(ip_long_start),
            'country': country,
            'province': province,
            'city': city,
            'district': district,
            'isp': isp,
            'isp_id': isp_id
        }
        ip_range_key_list.append(int(ip_long_start))
    ip_range_key_list.sort()
    #print sys.getsizeof(ip_range_key_list)/1024, sys.getsizeof(ip_dic)/1024
    return ip_range_key_list,ip_dic

def BSearch(ip_data, key):
    """
    Binary Search:
    Stored the items in a sorted list
    Algorithm: division of integers 
    return the floor of the quotient
    """
    li, ip_db = ip_data
    
    low = 0
    high = len(li) - 1
    i = 0
    while low <= high:
        
        i = i + 1
        mid = (low+high) / 2
        #print 'Low: %s    High: %s   Start: %s    End:%s ' %(low,high, li[low], li[high])
        if key == li[mid]:          # found the key
            #print "Got %d with index[%d] in %d times." % (key, mid, i)
            
            #return ip_db[key]['isp_id']
            return ip_db[key]['province']
        else:
            if key < li[mid]:        # key before the middle
                 high = mid -1
            else:                     # key after the middle
                 low = mid + 1       
    else:
        #print "No key: %d " % key, low, high
        try:
            #if key > li[high] and key< li[low]: 
            ip_range_end_high = ip_db[li[high]]['ip_long_end'] # get the ip_long_end   
            ip_range_end_low = ip_db[li[low]]['ip_long_end'] # get the ip_long_end   
            if key >= li[high] and  key <= ip_range_end_high:
                #print 'Key %s must between %s and %s'  %(key,li[high], li[low])
                ip_result = ip_db[li[high]]
                
                #for k,v in ip_result.items():
                #    print '-->',k,v
                return ip_result['province']
            elif key >= li[low] and  key<= ip_range_end_low:
                ip_result = ip_db[li[low]]
                #for k,v in ip_result.items():
                #    print '==>',k,v 
                return ip_result['province']
            else:
                #print 'No key found :\033[31;1m%s\033[0m' % key
                return '99999'
        except IndexError,err:
            print err

def handel(date1,date2):
	filename_list=[]
	date_list=[]
	static_dic=[]
	url="/home/redking/zhj/squid_web/rizhi/backend/apissl_"
	date1=int(date1)
	date2=int(date2)
	while date1 <= date2:
		date_s=time.strftime("%Y%m%d",(time.localtime(date1)))
		print date1,date2,
		filename=url+date_s+'.log'
		filename_list.append(filename)
		date1 +=86400
	for x in filename_list:
		try:
			f=file(x)
			date_list.extend(f.readlines())
		except IOError:
			static_dic=["Warning: No log file for %s" %(x.split("/")[-1])]
			print static_dic
			pass
	pv_dic={'total_pv':0}
	uv_dic={}
	region_dic={}
	cache_type_dic={}
	req_size=''
	result_dic={}
	p_times={'p_time1':0,
		 'p_time2':0,
		 'p_time3':0,
		 'p_time4':0,
		 'p_time5':0}
	for line in date_list:
		line = line.split()
		raw_ip,access_url,cache_type,response_size,process_time= line[0],line[3],line[8],line[9],line[-1]
		pv_dic['total_pv'] +=1
		#uv
		if uv_dic.has_key(raw_ip):
			uv_dic[raw_ip][0] +=1
		else:
			uv_dic[raw_ip] =[1]
		region_ip='.'.join(raw_ip.split('.')[:2])
		if region_dic.has_key(region_ip):
			region_dic[region_ip][0] +=1
		else:
			region_dic[region_ip] =[1,raw_ip]
		#print region_dic,
		#handle request status
		if cache_type != '"-"':
			if cache_type_dic.has_key(cache_type):
				cache_type_dic[cache_type] +=1
			else:
				cache_type_dic[cache_type] =1
		#handle request sizes
		req_size= req_size +response_size
		
		#this is process times
		p_time=process_time.split('"')[-2]
		
		#print type(p_time)
		if p_time < str(0.2):
			p_times['p_time1'] +=1
		elif p_time < str(0.7):
			p_times['p_time2'] +=1
		elif p_time < str(1.5):
			p_times['p_time3'] +=1
		elif p_time < str(3):
			p_times['p_time4'] +=1
		else: 
			p_times['p_time5'] +=1
	sorted_region_list=sorted(region_dic.items(),key=lambda x:x[1][0], reverse = False)
	sorted_ptimes_list=sorted(p_times.items(),key=lambda x:x[0],reverse = False)
	#print  sorted_ptimes_list,
	result_dic ={'sorted_ptimes_list':sorted_ptimes_list,
		 'sorted_region_list':sorted_region_list,
		 'cache_type'	     :cache_type_dic,
		 'pv_dic'	     :pv_dic,
		 'uv_dic'            :uv_dic,
		 'static_dic'	     :static_dic
		}				
	self_result=ip_ranges()
        uv_list=result_dic.get('uv_dic')
        #sorted_region_list=result_dic.get('sorted_region_list')
        #for i in sorted_region_list:
        for i,y in uv_list.items():
                #print i,y[0],
                IP=i
                IP_long=struct.unpack("!I",socket.inet_aton(IP))[0]
                IP_province=BSearch(self_result,IP_long)
                #print IP_province,
                y.append(IP_province)
	#print result_dic,'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
	return result_dic,


if __name__ == '__main__':
	#redis={}
	result = handel('1414857600','1414857600')
	#redis['log'] = json.dumps(result)
	#result = list(tuple(result))[0]
	#self_result=ip_ranges()
	#print '6666666666666666666', result,'&&&&&&&&&&&&&&&'
	#sorted_region_list=result.get('sorted_region_list')
	#for i in sorted_region_list:
        #	print i[1][1],'||||||||||中国'
        #       	IP=i[1][1]
        #       	IP_long=struct.unpack("!I",socket.inet_aton(IP))[0]
        #       	IP_province=BSearch(self_result,IP_long)
	#	print IP_province,
	#	i[1].append(IP_province)
	#	
	##result['sorted_region_list']=new_region_list
	##return result,
               
	



