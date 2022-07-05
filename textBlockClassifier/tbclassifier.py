# Text block classifier as HTTP server 
# All settings are loaded from 'config.json' in the same fodler

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse, parse_qs

import re
import json
import logging
import pandas as pd
from classify4 import classifier_train, classifier_predict

port = 8080
logfile = ''
loglevel = 0 # 0 <=> INFO, 1 <=> DEBUG

class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("go_GET")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
    def do_POST(self):
        print("go_POST")
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        logging.info("post_body=%s",post_body)
        logging.info("post_body[:5]=%s",post_body[:5])
        
        #args=post_body.decode().split('=')
        if (post_body[:5] == b'path='):
        #if (len(args)>1 and args[0] == 'path'): 
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            path = (post_body[5:]).decode("utf-8")
            logging.info('Path to CSV=%s',path)
            res = classifier_predict(path)
            pd.options.display.max_rows = 1000
            logging.debug('res=%s',res[0:1000])

            # TODO: return result
            data1 = {'status':'success','message':'','classes':res.tolist()}
            self.wfile.write((json.dumps(data1)).encode())
        else:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            data1 = {'status':'error','message':'Invalid request'}
            self.wfile.write((json.dumps(data1)).encode())

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  logging.info('TBClassifier is serving at port %d', port)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()

#
# Main block
#

import io
import os
import sys

############################################################################
## Read parametes from JSON

if (os.path.isfile('config.json') ):
    print("Loading setting from 'config.json'")
    f = open('config.json')
 
    # returns JSON object as
    # a dictionary
    data = json.load(f)
 
    # Extract settings from the json config
    port = int(data['port'])
    logfile = data['logfile']
    loglevel = int(data['loglevel'])
     
    # Closing file
    f.close()

############################################################################
## Configure logger

if (len(logfile)):
    print("Logs are written at", logfile)
    sys.stdout = open(logfile, 'a')

    filehandler = logging.FileHandler(logfile, 'a', 'utf-8')
    logger = logging.getLogger()
    logger.addHandler(filehandler)
    if (loglevel == 1):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

classifier_train('./bigdataset.csv')
run(handler_class=HttpGetHandler)