import random

class Proxy:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

proxies = []
f = open('/home/aansel/elevation/proxy.txt', 'r')
for line in f:
    if line.startswith('username:'):
        username = line.split(':')[1].rstrip('\n')
    elif line.startswith('password:'):
        password = line.split(':')[1].rstrip('\n')
    else:
        proxyTab = line.split(':')
        ip = proxyTab[0]
        port = proxyTab[1].rstrip('\n')
        p = Proxy(ip, port, username, password)
        proxies.append(p)

    

def getRandomProxy():
    nb = len(proxies)
    idx = random.randint(0, nb - 1)
    return proxies[idx]

