from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import time
import sys
import cgi, os
import subprocess
import cgitb
import re

fileServerPort = 8080
hdfsServer = "hdfs://ahmedali:9000"

""" ON GCE: Add property in hdfs-site.xml"""

params = len(sys.argv)
if params > 1:
	fileServerPort = int(sys.argv[1])
	if params > 2:
		hdfsServer = sys.argv[2]

class FileServer(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		print self.request.getProperty("Test")
		print "Tried GET"
		return
	
	def do_POST(self):
		form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type']})
		uploadedFile = form["uploadFile"]
		descr = form.getvalue("desc")
		category = form.getvalue("catalog")
		
		url = ""
		if uploadedFile.filename:
			message =  "File uploaded successfully at: "+time.ctime(time.time())
			fileName = os.path.basename(uploadedFile.filename)
			url = hdfsServer+"/user/ahmedali/files/"+fileName			
			open("/tmp/tempUpload", "wb").write(uploadedFile.file.read())
			with open("/tmp/tempUpload", "rb") as uploadFile:
				with open("/tmp/" + fileName, "wb") as uploadFileSave:
					schema = uploadFile.readline()[:-1]
					schema=schema.strip()
					schema=re.sub('[^A-Za-z0-9,]+','_',schema)
					descr=descr.strip();
					descr=re.sub('[^A-Za-z0-9]+','_',descr)
					temp = uploadFile.readline()[:-1]
					tempVal = temp.split(",")
					datatype=""
					flag = False
					for t in tempVal:
						try:
							x = int(t)
						except:
							try:
								x = float(t)
							except:
								x = str(t)
						y = type(x).__name__
						if flag == True:
							datatype = datatype + "," + y
						else:
							datatype = y
						flag = True
					uploadFileSave.write(temp+"\n")
					uploadFileSave.write(uploadFile.read())

			subprocess.call(["hdfs", "dfs", "-put", "/tmp/"+fileName, "files/"])
			subprocess.call(["rm", "/tmp/tempUpload"])
			subprocess.call(["rm", "/tmp/"+fileName])
		else:
			message =  "No file uploaded!"
		
		self.send_response(301)
		self.send_header("Method", "GET")
		self.send_header("Location", "http://harish-Inspiron-3521:8000/sparkapp/default/c1?descr="+descr+"&url="+url+"&schema="+schema+"&datatype="+datatype+"&category="+category)
		self.end_headers()
		#self.wfile.write(message)
		#self.wfile.write('\n')
		return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""
	def shutdown(self):
		self.socket.close()
		HTTPServer.shutdown(self)

if __name__ == '__main__':
	try:
		fileServer = ThreadedHTTPServer(("", fileServerPort), FileServer)
		print "Starting server at http://0.0.0.0:" + str(fileServerPort)
		fileServer.serve_forever()
	except KeyboardInterrupt:
		print "\nTerminating Server... CYA!"
