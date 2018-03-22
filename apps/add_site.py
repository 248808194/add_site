import tornado.ioloop
import tornado.web
import os, sys
import subprocess
import json
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
{'tiaozhuan': [b'2'], 
 'domain_name': [b'zhoutao990.51xidu.com'], 
 'page': [b'3'], 
 'site_id': [b'123'],
 'comp': [b'\xe6\x9f\x90\xe6\x9f\x90\xe5\x85\xac\xe5\x8f\xb8'], 
 'jdomain': [b'1.zhoutao.name1'],
 'page1': [b'1'], 
 'jsite_id': [b'3333'], 
 'jcomp': [b'\xe6\x9f\x90\xe6\x9f\x902\xe5\x85\xac\xe5\x8f\xb8']}
'''
dirdict = json.load(open('.temp.json','r'))

# pip3 install tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print('task begin --------------------------------------------------------------------------------------------------------------------------------')
        dirdict = json.load(open('.temp.json','r'))
        print(dirdict)
        asdf = self.request.arguments
        self.a = asdf['uniqcode'][0].decode()
        print(asdf)
        with open('.uniqcode.txt','r') as f1:
            line = f1.readlines()
	if not line:line.append('123')
        if self.a == line[0].strip():
	    print('found old uniqcode will finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            self.finish()
        else:


            self.T = asdf['tiaozhuan'][0].decode()
            print('self T is ',self.T)
            if self.T == '3': #shenghe
                if asdf['user_time'][0].decode():
                    time_file = '.'+asdf['user_time'][0].decode()
                    #get url list write into txt file
                    with open('%s'%(time_file), 'w') as f1:
                        for i in asdf['dirname'][0].decode().split(','):
                            f1.write(i+'\n')
                else:
                    time_file = '.tempurl.txt'
                    #get url list write into txt file
                    with open('%s'%(time_file), 'w') as f1:
                        for i in asdf['dirname'][0].decode().split(','):
                            f1.write(i+'\n')

                if asdf['user_time'][0].decode():
                    time = asdf['user_time'][0].decode().replace('-',' ')
                    cvb = 'echo "%s while read a;do cd /data/web/adsite/.\$a && \cp index.sh index.html -Rf;done < /root/%s "'%(time,time_file)
                    ddd = '>> /var/spool/cron/root'
                    print(cvb ,ddd)
                    subprocess.Popen('%s %s'%(cvb,ddd),shell=True).communicate()
                else:
                    subprocess.Popen('while read a;do cd /data/web/adsite/.$a && \cp index.sh index.html -Rf;done < /root/%s'%(time_file),shell=True).communicate()

            elif self.T =='4': #tiaozhuang
                if asdf['user_time'][0].decode():
                    time_file = '.'+asdf['user_time'][0].decode()
                    #get url list write into txt file
                    with open('%s'%(time_file), 'w') as f1:
                        for i in asdf['dirname'][0].decode().split(','):
                            f1.write(i+'\n')
                else:
                    time_file = '.tempurl.txt'
                    #get url list write into txt file
                    with open('%s'%(time_file), 'w') as f1:
                        for i in asdf['dirname'][0].decode().split(','):
                            f1.write(i+'\n')

                if asdf['user_time'][0].decode():
                    time = asdf['user_time'][0].decode().replace('-',' ')
                    cvb = 'echo "%s while read a;do cd /data/web/adsite/.\$a && \cp index.tz index.html -Rf;done < /root/%s "'%(time,time_file)
                    ddd = '>> /var/spool/cron/root'
                    print(cvb ,ddd)
                    subprocess.Popen('%s %s'%(cvb,ddd),shell=True).communicate()
                else:
                    subprocess.Popen('while read a;do cd /data/web/adsite/.$a && \cp index.tz index.html -Rf;done < /root/%s'%(time_file),shell=True).communicate()
            elif self.T == '5':
                self.cd = asdf['cdomain_name'][0].decode()
                self.cp = asdf['page11'][0].decode()
                olddict = self.getoldcode(self.cd)
                print(olddict)
                olddict['cdomain_name'] = self.cd
                olddict['src_dir'] = dirdict[self.cp]

                self.writejson('/data/web/adtemp/oldcode.json',olddict)
                self.change_dir(self.cd,'/data/web/adtemp/changepage.yml')


            else:


                self.u = asdf['domain_name'][0].decode()
                self.p = asdf['page'][0].decode()
                self.sid = asdf['site_id'][0].decode()
                self.pburl = asdf['pburl'][0].decode()
                self.compgongso = asdf['comp'][0].decode()
                self.b_city = asdf['b_city'][0].decode()
                dict1 = {'domain_name':self.u,'page':self.p,'site_id':self.sid,'comp':self.compgongso,'b_city':self.b_city,'pburl':self.pburl}
                #----
                self.ju = asdf['jdomain'][0].decode()
                self.jp = asdf['page1'][0].decode()
                self.jsid = asdf['jsite_id'][0].decode()
                self.jcimpgongso = asdf['jcomp'][0].decode()
                self.jb_city = asdf['jb_city'][0].decode()
                dict2 =  {'domain_name':self.ju,'page':self.jp,'site_id':self.jsid,'comp':self.jcimpgongso,'b_city':self.jb_city,}

                print(self.T)
                print('=====================================')
                if self.T == '1':
                    print('TTTTTT 11')
                    dict1['src_dir'] = dirdict[self.p]
                    json1 = '/data/web/adtemp/temp.json'
                    self.writejson(json1,dict1)
                    self.configall('.add_nginx.yml')

                elif self.T == '2':
                    print('TTTTTTT 22')
                    dict1['src_dir'] = dirdict[self.p]
                    json1 = '/data/web/adtemp/temp.json'
                    self.writejson(json1,dict1)
                    self.configall('.add_nginx.yml')

                    dict2['src_dir'] = dirdict[self.jp]
                    dict2['llldomain_name'] = dict1['domain_name']
                    print('dict2 is ',dict2)
                    json2 = '/data/web/adtemp/temp1.json'
                    self.writejson(json2,dict2)
                    self.configall('.add_nginxj.yml')
            self.huixie()
            print('task end +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            self.finish()



    def configall(self,file):
        subprocess.Popen('ansible-playbook %s'%(file), shell=True, cwd='/data/web/adtemp').communicate()

    def writejson(self,file,dic):
        with open(file, 'w') as f1:
            f1.write(json.dumps(dic, indent=4))

    def getoldcode(self,dname):
        oldfile = '/data/web/adsite/.%s/index.html'%(dname)
        with open(oldfile, 'r') as f1:
            templist = f1.readlines()
        aa = {'wxcode':'','comp':'','site_id':''}
        a = 0
        for i in templist:
            if i.startswith('//start'):
                a = templist.index(i) + 1
                aa['wxcode'] = (templist[a].strip())
                continue
            if 'compgongsi' in i:
                aa['comp'] = i.split('>')[1].split('<')[0]
                continue

            if 'cnzz' and 'web_id' in i:
                aa['site_id'] = i.split('web_id=')[1].split('"')[0]

        return aa

    def change_dir(self,dname,file):
        htmlfile = '/data/web/adsite/.%s/index.html'%(dname)
        bb = json.load(open('/data/web/adtemp/oldcode.json', 'r'))['wxcode']
        print('bb is',bb)
        print('html file is ',htmlfile)
        subprocess.Popen('ansible-playbook %s' % (file), shell=True, cwd='/data/web/adtemp').communicate()

        with open(htmlfile,'r') as f1:
            lines = f1.readlines()


        with open(htmlfile,'w') as f2:
            for line in lines:
                if line.startswith('//start'):
                    print(line)
                    lines[lines.index(line) + 1] = bb + '\n'
                    f2.write(line)
                    continue
                f2.write(line)


    def huixie(self):
        with open('.uniqcode.txt','w') as f1:
            f1.write(self.a)
        #self.write("<script>alert('SUCCESSFUL');window.history.back();</script>")  #
        self.write("<script>alert('SUCCESSFUL');window.location.href=document.referrer</script>")  #

application = tornado.web.Application([
    (r"/index", MainHandler),
])
if __name__ == "__main__":
    application.listen(2345)
    tornado.ioloop.IOLoop.instance().start()

