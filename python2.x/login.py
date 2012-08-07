#! /usr/bin/python

#Import some modules to scare newbies, or may be to get things done.
from BeautifulSoup import BeautifulSoup as soup  #Ah! me love soup!
import urllib2,urllib,sys,threading
from getpass import getpass

#Define a special confusing useless(?) wrapper function to accept user input.
def read_input(prompt):
    while True:
        try:
            inp=raw_input(prompt)
            return inp
        except EOFError:
            print """
You just broke my heart. Can't I even expect some input?
Still, I choose to give you another chance.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
	
proxycat=read_input("Enter proxy: http://www.cc.iitd.ernet.in/cgi-bin/proxy.")
userid=read_input("Enter your userid : ")

try:
    passwd=getpass("Enter your password : ")
except GetPassWarning:
    pass

proxyserv={'btech':'22','dual':'62','mtech':'62'}
# Check if proxycat is known to us.
try:
    address='https://proxy'+proxyserv[proxycat]+'.iitd.ernet.in/cgi-bin/proxy.cgi'
except KeyError:
    print "It looks like I dont know what your proxy server is."
    print 'https://proxyXX.iitd.ernet.in/cgi-bin/proxy.cgi'
    proxyserv[proxycat]=read_input("The XX is : ")
    address='https://proxy'+proxyserv[proxycat]+'.iitd.ernet.in/cgi-bin/proxy.cgi'

auto_proxy='http://www.cc.iitd.ernet.in/cgi-bin/proxy.'+proxycat
proxy=urllib2.ProxyHandler({'auto_proxy':auto_proxy})
urlopener=urllib2.build_opener(proxy)

print "Using category",proxycat
print "PAC :",auto_proxy
print "Login address:",address
print "Reading login page..."

html = urlopener.open(address).read()
print "Login page loaded succesfully"
htmlsoup=soup(html)
sessionid=htmlsoup.input['value']

print "The session id is : "+sessionid

loginform={'sessionid':sessionid,'action':'Validate','userid':userid,'pass':passwd}
response=urlopener.open(urllib2.Request(address,urllib.urlencode(loginform))).read()

loggedin_form={'sessionid':sessionid,'action':'Refresh'}
def refresh():
    threading.Timer(250.0,refresh).start()
    response=urlopener.open(urllib2.Request(address,urllib.urlencode(loggedin_form))).read()
    print "Heartbeat sent"

refresh()
