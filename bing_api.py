#coding=utf-8

mind_html = ''

file_name = ''

import requests,re,sys
import netaddr
import struct
import socket
from sys import argv


def ip2int(addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]
def int2ip(addr):
        return socket.inet_ntoa(struct.pack("!I", addr))

def RegexC(reg,str):
	p1 = reg
	pattern1 = re.compile(p1)
	matcher1 = re.findall(pattern1,str)
	return matcher1

def getNextUrl(html):
	tmp = RegexC('<a class="sb_pagN"(.*?)</a>',html)
	if len(tmp)==0:
		return 'done'
	for x in tmp:
		# print x
		url =  RegexC('href="(.*?)"',x)
		url = 'https://www.bing.com'+url[0]
		url = url.replace('amp;','')
		return url


def getNewx():
	pass


def BingWebSearch(url):
	global mind_html
	p1 = '<li class="b_algo"(.*?)</h2>'
	pattern1 = re.compile(p1)
	r = requests.get(url)

	matcher1 = re.findall(pattern1,r.text)
	# print matcher1
	

	print len(matcher1)
	for x in matcher1:
		x = x.replace('><div class="b_title"><h2>','')
		x = x.replace('><h2>','')

		mind_html+='<li class="">'+x+'</li>'
		print '<li class="">'+x+'</li>'
		pass

	print '=' * 130
	nexturl = getNextUrl(r.text)
	print nexturl
	print '#' * 130
	return nexturl

  # print r.text
	pass



def main(ip):

	global mind_html
	mind_html += '<li><a href="#" ref="#">'+ip+'</a></li>'
	mind_html += '<ul>'
	result = BingWebSearch('https://www.bing.com/search?q=ip%3a'+str(ip))
	while result != 'done':
		result = BingWebSearch(result)
 	mind_html +='</ul>'

 	outfile()

def outfile():
	global file_name
	file_object = open('./result/demo.html')
	all_the_text = file_object.read()

	start_html = all_the_text[0:all_the_text.find('<!-- #####C_INFO##### -->')]
	end_html = all_the_text[all_the_text.find('<!-- #####C_INFO##### -->'):]

	file_object = open('./result/'+file_name+'.html', 'w')
	file_object.write(start_html+mind_html+end_html)
	file_object.close()
	pass

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')



	if argv[1] != '':
		ips = argv[1]
		if '-' in ips:
			start, end = ips.split('-')
			startlong = ip2int(start)
			endlong = ip2int(end)
			ips = netaddr.IPRange(start,end)
			for x in ips:
				main(x)


		# file_name = argv[1]
		# for x in xrange(1,256):
		# 	main(argv[1]+str(x))
		# 	pass
	else:
		print 'xx.py 192.168.1.1-192.168.2.1'


