#coding:utf-8
import web
from mongo_init import count,get_one_doc,get_many_docs,update_docs,delete_docs,get_docs_paging_sort
import sys,os
import json,shutil
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
urls = (
    "/count/(.*)", "c",
    "/query/(.*)", "q",
    "/update/(.*)", "u",
    "/delete/(.*)", "d",
    "/query_many/(.*)", "qm",
    "/paging/(.*)", "qmps",
    "/qrcode", "signup",
    "/upload", "upload"
)
app = web.application(urls, globals())


def common_code(arg):
    # Split argument
    print 'arg:' + arg
    arr = str(arg).split('/')
    coll = arr[0]

    # Projection
    dic = {}
    if len(arr) > 1:
        crit = arr[1].split(',')
        for a in crit:
            a = a.split(':')
            dic[a[0]] = a[1]
        print dic

    proj_dic = {}
    if len(arr) > 2:
        proj = arr[2].split(',')
        for p in proj:
            p = p.split(':')
            proj_dic[p[0]] = int(p[1])
            # proj_dic[p[0]] = p[1]
    pos = 0
    page = 0
    if len(arr) > 3:
        pag = arr[3].split(',')
        pos = int(pag[0])
        page = int(pag[1])
        # pos = pag[0]
        # page = pag[1]

    filed = ''
    sort = 1
    if len(arr) > 3:
        s = arr[3].split(',')
        filed = s[0]
        sort = int(s[1])

    return coll, dic,proj_dic,pos,page,filed,sort

class c:
    def GET(self,arg):
        print arg
        arr = str(arg).split('/')
        coll = arr[0]

        dic = {}
        crit = arr[1].split(',')
        for a in crit:
            a = a.split(':')
            dic[a[0]] = a[1]
        print dic
        rst = count(coll,dic)
        return rst
class q:
    #query_*/collection name/key:value,key:value.../name:0or1,name:0or1
    #query_*/collection name/projection/criteria
    def GET(self,arg):
        #Get query string
        qs = str(web.ctx.get('query'))
        print qs

        #Get jsonp function name
        qs = qs.replace('?callback=','')
        qs = qs[0:qs.index('&')]
        # print qs

        qcc = common_code(arg)

        rst = get_one_doc(qcc[0],qcc[1])

        #All values into a string in the dict
        print rst
        p = {}
        for key in rst:
            p[key] = str(rst[key])
        print p

        #Transfor jsonp string
        js = json.dumps(p)
        rst = qs+'('+js+')'
        print rst
        return rst

class qm:
    #query_*/collection name/key:value,key:value.../name:0or1,name:0or1
    #query_*/collection name/projection/criteria
    def GET(self,arg):
        #Get query string
        qs = str(web.ctx.get('query'))
        print qs

        #Get jsonp function name
        qs = qs.replace('?callback=','')
        qs = qs[0:qs.index('&')]
        # print qs

        qcc = common_code(arg)

        rst = get_many_docs(qcc[0],qcc[1],qcc[2])

        #All values into a string in the dict
        print rst
        l = []
        for d in rst:
            p = {}
            for key in d:
                p[key] = str(d[key])
            l.append(p)
        print l

        #Transfor jsonp string
        js = json.dumps(l)
        rst = qs+'('+js+')'
        print rst
        return rst

class qmps:
    #query_*/collection name/key:value,key:value.../name:0or1,name:0or1
    #query_*/collection name/projection/criteria
    def GET(self,arg):
        #Get query string
        qs = str(web.ctx.get('query'))
        print qs

        #Get jsonp function name
        qs = qs.replace('?callback=','')
        qs = qs[0:qs.index('&')]
        # print qs

        qcc = common_code(arg)

        rst = get_docs_paging_sort(qcc[0],qcc[1],qcc[2],qcc[3],qcc[4],qcc[5],qcc[6])

        #All values into a string in the dict
        print rst
        l = []
        for d in rst:
            p = {}
            for key in d:
                p[key] = str(d[key])
            l.append(p)
        print l

        #Transfor jsonp string
        js = json.dumps(l)
        rst = qs+'('+js+')'
        print rst
        return rst

class u:
    #query_*/collection name/key:value,key:value.../name:0or1,name:0or1
    #query_*/collection name/projection/criteria
    def GET(self,arg):
        #Get query string
        qs = str(web.ctx.get('query'))
        print qs

        #Get jsonp function name
        qs = qs.replace('?callback=','')
        qs = qs[0:qs.index('&')]
        # print qs

        qcc = common_code(arg)

        temp = {}
        for key in qcc[1]:
            temp[key] = qcc[1][key]
        crit = {'$set':temp}

        proj = {}
        for key in qcc[2]:
            proj[key] = str(qcc[2][key])
        rst = update_docs(qcc[0],proj,crit)

        p = {}
        for key in rst:
            p[key] = str(rst[key])

        #Transfor jsonp string
        js = json.dumps(p)
        rst = qs+'('+js+')'
        print rst
        return rst
class d:
    def GET(self,arg):
        #Get query string
        qs = str(web.ctx.get('query'))
        print qs

        #Get jsonp function name
        qs = qs.replace('?callback=','')
        qs = qs[0:qs.index('&')]
        # print qs

        arr = str(arg).split('/')
        coll = arr[0]

        n = 0
        ids = arr[1].split(',')
        for id in ids:
            drst = delete_docs(coll,id)
            print drst
            n += int(drst['n'])
        #Transfor jsonp string
        p = {'result':n}
        js = json.dumps(p)
        rst = qs+'('+js+')'
        print rst
        return rst
class upload:
    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        x = web.input(pic={})
        arr = x.keys()
        filedir = os.path.split(os.path.realpath(__file__))[0]
        us = 'fail'
        try:
            # if arr[0] in x: # to check if the file-object is created
            filepath=x.get(arr[0]).filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fp = filedir +'/upload/'+ filename
            fout = open(fp,'w') # creates the file where the uploaded file should be stored
            fout.write(x.get(arr[0]).file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
                # raise web.seeother('/upload')
            shutil.copyfile(fp,'/var/www/html/upload/'+filename)
            us = 'success'
        except Exception,ex:
            print ex
            us = 'fail'
        return us

if __name__ == "__main__":
    app.run()