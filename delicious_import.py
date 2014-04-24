#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydelicious import DeliciousItemExistsError
from pydelicious import PyDeliciousException
from pydelicious import DeliciousAPI

from getpass import getpass
from lxml import etree

import webbrowser
import time
import sys

files = sys.argv[1:]

##files = ['delicios_import.png','delicios_import.png']
##files = ['bookmarks-2013-11-05.html']

if len(files) == 0:
    print "Please choose files with tags 'a' (and href attr) and try again."
    print "Exit."
    sys.exit()


k = 1
while k: 
    try:
        us = raw_input('Please type your login on Delicios: ')
        pa = raw_input('Please type your passw on Delicios: ')
        print "\n"
        user = DeliciousAPI(us,pa)
        sign = user.posts_recent()
        k = 0
    except Exception, d:
        print str(d) + "\n", "Authentication problem. Try again."
        k = 1


yes = True
no = False

# |  posts_add(self, url, description, extended='', tags='', dt='', replace=False, shared=True, **kwds)
# |      Add a post to del.icio.us. Returns a `result` message or raises an
# |      ``DeliciousError``. See ``self.request()``.
# |
# |      &url (required)
# |          the url of the item.
# |      &description (required)
# |          the description of the item.
# |      &extended (optional)
# |          notes for the item.
# |      &tags (optional)
# |          tags for the item (space delimited).
# |      &dt (optional)
# |          datestamp of the item (format "CCYY-MM-DDThh:mm:ssZ").
# |          Requires a LITERAL "T" and "Z" like in ISO8601 at
# |          http://www.cl.cam.ac.uk/~mgk25/iso-time.html for example:
# |          "1984-09-01T14:21:31Z"
# |      &replace=no (optional) - don't replace post if given url has already
# |          been posted.
# |      &shared=yes (optional) - wether the item is public.


def addtodelicios(name,link,date="",tags="",extd="",repl=no,shar=no):

    user.posts_add(link,name,extd,tags,date,repl,shar)


def alreadyposted():

    user.posts_update()

    bm = user.posts_all(results=9999)['posts']

    ap = {}
    for i in bm:
        ap[i['hash']] = i['description'],i['href']

    # check that no more than
    # one name with one link
    # for i in x.itervalues():
        # if len(i) > 2: print i

    # bad solution, because
    # maybe two name of one
    # link or contrariwise
    # ap = {}
    # for i in bm:
        # ap[i['description']] = i['href']

    g = []
    for i in ap.itervalues():
        g.append(i)

    return g


def addtime(j=""):

    if j == "current":
        x = time.localtime(int(time.time()))
        return "%02d-%02d-%02dT%02d:%02d:%02dZ" % (x[0],x[1],x[2],x[3],x[4],x[5])

    elif j == "":
        x = time.localtime()
        return "%02d-%02d-%02d %02d-%02d-%02d" % (x[0],x[1],x[2],x[3],x[4],x[5])

    else:
        x = time.localtime(int(j))
        return "%02d-%02d-%02dT00:00:00Z" % (x[0],x[1],x[2])


def pprint(message,color=""):

    d = {"red":31,"green":32,"yellow":33,"blue":34}

    if color == "":
        sys.stdout.write(u"%s" % message)
    else:
        sys.stdout.write(u"\x1B[%dm%s\x1B[0m" % (d[color], message))
        sys.stdout.flush()


def makereport(*argv):

    r = ""
    for n in argv:
        if len(n) > 1:
            for u in n:
                r += u

    html = '''
    <!DOCTYPE HTML>
    <html lang="ru-RU">
    <head>
    <meta charset="utf-8">
    <title>delicios import - report</title>
    <style>
    body {margin: 0 auto;width: 80%%;text-align:justify;}
    a {text-decoration:none;}
    </style>
    </head>
    <body>
    %s
    </body>
    <html>
    '''%r

    global f

    j = open("report-"+f,"w")
    j.write(html)
    j.close()
    
    try:
        webbrowser.open_new_tab("report-"+f)
    except:
        pass


def ih(name,link):
    name = name.encode('utf-8')
    link = link.encode('utf-8')
    result = "<a href='{0}'>{1}</a>".format(link,name)
    return result


for f in files:

    x = open(f)
    y = x.read()


    mainreport = ("<p><b>Total links found in file:</b></p>",)

    repalready = ("<p><b>Already added to Delicios:</b></p>",)
    repnormals = ("<p><b>Add at this time:</b></p>",)
    repnotcorr = ("<p><b>Not correct link:</b></p>",)
    repunnamed = ("<p><b>Unnamed link:</b></p>",)

    reperrrors = ("<p><b>Critical errors:</b></p>",)


    try:

        html = etree.HTML(y)
        
        # result = etree.tostring(html, pretty_print=True, method="html")
        # print "Pretty formatted html structure:" + "\n\n", result

        count = len(html.xpath("//a"))

        if count != 0:

            pprint("Found links in " + f + " " + str(count) + "." + "\n\n")
            mainreport += ("<p>Found links in " + "<i>" + f + "</i>" + " " + str(count) + ".</p>",)

            pprint("Wait for checking already added bookmarks." + "\n\n")

            ap = alreadyposted()
            
            for z in html.xpath("//a"):

                pprint("%04d -> " % (count))

                try:

                    # get name, link, date

                    name = z.text
                    if name == None:
                        name = ""

                    link = z.attrib["href"]
                    if link == "":
                        link = ""

                    try:
                        date = z.attrib["add_date"]
                    except KeyError, e:
                        if e.message == "add_date":
                            date = addtime("current")

                    s = link + " | " + name + " "

                    # main operations - begin
                    
                    y = []
                    for h in ap:
                        y.append(h[1])

                    if link in y:
                        pprint("this already added to Delicios: " + s, "blue")
                        repalready+=("*"+ih(name, link)+" ",)

                    else:

                        if link == "" or link.startswith("http") == False:
                            pprint("not correct link found: " + s, "red")
                            repnotcorr+=("*"+ih(name,link)+" ",)

                        else:

                            if name == "":
                                name = "UNNAMEDLINK"
                                addtodelicios(name,link)
                                pprint("added unnamed link: " + s, "yellow")
                                repunnamed+=("*"+ih(name, link)+" ",)

                            else:
                                addtodelicios(name,link)
                                pprint("added normal link to Delicios: " + s, "green")
                                repnormals+=("*"+ih(name, link)+" ",)

                    # main operations - finish

                except Exception,e:
                    pprint("exception: " + str(e) + " - " + str(sys.exc_info()[0])+ " ", "red")
                    reperrrors+=("<p>exception: " + str(e) + " - " + str(sys.exc_info()[0]) + "</p>",)
                    pass

                except PyDeliciousException, e:
                    pprint("exception: " + str(e) + " ", "red")
                    reperrrors+=("<p>exception: " + str(e) + "</p>",)
                    pass

                except DeliciousItemExistsError, e:
                    pprint("this link dublicated: " + s, "red")
                    reperrrors+=("<p>this link dublicated: " + s + "</p>",)
                    pass

                count -= 1

            pprint("Finished. " + "\n")

        else:

            pprint("No links found in file " + f + "\n")
            reperrrors+=("<p>No links found in file " + f + "</p>",)
            
    except Exception, q:

        pprint("Error, file " + f + " - " + str(q) + " - " + str(sys.exc_info()[0]) + "\n")
        reperrrors+=("<p>Error, file " + "<i>" + f + "</i>" + " - " + str(q) + " - " + str(sys.exc_info()[0]) + "</p>",)
        pass

    except (KeyboardInterrupt, SystemExit):
        makereport(mainreport, reperrrors, repnormals, repnotcorr, repunnamed, repalready)
        print "Script stopped."

    makereport(mainreport, reperrrors, repnormals, repnotcorr, repunnamed, repalready)

print "Exit."
