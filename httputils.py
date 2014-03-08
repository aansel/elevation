import proxy
import urllib2

def get(url):
    p = proxy.getRandomProxy()
    proxy_handler  = urllib2.ProxyHandler({'http': p.username + ':' + p.password + '@' + p.ip + ':' + p.port})
    opener = urllib2.build_opener(proxy_handler)
    f = opener.open(url)
    return f.read()
