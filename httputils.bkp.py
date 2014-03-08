import proxy
import urllib2

def get(url):
    p = proxy.getRandomProxy()
    proxy_handler  = urllib2.ProxyHandler({'https': p.username + ':' + p.password + '@' + p.ip + ':' + p.port})

    request = urllib2.Request(url)
#    request.add_header('Accept-Encoding', 'gzip, deflate')

    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('Accept-Encoding', 'gzip')]
    f = opener.open(request)
#    print f.info()
    return f.read()
