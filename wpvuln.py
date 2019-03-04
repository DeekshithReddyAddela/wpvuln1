import urllib3
import requests
import json
import sys
import os
import urllib.request as urllib
import xlrd
import xlwt
from bs4 import BeautifulSoup

urllib3.disable_warnings()
http = urllib3.PoolManager()
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.97 Safari/537.36'
headers = { 'User-Agent' : user_agent }
file = open("vulnurls.txt", "r")
for line in file:
    line=line.replace("\n","")
    if "www" in line:
        dir="static/files/"+line[line.find('://www.')+7:line.find('.',line.find('://www.')+7)]
    else:
        dir="static/files/"+line[line.find('://')+3:line.find('.',line.find('://')+3)]
    print(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

    open(dir+"/Plugins-Themes.xls", "w")
    open(dir+"/Plugins-ThemesVulnerabilities.xls", "w")

    f = open(dir+"/urls.txt", "w")
    loc1 = (dir+"/Plugins-Themes.xls")
    loc2 = (dir+"/Plugins-ThemesVulnerabilities.xls")
    wb1 = xlwt.Workbook()
    sheet1 = wb1.add_sheet("Sheet1",cell_overwrite_ok=True)

    queue = set()
    crawled = list()
    plugins = set()
    themes = set()
    plugins1 = set()
    themes1 = set()
    l=0
    m=0

    homepage=line#"https://www.pomalyst.com"
    url=homepage
    queue.add(url)
    while 1:
        if l==1:
            for l in crawled:
                if l[-1]!='/':
                    queue.discard(l+'/')
                queue.discard(l)
            if len(queue)==0 or m>10:
                break
        l=1
        m+=1
        url=str(queue.pop())
        print(url)
        f.write(url+"\n")
        crawled.append(url)
        r = http.request('GET', url, headers=headers, redirect=False)
        soup = BeautifulSoup(r.data, "html.parser", from_encoding="iso-8859-1")

        for u in soup.find_all('a'):
            b=str(u.get('href'))
            if "?" in b:
                continue
            elif "&" in b:
                continue
            elif "#" in b:
                continue
            elif ".pdf" in b:
                continue
            elif b=="":
                continue
            elif homepage[8:] in b:
                queue.add(b)
            elif b[0]=='/':
                queue.add(homepage+b)

        for u in soup.find_all('script'):
            b=str(u.get('src'))
            if "wp-content" in b or True:
                if "plugins" in b:
                    plugins.add(b)
                    start = b.find('plugins') + 8
                    end = b.find('/', start)
                    c=b[start:end]
                    d=str(u.get('ver'))
                    if "ver=" in b:
                        start = b.find('ver=') + 4
                        d=b[start:]
                    plugins1.add(c+"\t"+d)
                elif "themes" in b:
                    themes.add(b)
                    start = b.find('themes') + 7
                    end = b.find('/', start)
                    c=b[start:end]
                    d=str(u.get('ver'))
                    if "ver=" in b:
                        start = b.find('ver=') + 4
                        d=b[start:]
                    themes1.add(c+"\t"+d)

        for u in soup.find_all('link'):
            b=str(u.get('src'))
            if "wp-content" in b or True:
                if "plugins" in b:
                    plugins.add(b)
                    start = b.find('plugins') + 8
                    end = b.find('/', start)
                    c=b[start:end]
                    d=str(u.get('ver'))
                    if "ver=" in b:
                        start = b.find('ver=') + 4
                        d=b[start:]
                    plugins1.add(c+"\t"+d)
                elif "themes" in b:
                    themes.add(b)
                    start = b.find('themes') + 7
                    end = b.find('/', start)
                    c=b[start:end]
                    d=str(u.get('ver'))
                    if "ver=" in b:
                        start = b.find('ver=') + 4
                        d=b[start:]
                    themes1.add(c+"\t"+d)

    f.write("\n***************************************************************\nPlugins\n")
    for a in range(len(plugins)):
        f.write(plugins.pop()+"\n")
    f.write("\n###############################################################\nThemes\n")
    for a in range(len(themes)):
        f.write(themes.pop()+"\n")
    f.close()
    sheet1.col(0).width = 30 * 256
    plu=len(plugins1)
    the=len(themes1)
    print("***********************************\n"+str(plu)+" plugins mentioned")
    sheet1.write(0,0,"Plugins")
    for x in range(plu):
        pl=plugins1.pop()
        print(pl)
        sheet1.write(x+1,0,pl.split()[0])
        sheet1.write(x+1,1,pl.split()[1])
    wb1.save(loc1)

    print("###################################\n"+str(the)+" themes mentioned")
    sheet1.write(2+plu,0,"Themes")
    for x in range(the):
        th=themes1.pop()
        print(th)
        sheet1.write(x+3+plu,0,th.split()[0])
        sheet1.write(x+3+plu,1,th.split()[1])
    wb1.save(loc1)

    wb1 = xlrd.open_workbook(loc1)
    sheet1 = wb1.sheet_by_index(0)
    wb2 = xlwt.Workbook()
    sheet2 = wb2.add_sheet("Sheet1",cell_overwrite_ok=True)
    style = xlwt.easyxf('font: bold 1, color red;')
    style1 = xlwt.easyxf('font: bold 1;')
    style2 = xlwt.easyxf('font:color blue;')
    sheet2.col(0).width = 30 * 256
    sheet2.col(1).width = 13 * 256
    sheet2.col(2).width = 50 * 256
    sheet2.col(3).width = 10 * 256
    sheet2.write(0, 0, "ID", style1)
    sheet2.write(0, 1, "Type", style1)
    sheet2.write(0, 2, "Title", style1)
    sheet2.write(0, 3, "Fixed In", style1)
    sheet2.write(0, 4, "Link", style1)
    wb2.save(loc2)
    c=1
    l=0
    for j in range(sheet1.nrows):
        f1=1
        headers = {'User-Agent': 'WPVulnCLI-Client'}
        req1 = urllib.Request("https://wpvulndb.com/api/v2/plugins/eshop", headers=headers)
        res = json.loads(urllib.urlopen(req1).read().decode('utf-8'))
        if j==0:
            print("***********************************\nPlugins Vulnerabilities")
            sheet2.write(1, 0, "Plugins Vulnerabilities", style)
            c+=2
            continue
        elif j==plu+1:
            continue
        if j==plu+2:
            c+=1
            print("###################################\nThemes Vulnerabilities")
            sheet2.write(c, 0, "Themes Vulnerabilities", style)
            c+=2
            continue
        elif j<=plu:
            url="https://wpvulndb.com/api/v2/plugins/"+ sheet1.cell_value(j, 0)
            req = urllib.Request(url, headers=headers)
            try:
                res = json.loads(urllib.urlopen(req).read().decode('utf-8'))
            except IOError:
                f1=0
                print(sheet1.cell_value(j, 0)+"| not found in db")
                sheet2.write(c, 0, sheet1.cell_value(j, 0), style1)
                sheet2.write(c, 2, "Found version : "+sheet1.cell_value(j, 1))
                sheet2.write(c, 3, "not found in db")
                c+=2
        else:
            url="https://wpvulndb.com/api/v2/themes/"+ sheet1.cell_value(j, 0)
            req = urllib.Request(url, headers=headers)
            try:
                res = json.loads(urllib.urlopen(req).read().decode('utf-8'))
            except IOError:
                f1=0
                print(sheet1.cell_value(j, 0)+"| not found in db")
                sheet2.write(c, 0, sheet1.cell_value(j, 0), style1)
                sheet2.write(c, 2, "Found version : "+sheet1.cell_value(j, 1))
                sheet2.write(c, 3, "not found in db")
                c+=2

        if f1==1:
            if not bool(res[next(iter(res.keys()))]["vulnerabilities"]):
                print(sheet1.cell_value(j, 0)+"| mentioned in db")
                sheet2.write(c, 0, sheet1.cell_value(j, 0), style1)
                sheet2.write(c, 2, "Found version : "+sheet1.cell_value(j, 1))
                sheet2.write(c, 3, "mentioned in db")
                c+=2
                continue
            g=0
            for vuln in res[next(iter(res.keys()))]["vulnerabilities"]:
                v=str(vuln)
                u=v[v.find('url')+8:v.find("'",v.find('url')+8)]
                if vuln.get("fixed_in") is None:
                    fixed = "Unfixed"
                else:
                    fixed = vuln.get("fixed_in")
                if sheet1.cell_value(j, 1) in vuln.get("title"):
                    if g==0:
                        sheet2.write(c, 0, sheet1.cell_value(j, 0), style1)
                        sheet2.write(c, 1, "Found version : "+sheet1.cell_value(j, 1))
                        sheet2.write(c, 3, "latest version : "+res[next(iter(res.keys()))]["latest_version"])
                        c+=1
                        g=1
                    sheet2.write(c, 0, str(vuln.get("id")))
                    sheet2.write(c, 1, vuln.get("vuln_type"))
                    sheet2.write(c, 2, vuln.get("title"))
                    sheet2.write(c, 3, fixed)
                    sheet2.write(c, 4, u)
                    c+=1
                    l=1
                else:
                    if g==0:
                        sheet2.write(c, 0, sheet1.cell_value(j, 0), style1)
                        sheet2.write(c, 2, "Found version : "+sheet1.cell_value(j, 1))
                        sheet2.write(c, 3, "latest version : "+res[next(iter(res.keys()))]["latest_version"])
                        c+=1
                        g=1
                    sheet2.write(c, 0, str(vuln.get("id")))
                    sheet2.write(c, 1, vuln.get("vuln_type"))
                    sheet2.write(c, 2, vuln.get("title"))
                    sheet2.write(c, 3, fixed)
                    sheet2.write(c, 4, u)
                    c+=1
                    l=1
                print( str(vuln.get("id")) + " | " + vuln.get("vuln_type") + " | " + vuln.get("title") + " | " +str(vuln.get("fixed_in")) + " | https://wpvulndb.com/vulnerabilities/" + str(vuln.get("id")))
            c+=1
            if l==1:
                print(sheet1.cell_value(j, 0)+"| has vulnerabilities")
            else:
                print(sheet1.cell_value(j, 0)+"| version not found")
                sheet2.write(c-1, 3, "version not found")
    wb2.save(loc2)
