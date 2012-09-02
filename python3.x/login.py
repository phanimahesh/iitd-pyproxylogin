#! /usr/bin/python3

# Author      : J Phani Mahesh
# Description : A python3 utility to log into IITD proxy servers.
# Home        : http://phanimahesh.github.com/iitd-pyproxylogin
# Blog        : http://phanimahesh.wordpress.com
# Bugs        : Report bugs to phanimahesh.ee510 [at] ee.iitd.ac.in

# Import some modules to scare newbies, or may be to get things done.
# bs4 is BeautifulSoup version4, an awesome HTML/XML parser.
from bs4 import BeautifulSoup as soup,SoupStrainer as limiter
import urllib.request, urllib.error, urllib.parse
import sys
from getpass import getpass,GetPassWarning
import time
# TODO : If modules don't exist, offer to download them.

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
    print("RAGEQUIT!!") # :-(
    sys.exit(255)

# TODO : Offer config file support.
proxycat=read_input("Enter proxy: http://www.cc.iitd.ernet.in/cgi-bin/proxy.")
userid=read_input("Enter your userid : ")

try:
    passwd=getpass("Enter your password : ")
    # This tries its best not to echo password
except GetPassWarning:
    print("Free advice: Cover your screen, just in case..")

proxyserv={'btech':'22','dual':'62','mtech':'62','faculty':'81'}
# Check if proxycat is known to us. C'mon, you cant know everything. Ask if needed.
try:
    address='https://proxy'+proxyserv[proxycat]+'.iitd.ernet.in/cgi-bin/proxy.cgi'
except KeyError:
    print("It looks like I dont know what your proxy server is.")
    print('https://proxyXX.iitd.ernet.in/cgi-bin/proxy.cgi')
    proxyserv[proxycat]=read_input("The XX is : ")
    address='https://proxy'+proxyserv[proxycat]+'.iitd.ernet.in/cgi-bin/proxy.cgi'

# Le Proxy handling system
auto_proxy='http://www.cc.iitd.ernet.in/cgi-bin/proxy.'+proxycat
proxy=urllib.request.ProxyHandler({'auto_proxy':auto_proxy})
urlopener=urllib.request.build_opener(proxy)

# Le confirmation messages
print("Using category",proxycat)
print("PAC :",auto_proxy)
print("Login address:",address)
print("Reading login page...")

# Loading login page
try:
    html = urlopener.open(address).read()
except Error as e:
    print("There was an error retrieving the login page.\nExiting....")
    # TODO: Check network and report accordingly. C'mon, be intelligent!
    sys.exit(1)
print("Login page loaded succesfully")

# I'm Hungry. Make me a soup.
htmlsoup=soup(html,parse_only=limiter("input"))
sessionid=htmlsoup.input['value']
# TODO : Exception handling. Add some intelligence buddy.
print("The session id is : "+sessionid)

# Le Forms
login_form={'sessionid':sessionid,'action':'Validate','userid':userid,'pass':passwd}
loggedin_form={'sessionid':sessionid,'action':'Refresh'}
logout_form={'sessionid':sessionid,'action':'logout'}

# Le POST-able binary stream maker
def yunoencode(form):
    return urllib.parse.urlencode(form).encode('ascii')

# Le POST-able binary stream data
login_data=yunoencode(login_form)
loggedin_data=yunoencode(loggedin_form)
logout_data=yunoencode(logout_form)

response=urlopener.open(urllib.request.Request(address,login_data)).read()
print("You are now logged in.")
# TODO : Check if *really* logged in

# Le Functions
def refresh():
    response=urlopener.open(urllib.request.Request(address,loggedin_data)).read()
    print("Heartbeat sent at "+time.asctime())

def logout():
    response=urlopener.open(urllib.request.Request(address,logout_data)).read()
    # TODO : Verify if *really* logged out
    print("Logged out succesfully.")

# Le Keep-me-logged-in thingy
try:
    while True:
        time.sleep(240)
        refresh()
except KeyboardInterrupt as e:
    print("Keyboard Interrupt recieved.")
    logout()
    print("""
Thank you for using pyproxylogin.
Report any problems encountered to J Phani Mahesh.
He can be reached at phanimahesh.ee510 [at] ee.iitd.ac.in
Have a nice day!
""")
    sys.exit(0)
  # It is customary to exit with zero status on success
