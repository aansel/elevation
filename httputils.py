import proxy
from StringIO import StringIO
import gzip
import urllib2

def get(url):
    p = proxy.getRandomProxy()
    proxy_details = p.username + ':' + p.password + '@' + p.ip + ':' + p.port
    proxy_handler  = urllib2.ProxyHandler({'https': proxy_details, 'http': proxy_details})

    request = urllib2.Request(url)
    request.add_header('Accept-Encoding', 'gzip, deflate')
    request.add_header('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')

    opener = urllib2.build_opener(proxy_handler)
    response = opener.open(request)

    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        return f.read()
    else:
        return response.read()
