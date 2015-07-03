#autoSqlmap

autoSqlmap is a simple http(s) proxy with python based sqlmapapi wrapper.

When HTTP traffic goes through the proxy, it will auto launch sqlmap to test sqli vulnerability.

##Requirement
* python2
* sqlmap
* requests

##Usage
modify configurations in config.py, default config is for http://testphp.vulnweb.com/

sqlmap options please refer to `sqlmap_options_list.txt`

start sqlmap api

```
python sqlmapapi.py -s
```

start autoSqlmap

```
python run.py 2>/dev/null
```

go to http://testphp.vulnweb.com/ for test

##Enable HTTPS intercept
To intercept HTTPS connections, generate private keys and a private CA certificate:

```
./setup_https_intercept.sh
```

Through the proxy, you can access http://proxy2.test/ and install the CA certificate in the browsers.

(from proxy2)

##Contact
http://5alt.me

md5_salt [AT] qq.com

##Reference
* https://github.com/zt2/sqli-hunter
* https://github.com/manning23/MSpider
* https://github.com/inaz2/proxy2
* http://drops.wooyun.org/tips/6653
