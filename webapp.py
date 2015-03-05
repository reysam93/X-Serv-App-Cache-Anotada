#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket


class webApp:
    def parse(self, request):
        return None

    def process(self, parsedRequest):
        return ("200 OK", "<html><body><h1>IT WORKS!</h1></body></html>")

    def __init__(self, hostname, port):
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySocket.bind((hostname, port))
        self.mySocket.listen(5)

        while True:
            print "Waiting for connections"
            (recvSocket, address) = self.mySocket.accept()
            print "HTTP request reeived (going to parse and process):"
            request = recvSocket.recv(2048)
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print "Answering back..."
            print "HTTP/1.1 " + returnCode + "\r\n\r\n" + "content....."
            recvSocket.send("HTTP/1.1 " + returnCode + "\r\n\r\n"
                            + htmlAnswer + "\r\n")
            recvSocket.close()

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234)
