#coding=utf8
from __future__ import division
from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from backend.logminer import handel
from backend.manhua import check
import sys,os,time,json
from django.contrib import auth
from rizhi.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
	return render_to_response('login.html') 
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    #user=User.objects.filter(username=username,password=password)
    user = auth.authenticate(username=username, password=password)
    print user,'?????????'
    #if len(user):
    if user is not None:
        auth.login(request, user)
        #Redirect to a success page.
        return HttpResponseRedirect("/main")
    else:
    	return render_to_response('login.html',{'login_err':'wrong username or password!'})

@login_required
def main(request):
	return render_to_response('main.html')

@login_required
def get_log(request):
        start=request.GET['start_d']
	end=request.GET['end_d']
	start=start[:-3]
	end=end[:-3]
        #log_data = handel("/home/redking/zhj/squid_web/rizhi/backend/access_20141102.log")
	if start =='':
		start= int(time.time())-86400
	if end =='':
		end = start
        log_data = handel(start,end)
        #print type(log_data),'********************'
        log_data_dic=list(log_data)[0]
        #print log_data_dic,
	log_data_list=log_data_dic.get('sorted_ptimes_list')
	#print log_data_list,'>>>>>>>>>>>>>>'
	cache_type=log_data_dic.get('cache_type')
	#print type(cache_type),cache_type,'>>>>>>>>>>>>>>>>>>>>'
	total_pv=log_data_dic['pv_dic']['total_pv']
	uv=len(log_data_dic['uv_dic'])
	souce_ip=log_data_dic['uv_dic']
	static=log_data_dic['static_dic']
        name=[]
        data=[]
        numeber=0
        data_list=[]
        data_dic=[]
        #data_dic_list=[]
	souce_ip_dic={}
	souce_dic={}
	souce_list=[]
	cache_list=[]
        for i in log_data_list:
                name.append(i[0])
		#print i[1],'<<<<<<<<<<<<<<<<<<'
                numeber += i[1]
                data.append(i[1])
        for y in data:
		try:
                	data_list.append(round(int(y)*100/int(numeber),3))
		except ZeroDivisionError:
			pass
        #print name,numeber,data_list,'????????????????????'
        for y in range(len(name)):
		try:
                	data_dic_list=[name[y],data_list[y]]
                	data_dic.append(data_dic_list)
		except IndexError:
			pass
	for x in souce_ip.items():
		souce_ip_pro=x[1][1]
		if souce_ip_dic.has_key(souce_ip_pro):
			souce_ip_dic[souce_ip_pro] += 1
		else:
			souce_ip_dic[souce_ip_pro]= 1
	for i in souce_ip_dic.items():
		#print i,'||||||||||||||||||'
		souce_dic={ 'name': i[0],
			    'value': i[1]}
		#print souce_dic,
		souce_list.append(souce_dic)
	for i in cache_type.items():
		try:
			cache_type_list=[str(i[0]),round(i[1]*100/int(total_pv),3)]
		except ZeroDivisionError, msg:
			print msg,'??????????????'
			pass
		#print cache_type_list,'??????????????????'
		cache_list.append(cache_type_list)
	return_dic={'total_pv'  :total_pv,
		    'uv'        :uv,
		    'data_dic'  :data_dic,
		    'cache_list':cache_list,
		    'souce_list':souce_list,
		    'static'    :static}
	#print return_dic,')))))))))))))))'
        return HttpResponse (json.dumps(return_dic))      
	
@login_required	
def cartoon(request):
	cartoon_list=check()
	cartoon_dic=cartoon_list[0]
	return HttpResponse (json.dumps(cartoon_dic))
def logout_view(request):
	auth.logout(request)
	return HttpResponseRedirect("/index")
	#return render_to_response('login.html')
