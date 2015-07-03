# -*- coding: utf-8 -*-
import re
import urlparse
import uuid
import sys
import md5
import os.path
import time

from lib.sqlmapapiwrapper import SqlmapAPIWrapper
from lib.proxy2 import ProxyRequestHandler, ThreadingHTTPServer
import config

class myproxy(ProxyRequestHandler):

	query_log = {}

	def check_history(self, key):
		try:
			self.query_log[key]
			return True
		except KeyError:
			return False

	def make_sig(self, url):
		'''
		hostname+path+querykey
		'''
		parse = urlparse.urlparse(url)
		return md5.md5(parse.hostname+parse.path+''.join(sorted(urlparse.parse_qs(parse.query).keys()))).hexdigest()

	def save_handler(self, req, req_body, res, res_body):
		#check res.status
		if re.match(config.filter_code, str(res.status)): return
		#check host
		if not len([h for h in config.included_host if req.headers.get('Host', '').endswith(h)]): return
		if len([h for h in config.excluded_host if req.headers.get('Host', '').endswith(h)]): return
		#check fileext
		if len([h for h in config.filter_file if urlparse.urlparse(req.path).path.endswith(h)]): return
		#check query, get must have query string or url-rewrited
		#GET method, have ext and  do not have query string
		if os.path.splitext(req.path)[1] and req.command == 'GET' and not urlparse.urlparse(req.path).query: return

		#prepare request
		req_header_text = "%s %s %s\n%s" % (req.command, req.path, req.request_version, req.headers)

		if req.command == 'GET':
			request = req_header_text + '\n'
		else:
			request = req_header_text + '\n' + req_body

		#avoid same params multi test
		sig = self.make_sig(req.path)
		if self.check_history(sig):
			return

		self.query_log[sig] = True

		fname = str(uuid.uuid4())

		f = open(config.save_path + '/' + fname, 'w')
		f.write(request)
		f.close()

		i = SqlmapAPIWrapper(fname)
		if i.scan_start():
			config.queue.put((fname,i.taskid,req.path,time.time()))

		
if __name__ == '__main__':
	if sys.argv[1:]:
		port = int(sys.argv[1])
	else:
		port = 8888
	server_address = ('', port)

	HandlerClass = myproxy
	ServerClass = ThreadingHTTPServer
	protocol="HTTP/1.1"

	HandlerClass.protocol_version = protocol
	httpd = ServerClass(server_address, HandlerClass)

	sa = httpd.socket.getsockname()
	print "Serving HTTP Proxy on", sa[0], "port", sa[1], "..."
	httpd.serve_forever()
