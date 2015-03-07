#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import urllib2


class proxyApp(webapp.webApp):

    class headers():

        def __init__(self):
            self.heads = {}

        def getHeads(self, resource, myUrl, n):
            resource = resource[7:]
            myUrl = myUrl + resource
            if resource in self.heads:
                headers = self.heads[resource]
                code = "200 OK"
                html = "<html><h1>Cabeceras iteracion " + str(n) + "</h1> \
                        <body><p>" + self.toString(resource) + "</p><a href="\
                        + myUrl + ">Return</a></body></html>"
            else:
                code = "404 Not Found"
                html = "<html><h1>Headers not found</h1><a href=" + \
                        myUrl + ">Return</a></html>"
            return code, html

        def toString(self, resource):
            headers = self.heads[resource]
            if str(headers).find("\n") != -1:
                headers = str(headers).split("\n")
            string = ""
            for head in headers:
                string = string + "<p>" + head + "</p>"
            return string

    def __init__(self, hostname, port):
        self.cache = {}
        self.heads1 = self.headers()
        self.heads2 = self.headers()
        self.heads3 = self.headers()
        self.heads4 = self.headers()
        self.myUrl = "http://" + hostname + ":" + str(port) + "/"
        webapp.webApp.__init__(self, hostname, port)

    def parse(self, request):
        print "REQUEST:"
        print request
        resource = request.split()[1][1:]
        hs = request.split("\n")[1:]
        return (resource, hs)

    def processContent(self, content, url, request):
        pos = content.find("<body")
        pos = content.find(">", pos)
        html1 = content[:pos + 1]
        html2 = content[pos + 1:]
        if request.startswith("cache/"):
            request = request[6:]
        html = html1 + "<p>HOLA</p><p><a href=" + url + ">URL original</a>\
            </p><p><a href=" + self.myUrl + request + ">Recargar</a></p>\
            <p><a href=" + self.myUrl + "cache/" + request + ">Cache</a></p>\
            <p><a href=" + self.myUrl + "heads1/" + request + ">Cabeceras1</a>\
            </p><a href=" + self.myUrl + "heads2/" + request + ">Cabeceras2\
            </a><p><a href=" + self.myUrl + "heads3/" + request + ">Cabeceras3\
            </a></p><p><a href=" + self.myUrl + "heads4/" + request + \
            ">Cabeceras4</a></p>" + html2
        return html

    def getContent(self, resource, headers):
        url = "http://" + resource
        print "url: " + url
        try:
            self.heads1.heads[resource] = headers
            request = urllib2.Request(url, None, self.heads1.heads)
            urlDescriptor = urllib2.urlopen(request)
        except IOError:
            print "url does not exist"
            return ("404 Not Found", "<html><body><h1> 404 Not Found</h1> \
                    </body></html>")
        html = urlDescriptor.read()
        html = self.processContent(html, url, resource)
        try:
            code = str(urlDescriptor.getcode())
            self.cache[resource] = html
            self.heads2.heads[resource] = self.heads1.heads[resource]
            self.heads3.heads[resource] = urlDescriptor.info()
            self.heads4.heads[resource] = self.heads3.heads[resource]
            code = code + "\n" + str(self.heads3.heads[resource])
            urlDescriptor.close()
            return (code, html)
        except ValueError:
            return ("500", "<html><body><h1> 500 Intern Error</h1> \
                    </body></html>")

    def getFromCache(self, request):
        request = request[6:]
        try:
            content = self.cache[request]
            code = "200 OK"
        except KeyError:
            code = "404 Not Found"
            content = "<html><head1>Element requested is not in cache\
                        </head1></html>"
        return (code, content)

    def process(self, request):
        resource, headers = request
        if resource is "":
            print "wrong resource"
            return ("404 Not Found", "<html><body>ERROR: Page \
                    name needed</body></html>")
        elif resource.startswith("cache/"):
            print "asking for cache"
            (code, html) = self.getFromCache(resource)
        elif resource.startswith("heads1/"):
            print "asking for headers 1"
            (code, html) = self.heads1.getHeads(resource, self.myUrl, 1)
        elif resource.startswith("heads2/"):
            print "asking for headers 2"
            (code, html) = self.heads2.getHeads(resource, self.myUrl, 2)
        elif resource.startswith("heads3/"):
            print "asking for headers 3"
            (code, html) = self.heads3.getHeads(resource, self.myUrl, 3)
        elif resource.startswith("heads4/"):
            print "asking for headers 4"
            (code, html) = self.heads3.getHeads(resource, self.myUrl, 4)
        else:
            (code, html) = self.getContent(resource, headers)
        return (code, html)

if __name__ == "__main__":
    try:
        testProxy = proxyApp("localhost", 9999)
    except KeyboardInterrupt:
        print "Keyboard interrupt recived"
