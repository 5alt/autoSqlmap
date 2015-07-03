# -*- coding: utf-8 -*-
import multiprocessing
import sys,time
import requests

from lib.proxy2 import ProxyRequestHandler, ThreadingHTTPServer

import config
import myproxy
import myinjector

def banner():
	print '''
	               __          _________      .__                         
_____   __ ___/  |_  ____ /   _____/ _____|  |   _____ _____  ______  
\__  \ |  |  \   __\/  _ \\_____  \ / ____/  |  /     \\__  \ \____ \ 
 / __ \|  |  /|  | (  <_> )        < <_|  |  |_|  Y Y  \/ __ \|  |_> >
(____  /____/ |__|  \____/_______  /\__   |____/__|_|  (____  /   __/ 
     \/                          \/    |__|          \/     \/|__|    

    simple http(s) proxy with python based sqlmapapi wrapper
    Author: md5_salt (http://5alt.me)
'''

def TestSqlmapAPI():
	try:
		requests.get(config.sqlmap_host, timeout=1)
		return True
	except:
		return False

def RunProxy():
	server_address = ('', config.proxy_port)

	HandlerClass = myproxy.myproxy
	ServerClass = ThreadingHTTPServer
	protocol="HTTP/1.1"

	HandlerClass.protocol_version = protocol
	httpd = ServerClass(server_address, HandlerClass)

	sa = httpd.socket.getsockname()
	print "Serving HTTP Proxy on", sa[0], "port", sa[1], "..."
	httpd.serve_forever()

if __name__ == '__main__':
	banner()
	if not TestSqlmapAPI():
		print "Please start sqlmapapi first!"
		sys.exit(0)
	config.queue = multiprocessing.Queue()
	p = multiprocessing.Process(target=RunProxy)
	p.start()

	myinjector.myinjector().run()