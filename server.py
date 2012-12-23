import string,cgi,time, os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class Server(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			patharray = self.path.split('/')

			sc = ServerConfig()
			cdir = sc.getDir(patharray[1])
			if cdir is not False:
				fullpath = cdir
			else:
				self.send_error(404, 'Not found')
				return

			filename = ''

			for i in range(len(patharray)-2):
				filename += '/' + patharray[i+2]

			fullpath += filename

			forbidlist = ['server.py', 'main.py', 'template', 'list.conf']

			for forbid in forbidlist:
				if fullpath == os.getcwd() + '/' + forbid:
					self.send_error(403, 'Forbidden')
					return

			print 'path : ' + self.path
			print 'fullpath : ' + fullpath

			f = open(fullpath)
			self.send_response(200)
			readed = f.read()
			self.wfile.write(readed)
			f.close()
			return

		except IOError as e:
			if e.errno is 2:
				self.send_error(404,'Not found');
			elif e.errno is 13:
				self.send_error(403,'Fobidden');

class ServerConfig():
	def getDir(self, virtual_dir):
		count = 0
		for name in self.names:
			if name.find(virtual_dir) is not -1:
				return self.routes[count]
			count += 1
		return False

	def configListing(self):
		f = open('list.conf', 'r')
		datas = f.readlines()
		self.names = []
		self.routes = []
		for data in datas:
			dataarray = data.split(',')
			self.names.append(dataarray[0].strip())
			self.routes.append(dataarray[1].strip())

	def __init__(self):
		self.configListing()

def main():
	try:
		server = HTTPServer(('localhost', 3080), Server)
		print 'server start...'
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
		print 'server stop...'

if __name__ == '__main__':
	main()
