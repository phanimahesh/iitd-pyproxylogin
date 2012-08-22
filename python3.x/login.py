#! /usr/bin/python3

#Import some modules to scare newbies, or may be to get things done.
# bs4 is BeautifulSoup version4, an awesome HTML/XML parser.
from bs4 import BeautifulSoup as soup  #Ah! me love soup!
import urllib.request, urllib.error, urllib.parse
#import sys
from getpass import getpass,GetPassWarning
from threading import Timer as Repeater

#Define a special confusing useless(?) wrapper function to accept user input.
def read_input(prompt,retries=3):
    while retries>0:
        try:
            inp=input(prompt)
            if inp!='':
                return inp
            else:
                print("\nI demand input!!!\nHow dare you give an empty reply?")
                i=i-1
                continue 
        except EOFError:
            print("\nI demand input!!!\nHow dare you throw a EOF at me?")
            i=i-1
    print("RAGEQUIT!!")
    exit()
	
proxycat=read_input("Enter proxy: http://www.cc.iitd.ernet.in/cgi-bin/proxy.")
userid=read_input("Enter your userid : ")

try:
    passwd=getpass("Enter your password : ")
    # This tries its best not to echo password
except GetPassWarning:
    print("Free advice: Cover your screen, just in case..")

proxyserv={'btech':'22','dual':'62','mtech':'62'}
# Check if proxycat is known to us.
try:
    address='https://proxy'+proxyserv[proxycat]+'.iitd.ernet.in/cgi-bin/proxy.cgi'
except KeyError:
    print("It looks like I dont know what your proxy server is.")
    print('https://proxyXX.iitd.ernet.in/cgi-bin/proxy.cgi')
    proxyserv[proxycat]=read_input("The XX is : ")
    address='https://proxy'+proxyserv[proxycat]+'.iitd.ernet.in/cgi-bin/proxy.cgi'

auto_proxy='http://www.cc.iitd.ernet.in/cgi-bin/proxy.'+proxycat
proxy=urllib.request.ProxyHandler({'auto_proxy':auto_proxy})
urlopener=urllib.request.build_opener(proxy)

print("Using category",proxycat)
print("PAC :",auto_proxy)
print("Login address:",address)
print("Reading login page...")

html = urlopener.open(address).read()
print("Login page loaded succesfully")
htmlsoup=soup(html)
sessionid=htmlsoup.input['value']

print("The session id is : "+sessionid)

loginform={'sessionid':sessionid,'action':'Validate','userid':userid,'pass':passwd}
response=urlopener.open(urllib.request.Request(address,urllib.parse.urlencode(loginform))).read()

loggedin_form={'sessionid':sessionid,'action':'Refresh'}
def refresh():
    Repeater(250.0,refresh).start()
    response=urlopener.open(urllib.request.Request(address,urllib.parse.urlencode(loggedin_form))).read()
    print("Heartbeat sent")

refresh()
