#!/usr/bin/python
import sys
import getopt
import re
try:
    import urllib2 # py2
except ImportError:
    import urllib.request as urllib2 # py3
    from urllib.request import urlopen
import requests
import socks
import socket
import argparse
import logging
import string
import random
import time
from sockshandler import SocksiPyHandler
from multiprocessing.pool import ThreadPool as Pool

parser = argparse.ArgumentParser(description="PLeech is yet another proxy leecher and checker, with many other features")
group = parser.add_mutually_exclusive_group(required=True) #group required, because must be added one of group
group.add_argument("-u", "--url", help="URL to get proxies from")
group.add_argument("-U", "--urls-list",metavar="FILE", help="URLs list file to get proxies from")
group.add_argument("-p", "--proxy", metavar="IP:PORT", help="proxy to check, must be as form {ip:port}")
group.add_argument("-P", "--proxies-list", metavar="FILE",help="proxies list file to check line by line[first line ip:proxy,2nd line ip2:port2...etc]")
group2 = parser.add_mutually_exclusive_group(required=True)
group2.add_argument("-f", "--force", help="Try to bruteforce proxy type and check which one the proxy is",action='store_true') #action='store_true' because no arg is needed
group2.add_argument("-t", "--type", choices=["http","socks4","socks5"], help="Set the proxy type") #choices for choose only one of them
parser.add_argument("-c", "--check-listed", help="check the proxy if listed in opened proxies (abusing list)",action='store_true') #action='store_true' because no arg is needed
parser.add_argument("-d", "--delay", metavar="SEC", type=float ,help="The timeout while checking proxy and stop the process to the next one {min.sec}, (default is 5.0)",default=5.0) #type=float  because the argument must treated as float number
parser.add_argument("-T", "--thread", type=int, help="multithreading for faster process", default=1)
parser.add_argument("-i", "--irc-test",metavar="SERVER:PORT", help="check the proxy if works as an irc proxy") #action='store_true' because no arg is needed
parser.add_argument("-s", "--save-list", metavar="FILE", help="save the working proxies to specific file", required=True) #require, because -s must be taken
parser.add_argument("-v", "--verbose", action='count', help="show some details (-vv for more)") # this action will equal (-v 3) = -vvv
parser.add_argument("--version", action="version", version="%(prog)s 1.1") #special action for version, %(prog)s will print the program name
args = parser.parse_args()
argsdict = vars(args)

#initial values:
urlslist = []
proxieslist = []
workingproxies = []
proxiesdict = dict()
testloc = "https://4.ifcfg.me/"
proxynumber=0


#function to get html content from a url
def fitch(url):
   r = requests.get(url)
   content = r.text
   return content

#function to get lines from file and put them into list

def getlines(File):
   lineslist = []
   with open(File) as f:
      Filelist = f.readlines()
      for line in Filelist:
         line = line.replace("\n","")
         lineslist.append(line)
   return lineslist

#function to make dictinory ips/ports from an ips/ports list
def mkdict(ipports):
    proxydict = {}
    for ipport in ipports:
        ip = ipport.split(':')[0]
        port = int(ipport.split(':')[1])
        proxydict.update({ip : port})
    return proxydict

def extractproxies(content):
#   print (content)
   content = re.sub(r"([^0-9][54][^0-9])", " ", content)
#   content = re.sub('[^0-9:.]+', '', content)
   content = re.sub('([a-zA-Z</td>},{"=&])', ":", content)
   content = re.sub("\:+", ":", content)
#   print content
#   here is my piece of "ART" :P
   pattern = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)([ (\[]?(\.|dot)[ )\]]?(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}[\s,:]([0-6][0-5][0-5][0-3][0-5]|[0-6][0-5][0-5][0-2]\d{1}|[0-6][0-5][0-4]\d{2}|[0-6][0-4]\d{3}|[0-5]\d{4}]|\d{1,4}))"
   regex = re.compile(pattern)
   leechedproxies = [each[0] for each in regex.findall(content)]
   for item in leechedproxies: #get the repeated regex in all the text
      location = leechedproxies.index(item)
      ip = re.sub("[ ()\[\]]", "", item)
      ip = re.sub("dot", ".", ip)
      leechedproxies.remove(item)
      leechedproxies.insert(location, ip)
#      print (leechedproxies)
      proxiesdict = mkdict(leechedproxies)
      return proxiesdict

def checkproxy(proxytype,ip,port,urltookfrom,testloc,ircserver,ircport,checklisted):

   numwork = 0 #number of working proxie

   print ("IP : " + str(ip))
   print ("PORT : " + str(port))

   if proxytype == "http":
      proxytype = socks.PROXY_TYPE_HTTP
   elif proxytype == "socks4":
      proxytype = socks.PROXY_TYPE_SOCKS4
   elif proxytype == "socks5":
      proxytype = socks.PROXY_TYPE_SOCKS5
   isworking = False #flag if current proxy is working
   islisted = False #flag if the current proxy is listed as open proxy (not secure proxy)
   if ircserver:
      try:
         s = socks.socksocket()
         nicklength = random.randint(3,14)
         nick = "".join(random.choice(string.letters) for _ in range(nicklength))
         s.setproxy(proxytype, ip, port)
         s.connect((ircserver, ircport))
         s.send("USER "+ nick +" "+ nick +" "+ nick +" :"+ nick +"\n")
         s.send("NICK "+ nick +"\n")
         while 1:
            ircmsg = s.recv(1024)
            ircmsg = ircmsg.strip('\n')
            ircmsg = ircmsg.lower()
            print (ircmsg)
            if ircmsg != "":
               if ircmsg.find("checking ident")!= -1:
                  isworking = True
                  print ("State: WORKING.\n")
               else:
                  print ("State: IP is up, but not working as proxy.\n")
#                  s.close()
            s.close()
#               break
#               time.sleep(1)
      except Exception as error:
         s = None
         print ("State: "+ str(error) + "\n")
#         s.close()
#         continue
   else:
#      data=''
      try:
         opener = urllib2.build_opener(SocksiPyHandler(proxytype, ip, port))
         data = opener.open(testloc).read()
#         print (data)
         fafa = data.decode(encoding='utf-8')
         print (fafa)
         if fafa.find(str(ip))>-1:
            if fafa.find("Country")>-1:
               isworking = True
      except Exception as error:
         print ("Failed, Reason: " * format(error))
   if isworking == True:
      numwork = numwork+1
      if checklisted:
         content = fitch("https://dronebl.org/lookup?ip="+ip)
         if content.find( "There have been listings for the host")!=-1:
            islisted = True
            print ("Listed")
         else:
            islisted = False
            print ("Not Listed")
      workingproxies.append(ip + ":" + str(port) + ":" + args.type + ":" + str(islisted) + ":" + str(delay) + str(urltookfrom))
      savelistfile = open(args.save_list, "a")
      savelistfile.write(ip + ":"+ str(port) + ":" + args.type + ":"+ str(islisted) + ":"+ str(delay) + ":"+ str(urltookfrom) + "\n" )
      savelistfile.close()
   return workingproxies #,workingleech


#set values from parameters taken from command line to familiar variables
force = args.force
if args.irc_test:
   ircserver = args.irc_test.split(":")[0]
   ircport = int(args.irc_test.split(":")[1])
else:
   ircserver = None
   ircport = None

checklisted = args.check_listed
delay = args.delay
thread = args.thread
pool_size = thread  # your "parallelness"
pool = Pool(pool_size)
verbose = args.verbose



#workingleech=[]


#setting options:
if args.url:
   urlslist.append(args.url)
if args.urls_list:
   urlslist = getlines(args.urls_list)
if args.proxy:
   proxieslist.append(args.proxy)
   proxieslist2string = "".join(proxieslist)
   proxiesdict = extractproxies(proxieslist2string)
if args.proxies_list:
   proxieslist = open(args.proxies_list, "r")
   proxieslist2string = "".join(proxieslist)
   proxiesdict = extractproxies(proxieslist2string) #getting proxies dictionary using regex by extractproxies function
#   proxieslist = getlines(args.proxies_list)

#if verbose:
#   logging.basicConfig(level=logging.DEBUG)
if delay:
   socket.setdefaulttimeout(delay)
savelistfile = open(args.save_list, "w")
savelistfile.close()


def thread(proxiesdict,urltookfrom):
   for ip in proxiesdict:
      port = proxiesdict[ip]
      if force:
         for proxytype in ["http","socks4","socks5"]:
            pool.apply_async(checkproxy, (proxytype,ip,port,urltookfrom,testloc,ircserver,ircport,checklisted)).get(timeout=10)
      else:
         proxytype = args.type
         pool.apply_async(checkproxy,(proxytype,ip,port,urltookfrom,testloc,ircserver,ircport,checklisted)).get(timeout=10)

def run():
   if urlslist == []:
      print ("Testing "+ str(len(proxiesdict)) + " proxies.")
      thread(proxiesdict,None)
   else:
        for urltookfrom in urlslist:
            try:
                print ("leeching from " + urltookfrom)
                content = fitch(urltookfrom)
                proxiesdictleeched = extractproxies(content)
                if proxiesdictleeched:
                   print ("learned from " + urltookfrom + " " + str(len(proxiesdictleeched)) + " proxies")
                   thread(proxiesdictleeched, urltookfrom)
                else:
                   print ("I read it but I learned nothing from " + urltookfrom )
            except Exception as error:
                print ("couldn't leech the url: " + urltookfrom)
                print ("Failed, Reason: " .format(error))
   print (workingproxies)

run()


'''
#saving working proxies to the output
savelistfile.write("\n".join(set(workingproxies)))
#leeched.write("\n".join(set(workingleech)))
'''
