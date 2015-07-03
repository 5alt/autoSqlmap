# -*- coding: utf-8 -*-

save_path = '/tmp'

proxy_port = 8888

filter_file = ['.css', '.js', '.jpg', '.jpeg', '.gif', '.png', '.bmp', '.html', '.htm', '.swf', '.svg'] #host.endswith(item)
filter_code = r'4\d{2}' #re.match
included_host = ['vulnweb.com'] #host.endswith(item), [''] for all
excluded_host = ['google.com', '127.0.0.1'] #host.endswith(item)

sqlmap_host = 'http://127.0.0.1:8775'
sqlmap_tasktimeout = 3*60
sqlmap_options = {}
sqlmap_options['threads'] = 3

#sqlmap_options['proxyFile'] = ''
sqlmap_options['dbms'] = 'mysql'
sqlmap_options['hpp'] = True
sqlmap_options['timeout'] = 5

queue = None
