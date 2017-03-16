import urllib

if __name__=='__main__':
    nmc = urllib.urlopen('http://10.0.100.138:9000/a=query&text=*').read()
    print nmc