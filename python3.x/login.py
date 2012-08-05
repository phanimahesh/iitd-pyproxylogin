#! /usr/bin/python

from BeautifulSoup import BeautifulSoup as soup
import urllib.request, urllib.error, urllib.parse,urllib.request,urllib.parse,urllib.error,sys,threading
from getpass import getpass

proxycat=input("Enter proxy: http://www.cc.iitd.ernet.in/cgi-bin/proxy.")
userid=input("Enter your userid : ")
passwd=getpass("Enter your password : ")

auto_proxy='http://www.cc.iitd.ernet.in/cgi-bin/proxy.'+proxycat
proxy=urllib.request.ProxyHandler({'auto_proxy':auto_proxy})
urlopener=urllib.request.build_opener(proxy)
proxyserv={'btech':'22','dual':'62','mtech':'62'}
address='https://proxy'+proxyserv[proxycat]+'.iitd.ernet.in/cgi-bin/proxy.cgi'

print("Using category",proxycat)
print("PAC :",auto_proxy)
print("Login address:",address)

html = urlopener.open(address).read()
htmlsoup=soup(html)
sessionid=htmlsoup.input['value']

print("The session id is : "+sessionid)

loginform={'sessionid':sessionid,'action':'Validate','userid':userid,'pass':passwd}
response=urlopener.open(urllib.request.Request(address,urllib.parse.urlencode(loginform))).read()

loggedin_form={'sessionid':sessionid,'action':'Refresh'}
def refresh():
    threading.Timer(250.0,refresh).start()
    response=urlopener.open(urllib.request.Request(address,urllib.parse.urlencode(loggedin_form))).read()

refresh()
