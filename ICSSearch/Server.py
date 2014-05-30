import string,cgi,time,urllib,json
from io import open
from urlparse import urlparse,parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import sys
from threading import *

import DocFetcher, admin

src = "../FinalSet/" if ('PORT' not in os.environ) else "FinalSet/"
class QueryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            queries = parse_qs(parsed.query)
            hasResp = False
            if "as" in queries and queries["as"][0] == "true":
                #auto suggest part
                if "q" in queries:
                    jsonResp = json.dumps(DocFetcher.GetASResult(queries["q"][0]))
                    hasResp = True
            elif "q" in queries:
                rankingType = 'all'
                if "os" in queries:
                    rankingType = queries["os"][0] 
                print(rankingType) 
                #normal query part
                jsonResp = json.dumps(DocFetcher.GetResult(queries["q"][0],rankingType))
                hasResp = True
            if hasResp:    
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.send_header("Access-Control-Allow-Origin", "*");
                self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin");
                self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
                self.end_headers()
                self.wfile.write(jsonResp)
            else:
                if parsed.path != "":
                    self.send_response(200)
                    print(parsed.path)
                    if (parsed.path.endswith(".js")):
                        contenttype = "application/javascript"
                        path = src + "Webpage" + parsed.path
                    elif (".css" in parsed.path):
                        contenttype = "text/css"
                        path = src + "Webpage" + parsed.path
                    elif(".png" in parsed.path):
                        contenttype = "image/png"
                        path = src + "Webpage" + parsed.path
                    elif(".gif" in parsed.path):
                        contenttype = "image/gif"
                        path = src + "Webpage" + parsed.path
                    elif(".ico" in parsed.path):
                        contenttype = "image/x-icon"
                        path = src + "Webpage" + parsed.path
                    else:
                        contenttype = "text/html"
                        path = src + "Webpage/index.html"
                    self.send_header('Content-type',contenttype)
                    self.end_headers()
                    indexfile = open(path, "rb")
                    self.wfile.write(indexfile.read())
                    indexfile.close()
                else:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    indexfile = open(src + "Webpage/index.html", "r")
                    self.wfile.write(indexfile.read())
                    indexfile.close()
        except AttributeError:
            self.send_error(404,'What Shady Shit was tried?')

def DataLoader():
    DocFetcher.LoadTrie()
    print("Done")

def main(port):
    try:
        server = HTTPServer(('', port), QueryHandler)
        print 'Loading up Awesome server.'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Bye Bye'
        server.socket.close()

if __name__ == '__main__':
    #if not admin.isUserAdmin():
    #    admin.runAsAdmin()
    port = 80
    if ('PORT' in os.environ):
        port = int(os.environ['PORT'])
    print(sys.argv)
    Thread(target = DataLoader, args=()).start()
    main(port)